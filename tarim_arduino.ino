/*
  Basit Akıllı Tarım Sistemi (Arduino Köprüsü)
  
  Bu kod, Arduino'yu bir "köprü" olarak kullanır.
  1. Toprak nem sensörünün analog değerini okur.
  2. Bu değeri seri port üzerinden Python'a (bilgisayara) gönderir.
  3. Python'dan "SULA" veya "DUR" komutlarını bekler.
  4. Gelen komuta göre röleyi (pompayı) açar veya kapatır.
*/

// --- Pin Tanımlamaları ---
#define NEM_SENSOR_PIN A0  // Toprak nem sensörünün ANALOG çıkış pini
#define RELAY_PIN 7        // Röle modülünün IN pini

void setup() {
  // Seri iletişimi başlat (Python ile bu hızda konuşacağız)
  Serial.begin(9600);
  
  // Pin modlarını ayarla
  pinMode(RELAY_PIN, OUTPUT);
  
  // Başlangıçta pompanın kapalı olduğundan emin ol
  // Çoğu röle modülü 'LOW' (DÜŞÜK) sinyali ile aktif olur (Active-LOW).
  // Bu yüzden 'HIGH' (YÜKSEK) göndererek pompayı başlangıçta kapalı tutuyoruz.
  digitalWrite(RELAY_PIN, HIGH); 
  
  Serial.println("Arduino Hazir. Python baglantisi bekleniyor...");
}

void loop() {
  // 1. Sensörden veriyi oku
  // analogRead 0 (çok ıslak) ile 1023 (çok kuru) arasında bir değer verir
  int nemDegeri = analogRead(NEM_SENSOR_PIN);

  // 2. Veriyi Python'a Gönder
  // Format: NEM:DEGER
  Serial.print("NEM:");
  Serial.println(nemDegeri);

  // 3. Python'dan komut bekle
  if (Serial.available() > 0) {
    // Satır sonuna kadar gelen veriyi oku
    String command = Serial.readStringUntil('\n');
    command.trim(); // Başındaki/sonundaki boşlukları temizle

    if (command == "SULA") {
      // Röleyi aktif et (pompayı çalıştır)
      digitalWrite(RELAY_PIN, LOW); // Active-LOW röle için
    } 
    else if (command == "DUR") {
      // Röleyi kapat (pompayı durdur)
      digitalWrite(RELAY_PIN, HIGH); // Active-LOW röle için
    }
  }

  // Veri gönderme ve okuma arasında bir gecikme
  // Python betiğiyle senkronize olması için
  delay(2000); 
}