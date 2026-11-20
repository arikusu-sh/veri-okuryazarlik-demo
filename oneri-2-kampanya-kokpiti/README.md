# 🟡 Turkcell 360° Kampanya Performans & A/B Testi Kokpiti

**Yapay Zekâ ile Veri Okuryazarlığı & Vibe Coding Atölyesi (Öneri 2)**

Bu klasör, Turkcell **Pazarlama ve Dijital Servisler** ekiplerinin yazılımcı olmadan **Gemini Desktop App** ile **Keşifsel Veri Analizi (EDA)** yapmasını, verideki gizli **Simpson Paradoksu**'nu yakalamasını ve yarım bırakılmış bir rapor ekranını (**Skeleton**) tam teşekküllü bir karar destek kokpitine dönüştürmesini sağlar.

## 📁 Klasör Yapısı

* `katilimci_handbook.html`: **Katılımcı Uygulama Rehberi (Trainee Handbook)** — Katılımcıların tarayıcıda açıp adım adım takip edeceği, sıfır terminal komutu içeren, tek tıkla kopyalanabilir prompt rehberi.
* `egitmen_handbook.html`: **Eğitmen El Kitabı (Instructor Handbook)** — Eğitmenin atölye akışını, verideki gizli tuzakların tam sayılarını ve canlı müdahale ipuçlarını takip edeceği rehber.
* `data/turkcell_kampanya_ab_verisi.csv`: 1.200 satırlık, içerisinde bilerek bırakılmış veri kirlilikleri, Gece 22-03 Bot Saldırısı ve Instagram Simpson Paradoksu barındıran kampanya veri seti.
* `data/generate_data.py`: Veri setini sıfırdan üreten Python betiği.
* `app_skeleton.py`: Katılımcıların başlangıçta açacağı **eksik/bozuk iskelet Streamlit uygulaması**.
* `app_cozum_referans.py`: Atölye sonunda ulaşılması hedeflenen **tamamlanmış referans kokpit uygulaması**.
* `requirements.txt`: Gerekli Python kütüphaneleri (`streamlit`, `pandas`).

---

## 💬 Katılımcılar İçin: Gemini Desktop App ile Başlatma (Sıfır Terminal Komutu)

Katılımcıların terminal açmasına gerek yoktur. **Gemini Desktop App** içinde bu klasörü açıp sohbet ekranına şu promptu yapıştırmaları yeterlidir:

> **Prompt #0 (Kurulum ve Başlatma):**
> Merhaba! Ben yazılımcı değilim, bu yüzden tüm teknik kurulum adımlarını benim yerime senin yapmanı istiyorum:
> 1. Bu proje klasöründe `.venv` adında bir Python sanal ortamı yoksa oluştur ve `requirements.txt` içindeki paketleri bu sanal ortama yükle.
> 2. Ardından bu sanal ortamı kullanarak `app_skeleton.py` uygulamasını arka planda çalıştır ve tarayıcımda açabileceğim bağlantıyı (`http://localhost:8501` gibi) bana yaz.
> 3. Son olarak bu klasördeki dosyaların ne işe yaradığını bana kısaca iş birimi dilinde özetle.

---

## 🛠️ Eğitmen / Geliştirici İçin Manuel Terminal Komutları (Opsiyonel)

Eğer terminalden manuel kurulum yapmak isterseniz (`externally-managed-environment` hatası almamak için sanal ortam ile):

```bash
cd oneri-2-kampanya-kokpiti
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app_skeleton.py
```
