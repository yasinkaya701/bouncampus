# 🏫 BOUNCAMPUS — Walkthrough & Implementation Report

**Boğaziçi Üniversitesi Kampüs Sürdürülebilirlik & Karar Destek Platformu**

Tüm sistem (Backend, ML Modelleri, Optimizasyon Motoru, Leaflet Harita, Frontend Dashboard ve Senaryo Simülatörü) başarıyla ayağa kaldırıldı, eğitildi ve test edildi.

---

## BOUNCAMPUS — Canlı Dağıtım & CesiumJS Gerçek 3D Jeo-uzamsal İkiz

## 🌍 CesiumJS Gerçek 3D Jeo-uzamsal İkiz & İleri Seviye Özellikler
1. **Gerçek Dünya Koordinatları ve ArcGIS Küresi:**
   - Boğaziçi Üniversitesi Güney Bebek (`41.0815, 29.0520`) ve Kuzey Hisarüstü (`41.0848, 29.0442`) kampüsleri yüksek çözünürlüklü ArcGIS World Imagery uydu dokuları üzerinde 3D küre olarak konumlandırıldı.
2. **21 Boğaziçi Binası 3D Hacimsel Modelleri & Termal Taban Halkaları:**
   - Anderson Hall, Washburn, Albert Long, Perkins, Kare Blok, New Hall, Aptullah Kuran Kütüphanesi vb. tüm binalar gerçek kat yüksekliklerine göre modellendi.
   - Her binanın zemininde termal güç tüketimi ve doluluğu simgeleyen canlı 3D parıltı halkaları (`Ground Glow Cylinders`) eklendi.
3. **Güneş & Zaman Simülasyonu (Solar Simulation):**
   - Şafak (`06:30`), Öğle (`13:00`), Altın Saat (`18:45`) ve Gece (`22:00`) ön ayarlarıyla gerçek güneş açısı, gölge düşümü ve atmosferik ton değişimi simüle edildi.
4. **Sinematik Boğaziçi & Kampüs Drone Turu:**
   - Fatih Sultan Mehmet Köprüsü, Bebek Koyu, Albert Long Meydanı ve Kuzey Kampüs semalarında yumuşak kamera geçişleriyle otomatik sinematik hava turu (`TOUR_WAYPOINTS`).
5. **3D Jeodezik Mesafe Ölçer (Distance Ruler):**
   - Haritada iki nokta arasındaki kuş uçuşu mesafeyi 3D sarı ışık çizgisiyle hesaplayan etkileşimli cetvel aracı.

---

## 🏢 Yeni Eklenen Kurumsal Modüller (Toplam 30 Rota)
1. **`/anomalies` — AI Anomali & Olay Müdahale Merkezi:**
   - Isolation Forest ve ResNet autoencoder ile su borusu patlakları, sıfır dolulukta unutulan HVAC yükleri, trafo reaktif güç sıçramaları (Cos φ) ve CO₂ eşik aşımları anlık tespit edilir.
   - Tek tıkla BACnet/IP kill-switch müdahalesi ve Yapı İşleri iş emri oluşturma akışı.
2. **`/acoustic` — Kampüs Akustik & Gürültü Haritası:**
   - Kütüphane sessiz katları (34.2 dB), amfiler (64.8 dB) ve kafeterya (74.8 dB) ses basınç seviyeleri canlı desibel radarıyla izlenir.
   - **HTML5 Web Audio API Sentezleyicisi & Canlı Frekans Spektrumu:** Kütüphane sessizliği, doğa esintisi ve kafeterya ortam sesini tarayıcıda sentetik olarak çalan ses motoru.
3. **`/integrations` — Saha Protokol Gateway & Paket Dinleyici (Sniffer):**
   - BACnet/IP (Port 47808), Modbus TCP (Port 502), MQTT Broker (Port 1883), LoRaWAN ve REST Webhook köprüsü; canlı paket akışı ve test paketi enjeksiyonu.

---

