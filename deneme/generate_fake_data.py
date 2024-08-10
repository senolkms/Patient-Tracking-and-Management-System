import os
import secrets,time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deneme.settings")
import django  
django.setup()

from faker import Faker
from faker.providers import person
import random
from ilkUygulama.models import Hasta, Doktor, Randevu, Yonetici

fake = Faker('tr_TR') 
fake.add_provider(person)

def generate_hastalar(num_hastalar):
    for i in range(num_hastalar):
        # Zaman damgası ve rastgele sayı ekleyerek kullanıcı adını benzersiz yapın
        kullanici_adi = f"hasta{i+1}_{int(time.time())}_{random.randint(1000, 9999)}"
        sifre = generate_secure_password()
        Hasta.objects.create(
            Ad = fake.first_name(),
            Soyad = fake.last_name(),
            DogumTarihi = fake.date_of_birth(),
            Cinsiyet = random.choice(['Erkek', 'Kadın']),
            Telefon = fake.phone_number(),
            Adres = fake.address(),
            KullaniciAdi=kullanici_adi,
            Sifre=sifre
        )
        
def generate_doktorlar(num_doktorlar):
    for i in range(num_doktorlar):
        kullanici_adi = f"doktor{i+1}_{int(time.time())}_{random.randint(1000, 9999)}"
        sifre = generate_secure_password()  # Rastgele şifre oluştur
        Doktor.objects.create(
            Ad=fake.first_name(),
            Soyad=fake.last_name(),
            UzmanlikAlani=fake.job(),
            CalistigiHastane=fake.company(),
            KullaniciAdi=kullanici_adi,
            Sifre=sifre 
        )
def generate_yoneticiler(num_yoneticiler):
    for i in range(num_yoneticiler):
        kullanici_adi = f"yonetici{i+1}_{int(time.time())}_{random.randint(1000, 9999)}"
        sifre = generate_secure_password()  # Rastgele şifre oluştur
        yonetici = Yonetici(
            KullaniciAdi=kullanici_adi,
            Sifre=sifre
        )
        yonetici.save()

def generate_randevular(num_randevular):
    hastalar = list(Hasta.objects.all())
    doktorlar = list(Doktor.objects.all())
    for _ in range(num_randevular):
        hasta = random.choice(hastalar)
        doktor = random.choice(doktorlar)
        
        # Rastgele bir tarih ve saat oluştur
        tarih = fake.date_this_year()
        saat = fake.time()
        
        # Randevu oluştur
        Randevu.objects.create(
            hasta=hasta,
            doktor=doktor,
            tarih=tarih,
            saat=saat
        )

def generate_secure_password(length=12):
    # ASCII karakterlerinin bir kombinasyonunu kullanarak güvenli bir şifre oluşturur
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

if __name__ == '__main__':
    generate_hastalar(50)  # 50 hasta oluştur
    generate_doktorlar(20)  # 20 doktor oluştur
    generate_randevular(100) 
    generate_yoneticiler(1) # 5 yönetici oluştur
