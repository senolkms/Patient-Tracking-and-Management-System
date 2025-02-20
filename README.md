# 🏥 Hasta Takip ve Yönetim Sistemi

Bu proje, bir **hastane yönetim sistemi** olarak tasarlanmış bir **web uygulamasıdır**.  
Hastalar **kayıt oluşturabilir**, **doktorlarla randevu alabilir**, **tıbbi raporlarını saklayabilir** ve sağlıkla ilgili işlemleri yönetebilir.  

🛠 **Backend:** Python-Django  
🗄 **Veritabanı:** MySQL 
🎨 **Frontend:** HTML, CSS, JavaScript, Bootstrap  
🔐 **Güvenlik:** HTTPS, Şifreleme, Yetkilendirme  

---

## 📌 **Özellikler**

✅ **Hasta Yönetimi**  
- Hasta ekleme, silme, güncelleme  
- Hasta geçmişi ve tıbbi rapor erişimi  

✅ **Doktor Yönetimi**  
- Doktor ekleme, silme, güncelleme  
- Uzmanlık alanına göre doktor listesi  

✅ **Randevu Sistemi**  
- Hastaların doktorlardan randevu alması  
- Randevu iptal etme ve güncelleme  
- Randevu geçmişini görüntüleme  

✅ **Tıbbi Rapor Yönetimi**  
- Tıbbi rapor ekleme, silme ve güncelleme  
- Görsel raporları saklama (dosya yükleme)  
- JSON formatında rapor kaydetme  

✅ **Gelişmiş Arama & Filtreleme**  
- Hasta adına, doktora veya randevu tarihine göre arama  
- Hasta profili üzerinden tıbbi geçmişe erişim  

✅ **Güvenlik & Yetkilendirme**  
- **HTTPS & Şifreleme** ile güvenli veri saklama  
- **Yetkilendirme (Authentication)**: Yönetici, Doktor ve Hasta rolleri  

---

## 📂 **Veritabanı Tasarımı**
Bu proje ilişkisel bir veritabanı modeline sahiptir ve **normalizasyon kurallarına (1NF, 2NF, 3NF)** uygundur.

### **🔹 Temel Tablolar**
📌 **Hastalar Tablosu (`Patients`)**  
- `HastaID (PK)`, `Ad`, `Soyad`, `Doğum Tarihi`, `Cinsiyet`, `Telefon Numarası`, `Adres`  

📌 **Doktorlar Tablosu (`Doctors`)**  
- `DoktorID (PK)`, `Ad`, `Soyad`, `Uzmanlık Alanı`, `Çalıştığı Hastane`  

📌 **Randevular Tablosu (`Appointments`)**  
- `RandevuID (PK)`, `HastaID (FK)`, `DoktorID (FK)`, `Randevu Tarihi`, `Randevu Saati`  

📌 **Tıbbi Raporlar Tablosu (`MedicalReports`)**  
- `RaporID (PK)`, `HastaID (FK)`, `DoktorID (FK)`, `Rapor Tarihi`, `Rapor İçeriği`, `Dosya URL`  

📌 **Yöneticiler Tablosu (`Admins`)**  
- `YoneticiID (PK)`, `Ad`, `Soyad`  

---

## 🖥 **Kullanıcı Arayüzü (GUI)**  

- 📌 **Ana Sayfa:** Genel hasta ve doktor bilgileri  
- 📋 **Hasta Paneli:** Randevu geçmişi, tıbbi raporlar  
- 🔍 **Doktor Paneli:** Hastalarını ve tıbbi raporlarını görüntüleyebilir  
- 🏥 **Yönetici Paneli:** Hasta, doktor, randevu ve raporları yönetebilir  

💡 **Dinamik Bileşenler:**  
✔ **AJAX Kullanımı** – Sayfa yenilenmeden randevu alma ve dosya yükleme  
✔ **Hasta/Doktor Dashboard** – Profil bazlı veri görüntüleme  

