from django.db import models


class Gra(models.Model):
    GATUNKI = [
        ('rpg', 'RPG'),
        ('strategia', 'Strategia'),
        ('platformowa', 'Platformowa'),
        ('zrecznosciowa', 'Zręcznościowa'),
        ('symulacja', 'Symulacja'),
        ('przygodowa', 'Przygodowa'),
        ('strzelanka', 'Strzelanka'),
        ('moba', 'MOBA'),
        ('horror', 'horror'),
    ]

    tytul = models.CharField('Tytuł', max_length=120)
    opis = models.TextField('Opis', blank=True)
    gatunek = models.CharField('Gatunek', max_length=20, choices=GATUNKI)
    data_premiery = models.DateField('Data premiery')
    ocena = models.IntegerField('Ocena (1-10)')
    wieloosobowa = models.BooleanField('Tryb wieloosobowy', default=False)
    cena = models.DecimalField('Cena (zł)', max_digits=7, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Gra'
        verbose_name_plural = 'Gry'
        ordering = ['tytul']

    def __str__(self):
        return f'{self.tytul} ({self.data_premiery.year})'
