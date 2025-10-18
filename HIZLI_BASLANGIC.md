# DMX Controller - Hızlı Başlangıç Kılavuzu

## 🎉 Yeni Özellikler v1.1.0

### ⚡ v1.1.0 Güncellemesi (YENİ!)

#### USB Doğrudan Bağlantı
- ❌ **Eski**: COM port üzerinden Serial bağlantı (sorunluydu)
- ✅ **Yeni**: USB üzerinden doğrudan UDMX bağlantısı
- ⚡ Daha hızlı ve güvenilir
- 🔌 Otomatik UDMX cihaz tespiti

#### Gerekli Kurulum
- **libusb driver** kurulumu zorunlu!
- Detaylı kurulum: [INSTALL_DRIVERS.md](INSTALL_DRIVERS.md)
- Test script'i: `python test_udmx.py`

---

## 🎉 Özellikler v1.0.0

### ✅ Eklenen Özellikler

#### 1. 📊 Loglama Sistemi
- **Otomatik Log Kayıtları**: Tüm işlemler `logs/` klasöründe kaydedilir
- **Zaman Damgalı Dosyalar**: Her oturum için ayrı log dosyası
- **Otomatik Temizlik**: Son 10 oturum saklanır, eskiler silinir
- **Detaylı Bilgi**: Tüm bağlantı, kanal değişimi ve hata kayıtları

#### 2. 🐛 Debug (Hata Ayıklama) Modu
- **Açma/Kapama**: Debug & Logs sekmesinden aktif edilir
- **Detaylı Kayıt**: Her kanal değişimi kaydedilir
- **Performans Metrikleri**: Frame iletim süreleri ve istatistikler
- **Kalıcı Ayar**: Debug modu tercihi kaydedilir

#### 3. 📺 Kanal Monitörü
- **Canlı Görüntüleme**: 9 kanalın anlık değerleri
- **Otomatik Güncelleme**: 100ms'de bir güncellenir
- **Kolay Okunabilir**: Tablo formatında gösterim

#### 4. 📈 İstatistik Paneli
- **Frame Sayacı**: Gönderilen toplam DMX frame sayısı
- **Hata Sayacı**: İletim hatalarının sayısı
- **FPS Göstergesi**: Saniyedeki frame sayısı (~40 olmalı)

#### 5. ⚙️ Yapılandırma Yönetimi
- **Otomatik Kayıt**: Ayarlar otomatik kaydedilir
- **Son Port**: Son kullanılan seri port hatırlanır
- **Debug Modu**: Tercih edilen debug modu durumu

## 🚀 Kullanım

### İlk Kullanım

#### 1. libusb Driver Kurulumu (ZORUNLU!)
```bash
# Windows: Zadig kullan (https://zadig.akeo.ie/)
# Linux: sudo apt-get install libusb-1.0-0-dev
# macOS: brew install libusb
```
**Detaylı kurulum**: [INSTALL_DRIVERS.md](INSTALL_DRIVERS.md)

#### 2. Python Bağımlılıkları
```bash
pip install -r requirements.txt
```

#### 3. Bağlantıyı Test Et
```bash
python test_udmx.py
```

#### 4. Uygulamayı Başlat
```bash
python dmx_controller.py
```

### Ana Arayüz

#### 📑 Sekmeler

**1. Controls (Kontroller)**
- DMX kanal kontrolleri (1-9)
- Bağlantı yönetimi
- İstatistik görüntüleme
- Hızlı işlem butonları

**2. Debug & Logs (Hata Ayıklama & Loglar)**
- Debug modu açma/kapama
- Kanal monitörü (canlı değerler)
- Log görüntüleme
- Log dışa aktarma

**3. Info (Bilgi)**
- Sürüm bilgileri
- Kanal haritası
- Teknik detaylar
- Dokümantasyon

### Debug Modunu Kullanma

1. **Debug Modunu Aç**
   ```
   - "Debug & Logs" sekmesine git
   - "Debug Mode (Verbose Logging)" kutusunu işaretle
   - Artık detaylı loglar kaydediliyor
   ```

2. **Kanalları İzle**
   ```
   - Cihaza bağlan
   - "Debug & Logs" sekmesinde "Channel Monitor" bölümünü izle
   - Tüm kanal değerleri canlı görünür
   ```

3. **İstatistikleri Kontrol Et**
   ```
   - "Controls" sekmesinde "Statistics" paneline bak
   - Frames: Gönderilen frame sayısı
   - Errors: Hata sayısı (0 olmalı)
   - FPS: Saniyedeki frame (38-42 arası normal)
   ```

4. **Logları Dışa Aktar**
   ```
   - "Debug & Logs" sekmesine git
   - "Export Logs" butonuna tıkla
   - Log dosyası logs/ klasörüne kaydedilir
   ```

## 📊 Log Örnekleri

### Normal Çalışma
```
2025-10-18 15:30:45 - INFO - DMX Controller v1.0.0 başlatılıyor
2025-10-18 15:30:50 - INFO - COM3 portuna bağlanılıyor
2025-10-18 15:30:51 - INFO - Başarıyla bağlandı
```

