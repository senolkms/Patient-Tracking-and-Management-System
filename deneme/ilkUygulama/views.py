from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Hasta, Doktor,Yonetici,Randevu,TıbbiRapor
from django.db import connection,IntegrityError

def index(request):
    return render(request, 'index.html')

def hastalar(request):
    if 'hasta_id' not in request.session:
        return redirect('index')
    else:
        hasta_id = request.session['hasta_id']
        hasta = Hasta.objects.get(HastaID=hasta_id)
        randevular = Randevu.objects.filter(hasta=hasta).select_related('doktor')
        
        return render(request, 'hastalar.html', {'hasta': hasta, 'randevular': randevular})

def rapor_islemleri(request):
    raporlar = TıbbiRapor.objects.all()
    return render(request, 'rapor_islemleri.html', {'raporlar': raporlar})
def hasta_giris(request):
    if request.method == 'POST':
        kullanici_adi = request.POST.get('hasta_kullanici_adi')
        sifre = request.POST.get('hasta_sifre')

        with connection.cursor() as cursor:
            cursor.execute("SELECT HastaID FROM ilkuygulama_hasta WHERE KullaniciAdi = %s AND Sifre = %s", [kullanici_adi, sifre])
            result = cursor.fetchone()
            if result:
                request.session['hasta_id'] = result[0]  # Oturum bilgisini ayarla
                return redirect('hastalar')
            else:
                messages.error(request, 'Geçersiz kullanıcı adı veya şifre.')
                return render(request, 'index.html')
    else:
        messages.error(request, 'Kullanıcı adı veya şifre eksik.')
        return render(request,'index.html')

def doktorlar(request):
    if 'doktor_id' not in request.session:
        return redirect('index')
    else:
        doktor_id = request.session['doktor_id']
        doktor = Doktor.objects.get(DoktorID=doktor_id)
        return render(request, 'doktorlar.html', {'doktor': doktor})

def doktor_giris(request):
    if request.method == 'POST':
        kullanici_adi = request.POST.get('doktor_kullanici_adi')
        sifre = request.POST.get('doktor_sifre')

        with connection.cursor() as cursor:
            cursor.execute("SELECT DoktorID FROM ilkuygulama_doktor WHERE KullaniciAdi = %s AND Sifre = %s", [kullanici_adi, sifre])
            result = cursor.fetchone()
            if result:
                request.session['doktor_id'] = result[0]  # Oturum bilgisini ayarla
                return redirect('doktorlar')
            else:
                messages.error(request, 'Geçersiz kullanıcı adı veya şifre.')
                return render(request, 'index.html')
    else:
        messages.error(request, 'Kullanıcı adı veya şifre eksik.')
        return render(request,'index.html')

def yoneticiler(request):
    if 'yonetici_id' not in request.session:
        return redirect('index')  # Kullanıcı oturum açmamışsa anasayfaya yönlendir
    else:
        with connection.cursor() as cursor:
            # Hastaları çekmek için SQL sorgusu
            cursor.execute("SELECT * FROM ilkuygulama_hasta")
            hastalar = cursor.fetchall()
            cursor.execute("SELECT COUNT(*) FROM ilkuygulama_hasta")
            hasta_sayisi = cursor.fetchone()[0]

            # Doktorları çekmek için SQL sorgusu
            cursor.execute("SELECT * FROM ilkuygulama_doktor")
            doktorlar = cursor.fetchall()
            cursor.execute("SELECT COUNT(*) FROM ilkuygulama_doktor")
            doktor_sayisi = cursor.fetchone()[0]

        context = {
            'hastalar': [{'id': h[0], 'isim': h[1], 'soyisim': h[2], 'kullaniciAdi': h[7], 'sifre': h[8]} for h in hastalar],  # Örnek stun indeksleri
            'doktorlar': [{'id': d[0], 'isim': d[1], 'soyisim': d[2], 'kullaniciAdi': d[5], 'sifre': d[6]} for d in doktorlar],  # Örnek stun indeksleri
            'hasta_sayisi': hasta_sayisi,
            'doktor_sayisi': doktor_sayisi
        }
        return render(request, 'yoneticiler.html', context)

