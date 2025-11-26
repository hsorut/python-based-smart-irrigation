# Python + Arduino Basit Akıllı Tarım Sistemi

Bu proje, bir toprak nem sensörü kullanarak toprağın nem durumunu ölçen, bu veriyi seri port üzerinden Python'a gönderen ve PC'de çalışan Python betiği tarafından belirlenen nem eşiğine göre sulama pompasını otomatik olarak çalıştıran bir sistemdir.

Tüm karar verme mantığı Python tarafındadır; Arduino sadece sensör okuma ve röle tetikleme için bir "köprü" görevi görür.

# Donanım Gereksinimleri

* Arduino UNO (veya klonu)
* Toprak Nem Sensörü (Analog çıkışlı, A0 pini olan)
* 5V Tek Kanallı Röle Modülü
* Mini Su Pompası (Genellikle 5V veya 6V ile çalışır)
* **Harici Güç Kaynağı** (Pompa için, örn: 5V 2A adaptör veya 4'lü kalem pil kutusu. **Pompa ASLA Arduino'dan beslenmemelidir.**)
* Breadboard
* Jumper Kablolar
* USB-A'dan USB-B'ye kablo (Arduino için)

# Yazılım Gereksinimleri

* **Arduino IDE**
* **Python 3**
* **Python Kütüphanesi:**
    * `pyserial`

---

# Kurulum ve Hazırlık

## FAZ 1: Bilgisayar Hazırlığı (Yazılım)
Devreyi kurmaya başlamadan önce bilgisayarındaki yazılımların tam olduğundan emin ol.

1.  **Arduino IDE'yi Kur:** Zaten kurulu değilse, resmi sitesinden indir ve kur.

2.  **Python'u Kur:** Zaten kurulu değilse, python.org'dan kur.

3.  **Gerekli Arduino Kütüphanelerini Yükle:**
    * Bu proje için (`DHT` veya `LiquidCrystal` gibi) **ekstra bir kütüphaneye gerek yoktur**. Gerekli tüm fonksiyonlar Arduino'nun temel kütüphanesinde mevcuttur.

4.  **Gerekli Python Kütüphanesini Yükle (Kritik Adım):**
    * Bilgisayarının Terminal'ini (veya Komut İstemi'ni / CMD) aç.
    * Şu komutu yazıp Enter'a bas: `pip install pyserial`
    * **Neden?** `pyserial` kütüphanesi, Python'un bilgisayarının USB portları üzerinden Arduino ile konuşmasını ("seri iletişim") sağlayan araçtır. Bu olmadan Python kodu çalışmaz.

## FAZ 2: Devre Kurulumu (Donanım)
**Önemli:** Bu adımları yaparken Arduino'nun USB kablosu bilgisayara takılı olmasın.

1.  **Breadboard'a Güç Ver (Arduino için):**
    * Arduino'daki **5V** pininden Breadboard'un kırmızı **(+)** hattına bir kablo çek.
    * Arduino'daki **GND** pininden Breadboard'un mavi **(-)** hattına bir kablo çek.

2.  **Toprak Nem Sensörünü Bağla:**
    * **VCC** pinini -> Breadboard'un kırmızı **(+)** hattına.
    * **GND** pinini -> Breadboard'un mavi **(-)** hattına.
    * **A0 (Analog Çıkış)** pinini -> Arduino'nun **A0** pinine.
    * **Neden A0?** Çünkü `tarim_arduino.ino` dosyasında `#define NEM_SENSOR_PIN A0` olarak bu pini biz belirledik.

3.  **Röle Modülünü Bağla (Kontrol Tarafı):**
    * **VCC** pinini -> Breadboard'un kırmızı **(+)** hattına (Arduino 5V).
    * **GND** pinini -> Breadboard'un mavi **(-)** hattına (Arduino GND).
    * **IN** pinini -> Arduino'nun Dijital Pin **7**'sine.
    * **Neden Pin 7?** Çünkü `tarim_arduino.ino` dosyasında `#define RELAY_PIN 7` olarak bu pini biz belirledik.

4.  **Pompa ve Harici Güç Bağlantısı (Yük Tarafı - ÇOK ÖNEMLİ):**
    * **Kesinlikle Arduino'nun 5V pinini KULLANMAYIN!**
    * Harici 5V Güç Kaynağının **(+) Artı** ucunu -> Rölenin **COM** (Ortak) klemensine bağlayın.
    * Rölenin **NO** (Normally Open / Normalde Açık) klemensinden -> Mini Su Pompasının **(+) Artı** kablosuna bir kablo çekin.
    * Harici 5V Güç Kaynağının **(-) Eksi** ucunu -> Mini Su Pompasının **(-) Eksi** kablosuna bağlayın.
    * **Neden?** Pompa, Arduino'nun verebileceğinden çok daha fazla akım çeker. Doğrudan bağlarsanız Arduino'nuzu yakarsınız. Röle, düşük güçlü Arduino sinyaliyle yüksek güçlü harici bir gücü anahtarlamamızı sağlar.

