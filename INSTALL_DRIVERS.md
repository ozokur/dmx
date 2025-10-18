# UDMX Driver Kurulum Kılavuzu

DMX Controller artık **doğrudan USB üzerinden UDMX** cihazlarına bağlanıyor!

## ⚠️ Önemli: libusb Kurulumu Gerekli

UDMX cihazları ile çalışmak için **libusb** sürücüleri gereklidir.

---

## 🪟 Windows Kurulum

### Yöntem 1: Zadig ile Kolay Kurulum (Önerilen)

1. **Zadig İndir**
   - https://zadig.akeo.ie/ adresinden indirin
   - Kurulum gerektirmez, direkt çalıştırın

2. **UDMX Cihazını Takın**
   - USB portuna UDMX cihazınızı takın

3. **Zadig'i Çalıştırın**
   - Zadig'i **Yönetici olarak çalıştırın**
   - Options > List All Devices'i işaretleyin

4. **UDMX Cihazını Seçin**
   - Listeden UDMX cihazınızı bulun:
     - "uDMX" veya
     - "DMXControl" veya
     - VID: 16C0, PID: 05DC şeklinde

5. **Driver Değiştirin**
   - Sağ taraftaki dropdown'dan **libusb-win32** veya **WinUSB** seçin
   - "Replace Driver" veya "Install Driver" butonuna tıklayın
   - İşlem bitene kadar bekleyin (1-2 dakika)

6. **Tamamlandı!**
   - Zadig'i kapatın
   - DMX Controller'ı başlatın

### Yöntem 2: libusb-win32 Manuel Kurulum

1. https://sourceforge.net/projects/libusb-win32/ adresinden indirin
2. Kurulum sihirbazını çalıştırın
3. UDMX cihazınız için driver'ı seçin ve yükleyin

---

## 🐧 Linux Kurulum

### Ubuntu/Debian

```bash
# libusb kütüphanesini yükle
sudo apt-get update
sudo apt-get install libusb-1.0-0-dev

# Python bağımlılıklarını yükle
pip install -r requirements.txt

# USB erişim izinleri (önemli!)
sudo nano /etc/udev/rules.d/50-udmx.rules
```

Aşağıdaki satırı ekleyin:
```
SUBSYSTEM=="usb", ATTR{idVendor}=="16c0", ATTR{idProduct}=="05dc", MODE="0666"
```

Kaydedin ve udev'i yeniden yükleyin:
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

UDMX cihazını çıkarıp tekrar takın.

### Fedora/RedHat/CentOS

```bash
sudo dnf install libusb-devel
pip install -r requirements.txt

# USB izinleri için yukarıdaki udev kuralını uygulayın
```

### Arch Linux

```bash
sudo pacman -S libusb
pip install -r requirements.txt

# USB izinleri için yukarıdaki udev kuralını uygulayın
```

---

## 🍎 macOS Kurulum

### Homebrew ile

```bash
# libusb kur
brew install libusb

# Python bağımlılıkları
pip install -r requirements.txt
```

macOS'ta genellikle ek izin gerekmez, ancak ilk kullanımda "System Preferences > Security" onayı istenebilir.

---

## 🔍 Bağlantı Testi

### Python ile Test

```python
import usb.core

# UDMX cihazını bul
dev = usb.core.find(idVendor=0x16C0, idProduct=0x05DC)

if dev is None:
    print("UDMX cihazı bulunamadı!")
    print("- USB kablosunu kontrol edin")
    print("- Driver kurulumunu kontrol edin")
else:
    print(f"UDMX cihazı bulundu!")
    print(f"Vendor ID: {dev.idVendor:04X}")
    print(f"Product ID: {dev.idProduct:04X}")
```

Bu scripti `test_udmx.py` olarak kaydedin ve çalıştırın:
```bash
python test_udmx.py
```

---

## ❗ Sorun Giderme

### "No backend available" Hatası

**Windows:**
- Zadig ile libusb driver kurulumunu tekrarlayın
- WinUSB yerine libusb-win32 deneyin

**Linux:**
```bash
sudo apt-get install libusb-1.0-0-dev
pip uninstall pyusb
pip install pyusb --no-cache-dir
```

**macOS:**
```bash
brew reinstall libusb
pip install pyusb --force-reinstall
```

### "Access Denied" veya "Permission Denied" Hatası

**Windows:**
- DMX Controller'ı **Yönetici olarak çalıştırın**
- Zadig ile driver'ı tekrar yükleyin

**Linux:**
- udev kurallarını kontrol edin (yukarıya bakın)
- Kullanıcınızı `plugdev` grubuna ekleyin:
```bash
sudo usermod -a -G plugdev $USER
```
- Çıkış yapıp tekrar giriş yapın

**macOS:**
- Genellikle izin sorunu olmaz
- Gerekirse `sudo python dmx_controller.py` deneyin (önerilmez)

### "Device Not Found" Hatası

1. **USB Kablosunu Kontrol Edin**
   - Farklı bir USB portu deneyin
   - Hub yerine doğrudan PC'ye takın

2. **Device Manager Kontrolü (Windows)**
   - Device Manager'ı açın
   - "Universal Serial Bus devices" veya "Unknown devices" kontrol edin
   - Sarı ünlem işareti varsa driver sorunu var

3. **lsusb ile Kontrol (Linux)**
```bash
lsusb | grep -i dmx
# veya
lsusb
# Listede 16c0:05dc arıyın
```

4. **System Information (macOS)**
   - Apple menü > About This Mac > System Report
   - USB bölümünü kontrol edin

### Driver Çakışması

**Windows'ta COM port driver'ı yüklüyse:**
1. Device Manager'ı açın
2. UDMX cihazını bulun
3. Sağ tık > "Uninstall device"
4. "Delete the driver software" işaretleyin
5. Cihazı çıkarıp tekrar takın
6. Zadig ile libusb driver yükleyin

---

## 📋 Desteklenen UDMX Cihazları

### Test Edilmiş Cihazlar
- ✅ Anyma uDMX (VID:16C0 PID:05DC)
- ✅ DMXControl uDMX (VID:03EB PID:8888)

### Desteklenen Chip'ler
- FTDI FT245RL
- Atmel AVR
- Generic USB-DMX adaptörleri

---

## 🆘 Hala Çalışmıyor mu?

### Debug Bilgisi Toplama

1. DMX Controller'ı başlatın
2. "Debug & Logs" sekmesine gidin
3. "Debug Mode" açın
4. Bağlanmayı deneyin
5. "Export Logs" ile logları kaydedin

### Destek İçin Gereken Bilgiler
- İşletim sistemi ve versiyonu
- UDMX cihaz modeli
- Exported log dosyası
- `lsusb` çıktısı (Linux/Mac) veya Device Manager ekran görüntüsü (Windows)

---

## 🎯 Başarılı Bağlantı

Bağlantı başarılı olduğunda:
- ✅ "Status: Connected" yeşil olur
- ✅ "Refresh" butonuyla UDMX cihazı listede görünür
- ✅ İstatistikler güncellenir (Frames, FPS)
- ✅ Kanal değişiklikleri cihaza gönderilir

---

## 📚 Ek Kaynaklar

- **Zadig**: https://zadig.akeo.ie/
- **libusb**: https://libusb.info/
- **pyusb Documentation**: https://github.com/pyusb/pyusb
- **UDMX Protocol**: http://www.anyma.ch/research/udmx/

---

**Başarılı kurulumlar!** 🎭✨