def yonetici_giris(request):
    if request.method == 'POST':
        kullanici_adi = request.POST.get('yonetici_kullanici_adi')
        sifre = request.POST.get('yonetici_sifre')

        with connection.cursor() as cursor:
            cursor.execute("SELECT YoneticiID FROM ilkuygulama_yonetici WHERE KullaniciAdi = %s AND Sifre = %s", [kullanici_adi, sifre])
            result = cursor.fetchone()
            if result:
                request.session['yonetici_id'] = result[0]  # Oturum bilgisini ayarla
                return redirect('yoneticiler')
            else:
                messages.error(request, 'Geçersiz kullanıcı adı veya şifre.')
                return render(request, 'index.html')
    else:
        messages.error(request, 'Kullanıcı adı veya şifre eksik.')
        return render(request,'index.html')

def doktor_islemleri(request):
    return render(request, 'doktor_islemleri.html')
def doktor_ekle(request):
    if request.method == 'POST':
        kullanici_adi = request.POST.get('doktor_kullanici_adi')
        adi = request.POST.get('doktor_adi')
        soyadi = request.POST.get('doktor_soyadi')
        uzmanlik_alani = request.POST.get('doktor_uzmanlik_alani')
        calistigi_hastane = request.POST.get('doktor_calistigi_hastane')
        sifre = request.POST.get('doktor_sifre')
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO ilkuygulama_doktor (KullaniciAdi, Ad, Soyad, UzmanlikAlani, CalistigiHastane, Sifre) VALUES (%s, %s, %s, %s, %s, %s)", [kullanici_adi, adi, soyadi, uzmanlik_alani, calistigi_hastane, sifre])
            messages.success(request, 'Doktor başarıyla eklendi.')
        except IntegrityError:
            messages.error(request, 'Doktor eklenirken bir hata oluştu.')
        return redirect('doktor_islemleri')

def doktor_sil(request):
    if request.method == 'POST':
        doktor_id = request.POST.get('doktor_id')
        try:
            Randevu.objects.filter(doktor_id=doktor_id).delete()
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM ilkuygulama_doktor WHERE DoktorID = %s", [doktor_id])
            messages.success(request, 'Doktor başarıyla silindi.')
        except IntegrityError:
            messages.error(request, 'Doktor silinirken bir hata oluştu.')
        return redirect('doktor_islemleri')
def doktor_guncelle(request):
    if request.method == 'POST':
        doktor_id = request.POST.get('doktor_id')
        kullanici_adi = request.POST.get('doktor_kullanici_adi')
        adi = request.POST.get('doktor_adi')
        soyadi = request.POST.get('doktor_soyadi')
        uzmanlik_alani = request.POST.get('doktor_uzmanlik_alani')
        calistigi_hastane = request.POST.get('doktor_calistigi_hastane')
        sifre = request.POST.get('doktor_sifre')
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE ilkuygulama_doktor 
                    SET KullaniciAdi=%s, Ad=%s, Soyad=%s, UzmanlikAlani=%s, CalistigiHastane=%s, Sifre=%s 
                    WHERE DoktorID=%s
                """, [kullanici_adi, adi, soyadi, uzmanlik_alani, calistigi_hastane, sifre, doktor_id])
            messages.success(request, 'Doktor başarıyla güncellendi.')
        except IntegrityError:
            messages.error(request, 'Doktor güncellenirken bir hata oluştu.')
        return redirect('doktor_islemleri')

def doktor_bilgi_guncelle(request):
    if request.method == 'POST':
        doktor_id = request.POST.get('doktor_id')
        kullanici_adi = request.POST.get('kullanici_adi')
        adi = request.POST.get('adi')
        soyadi = request.POST.get('soyadi')
        uzmanlik_alani = request.POST.get('uzmanlik_alani')
        calistigi_hastane = request.POST.get('calistigi_hastane')
        sifre = request.POST.get('sifre')
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE ilkuygulama_doktor 
                    SET KullaniciAdi=%s, Ad=%s, Soyad=%s, UzmanlikAlani=%s, CalistigiHastane=%s, Sifre=%s 
                    WHERE DoktorID=%s
                """, [kullanici_adi, adi, soyadi, uzmanlik_alani, calistigi_hastane, sifre, doktor_id])
            messages.success(request, 'Doktor başarıyla güncellendi.')
        except IntegrityError:
            messages.error(request, 'Doktor güncellenirken bir hata oluştu.')
        return redirect('doktorlar')
def hasta_islemleri(request):
    return render(request, 'hasta_islemleri.html')

