from django.db import models

# Create your models here.

class Game(models.Model):
    nama = models.CharField(max_length=100)
    genre = models.CharField(max_length=50, default='Unknown')
    deskripsi = models.TextField(blank=True, default='Belum ada deskripsi.')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    gambar = models.ImageField(upload_to='game_images/', blank=True, null=True)  # gambar wajib

    def __str__(self):
        return self.nama
