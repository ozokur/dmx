# 🎮 Gamepad Control Guide - PS5 DualSense

DMX Controller artık **PS5 DualSense** kontrolcüsü ile pan/tilt kontrolünü destekliyor!

## ✨ Özellikler

- 🕹️ **Sol Analog Stick** → Pan & Tilt kontrolü
- 🎯 **Gerçek zamanlı** hareket
- 🎚️ **Hassas kontrol** (deadzone desteği)
- 🔄 **Otomatik güncelleme** (~50 Hz)
- 📊 **GUI senkronizasyonu**

## 🎮 Kontrol Haritası

### Sol Analog Stick (Left Stick)
```
        ↑ Tilt Up
        |
← Pan Left — • — Pan Right →
        |
      ↓ Tilt Down
```

- **X Ekseni (Yatay)** → Channel 1 (Horizontal Rotation / Pan)
- **Y Ekseni (Dikey)** → Channel 2 (Vertical Rotation / Tilt)

### L2 Trigger (Left Trigger)
```
Not Pressed ═══════════ Fully Pressed
    0                       249 (max)
```

- **L2 Analog Trigger** → Channel 5 (Strobe Speed)
- Hafif bas = yavaş strobe
- Tam bas = hızlı strobe (max 249)

### R2 Trigger (Right Trigger)
```
Not Pressed ═══════════ Fully Pressed
    0                       255
```

- **R2 Analog Trigger** → Channel 6 (Dimming / Brightness)
- Hafif bas = az ışık
- Tam bas = tam ışık

### Değer Dönüşümü

**Analog Stick (Pan/Tilt):**
```
Analog Value:  -1.0  ←→  0.0  ←→  +1.0
DMX Value:       0   ←→  127  ←→   255
```

**L2 Trigger (Strobe):**
```
Trigger Value: -1.0 (not pressed) ←→ +1.0 (fully pressed)
DMX Value:       0  (no strobe)   ←→  249  (max strobe speed)
```

**R2 Trigger (Dimmer):**
```
Trigger Value: -1.0 (not pressed) ←→ +1.0 (fully pressed)
DMX Value:       0  (dark)        ←→  255  (full brightness)
```

### Face Buttons (Color Control)
```
X Button     → Channel 3 = 5
Square Button → Channel 3 = 18
Circle Button → Channel 3 = 34
```

- **Face Buttons** → Channel 3 (Color selection)
- **Toggle behavior**: Değer başka butona basılana kadar kalır
- X → Kırmızı renk tonu
- Square → Yeşil renk tonu
- Circle → Mavi renk tonu

## 📦 Kurulum

### 1. pygame Kütüphanesini Yükle
```bash
pip install pygame
# veya
pip install -r requirements.txt
```

### 2. PS5 DualSense Bluetooth Bağlantısı

#### Windows 10/11
1. **Bluetooth Ayarları**
   - Settings > Devices > Bluetooth & other devices
   - "Add Bluetooth or other device" tıkla

2. **DualSense Pairing Modu**
   - PS Button + Share Button'a 3 saniye basılı tut
   - Işık bar yanıp sönmeye başlayacak

3. **Cihazı Bağla**
   - "Wireless Controller" görünecek
   - Tıkla ve pair et
   - Işık bar sabit mavi yanacak

#### Windows (DS4Windows - Alternatif)
```bash
# DS4Windows indir (daha iyi uyumluluk)
https://ds4-windows.com/

# Kurulum sonrası otomatik tanınır
```

#### Linux
```bash
# Bluetooth servisini başlat
sudo systemctl start bluetooth

# bluetoothctl ile pair
bluetoothctl
> scan on
> pair [MAC_ADDRESS]
> connect [MAC_ADDRESS]
> trust [MAC_ADDRESS]
```

#### macOS
1. System Preferences > Bluetooth
2. DualSense'i pairing moduna al (PS + Share)
3. Listede "DualSense Wireless Controller" göründüğünde pair et

## 🚀 Kullanım

### 1. Uygulamayı Başlat
```bash
python dmx_controller.py
```

### 2. UDMX Cihazına Bağlan
1. "Refresh" → UDMX cihazını bul
2. "Connect" → Bağlan

### 3. Gamepad Kontrolünü Aktif Et
1. "🎮 Gamepad Control" bölümünü bul
2. ✅ DualSense tespit edildiyse yeşil işaret göreceksin
3. "Enable Pan/Tilt Control (Left Stick)" kutusunu işaretle
4. Status: **Active 🎮** olacak

### 4. Kontrol Et!
- Sol analog stick'i hareket ettir
- Pan/Tilt kanalları otomatik güncellenecek
- Slider'lar da real-time hareket edecek

## ⚙️ Ayarlar

### Deadzone (Ölü Bölge)
```python
# dmx_controller.py içinde
deadzone = 0.1  # 0.0 ile 1.0 arası
```
- **Düşük değer** (0.05): Daha hassas, drift olabilir
- **Yüksek değer** (0.2): Daha az hassas, drift yok

### Güncelleme Hızı
```python
time.sleep(0.02)  # 50 Hz (20ms)
```
- **Daha hızlı**: `0.01` (100 Hz) - Daha responsive ama CPU kullanımı yüksek
- **Daha yavaş**: `0.05` (20 Hz) - CPU tasarrufu ama delay olabilir

## 🐛 Debug Modu

Debug modunda gamepad aktivitesini izle:

1. **"Debug & Logs"** sekmesine git
2. **"Debug Mode"** aktif et
3. Log'larda göreceksin:
```
DEBUG - Gamepad control loop started
DEBUG - Channel 1: 127 -> 143
DEBUG - Channel 2: 127 -> 98
```

## ❗ Sorun Giderme

### "No gamepad detected"

**Windows:**
```
1. Bluetooth bağlantısını kontrol et
2. Settings > Devices > DualSense görünüyor mu?
3. DS4Windows kullanıyorsan kapatmayı dene
4. Uygulamayı yeniden başlat
```

**Test et:**
```bash
python -c "import pygame; pygame.init(); pygame.joystick.init(); print(f'Gamepads: {pygame.joystick.get_count()}')"
```

### Gamepad lag/gecikme

1. **Bluetooth bağlantı kalitesini iyileştir**
   - USB Bluetooth dongle kullan (dahili yerine)
   - Uzaklığı azalt (maksimum 3 metre)
   - Engelleri kaldır

2. **Güncelleme hızını artır**
   ```python
   time.sleep(0.01)  # 100 Hz
   ```

3. **USB kablo kullan**
   - DualSense'i USB-C kablo ile bağla
   - Daha az gecikme, şarj da olur

### Stick drift (istenmeyen hareket)

```python
# Deadzone'u artır
deadzone = 0.15  # Varsayılan: 0.1
```

### Eksik veya yanlış eksen

```bash
# Eksen numaralarını kontrol et
python test_gamepad.py  # (aşağıda)
```

## 🧪 Test Scripti

Gamepad'in doğru çalışıp çalışmadığını test et:

```python
# test_gamepad.py
import pygame
import time

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("❌ No gamepad detected!")
    exit()

gamepad = pygame.joystick.Joystick(0)
gamepad.init()

print(f"✅ Gamepad: {gamepad.get_name()}")
print(f"Axes: {gamepad.get_numaxes()}")
print(f"Buttons: {gamepad.get_numbuttons()}")
print("\nMove left stick and watch values:")
print("Press Ctrl+C to exit\n")

try:
    while True:
        pygame.event.pump()
        
        x = gamepad.get_axis(0)
        y = gamepad.get_axis(1)
        
        print(f"\rLeft Stick - X: {x:+.3f}  Y: {y:+.3f}  ", end='')
        time.sleep(0.05)
except KeyboardInterrupt:
    print("\n\nTest completed!")
```

Kaydet ve çalıştır:
```bash
python test_gamepad.py
```

## 📊 Performans

### Beklenen Değerler
- **Update Rate**: ~50 Hz (20ms)
- **Input Lag**: < 30ms (Bluetooth), < 10ms (USB)
- **CPU Usage**: ~1-2%

### İyileştirme İpuçları
1. **USB kablo kullan** (en iyi performans)
2. **Bluetooth 5.0+ adaptör** kullan
3. **Arka plan programlarını** kapat
4. **Debug modunu** kapat (daha hızlı)

## 🎯 Gelişmiş Kullanım

### Diğer Kanallar İçin Buton Mapping (Gelecek)

```python
# Örnek: Sağ analog stick → Color & Gobo
right_x = gamepad.get_axis(2)  # Color
right_y = gamepad.get_axis(3)  # Gobo

# Trigger → Dimming
l2_trigger = gamepad.get_axis(4)  # Dimming

# Face buttons → Quick actions
if gamepad.get_button(0):  # X button
    self.all_off()
if gamepad.get_button(3):  # Triangle
    self.full_brightness()
```

## 🌟 PS5 DualSense Özellikleri

### Şu Anda Kullanılan
- ✅ Sol analog stick (Pan/Tilt)

### Gelecekte Eklenebilir
- 🔲 Sağ analog stick (Color/Gobo)
- 🔲 L2/R2 Triggers (Dimming/Strobe)
- 🔲 D-Pad (Preset selection)
- 🔲 Face buttons (Quick actions)
- 🔲 Touchpad (Scene switching)
- 🔲 Gyro (Motion control)
- 🔲 Haptic feedback (İşlem onayı)
- 🔲 Adaptive triggers (Efekt yoğunluğu)

## 💡 İpuçları

1. **Hassas Ayar İçin**
   - Stick'i yavaşça hareket ettir
   - Merkezde tutmak için hafifçe basınç uygula

2. **Hızlı Hareket İçin**
   - Stick'i tam olarak yana bastır
   - Quick snap movements için

3. **Sabit Pozisyon İçin**
   - İstediğin pozisyonda bırak
   - DMX değeri sabit kalacak

4. **Sıfırlama**
   - Gamepad kontrolünü kapat
   - Manuel slider'ları kullan
   - Tekrar aç

## 📝 Notlar

- ⚠️ **Gamepad kontrolü aktifken** manuel slider'lar güncellenecek ama gamepad değerleri üzerine yazacak
- 💡 **Hassas ayar** için hem gamepad hem manuel kullanabilirsin (gamepad'i kapat, fine-tune et)
- 🔋 **Pil durumu** düşükse gecikme artabilir
- 🔌 **USB bağlantı** en iyi performansı verir

## 🆘 Yardım

Sorun yaşıyorsan:
1. `test_gamepad.py` çalıştır
2. "Debug & Logs" sekmesinde logları kontrol et
3. DualSense'i yeniden pair et
4. Uygulamayı yeniden başlat

---

**İyi eğlenceler!** 🎮🎭✨