def hasta_ekle(request):
    if request.method == 'POST':
        kullanici_adi = request.POST.get('hasta_kullanici_adi')
        adi = request.POST.get('hasta_adi')
        soyadi = request.POST.get('hasta_soyadi')
        dogum_tarihi = request.POST.get('hasta_dogum_tarihi')
        tel = request.POST.get('hasta_tel')
        cinsiyet = request.POST.get('hasta_cinsiyet')
        adres = request.POST.get('hasta_adres')
        sifre = request.POST.get('hasta_sifre')
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO ilkuygulama_hasta (Ad, Soyad, DogumTarihi, Cinsiyet, Telefon, Adres, KullaniciAdi, Sifre) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", [adi, soyadi, dogum_tarihi, cinsiyet, tel, adres, kullanici_adi, sifre])
            messages.success(request, 'Hasta başarıyla eklendi.')
        except IntegrityError:
            messages.error(request, 'Hasta eklenirken bir hata oluştu.')
        return redirect('hasta_islemleri') 
    
def hasta_guncelle(request):
    if request.method == 'POST':
        hasta_id = request.POST.get('hasta_id')
        kullanici_adi = request.POST.get('hasta_kullanici_adi')
        adi = request.POST.get('hasta_adi')
        soyadi = request.POST.get('hasta_soyadi')
        dogum_tarihi = request.POST.get('hasta_dogum_tarihi')
        tel = request.POST.get('hasta_tel')
        cinsiyet = request.POST.get('hasta_cinsiyet')
        adres = request.POST.get('hasta_adres')
        sifre = request.POST.get('hasta_sifre')
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE ilkuygulama_hasta 
                    SET Ad=%s, Soyad=%s, DogumTarihi=%s, Telefon=%s, Cinsiyet=%s, Adres=%s,KullaniciAdi=%s, Sifre=%s 
                    WHERE HastaID=%s
                """, [adi, soyadi, dogum_tarihi, tel, cinsiyet, adres, kullanici_adi, sifre, hasta_id])
            messages.success(request, 'Hasta başarıyla gncellendi.')
        except IntegrityError as e:
            messages.error(request, f'Hasta güncellenirken bir hata oluştu.{str(e)}')
        return redirect('hasta_islemleri')
def hasta_sil(request):
    if request.method == 'POST':
        hasta_id = request.POST.get('hasta_id')
        try:
            Randevu.objects.filter(hasta_id=hasta_id).delete()
            TıbbiRapor.objects.filter(hasta_id=hasta_id).delete()
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM ilkuygulama_hasta WHERE HastaID = %s", [hasta_id])
            messages.success(request, 'Hasta başarıyla silindi.')
        except IntegrityError:
            messages.error(request, 'Hasta silinirken bir hata oluştu.')
        return redirect('hasta_islemleri')

def hasta_bilgi_guncelle(request):
    if request.method == 'POST':
        hasta_id = request.POST.get('hasta_id')
        adi = request.POST.get('adi')
        soyadi = request.POST.get('soyadi')
        #dogum_tarihi = request.POST.get('dogum_tarihi')
        telefon = request.POST.get('telefon')
        adres = request.POST.get('adres')
        kullanici_adi = request.POST.get('kullanici_adi')
        sifre = request.POST.get('sifre')
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE ilkuygulama_hasta 
                    SET Ad=%s, Soyad=%s, Telefon=%s, Adres=%s, KullaniciAdi=%s, Sifre=%s 
                    WHERE HastaID=%s
                """, [adi, soyadi, telefon, adres, kullanici_adi, sifre, hasta_id])
            messages.success(request, 'Hasta başarıyla güncellendi.')
        except IntegrityError as e:
            messages.error(request, f'Hasta güncellenirken bir hata oluştu: {str(e)}')
        return redirect('hastalar')
    
def tibbi_raporlar(request):
    return render(request, 'tibbi_raporlar.html')

def doktor_tibbi_rapor(request):
    return render(request, 'doktor_tibbi_rapor.html')

def hasta_tibbi_rapor(request):
    if 'hasta_id' not in request.session:
        return redirect('index')  # Eğer hasta_id yoksa anasayfa veya giriş sayfasına yönlendir

    hasta_id = request.session['hasta_id']
    # Hasta'nın raporlarını çek
    raporlar = TıbbiRapor.objects.filter(hasta_id=hasta_id)

    return render(request, 'hasta_tibbi_rapor.html', {'raporlar': raporlar})

