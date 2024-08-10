from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Hasta(models.Model):
    HastaID = models.AutoField(primary_key=True) 
    KullaniciAdi = models.CharField(max_length=100, unique=True, null=True)
    Ad = models.CharField(max_length=100)
    Soyad = models.CharField(max_length=100)
    DogumTarihi = models.DateField()
    Cinsiyet = models.CharField(max_length=10)
    Telefon = models.CharField(max_length=50)
    Adres = models.CharField(max_length=255)
    Sifre = models.CharField(max_length=100, default='sifre')  # Şifre sütunu eklendi

class Doktor(models.Model):
    DoktorID = models.AutoField(primary_key=True)
    KullaniciAdi = models.CharField(max_length=100, unique=True, null=True)
    Ad = models.CharField(max_length=100)
    Soyad = models.CharField(max_length=100)
    UzmanlikAlani = models.CharField(max_length=100)
    CalistigiHastane = models.CharField(max_length=255)
    Sifre = models.CharField(max_length=100, default='sifre')  # Şifre sütunu eklendi

class Yonetici(models.Model):
    YoneticiID = models.AutoField(primary_key=True)
    KullaniciAdi = models.CharField(max_length=100, unique=True, null=True)
    Sifre = models.CharField(max_length=100, default='sifre')  # Şifre sütunu eklendi

class Randevu(models.Model):
    randevu_id = models.AutoField(primary_key=True) 
    hasta = models.ForeignKey(Hasta, on_delete=models.CASCADE)
    doktor = models.ForeignKey(Doktor, on_delete=models.CASCADE)
    tarih = models.DateField()
    saat = models.TimeField()
    def __str__(self):
        return f"{self.hasta} {self.doktor} {self.tarih} {self.saat.strftime('%H:%M')}"
    
class TıbbiRapor(models.Model):
    RaporID = models.AutoField(primary_key=True)
    RaporTarihi = models.DateField()
    RaporIcerigi = models.TextField()
    hasta = models.ForeignKey(Hasta, on_delete=models.CASCADE, related_name='tibbi_raporlar')
    URL = models.CharField(max_length=200, default='')

