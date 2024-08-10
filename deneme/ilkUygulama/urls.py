from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Anasayfa için URL tanımı
    path('hastalar/', views.hastalar, name='hastalar'), 
    path('hasta_giris/', views.hasta_giris, name='hasta_giris'),  # hasta girişi için URL tanımı
    path('doktor_giris/', views.doktor_giris, name='doktor_giris'), # doktor girişi için URL tanımı
    path('doktorlar/', views.doktorlar, name='doktorlar'),
    path('yonetici/', views.yoneticiler, name='yoneticiler'),
    path('yonetici_giris/', views.yonetici_giris, name='yonetici_giris'),
    path('doktor_islemleri/', views.doktor_islemleri, name='doktor_islemleri'),
    path('doktor_ekle/',views.doktor_ekle, name='doktor_ekle'),
    path('doktor_sil/',views.doktor_sil, name='doktor_sil'),
    path('doktor_guncelle/',views.doktor_guncelle, name='doktor_guncelle'),
    path('hasta_islemleri/', views.hasta_islemleri, name='hasta_islemleri'),
    path('hasta_ekle/',views.hasta_ekle, name='hasta_ekle'),
    path('hasta_sil/',views.hasta_sil, name='hasta_sil'),
    path('hasta_guncelle/',views.hasta_guncelle, name='hasta_guncelle'),
    path('tibbi_raporlar/', views.tibbi_raporlar, name='tibbi_raporlar'),
    path('rapor_ekle/', views.rapor_ekle, name='rapor_ekle'),
    path('rapor_sil/', views.rapor_sil, name='rapor_sil'),
    path('rapor_guncelle/', views.rapor_guncelle, name='rapor_guncelle'),
    path('hasta_takip/', views.hasta_takip, name='hasta_takip'),
    path('rapor_takip/', views.rapor_takip, name='rapor_takip'),
    path('doktor_tibbi_rapor/', views.doktor_tibbi_rapor, name='doktor_tibbi_rapor'),
    path('hasta_tibbi_rapor/', views.hasta_tibbi_rapor, name='hasta_tibbi_rapor'),
    path('randevu_islem/', views.randevu_islem, name='randevu_islem'),
    path('doktorlari_getir/', views.doktorlari_getir, name='doktorlari_getir'),
    path('hasta_rapor_ekle/', views.hasta_rapor_ekle, name='hasta_rapor_ekle'),
    path('hasta_rapor_sil/', views.hasta_rapor_sil, name='hasta_rapor_sil'),
    path('hasta_rapor_guncelle/', views.hasta_rapor_guncelle, name='hasta_rapor_guncelle'),
    path('randevu-iptal/<int:randevu_id>/', views.randevu_iptal, name='randevu_iptal'),
    path('doktor_rapor_ekle/', views.doktor_rapor_ekle, name='doktor_rapor_ekle'),
    path('doktor_rapor_sil/', views.doktor_rapor_sil, name='doktor_rapor_sil'),
    path('doktor_rapor_guncelle/', views.doktor_rapor_guncelle, name='doktor_rapor_guncelle'),
    path('hasta_bilgi_guncelle/', views.hasta_bilgi_guncelle, name='hasta_bilgi_guncelle'),
    path('doktor_bilgi_guncelle/', views.doktor_bilgi_guncelle, name='doktor_bilgi_guncelle'),
]
