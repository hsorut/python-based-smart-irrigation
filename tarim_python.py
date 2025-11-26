import serial # pyserial kütüphanesi
import time

# --- Ayarlar ---
# Bu değeri kendi sensörünüz ve toprağınız için kalibre etmelisiniz.
# Arduino'dan gelen analog değere (0-1023) göre bir eşik belirleyin.
# Yüksek değer = Kuru, Düşük değer = Islak
# Test için Serial Monitor'den kuru ve ıslak değerleri okuyun.
NEM_ESIGI = 700  # Örnek: Değer 700'ün üstündeyse "kuru" kabul et

# BU KISIM ÇOK ÖNEMLİ
# Arduino IDE'de (Araçlar > Port) gördüğünüz port adını buraya yazın
# Windows için: 'COM3', 'COM4' vb.
# macOS/Linux için: '/dev/ttyUSB0', '/dev/tty.usbmodemXXXX' vb.
ARDUINO_PORT = 'COM3' 
BAUD_RATE = 9600

def baslat_baglanti(port, baud):
    """Seri port bağlantısını başlatmayı dener."""
    try:
        ser = serial.Serial(port, baud, timeout=2) # 2 saniye zaman aşımı
        print(f"{port} portu açıldı. Arduino verisi bekleniyor...")
        time.sleep(2) # Arduino'nun yeniden başlaması için bekleme süresi
        return ser
    except serial.SerialException as e:
        print(f"HATA: Port açılamadı ({port}). {e}")
        print("Arduino'nun bağlı olduğundan ve doğru portu seçtiğinizden emin olun.")
        print("Arduino IDE'nin Seri Port Ekranı'nın kapalı olduğundan emin olun.")
        return None

def ana_dongu(ser):
    """Ana veri okuma ve karar verme döngüsü."""
    sulama_durumu = False # Mevcut sulama durumunu takip et
    try:
        while True:
            # Arduino'dan gelen bir satır veriyi oku (örn: b'NEM:750\r\n')
            try:
                line = ser.readline()
                if not line:
                    continue
                
                # Gelen veriyi (byte) string'e çevir ve temizle
                data_str = line.decode('utf-8').strip()
                
                if not data_str.startswith("NEM:"):
                    # Veri bozuksa veya başlangıç verisiyse atla
                    continue 

                # Veriyi parçala: "NEM:750"
                nem_str = data_str.split(':')[1] 
                nem_degeri = int(nem_str)
                
                print(f"Alınan Veri: Toprak Nem Düzeyi = {nem_degeri}")

                # --- Karar Verme (Projenin kalbi) ---
                if nem_degeri > NEM_ESIGI: # Toprak kuru
                    if not sulama_durumu: # Eğer zaten sulama yapılmıyorsa
                        print(f"UYARI! Nem ({nem_degeri}) eşik değerini ({NEM_ESIGI}) aştı!")
                        print("Sulama başlatılıyor...")
                        ser.write(b"SULA\n") # Arduino'ya 'SULA' komutu gönder
                        sulama_durumu = True
                
                else: # Toprak yeterince nemli
                    if sulama_durumu: # Eğer daha önce sulama yapıldıysa
                        print("Nem normale döndü. Sulama durduruldu.")
                        ser.write(b"DUR\n") # Arduino'ya 'DUR' komutu gönder
                        sulama_durumu = False

            except (UnicodeDecodeError, IndexError, ValueError, TypeError):
                # Arduino başladığında veya veri bozulduğunda oluşabilir
                print(f"Geçersiz veya bozuk veri alındı: {line}")
                continue
            except Exception as e:
                print(f"Beklenmedik bir hata oluştu: {e}")

    except KeyboardInterrupt:
        print("\nProgram kullanıcı tarafından sonlandırıldı.")
    finally:
        # Program kapanırken her şeyi normale döndür
        if ser and ser.is_open:
            print("Çıkış yapılıyor... Pompa kapatılıyor.")
            ser.write(b"DUR\n") # Pompayı kesin olarak kapat
            ser.close()
            print("Seri port kapatıldı.")

if __name__ == "__main__":
    seri_port = baslat_baglanti(ARDUINO_PORT, BAUD_RATE)
    if seri_port:
        ana_dongu(seri_port)
    else:
        print("Bağlantı kurulamadı. Program sonlandırılıyor.")