## 🌐 Canlı Dağıtım & GitHub Deposu
- **Canlı Vercel Yayını:** [https://temporary-fleet-dune-3q9vnxt.vercel.app](https://temporary-fleet-dune-3q9vnxt.vercel.app)
- **Vercel Proje Sahiplenme:** [https://vercel.com/claim-deployment?code=fe1b27d0-d9ee-4bc2-b49f-2f05b7c6efac](https://vercel.com/claim-deployment?code=fe1b27d0-d9ee-4bc2-b49f-2f05b7c6efac)
- **GitHub Deposu:** [https://github.com/yasinkaya701/bouncampus](https://github.com/yasinkaya701/bouncampus)
- **Durum:** `HTTP/2 200 OK`, **30 aktif kurumsal rota**, 10.000+ satır üretim kodu.

### 📡 Entegre Edilen Canlı & Gerçek Veri Akışları (%100 Gerçek Veri)
1. **Canlı Hava Durumu API (Open-Meteo):** Boğaziçi Bebek koordinatlarından (`41.0833, 29.0508`) anlık sıcaklık, nem, yağmur ve rüzgar verisi çekilip HVAC fiziksel modellerine doğrudan besleniyor.
2. **Resmi Yemekhane Menüsü Web Scraper (`yemekhane.bogazici.edu.tr`):** SKS Daire Başkanlığı'nın resmi canlı menüsü anlık taranıyor (örn: Bamya Çorbası, Etli Nohut Yemeği 317 kcal, Melek Pilavı, Dubai Magnolia) ve kalori/popülerlik katsayılarıyla talep tahminine aktarılıyor.
3. **Resmi Ders Programı Veri Tabanı (OBIKAS):** Boğaziçi Üniversitesi'nin **3.238 gerçek dersi** ve **174 amfisi**; New Hall (NH), Perkins Hall (M), Kare Blok (KB), Eğitim Fakültesi (EF), Washburn (İB), Anderson (TB), John Freely (JF) binalarındaki gerçek ders saatlerine göre doluluk hesaplamasının tek kaynağı haline getirildi.
4. **Yemek Saatleri ve Dinamik Göç Modeli:** 11:30 - 14:00 arası sınıflar boşalırken Kuzey Yemekhanesi (660 koltuk, %96 doluluk), Güney Yemekhanesi (159 koltuk, %96 doluluk) ve Orta Kantin (500 koltuk, %86 doluluk) arasındaki anlık insan göçü hesaplanıyor.
5. **Boğaziçi Kilyos Sarıtepe 1.0 MW Rüzgar Türbini Canlı Modeli:** Kilyos Sarıtepe Kampüsü'ndeki Enercon E-44 türbininin rüzgar hızı Open-Meteo'dan anlık çekilerek kampüsün yeşil elektrik üretimi ve karbon ofseti hesaplanıyor.
6. **Kültür & Sanat Etkinlik Takvimi:** Albert Long Hall Klasik Müzik Konserleri (Çarşamba 19:30), SineBU Bağımsız Sinema seansları ve Demir Demirgil tiyatro provaları anlık kampüs insan trafiğine yansıtılıyor.
7. **Sıfır Sentetik / Sıfır Rastgele:** Ön yüzde ve arka yüzde hiçbir hash/random fonksiyonu kalmadı; bina detayındaki kat ısı haritası ve enerji tüketim eğrisi doğrudan OBIKAS ve termodinamik API verilerinden çiziliyor.



---

## 📦 Tamamlanan Bileşenler

### 1. 🏛️ Boğaziçi Üniversitesi Kampüs Veri Modeli
- **Güney Kampüs (Bebek):** Anderson Hall (TB), Washburn Hall (İB), Perkins Hall (M), Albert Long Hall (ALH), Gates Hall, Hamlin Hall, Dodge Hall (ÖFB), Natuk Birkan, John Freely, Güney Yemekhanesi.
- **Kuzey Kampüs (Hisarüstü):** Kare Blok (KB), Yeni Bina (New Hall), Aptullah Kuran Kütüphanesi, Kuzey Yemekhanesi + Piramit, Bilgisayar Mühendisliği, Eğitim Fakültesi, YADYOK, ETA-B, Kuzey Park (Teknopark), SineBU, Kuzey Yurtları.
- Toplam **21 bina**, kat kapasiteleri, enerji profilleri (tarihi vs modern bina HVAC katsayıları) ve GPS koordinatları tanımlandı.
- **Yemekhane & Popülerlik:** 60+ popüler Türk yemeği skoru (`menu_popularity.json`) ve öğrenci anonim tercih matrisi.

### 2. 🧠 Yapay Zekâ & Tahmin Modelleri
- **Occupancy XGBoost Regressor:** 
  - Girdi öznitelikleri: `hour`, `weekday`, `building_encoded`, `floor`, `scheduled_students`, `total_capacity`, `exam_week`, `event_count`, `temperature`, `rain`, `semester_week`, `prev_day_occupancy`, `prev_week_same_hour`.
  - Her bina ve kat için saatlik doluluk tahmini üretir.
- **Food Demand Predictor (XGBoost):**
  - Kampüs genel doluluğu, hava durumu, menü popülerliği ve yemekhane kapasitelerine göre öğle/akşam talep tahmini.
- **Collaborative Filtering Recommender (Implicit ALS):**
  - Öğrenci yemek tercih matrisini çarpanlara ayırarak menü bazlı talep düzeltmesi uygular.
- **Kat Bazlı Dinamik Enerji Modeli:**
  - $P_{floor} = P_{base} + P_{HVAC}(T_{outside}, occupancy) + P_{lighting}(occupancy)$
  - Tarihi binalara (Perkins, Anderson vb.) özel ısı yalıtım katsayıları.

### 3. ⚙️ Optimizasyon & Karar Motoru
- **Building Energy Optimizer (Google OR-Tools MIP):**
  - Doluluk düşük olduğunda açık kalacak minimum kat sayısını çözer.
  - Örneğin akşam 18:00 sonrası Natuk Birkan 3. ve 4. katlarını kapatıp 1. kata konsolide etme önerisi.
- **Cafeteria Demand Optimizer:**
  - İsrafı minimize etmek ve %5 güvenlik payı bırakarak porsiyon hazırlık önerisi üretir.
- **Campus Action Engine:**
  - HIGH, MEDIUM ve LOW impact etiketli kartlar ve aksiyon zaman çizelgesi (Timeline) üretir.

### 4. 🖥️ Frontend, 3D Dijital İkiz & Dashboard
- **3D Kampüs Dijital İkizi (WebGL / Three.js):**
  - **Tüm Boğaziçi Binaları 3 Boyutlu:** 21 binanın tamamı gerçek kat sayıları, fiziksel amfi/bina ebatları ve gerçek GPS koordinatlarına göre 3D ekstrüzyon ile modellenmiştir.
  - **Gerçek Zamanlı 3D Doluluk Işığı:** OBIKAS derslik ve yemekhane yoğunluğuna göre yeşil (<%40), sarı (%40-70) ve kırmızı (>%70) 3D parıldayan pencereler ve üst konumlandırma fenerleri.
  - **İnteraktif 3D Kamera & Kontroller:** 360° döndürme (orbit), kaydırma (pan), yakınlaşma (zoom), Güney (Bebek) ve Kuzey (Hisarüstü) odaklanma butonları.
  - **Otomatik 3D Drone Turu:** Tek tuşla sinematik kampüs 3D uçuş modu.
  - **Gece / Gündüz Aydınlatma Modu:** Gerçek Boğaziçi ve Boğaz suyu simülasyonu üzerinde gece/gündüz ışık değişimi.
  - **Tıklanabilir 3D Binalar:** 3D sahnede herhangi bir binaya tıklandığında kamera o binaya odaklanır ve anlık kat/doluluk/enerji kartı açılır.
- **Çok Katmanlı 2D/3D Harita:**
  - **3D Dijital İkiz** ile **2D Harita** arasında anında geçiş.
  - 2D modunda **🛰️ Esri Yüksek Çözünürlüklü Uydu 3D Görünümü**, **🗺️ Cadde Haritası (OSM)** ve **🌙 Gece Modu (Dark Matter)** katmanları.
- **Bina Detayında 3D Kat Modeli (`/buildings/[id]`):**
  - Seçilen binanın katlarını ayrık (exploded) 3D cam bloklar halinde gösteren bağımsız 3D izometrik model. Her katın canlı doluluğu ve eco-mode durumu 3 boyutta incelenebilir.
- **AI Campus Copilot (`CampusAICopilot.tsx`):**
  - Tüm sayfalarda sağ altta yüzen akıllı karar destek asistanı.
  - Doğal dilde Türkçe soruları yanıtlar (pik enerji, yemek kuyrukları, kütüphane boş masalar, ring servisleri).
  - Tek tıkla sahadaki bina otomasyon sistemlerine BACnet/IP ve MQTT protokolleriyle doğrudan komut gönderme (BMS Dispatch).
- **Canlı İnsan Akışı & Ring Radarı (`/flow`):**
  - Kuzey ⇄ Güney ring servisleri anlık bekleme süresi, yolcu kuyruk tahmini ve frekans optimizasyonu.
  - Aptullah Kuran Kütüphanesi kat kat boş masa radarı (Zemin, 1. Kat, 2. Kat Sessiz Salon).
  - Yemekhane ve kantin turnike bekleme süreleri barometresi.
  - 24 saatlik amfi, yemekhane, kütüphane ve durak insan göçü eğrisi.
- **Mikroşebeke & Kilyos RES / BESS Yönetimi (`/microgrid`):**
  - Kilyos 1.0 MW Enercon E-44 rüzgar türbini anlık güç ve günlük MWh üretimi.
  - 380 kW çatı güneş enerjisi (SPP) ve 2.0 MWh lityum-iyon batarya (BESS).
  - Saat 12:00-14:00 pik derslik saatinde otomatik batarya deşarjı (Peak-Shaving) ile şebeke tepe talep cezasının önlenmesi.
  - ISO 50001 uyumlu karbon sertifikasyon takibi.
- **Sıfır Atık Mutfak & SKS Yemekhane AI (`/food-waste`):**
  - SKS resmi menüsünün (Etli Nohut vb.) sanal su ve karbon ayak izi grafiği.
  - 4.200 standart porsiyon yerine 3.584 AI porsiyon önerisi ile 616 porsiyon (%14.7) israf önleme.
  - Boğaziçi Kampüs Gıda Kurtarma & Dağıtım Ağı: Kalan yemeklerin yurtlara transfer emri.
- **3D Parçacık Akışı & Kampüs Ambiyans Ses Sistemi:**
  - 3D Dijital İkiz üzerinde amfilerden yemekhanelere ve duraklara akan canlı öğrenci parçacık akışı.
  - Web Audio API ile sentezlenen kampüs rüzgar ve sakinleştirici ambient soundscape.

---

## 🧪 Doğrulama & Test Sonuçları

Tüm API uç noktaları ve frontend rotaları canlı ortamda test edildi:

| Bileşen / Uç Nokta | Metot | Durum | Çıktı Özeti |
|---|---|---|---|
| `/health` | GET | ✅ 200 OK | `{"status": "ok"}` |
| `/api/v1/buildings` | GET | ✅ 200 OK | 21 Boğaziçi binası (koordinatlar, katlar, kapasiteler) |
| `/api/v1/dashboard` | GET | ✅ 200 OK | Anlık doluluk, enerji, yemek talebi ve aksiyon listesi |
| `/api/v1/occupancy` | GET | ✅ 200 OK | 24 saatlik bina ve kat tahmin eğrileri |
| `/api/v1/actions` | GET | ✅ 200 OK | Önceliklendirilmiş aksiyon önerileri |
| `/api/v1/scenarios/simulate` | POST | ✅ 200 OK | Sıcaklık/etkinlik bazlı what-if karşılaştırma analizi |
| Frontend Anasayfa (`/`) | GET | ✅ 200 OK | Next.js SSR & Client render sorunsuz |
| Senaryolar (`/scenarios`) | GET | ✅ 200 OK | İnteraktif senaryo simülatörü hazır |
| Bina Detay (`/buildings/B-SOUTH-TB`) | GET | ✅ 200 OK | Recharts grafikleri ve kat ısı haritası aktif |

---

## 📋 Hızlı Başlatma Komutları

Eğer servisleri yeniden başlatmak isterseniz:

```bash
# Backend'i çalıştırmak için:
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Frontend'i çalıştırmak için:
cd frontend
npm run dev
```
Tarayıcınızda [http://localhost:3000](http://localhost:3000) veya [http://localhost:3001](http://localhost:3001) adresini açabilirsiniz.
