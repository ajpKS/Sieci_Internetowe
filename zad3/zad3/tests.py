import json

from django.test import Client, TestCase

from .models import Task


class TaskApiTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get("/")  # sets the csrftoken cookie
        self.token = self.client.cookies["csrftoken"].value

    def send(self, method, url, payload=None):
        return self.client.generic(
            method, url,
            data=json.dumps(payload) if payload is not None else "",
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.token,
        )

    def test_list_empty_and_ordered(self):
        self.assertEqual(self.client.get("/api/tasks/").json(), [])
        Task.objects.create(title="a")
        Task.objects.create(title="b")
        self.assertEqual([t["title"] for t in self.client.get("/api/tasks/").json()], ["b", "a"])

    def test_create(self):
        r = self.send("POST", "/api/tasks/", {"title": "  Kup mleko "})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["title"], "Kup mleko")
        self.assertFalse(r.json()["completed"])

    def test_create_rejects_bad_input(self):
        for payload in ({"title": ""}, {"title": "   "}, {}, {"title": 5}, {"title": "x" * 201}):
            self.assertEqual(self.send("POST", "/api/tasks/", payload).status_code, 400, payload)
        r = self.client.post("/api/tasks/", data="{oops", content_type="application/json",
                             HTTP_X_CSRFTOKEN=self.token)
        self.assertEqual(r.status_code, 400)

    def test_patch_and_delete(self):
        t = Task.objects.create(title="x")
        r = self.send("PATCH", f"/api/tasks/{t.id}/", {"completed": True})
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()["completed"])
        self.assertEqual(self.send("PATCH", f"/api/tasks/{t.id}/", {"completed": "yes"}).status_code, 400)
        self.assertEqual(self.send("DELETE", f"/api/tasks/{t.id}/").status_code, 200)
        self.assertEqual(Task.objects.count(), 0)

    def test_missing_id_returns_404(self):
        self.assertEqual(self.send("PATCH", "/api/tasks/999/", {"completed": True}).status_code, 404)
        self.assertEqual(self.send("DELETE", "/api/tasks/999/").status_code, 404)

    def test_csrf_required(self):
        bare = Client(enforce_csrf_checks=True)
        r = bare.post("/api/tasks/", data='{"title":"x"}', content_type="application/json")
        self.assertEqual(r.status_code, 403)

    def test_method_not_allowed(self):
        self.assertEqual(self.send("PUT", "/api/tasks/").status_code, 405)