### Debug Modu
```
2025-10-18 15:31:15 - DEBUG - Kanal 6: 0 -> 128
2025-10-18 15:31:16 - DEBUG - Kanal 6: 128 -> 255
2025-10-18 15:31:20 - DEBUG - 1000 frame gönderildi, süre: 1.23ms
```

### Hatalar
```
2025-10-18 15:35:10 - ERROR - Bağlantı hatası: Port bulunamadı
2025-10-18 15:35:20 - ERROR - Gönderim hatası: Erişim engellendi
```

## 📁 Dosya Yapısı

```
dmx/
├── dmx_controller.py       # Ana uygulama
├── dmx_simple_test.py      # Test scripti
├── requirements.txt        # Python bağımlılıkları
├── README.md               # Ana dokümantasyon
├── CHANGELOG.md            # Sürüm geçmişi
├── DEBUG_GUIDE.md          # Debug kılavuzu (İngilizce)
├── VERSION_INFO.md         # Sürüm detayları
├── HIZLI_BASLANGIC.md     # Bu dosya
├── config.json            # Ayarlar (otomatik oluşur)
└── logs/                  # Log dosyaları
    └── dmx_controller_YYYYMMDD_HHMMSS.log
```

## 🎯 İstatistikleri Yorumlama

### İyi Performans ✅
```
Frames: 12,450
Errors: 0
FPS: 39.8
```
**Durum**: Her şey normal çalışıyor

### Sorunlu Durum ⚠️
```
Frames: 2,100
Errors: 45
FPS: 15.2
```
**Olası Sebepler**:
- USB kablosu kalitesi düşük
- Sürücü sorunu
- Port başka bir uygulama tarafından kullanılıyor

## 🔧 Sorun Giderme

### Bağlantı Sorunu
1. "Debug & Logs" sekmesini aç
2. Logları kontrol et
3. Hata mesajını gör:
   ```
   ERROR - Connection error: Port not found
   ```
4. **Çözüm**: USB kablosunu kontrol et, sürücüleri kur

### Performans Sorunu
1. İstatistiklere bak (FPS < 30)
2. Logları kontrol et:
   ```
   DEBUG - Last frame time: 15.67ms
   ```
3. **Çözüm**: 
   - Diğer USB uygulamalarını kapat
   - Daha iyi USB kablosu kullan
   - USB 2.0/3.0 portuna takın (hub değil)

### Hata Sayısı Artıyor
1. Error sayısını izle
2. Logları kontrol et
3. **Olası sebepler**:
   - Port başka uygulamada açık
   - USB bağlantısı kopuyor
   - UDMX cihazı sorunlu

## 📝 Log Dosyalarını Görüntüleme

### Windows PowerShell
```powershell
# Son log dosyasını canlı izle
Get-Content logs\dmx_controller_*.log -Wait -Tail 50
```

### Uygulama İçinde
```
1. "Debug & Logs" sekmesine git
2. Log görüntüleyici otomatik güncellenir (2 saniyede bir)
3. "Refresh" butonu ile manuel güncelle
```

## 🎓 İpuçları

### 1. Sürekli Kullanım
- Debug modunu açık bırakmayın (performans için)
- İstatistikleri düzenli kontrol edin
- Sorun olduğunda logları dışa aktarın

### 2. Hata Ayıklama
- Sorun yaşadığınızda debug modunu açın
- Kanal monitörünü izleyin
- Logları kaydedin

### 3. Performans
- FPS 38-42 arasında olmalı
- Error sayısı 0 olmalı
- Frame süresi < 5ms olmalı

## 📞 Destek

Sorun bildirirken ekleyin:
1. Dışa aktarılmış log dosyası
2. İstatistik paneli ekran görüntüsü
3. Kanal monitörü değerleri
4. UDMX cihaz modeli
5. İşletim sistemi versiyonu

## 🔗 Kaynaklar

- **README.md** - Tam dokümantasyon (İngilizce)
- **DEBUG_GUIDE.md** - Detaylı debug kılavuzu (İngilizce)
- **CHANGELOG.md** - Sürüm geçmişi
- **Info Sekmesi** - Uygulama içi yardım

## 🎉 Özet

### Ana Özellikler
✅ 9 kanal DMX kontrolü  
✅ Grafik arayüz  
✅ Kapsamlı loglama sistemi  
✅ Debug modu ile detaylı takip  
✅ Canlı kanal monitörü  
✅ İstatistik takibi  
✅ Otomatik yapılandırma kaydetme  
✅ Log dışa aktarma  

### Teknik Detaylar
- **Versiyon**: 1.0.0
- **Baud Rate**: 250000 (DMX standardı)
- **Güncelleme Hızı**: ~40 Hz
- **Kanal Sayısı**: 9 (512 desteklenir)
- **Log Tutma**: Son 10 oturum

---

**İyi kullanımlar!** 🎭✨