def rapor_ekle(request):
    if request.method == 'POST':
        rapor_tarihi = request.POST.get('rapor_tarihi')
        rapor_icerigi = request.POST.get('rapor_icerigi')
        hasta_id = request.POST.get('hasta_id')
        url = request.POST.get('url')
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO ilkuygulama_tıbbirapor (RaporTarihi, RaporIcerigi, hasta_id, URL) VALUES (%s, %s, %s, %s)", [rapor_tarihi, rapor_icerigi, hasta_id, url])
            messages.success(request, 'Rapor başarıyla eklendi.')
        except IntegrityError:
            messages.error(request, 'Rapor eklenirken bir hata oluştu.')
        return redirect('tibbi_raporlar') 
    
def hasta_rapor_ekle(request):
    if request.method == 'POST':
        rapor_tarihi = request.POST.get('rapor_tarihi')
        rapor_icerigi = request.POST.get('rapor_icerigi')
        hasta_id = request.POST.get('hasta_id')
        url = request.POST.get('url')
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO ilkuygulama_tıbbirapor (RaporTarihi, RaporIcerigi, hasta_id, URL) VALUES (%s, %s, %s, %s)", [rapor_tarihi, rapor_icerigi, hasta_id, url])
            messages.success(request, 'Rapor başarıyla eklendi.')
        except IntegrityError:
            messages.error(request, 'Rapor eklenirken bir hata oluştu.')
        return redirect('hasta_tibbi_rapor') 

def hasta_rapor_sil(request):
    if request.method == 'POST':
        rapor_id = request.POST.get('rapor_id')
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM ilkuygulama_tıbbirapor WHERE RaporID = %s", [rapor_id])
            messages.success(request, 'Rapor başarıyla silindi.')
        except IntegrityError:
            messages.error(request, 'Rapor silinirken bir hata oluştu.')
        return redirect('tibbi_raporlar')
    
def rapor_sil(request):
    if request.method == 'POST':
        rapor_id = request.POST.get('rapor_id')
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM ilkuygulama_tıbbirapor WHERE RaporID = %s", [rapor_id])
            messages.success(request, 'Rapor başarıyla silindi.')
        except IntegrityError:
            messages.error(request, 'Rapor silinirken bir hata oluştu.')
        return redirect('hasta_tibbi_rapor')

def rapor_guncelle(request):
    if request.method == 'POST':
        rapor_id = request.POST.get('rapor_id')
        rapor_tarihi = request.POST.get('rapor_tarihi')
        rapor_icerigi = request.POST.get('rapor_icerigi')
        hasta_id = request.POST.get('hasta_id')
        url = request.POST.get('url')

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE ilkuygulama_tıbbirapor
                    SET RaporTarihi=%s, RaporIcerigi=%s, hasta_id=%s, URL=%s
                    WHERE RaporID=%s
                """, [rapor_tarihi, rapor_icerigi, hasta_id, url, rapor_id])
            messages.success(request, 'Tıbbi rapor başarıyla güncellendi.')
        except IntegrityError:
            messages.error(request, 'Tıbbi rapor gncellenirken bir hata oluştu.')
        return redirect('tibbi_raporlar')
    
def hasta_rapor_guncelle(request):
    if request.method == 'POST':
        rapor_id = request.POST.get('rapor_id')
        rapor_tarihi = request.POST.get('rapor_tarihi')
        rapor_icerigi = request.POST.get('rapor_icerigi')
        hasta_id = request.POST.get('hasta_id')
        url = request.POST.get('url')

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE ilkuygulama_tıbbirapor
                    SET RaporTarihi=%s, RaporIcerigi=%s, hasta_id=%s, URL=%s
                    WHERE RaporID=%s
                """, [rapor_tarihi, rapor_icerigi, hasta_id, url, rapor_id])
            messages.success(request, 'Tıbbi rapor başarıyla güncellendi.')
        except IntegrityError:
            messages.error(request, 'Tıbbi rapor gncellenirken bir hata oluştu.')
        return redirect('hasta_tibbi_rapor')
    
def hasta_takip(request):
    if 'doktor_id' not in request.session:
        return redirect('hasta_takip')
    
    doktor_id = request.session['doktor_id']
    hastalar = Hasta.objects.filter(randevu__doktor_id=doktor_id).distinct()
    for hasta in hastalar:
        hasta.randevular = hasta.randevu_set.filter(doktor=doktor_id)  # Sadece belirli doktora ait randevuları filtrele
    context = {
        'hastalar': hastalar,
        'doktor_id': doktor_id
    }
    return render(request, 'hasta_takip.html',context)

