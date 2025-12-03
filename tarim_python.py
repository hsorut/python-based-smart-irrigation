import serial 
import time


NEM_ESIGI = 700  


# Arduino IDE'de (Araçlar > Port) gördüğünüz port adını buraya yaz
# Windows için: 'COM3', 'COM4' vb.
# macOS/Linux için: '/dev/ttyUSB0', '/dev/tty.usbmodemXXXX' vb.
ARDUINO_PORT = 'COM3' 
BAUD_RATE = 9600

def baslat_baglanti(port, baud):
    """Seri port bağlantısını başlatmayı dener."""
    try:
        ser = serial.Serial(port, baud, timeout=2)
        print(f"{port} portu açıldı. Arduino verisi bekleniyor...")
        time.sleep(2) 
        return ser
    except serial.SerialException as e:
        print(f"HATA: Port açılamadı ({port}). {e}")
        print("Arduino'nun bağlı olduğundan ve doğru portu seçtiğinizden emin olun.")
        print("Arduino IDE'nin Seri Port Ekranı'nın kapalı olduğundan emin olun.")
        return None

def ana_dongu(ser):
    """Ana veri okuma ve karar verme döngüsü."""
    sulama_durumu = False 
    try:
        while True:
            
            try:
                line = ser.readline()
                if not line:
                    continue
                
                
                data_str = line.decode('utf-8').strip()
                
                if not data_str.startswith("NEM:"):
                    
                    continue 

                
                nem_str = data_str.split(':')[1] 
                nem_degeri = int(nem_str)
                
                print(f"Alınan Veri: Toprak Nem Düzeyi = {nem_degeri}")

                # --- Karar Verme 
                if nem_degeri > NEM_ESIGI: 
                    if not sulama_durumu: 
                        print(f"UYARI! Nem ({nem_degeri}) eşik değerini ({NEM_ESIGI}) aştı!")
                        print("Sulama başlatılıyor...")
                        ser.write(b"SULA\n") 
                        sulama_durumu = True
                
                else: 
                    if sulama_durumu: 
                        print("Nem normale döndü. Sulama durduruldu.")
                        ser.write(b"DUR\n") 
                        sulama_durumu = False

            except (UnicodeDecodeError, IndexError, ValueError, TypeError):
                
                print(f"Geçersiz veya bozuk veri alındı: {line}")
                continue
            except Exception as e:
                print(f"Beklenmedik bir hata oluştu: {e}")

    except KeyboardInterrupt:
        print("\nProgram kullanıcı tarafından sonlandırıldı.")
    finally:
        
        if ser and ser.is_open:
            print("Çıkış yapılıyor... Pompa kapatılıyor.")
            ser.write(b"DUR\n") 
            ser.close()
            print("Seri port kapatıldı.")

if __name__ == "__main__":
    seri_port = baslat_baglanti(ARDUINO_PORT, BAUD_RATE)
    if seri_port:
        ana_dongu(seri_port)
    else:
        print("Bağlantı kurulamadı. Program sonlandırılıyor.")