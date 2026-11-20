import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

OUTPUT_PATH = Path(__file__).parent / "turkcell_kampanya_ab_verisi.csv"

SERVICES = ["TV+ Süper Paket", "Fizy Premium", "Game+ GeForce NOW", "Lifebox 500GB", "BiP Yıldızlar"]
CREATIVES = [
    "A - %40 İndirim Fırsatı",
    "B - İlk Ay +10GB Hediye",
    "C - Gamer & E-Spor Özel",
    "D - Son 24 Saat (FOMO)",
]
SEGMENTS = ["GNÇ (18-26)", "Profesyonel (27-40)", "Aile & Ev (41+)", "Gamer Pro"]
DEVICES = ["iOS", "Android"]
TIME_SLOTS = ["Sabah (08-12)", "Öğle (12-17)", "Akşam (17-22)", "Gece (22-03)"]


def format_dirty_budget(amount_tl: float, row_idx: int) -> str:
    """Bilerek farklı para birimi/yazım formatları ve hatalı negatif kayıtlar üretir."""
    if row_idx % 85 == 0:
        # İade/mahsuplaşma hatası olarak girilmiş negatif bütçe
        return f"-{amount_tl:.0f} TL"
    if row_idx % 47 == 0:
        # Dolar olarak girilmiş bütçe (Kur ~35 TL varsayımı)
        usd_val = max(10, round(amount_tl / 35))
        return f"${usd_val}"
    if row_idx % 19 == 0:
        return f"₺{amount_tl:,.0f}"
    if row_idx % 11 == 0:
        return f"{amount_tl:.2f} TL"
    return f"{round(amount_tl)}"


def generate_dataset(num_rows: int = 1200):
    rows = []
    start_date = datetime(2026, 10, 1)

    for i in range(1, num_rows + 1):
        day_offset = random.randint(0, 29)
        tarih = (start_date + timedelta(days=day_offset)).strftime("%Y-%m-%d")

        # Kanal seçimi ve bilerek yapılan yazım hataları (Dirty Data #1)
        true_channel = random.choices(
            ["Instagram", "SMS", "BiP", "Push Bildirim"],
            weights=[0.35, 0.25, 0.22, 0.18],
        )[0]

        if true_channel == "Instagram" and random.random() < 0.08:
            kanal = random.choice(["IG", "instagram", "Instagram "])
        elif true_channel == "BiP" and random.random() < 0.09:
            kanal = random.choice(["bip", "BiP "])
        else:
            kanal = true_channel

        # Simpson Paradoksu Kurgusu:
        # Instagram bütçesinin %75'i yanlışlıkla "Aile & Ev (41+)" segmentine ve "Sabah (08-12)" saatine harcanıyor!
        # Orada dönüşüm çok düşük (%0.3). Ama "Gamer Pro" veya "GNÇ (18-26)" + "Akşam (17-22)" + "C - Gamer & E-Spor Özel"
        # kombinasyonunda Instagram dönüşümü %8.5 ve LTV çok yüksek!
        if true_channel == "Instagram":
            if random.random() < 0.74:
                segment = "Aile & Ev (41+)"
                saat = "Sabah (08-12)"
                kreatif = "A - %40 İndirim Fırsatı"
                servis = random.choice(["TV+ Süper Paket", "Lifebox 500GB"])
            else:
                segment = random.choice(["Gamer Pro", "GNÇ (18-26)"])
                saat = "Akşam (17-22)"
                kreatif = random.choice(["C - Gamer & E-Spor Özel", "B - İlk Ay +10GB Hediye"])
                servis = random.choice(["Game+ GeForce NOW", "Fizy Premium"])
        elif true_channel == "BiP":
            segment = random.choices(SEGMENTS, weights=[0.35, 0.30, 0.20, 0.15])[0]
            saat = random.choices(TIME_SLOTS, weights=[0.20, 0.25, 0.45, 0.10])[0]
            kreatif = random.choices(CREATIVES, weights=[0.20, 0.45, 0.20, 0.15])[0]
            servis = random.choice(SERVICES)
        else:
            segment = random.choice(SEGMENTS)
            saat = random.choice(TIME_SLOTS)
            kreatif = random.choice(CREATIVES)
            servis = random.choice(SERVICES)

        cihaz = random.choices(DEVICES, weights=[0.42, 0.58])[0]
        gosterim = random.randint(1500, 25000)

        # Temel CTR ve Dönüşüm Oranları
        if true_channel == "Instagram":
            if segment in ["Gamer Pro", "GNÇ (18-26)"] and saat == "Akşam (17-22)":
                ctr = random.uniform(0.065, 0.095)
                cvr = random.uniform(0.075, 0.105) if "Gamer" in kreatif else random.uniform(0.055, 0.080)
                cpm = random.uniform(85, 115)
                ltv_base = random.uniform(1450, 2100)
            else:
                # Yanlış hedefleme yapılan devasa bütçe dilimi
                ctr = random.uniform(0.008, 0.016)
                cvr = random.uniform(0.002, 0.006)
                cpm = random.uniform(110, 150)
                ltv_base = random.uniform(450, 750)
        elif true_channel == "BiP":
            ctr = random.uniform(0.045, 0.075)
            cvr = random.uniform(0.048, 0.072) if "Hediye" in kreatif else random.uniform(0.032, 0.050)
            cpm = random.uniform(22, 38)  # Kendi kanalımız olduğu için çok düşük maliyet!
            ltv_base = random.uniform(1100, 1650)
        elif true_channel == "SMS":
            ctr = random.uniform(0.022, 0.038)
            cvr = random.uniform(0.025, 0.040)
            cpm = random.uniform(45, 65)
            ltv_base = random.uniform(700, 1050)
        else:  # Push Bildirim
            ctr = random.uniform(0.030, 0.052)
            cvr = random.uniform(0.028, 0.048)
            cpm = random.uniform(15, 28)
            ltv_base = random.uniform(850, 1300)

        tiklama = max(1, int(gosterim * ctr))
        abonelik_donusumu = max(0, int(tiklama * cvr))
        butce_tl = (gosterim / 1000.0) * cpm

        # Anomali: Gece saatlerinde Bot Tıklama Saldırısı (Tıklama > Gösterim ve 0 Dönüşüm!)
        if saat == "Gece (22-03)" and i % 9 == 0:
            tiklama = int(gosterim * random.uniform(1.15, 1.65))
            abonelik_donusumu = 0
            butce_tl = butce_tl * 2.5

        # Eksik veri (Missing Values)
        hedef_kitle_str = "" if (i % 37 == 0) else segment
        ltv_str = "" if (i % 53 == 0) else f"{ltv_base:.1f}"

        rows.append(
            {
                "kampanya_id": f"TKC-{1000 + i}",
                "tarih": tarih,
                "servis_adi": servis,
                "kanal": kanal,
                "kreatif_varyant": kreatif,
                "hedef_kitle": hedef_kitle_str,
                "cihaz_tipi": cihaz,
                "gonderim_saati": saat,
                "gosterim": gosterim,
                "tiklama": tiklama,
                "abonelik_donusumu": abonelik_donusumu,
                "harcanan_butce": format_dirty_budget(butce_tl, i),
                "kullanici_degeri_ltv": ltv_str,
            }
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Veri seti oluşturuldu: {OUTPUT_PATH} ({len(rows)} satır)")


if __name__ == "__main__":
    generate_dataset()