## FAZ 3: Arduino'yu Programlama (Devrenin Beyni)

1.  Devre kurulumu bittikten sonra, Arduino'yu USB kablosuyla bilgisayara bağla.
2.  `tarim_arduino.ino` dosyasını Arduino IDE ile aç.
3.  **En Önemli Kontrol (Port Seçimi):**
    * Arduino IDE'de **Araçlar > Kart** menüsünden "Arduino UNO" seçili olmalı.
    * **Araçlar > Port** menüsüne git. Orada **COM3**, **COM5** (Windows) veya **/dev/ttyUSB0** (Mac/Linux) gibi bir port görmelisin. Bu, Arduino'nun bilgisayara bağlandığı kapıdır. **Bu portun adını (örn: COM3) aklında tut.**
4.  IDE'deki "Upload" (Sağa bakan ok) düğmesine bas.
5.  **Doğrulama (Opsiyonel ama Önemli):**
    * Yükleme bittikten sonra Arduino IDE'nin sağ üst köşesindeki "Serial Monitor" (Seri Port Ekranı) simgesine tıkla.
    * Açılan pencerenin sağ alt köşesindeki baud hızını **9600** olarak ayarla.
    * Ekranda her 2 saniyede bir `NEM:750`... `NEM:745`... `NEM:760`... gibi değerlerin aktığını görmelisin.
    * Sensörü elinle sıktığında değerin düşmesi (ıslanması), havaya kaldırdığında yükselmesi (kuruması) gerekir.
    * **Bu çalışıyorsa, devren ve Arduino kodun %100 doğrudur.**

## FAZ 4: Python'u Çalıştırma (Bilgisayar Kontrolü)

1.  **KRİTİK UYARI:** Arduino IDE'deki **"Serial Monitor" (Seri Port Ekranı) penceresini KAPAT.**
    * **Neden?** Bir USB portu (örn: COM3) aynı anda sadece tek bir program tarafından kullanılabilir. Python'un çalışması için portu IDE'nin serbest bırakması gerekir. "Port açılamadı" hatası alırsan ilk bakacağın yer burasıdır.

2.  `tarim_python.py` dosyasını bir metin editörü (VS Code, Notepad++ vb.) ile aç.

3.  **ZORUNLU DEĞİŞİKLİK:** Kodun üstlerindeki şu satırı bul:
    ```python
    ARDUINO_PORT = 'COM3' 
    ```
    * Buradaki `'COM3'` yazan yeri, **FAZ 3, Adım 3'te aklında tuttuğun kendi port adınla değiştir.** (Belki seninki COM4 veya COM5'tir). Tırnak işaretleri kalsın.

4.  **KALİBRASYON:** Aynı dosyada `NEM_ESIGI = 700` satırını bul. FAZ 3, Adım 5'te yaptığın teste göre (toprağın kuruduğunu kabul ettiğin değer) bu eşiği güncelle.

5.  Dosyayı kaydet.

6.  Terminali (Komut İstemi) aç ve `cd` komutu ile `tarim_python.py` dosyasının bulunduğu klasörün içine git.

7.  Şu komutu yazarak programı başlat:
    ```sh
    python tarim_python.py
    ```

## FAZ 5: Projeyi Test Etme

1.  Terminal ekranında `COM3 portu açıldı...` mesajını ve ardından her 2 saniyede bir `Alınan Veri: Toprak Nem Düzeyi = ...` şeklinde akan verileri görmelisin.

2.  **Alarmı Test Et (Kuru Durum):**
    * Sensör probunu topraktan veya sudan çıkarıp havada tut (en kuru durum).
    * Nem değeri `NEM_ESIGI` olarak belirlediğin eşiği geçtiği anda:
    * **Terminalde:** `UYARI! Nem... Sulama başlatılıyor...` yazısı çıkacak.
    * **Donanımda:** Röle modülü "tık" diye bir ses çıkaracak ve üzerindeki ışık yanacak. Su pompası çalışmaya başlayacak.

3.  **Sistemin Normale Dönüşü (Islak Durum):**
    * Sensör probunu bir bardak suya veya çok ıslak toprağa daldır.
    * Nem değeri eşiğin altına düştüğü anda:
    * **Terminalde:** `Nem normale döndü. Sulama durduruldu.` yazısı çıkacak.
    * **Donanımda:** Röle modülü tekrar "tık" diyecek ve pompa duracaktır.