def rapor_takip(request):
    if 'doktor_id' not in request.session:
        return redirect('index')  # Eğer doktor_id yoksa anasayfa veya giriş sayfasına yönlendir

    doktor_id = request.session['doktor_id']
    hastalar_con_rapor = Hasta.objects.filter(
        randevu__doktor_id=doktor_id,
        tibbi_raporlar__isnull=False
    ).distinct().prefetch_related('tibbi_raporlar')

    return render(request, 'rapor_takip.html', {'hastalar': hastalar_con_rapor})

def randevu_islem(request):
    uzmanlik_alanlari = Doktor.objects.values_list('UzmanlikAlani', flat=True).distinct()
    if request.method == 'POST':
        doktor_id = request.POST.get('doktor_id')
        tarih = request.POST.get('tarih')
        saat = request.POST.get('saat')

        # Oturumdan hasta_id'yi al
        hasta_id = request.session.get('hasta_id')
        if not hasta_id:
            messages.error(request, 'Hasta girişi yapılmamış.')
            return redirect('hasta_giris')
        try:
            # SQL sorgusu ile randevu oluştur
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO ilkuygulama_randevu (doktor_id, hasta_id, tarih, saat)
                    VALUES (%s, %s, %s, %s)
                """, [doktor_id, hasta_id, tarih, saat])
            messages.success(request, 'Randevu başarıyla oluşturuldu.')
            return redirect('hastalar')
        except Exception as e:
            messages.error(request, f'Randevu oluşturulurken bir hata oluştu: {str(e)}')
            return redirect('randevu_islem')
    else:
        return render(request, 'randevu_islem.html', {
            'uzmanlik_alanlari': uzmanlik_alanlari
        })
    
def doktorlari_getir(request):
    uzmanlik = request.GET.get('uzmanlik')
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DoktorID, Ad, Soyad FROM ilkuygulama_doktor
            WHERE UzmanlikAlani = %s
        """, [uzmanlik])
        doktorlar = cursor.fetchall()

    doktor_listesi = [{'id': doktor[0], 'adi': doktor[1], 'soyadi': doktor[2]} for doktor in doktorlar]
    return JsonResponse({'doktorlar': doktor_listesi})

def randevu_iptal(request, randevu_id):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM ilkuygulama_randevu WHERE randevu_id = %s", [randevu_id])
            messages.success(request, 'Randevu başarıyla iptal edildi.')
        except Exception as e:
            messages.error(request, f'Randevu iptal edilirken bir hata oluştu: {str(e)}')
        return redirect('hastalar')
    else:
        messages.error(request, 'Geçersiz işlem.')
        return redirect('hastalar')
    
def doktor_rapor_ekle(request):
    if request.method == 'POST':
        rapor_tarihi = request.POST.get('rapor_tarihi')
        rapor_icerigi = request.POST.get('rapor_icerigi')
        hasta_id = request.POST.get('hasta_id')
        url = request.POST.get('url')
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO ilkuygulama_tıbbirapor (RaporTarihi, RaporIcerigi, hasta_id, URL) VALUES (%s, %s, %s, %s)", [rapor_tarihi, rapor_icerigi, hasta_id, url])
            messages.success(request, 'Rapor başarıyla eklendi.')
        except IntegrityError:
            messages.error(request, 'Rapor eklenirken bir hata oluştu.')
        return redirect('doktor_tibbi_rapor') 
    
def doktor_rapor_guncelle(request):
    if request.method == 'POST':
        rapor_id = request.POST.get('rapor_id')
        rapor_tarihi = request.POST.get('rapor_tarihi')
        rapor_icerigi = request.POST.get('rapor_icerigi')
        hasta_id = request.POST.get('hasta_id')
        url = request.POST.get('url')

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE ilkuygulama_tıbbirapor
                    SET RaporTarihi=%s, RaporIcerigi=%s, hasta_id=%s, URL=%s
                    WHERE RaporID=%s
                """, [rapor_tarihi, rapor_icerigi, hasta_id, url, rapor_id])
            messages.success(request, 'Tıbbi rapor başarıyla güncellendi.')
        except IntegrityError:
            messages.error(request, 'Tıbbi rapor gncellenirken bir hata oluştu.')
        return redirect('doktor_tibbi_rapor')
    
def doktor_rapor_sil(request):
    if request.method == 'POST':
        rapor_id = request.POST.get('rapor_id')
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM ilkuygulama_tıbbirapor WHERE RaporID = %s", [rapor_id])
            messages.success(request, 'Rapor başarıyla silindi.')
        except IntegrityError:
            messages.error(request, 'Rapor silinirken bir hata oluştu.')
        return redirect('doktor_tibbi_rapor')

    
