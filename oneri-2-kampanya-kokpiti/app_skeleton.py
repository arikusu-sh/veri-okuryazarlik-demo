from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Kampanya Raporu (Taslak - v0.1)",
    page_icon="📊",
    layout="wide",
)

DATA_PATH = Path(__file__).parent / "data" / "turkcell_kampanya_ab_verisi.csv"

st.title("📊 Dijital Servisler Kampanya Raporu (Skeleton v0.1)")
st.warning(
    "⚠️ **Atölye Başlangıç Noktası:** Bu ekran henüz tamamlanmamış bir iskelettir (skeleton). "
    "Verideki kalite sorunları temizlenmemiş, sol menüdeki filtreler tabloya bağlanmamış ve "
    "bütçe simülatörü henüz kodlanmamıştır. Antigravity ile konuşarak bu ekranı **360° Kampanya Kokpiti**ne dönüştüreceğiz!"
)

# 1. Ham veriyi doğrudan yüklüyoruz (Henüz veri temizliği yok!)
df = pd.read_csv(DATA_PATH)

# Sol Menü (Sidebar) - Henüz çalışmayan taslak filtreler
st.sidebar.header("🔍 Filtreler (Henüz Çalışmıyor)")
secilen_servis = st.sidebar.selectbox("Servis Seçin", ["Tümü"] + list(df["servis_adi"].unique()))
secilen_kanal = st.sidebar.multiselect("Kanal Seçin", list(df["kanal"].unique()))
st.sidebar.info("💡 İpucu: Bu filtreler henüz aşağıdaki grafiklere bağlı değil. Vibe Coding ile bağlayacağız!")

# 2. Üst Metrik Kartları (Bazı metrikler kirli veri yüzünden hesaplanamıyor!)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Toplam Kayıt (Satır)", f"{len(df):,}")
with col2:
    st.metric("Toplam Gösterim", f"{df['gosterim'].sum():,}")
with col3:
    st.metric("Toplam Tıklama", f"{df['tiklama'].sum():,}")
with col4:
    # harcanan_butce sütununda 'TL', '$', '₺' gibi metinler olduğu için doğrudan toplanamıyor!
    st.metric("Toplam Harcanan Bütçe", "❌ HESAPLANAMIYOR (Kirli Veri)")

st.divider()

# 3. Basit Kanal Grafiği (Yazım hataları yüzünden aynı kanal 3-4 farklı sütun gibi görünüyor!)
st.subheader("1. Kanallara Göre Abonelik Dönüşümü (Ham Veri)")
st.caption("Dikkat: 'Instagram', 'IG', 'instagram' ve 'BiP', 'bip' ayrı kanallar gibi görünüyor!")
kanal_ozet = df.groupby("kanal")[["gosterim", "tiklama", "abonelik_donusumu"]].sum()
st.bar_chart(kanal_ozet["abonelik_donusumu"])

st.divider()

# 4. Atölye Boyunca Eklenecek Modüller İçin Boş Alanlar
tab1, tab2, tab3 = st.tabs([
    "📋 Ham Veri Tablosu",
    "🕵️ Simpson Paradoksu & Kırılım Analizi (TODO)",
    "🎛️ Bütçe & ROAS Simülatörü (TODO)",
])

with tab1:
    st.write("İlk 100 satır (Ham CSV içeriği):")
    st.dataframe(df.head(100), use_container_width=True)

with tab2:
    st.info(
        "🚧 **Görev 2:** Genel ortalamaya bakınca Instagram başarısız görünüyor olabilir. "
        "Ancak `hedef_kitle`, `gonderim_saati` ve `kreatif_varyant` kırılımlarında gizli bir şampiyon var! "
        "Antigravity'den buraya interaktif bir kırılım (heatmap / grup grafik) eklemesini isteyin."
    )

with tab3:
    st.info(
        "🚧 **Görev 3:** Pazarlama bütçesini kanallar arasında kaydırdığımızda (slider ile) "
        "beklenen yeni abone sayısını ve ROAS'ı (Yatırım Getirisi) anlık hesaplayan simülatörü buraya kodlatın."
    )
