import os,sys
import secrets
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deneme.settings")
sys.path.append('C:\\Users\\senol\\Desktop\\django_deneme\\deneme')
import django  
django.setup()
from datetime import date, timedelta, datetime
from faker import Faker
from faker.providers import BaseProvider
from django.db import connection
import random
from ilkUygulama.models import Hasta, Doktor, Randevu, Yonetici, TıbbiRapor


class TurkishLocaleProvider(BaseProvider):
       def turkish_phone_number(self):
           # Türkiye'ye özgü telefon numarası formatı
           formats = ['+90 5## ### ## ##', '0(5##) ### ## ##']
           return self.generator.format('numerify', self.random_element(formats))

       def turkish_address(self):
           # Basit bir örnek, daha detaylı adresler için genişletilebilir
           return self.generator.city() + " Mahallesi, " + self.generator.street_name() + " No:" + self.generator.building_number()

fake = Faker('tr_TR') 
fake.add_provider(TurkishLocaleProvider)

def reset_auto_increment(model):
    cursor = connection.cursor()
    table_name = model._meta.db_table
    cursor.execute(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1;")
    cursor.close()

def delete_and_reset():
    Hasta.objects.all().delete()
    Doktor.objects.all().delete()
    Randevu.objects.all().delete()
    Yonetici.objects.all().delete()
    TıbbiRapor.objects.all().delete()

    reset_auto_increment(Hasta)
    reset_auto_increment(Doktor)
    reset_auto_increment(Randevu)
    reset_auto_increment(Yonetici)
    reset_auto_increment(TıbbiRapor)

def generate_hastalar(num_hastalar):
    for i in range(num_hastalar):
        kullanici_adi = f"hasta{i+1}"
        sifre = generate_secure_password()
        Hasta.objects.create(
            Ad = fake.first_name(),
            Soyad = fake.last_name(),
            DogumTarihi = fake.date_of_birth(),
            Cinsiyet = random.choice(['Erkek', 'Kadın']),
            Telefon = fake.turkish_phone_number(),
            Adres = fake.turkish_address(),
            KullaniciAdi=kullanici_adi,
            Sifre=sifre
        )
        
def generate_doktorlar(num_doktorlar):
    uzmanlik_dallari = [
        "Genel Cerrahi", "Kardiyoloji", "Nöroloji", "Ortopedi", "Radyoloji",
        "Dermatoloji", "Pediatri", "Üroloji", "Göz Hastalıkları",
        "Kadın Hastalıkları ve Doğum", "Kulak Burun Boğaz", "Psikiyatri",
        "Onkoloji", "Endokrinoloji", "Gastroenteroloji"
    ]
    hastaneler = [
        "Florence Nightingale Hastanesi", "Liv Hospital", "Medical Park Hastaneler Grubu",
        "Anadolu Sağlık Merkezi", "İstanbul Cerrahi Hastanesi", "Koç Üniversitesi Hastanesi",
        "Amerikan Hastanesi", "Şişli Florence Nightingale Hastanesi",
        "Kocaeli Üniversitesi Araştırma ve Uygulama Hastanesi", "Dokuz Eylül Üniversitesi Hastanesi",
        "Marmara Üniversitesi Pendik Eğitim ve Araştırma Hastanesi", "Ankara Üniversitesi Tıp Fakültesi Hastanesi",
        "Ege Üniversitesi Tıp Fakültesi Hastanesi", "Hacettepe Üniversitesi Tıp Fakültesi Hastanesi",
        "Gazi Üniversitesi Tıp Fakültesi Hastanesi", "İzmir Ekonomi Üniversitesi Hastanesi",
        "İstanbul Üniversitesi İstanbul Tıp Fakültesi Hastanesi", "Başkent Üniversitesi Hastanesi"
    ]
    for i in range(num_doktorlar):
        kullanici_adi = f"doktor{i+1}"      #_{random.randint(1000, 9999)}
        sifre = generate_secure_password()  
        Doktor.objects.create(
            Ad=fake.first_name(),
            Soyad=fake.last_name(),
            UzmanlikAlani=random.choice(uzmanlik_dallari),
            CalistigiHastane=random.choice(hastaneler),
            KullaniciAdi=kullanici_adi,
            Sifre=sifre 
        )
def generate_yoneticiler(num_yoneticiler):
    for i in range(num_yoneticiler):
        kullanici_adi = f"yonetici{i+1}"
        sifre = generate_secure_password()  
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
        
        start_date = date.today()
        end_date = date.today() + timedelta(days=150)  
        tarih = fake.date_between(start_date=start_date, end_date=end_date)
        saat = datetime.combine(date.today(), datetime.min.time()) + timedelta(hours=9, minutes=random.randint(0, 420))
        saat = saat.strftime('%H:%M')
        
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

def generate_tibbi_raporlar(num_raporlar):
    urls = [
        ("https://drive.google.com/drive/folders/1-bW8dFJoKCEdUKni5a0KYr77GxIc99ns?usp=sharing", "Kol MR"),
        ("https://drive.google.com/drive/folders/1xpqrHl-oeruhKTas1HnVHS-GGDIc8wIG?usp=sharing", "Diş, Panoromik "),
        ("https://drive.google.com/drive/folders/1eNqy1B3CnSbxaCvgnOQf0nOrJpF7a6qC?usp=sharing", "MR, El bileği - sol, kontrastsız"),
        ("https://drive.google.com/drive/folders/1Y2rDf7LucIeX7CD9QRmvuzV6zyvZ5_4p?usp=sharing", "MRG, BEYİN, KONTRASTSIZ"),
        ("https://drive.google.com/drive/folders/1ar1e-R3ulFnd_qEyJpsUkKFizWI6XfqV?usp=sharing", "AKCİĞER GRAFİSİ")
    ]
    hastalar = list(Hasta.objects.all())
    if not hastalar:
        print("Hasta veritabanında kayıt bulunamadı. Önce hasta üretin.")
        return
    for _ in range(num_raporlar):
        hasta = random.choice(hastalar)
        rapor_tarihi = fake.date_between(start_date='-1y', end_date='today')
        chosen_url, description = random.choice(urls)  # URL ve açıklamasını birlikte seç
        rapor_icerigi = description
        TıbbiRapor.objects.create(
            RaporTarihi=rapor_tarihi,
            RaporIcerigi=rapor_icerigi,
            hasta=hasta,
            URL=chosen_url
        )

if __name__ == '__main__':
    generate_hastalar(1000)  
    generate_doktorlar(500)  
    generate_randevular(1000) 
    generate_yoneticiler(1) #  yönetici oluştur
    generate_tibbi_raporlar(250)
    #delete_and_reset()
