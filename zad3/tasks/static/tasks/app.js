"use strict";

const API_URL = "/api/tasks/";

// ---- state ---------------------------------------------------------------
let tasks = [];
let currentFilter = "all";

// ---- DOM references ------------------------------------------------------
const form = document.getElementById("task-form");
const titleInput = document.getElementById("task-title");
const listEl = document.getElementById("task-list");
const emptyEl = document.getElementById("empty");
const messageEl = document.getElementById("message");
const totalEl = document.getElementById("count-total");
const doneEl = document.getElementById("count-done");
const filterButtons = document.querySelectorAll(".filter");

// ---- helpers -------------------------------------------------------------
function getCookie(name) {
  const match = document.cookie
    .split("; ")
    .find((row) => row.startsWith(name + "="));
  return match ? decodeURIComponent(match.split("=")[1]) : null;
}

function showMessage(text) {
  messageEl.textContent = text;
  messageEl.hidden = false;
}

function clearMessage() {
  messageEl.textContent = "";
  messageEl.hidden = true;
  titleInput.classList.remove("is-invalid");
}

/**
 * Wrapper around fetch(): adds JSON + CSRF headers and turns HTTP 4xx/5xx
 * responses into thrown errors carrying the message sent by the API.
 */
async function apiRequest(url, options = {}) {
  const headers = { Accept: "application/json" };
  if (options.body !== undefined) {
    headers["Content-Type"] = "application/json";
  }
  if (options.method && options.method !== "GET") {
    headers["X-CSRFToken"] = getCookie("csrftoken");
  }

  let response;
  try {
    response = await fetch(url, { ...options, headers });
  } catch (networkError) {
    throw new Error("Brak połączenia z serwerem. Spróbuj ponownie.");
  }

  let data = null;
  try {
    data = await response.json();
  } catch (parseError) {
    // body is not JSON; handled below
  }

  if (!response.ok) {
    const reason = data && data.error ? data.error : `Błąd serwera (${response.status}).`;
    throw new Error(reason);
  }
  return data;
}

// ---- rendering -----------------------------------------------------------
function visibleTasks() {
  if (currentFilter === "active") return tasks.filter((t) => !t.completed);
  if (currentFilter === "completed") return tasks.filter((t) => t.completed);
  return tasks;
}

function createTaskElement(task) {
  const li = document.createElement("li");
  li.className = "task" + (task.completed ? " is-completed" : "");
  li.dataset.id = task.id;

  const title = document.createElement("span");
  title.className = "task__title";
  title.textContent = task.title; // textContent: user text is never parsed as HTML

  const actions = document.createElement("div");
  actions.className = "task__actions";

  const toggle = document.createElement("button");
  toggle.type = "button";
  toggle.className = "toggle";
  toggle.textContent = task.completed ? "Przywróć" : "Ukończ";
  toggle.addEventListener("click", () => toggleTask(task.id));

  const remove = document.createElement("button");
  remove.type = "button";
  remove.className = "delete";
  remove.textContent = "Usuń";
  remove.addEventListener("click", () => deleteTask(task.id));

  actions.append(toggle, remove);
  li.append(title, actions);
  return li;
}

function renderTasks() {
  const shown = visibleTasks();
  listEl.replaceChildren(...shown.map(createTaskElement));

  const emptyTexts = {
    all: "Brak zadań. Dodaj pierwsze powyżej.",
    active: "Brak aktywnych zadań.",
    completed: "Brak ukończonych zadań.",
  };
  emptyEl.textContent = emptyTexts[currentFilter];
  emptyEl.hidden = shown.length > 0;

  renderSummary();
}

function renderSummary() {
  totalEl.textContent = tasks.length;
  doneEl.textContent = tasks.filter((t) => t.completed).length;
}

function renderFilters() {
  filterButtons.forEach((btn) => {
    const active = btn.dataset.filter === currentFilter;
    btn.classList.toggle("is-active", active);
    btn.setAttribute("aria-pressed", String(active));
  });
}

// ---- API operations ------------------------------------------------------
async function loadTasks() {
  try {
    tasks = await apiRequest(API_URL);
    clearMessage();
    renderTasks();
  } catch (error) {
    showMessage(error.message);
  }
}

async function addTask(title) {
  try {
    await apiRequest(API_URL, { method: "POST", body: JSON.stringify({ title }) });
    form.reset();
    clearMessage();
    await loadTasks();
  } catch (error) {
    showMessage(error.message);
  }
}

async function toggleTask(id) {
  const task = tasks.find((t) => t.id === id);
  if (!task) return;
  try {
    await apiRequest(`${API_URL}${id}/`, {
      method: "PATCH",
      body: JSON.stringify({ completed: !task.completed }),
    });
    clearMessage();
    await loadTasks();
  } catch (error) {
    await loadTasks(); // the task may no longer exist; resync with the server
    showMessage(error.message);
  }
}

async function deleteTask(id) {
  try {
    await apiRequest(`${API_URL}${id}/`, { method: "DELETE" });
    clearMessage();
    await loadTasks();
  } catch (error) {
    await loadTasks();
    showMessage(error.message);
  }
}

// ---- events --------------------------------------------------------------
form.addEventListener("submit", (event) => {
  event.preventDefault();
  const title = titleInput.value.trim();
  if (!title) {
    titleInput.classList.add("is-invalid");
    showMessage("Wpisz treść zadania, zanim je dodasz.");
    titleInput.focus();
    return;
  }
  addTask(title);
});

filterButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    currentFilter = btn.dataset.filter;
    renderFilters();
    renderTasks();
  });
});

document.addEventListener("DOMContentLoaded", loadTasks);
