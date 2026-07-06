import streamlit as strl
import yfinance as yf
import time
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

strl.set_page_config(page_title="BIST Alım Radarı Pro", page_icon="🤖", layout="wide")

strl.title("📈 Yapay Zeka Destekli Gelişmiş BIST Tarama ve Analiz Terminali")
strl.markdown("Tüm BIST hisseleri havuzu; Borç, Karlılık, İskonto, **Hacim**, **Temettü Verimi**, **F/K**, **ROE** ve **Teknik Göstergelere** göre filtrelenip yapay zeka tarafından puanlanır.")

# Genişletilmiş Tüm BIST Listesi
tum_bist_kodlari = sorted([
    "A1CAP", "ACSEL", "ADEL", "ADESE", "AGHOL", "AGROT", "AHGAZ", "AKBNK", "AKCNS", "AKENR", "AKFGY", "AKFYE", "AKGRT", "AKSA", 
    "AKSEN", "ALARK", "ALBRK", "ALCAR", "ALCTL", "ALFAS", "ALGYO", "ALKA", "ALMAD", "ALTNY", "ALVES", "ANELE", "ANGEN", "ANHYT", 
    "ANSGR", "ARASE", "ARCLK", "ARDYZ", "ARENA", "ARSAN", "ARTMS", "ASCEG", "ASELS", "ASGYO", "ASTOR", "ASUZU", "ATAGY", "ATAKP", 
    "ATATP", "ATEKS", "ATLAS", "ATSYH", "AVGYO", "AVHOL", "AVOD", "AVTUR", "AYCES", "AYDEM", "AYEN", "AYGAZ", "AZTEK", "BAGFS", 
    "BARMA", "BERA", "BEYAZ", "BIENM", "BIMAS", "BIOEN", "BOBET", "BRISA", "BRSAN", "BRYAT", "BUCIM", "BVSAN", "CATES", "CCOLA", 
    "CELHA", "CEMENT", "CIMSA", "CONSE", "CVKMD", "CWENE", "DAPGM", "DERHL", "DESA", "DESPC", "DEVA", "DITAS", "DMSAS", "DOAS", 
    "DOHOL", "DOFER", "DURDO", "DYOBY", "EBEBK", "ECILC", "ECZYT", "EDATA", "EGEEN", "EGSER", "EKGYO", "EKLMN", "ELITE", "ENJSA", 
    "ENKAI", "ERCB", "EREGL", "ERSU", "ESEN", "EUPWR", "EUREN", "FLAP", "FMIZP", "FONET", "FORMT", "FRIGO", "FROTO", "GARAN", 
    "GENTS", "GEREL", "GESAN", "GIPTA", "GLBMD", "GLYHO", "GSDHO", "GUBRF", "GWIND", "GZNMI", "HALKB", "HATEK", "HEKTS", "HRZMN", 
    "HUBVC", "HUNER", "IHAAS", "IHEVA", "IHGZT", "IHLAS", "IHLGM", "INVES", "IPEKE", "ISCTR", "ISDMR", "ISFIN", "ISGYO", "ISMEN", 
    "IZENR", "IZMDC", "JANTS", "KAPLM", "KAREL", "KARSN", "KAYSE", "KCAER", "KCHOL", "KENT", "KERVT", "KFEIN", "KLMSN", "KLSYN", 
    "KLYHO", "KMPUR", "KNFRT", "KOCAER", "KONTR", "KONYA", "KORDS", "KOZAL", "KOZAA", "KPOWR", "KRVGD", "KTLEV", "KUTPO", "KSTUR", 
    "LIDER", "LKMNH", "LOGAN", "LOGO", "LUKSK", "MAALT", "MACKOL", "MAGEN", "MAKIM", "MANAS", "MARBL", "MAVI", "MEDTR", "MEGAP", 
    "MEGMT", "MEPET", "MERCN", "MERKO", "MIATK", "MIPAZ", "MMCAS", "MNDRS", "MNDTR", "MOBTL", "MPARK", "MRGYO", "MRSHL", "MSGYO", 
    "MTRKS", "MUDUR", "MUPWR", "MZHLD", "NATEN", "NETAS", "NIBAS", "NTGAZ", "NTHOL", "NUGYO", "NUHCM", "OBASE", "ODAS", "ONCSM", 
    "ORCA", "ORGE", "OSMEN", "OSTIM", "OTKAR", "OYAKC", "OYAYO", "OYLUM", "OYYAT", "OZGYO", "OZKGY", "OZSUB", "PAGYO", "PAMEL", 
    "PARSN", "PASEI", "PATEK", "PCILT", "PEGYO", "PENGD", "PETKM", "PETUN", "PGSUS", "PINSU", "PKART", "PKENT", "PNLSN", "PNSUT", 
    "POLHO", "POLTK", "PRKAB", "PRKME", "PRZMA", "PSDTC", "QUAGR", "RALYL", "RAYSG", "REEDR", "RNPOL", "RODRG", "ROYAL", "RYSAS", 
    "SAHOL", "SAMAT", "SANEL", "SANFM", "SANKO", "SARKY", "SAYAS", "SDTTR", "SEKFK", "SEKUR", "SELEC", "SELVA", "SEYKM", "SILVR", 
    "SISE", "SKBNK", "SKTAS", "SMART", "SMRTG", "SNAAM", "SNGYO", "SNICA", "SNKRN", "SOKMD", "SOKM", "SONME", "SRVGY", "SUMAS", 
    "SUNTK", "SURGY", "SUWEN", "TABGD", "TARKM", "TATGD", "TAVHL", "TCELL", "TDGYO", "TEKTU", "TERA", "TETMT", "TEZOL", "THYAO", 
    "TLMAN", "TMPOL", "TMSN", "TOASO", "TRCAS", "TRGYO", "TRILC", "TSKB", "TSPOR", "TTKOM", "TTRAK", "TUCLK", "TUKAS", "TUPRS", 
    "TUREX", "TURGG", "TURSG", "UFUK", "ULAS", "ULKER", "ULUFA", "ULUSE", "USAK", "VAKBN", "VAKFN", "VAKKO", "VANGD", "VBTYZ", 
    "VERTU", "VERUS", "VESBE", "VESTL", "VKGYO", "VKING", "YAPRK", "YATAS", "YAYLA", "YGGYO", "YGYO", "YKBNK", "YLTEK", "YONGA", 
    "YOTAS", "YYLGD", "ZEDUR", "ZNGRM", "ZRGYO"
])

def yerel_rsi_hesapla(seri, periyot=14):
    try:
        delta = seri.diff()
        kazanc = (delta.where(delta > 0, 0)).copy()
        kayip = (-delta.where(delta < 0, 0)).copy()
        
        ort_kazanc = kazanc.rolling(window=periyot, min_periods=periyot).mean()
        ort_kayip = kayip.rolling(window=periyot, min_periods=periyot).mean()
        
        for i in range(periyot, len(seri)):
            ort_kazanc.iloc[i] = (ort_kazanc.iloc[i-1] * (periyot - 1) + kazanc.iloc[i]) / periyot
            ort_kayip.iloc[i] = (ort_kayip.iloc[i-1] * (periyot - 1) + kayip.iloc[i]) / periyot
            
        rs = ort_kazanc / ort_kayip
        rsi = 100 - (100 / (1 + rs))
        return rsi
    except Exception:
        return pd.Series(50.0, index=seri.index)

def yapay_zeka_yorum_uret(sembol, potansiyel, roe_metni, borc_durumu, net_borc, temettü_verimi, rsi_degeri=None):
    yorum = f"**🤖 AI Analitik Yorumu ({sembol}):** "
    if potansiyel > 100:
        yorum += f"Gelecekteki büyüme projeksiyonlarına göre oldukça ucuz kalmış ve geniş bir güvenlik marjı sunuyor. "
    elif potansiyel > 40:
        yorum += f"Dengeli ve makul bir getiri potansiyeline sahip, adil değerinin altında işlem görüyor. "
    else:
        yorum += f"Hedef fiyatına yaklaşmış, mevcut seviyelerden giriş yapmak risk primini artırabilir. "

    if temettü_verimi > 4:
        yorum += f"🚀 %{round(temettü_verimi,1)} temettü verimiyle yatırımcısına düzenli nakit akışı sağlayan bir temettü şirketidir. "

    if net_borc == "Nakit Zengini 💰":
        yorum += "Şirket nakit zengini; bu durum yüksek faiz ortamlarında yatırımlar için devasa bir güçtür. "
    elif borc_durumu == "Yüksek Borç ⚠️":
        yorum += "Yüksek borç yükü operasyonel karlılığı faiz giderleriyle baskılayabilir, dikkat edilmeli. "
    
    if "%" in roe_metni and roe_metni != "Veri Yok":
        roe_val = float(roe_metni.replace("%", ""))
        if roe_val > 25:
            yorum += f"Özsermaye karlılığı ({roe_metni}) ile harika bir operasyonel verimliliğe sahip. "

    if rsi_degeri is not None:
        if rsi_degeri <= 35:
            yorum += f"📉 **Teknik Uyarı:** RSI değeri ({round(rsi_degeri,1)}) aşırı satım bölgesine yakın, fiyatta tepki yükselişi gelebilir."
        elif rsi_degeri >= 65:
            yorum += f"⚠️ **Teknik Uyarı:** RSI değeri ({round(rsi_degeri,1)}) aşırı alım sınırında, kısa vadeli kar satışlarına dikkat edilmeli."
        else:
            yorum += f"📊 RSI seviyesi ({round(rsi_degeri,1)}) teknik olarak nötr/dengeli bir momentumda seyrediyor."
            
    return yorum

def detayli_analiz_et(ticker_sembolu):
    hisse = yf.Ticker(f"{ticker_sembolu}.IS")
    try:
        info = hisse.info
        gecmis_1d = hisse.history(period="1d")
        if gecmis_1d.empty: return None
        
        guncel_fiyat = gecmis_1d['Close'].iloc[-1]
        son_hacim_lot = gecmis_1d['Volume'].iloc[-1]
        gunluk_hacim_tl = son_hacim_lot * guncel_fiyat
        
        raw_yield = info.get('dividendYield', 0.0)
        if raw_yield is None: raw_yield = 0.0
        temettü_verimi = raw_yield if raw_yield > 1.0 else raw_yield * 100
        if temettü_verimi > 30.0:
            temettü_verimi = temettü_verimi / 100 if (temettü_verimi / 100) < 30.0 else 0.0
        
        fk = info.get('trailingPE', 12.0)
        if fk > 100 or fk <= 0: fk = 12.0
        
        hisse_basi_kar = info.get('trailingEps', None)
        if not hisse_basi_kar or hisse_basi_kar <= 0: hisse_basi_kar = guncel_fiyat / fk

        eps_buyume = info.get('earningsGrowth', 0.25)
        buyume_yuzdesi = 25.0 if eps_buyume is None or eps_buyume <= 0 or eps_buyume > 0.40 else eps_buyume * 100

        borc_favok = info.get('debtToEbitda', None)
        borc_durumu = "Güvenli ✅" if (borc_favok is None or borc_favok < 3) else "Yüksek Borç ⚠️"

        roe = info.get('returnOnEquity', None)
        roe_val = roe * 100 if roe else 10.0
        roe_metni = f"%{round(roe_val, 1)}" if roe else "Veri Yok"

        toplam_nakit = info.get('totalCash', 0)
        toplam_borc = info.get('totalDebt', 0)
        net_borc_tutar = toplam_borc - toplam_nakit
        net_borc_metni = f"{net_borc_tutar:,.0f} TL" if net_borc_tutar > 0 else "Nakit Zengini 💰"

        carpan = min(8.5 + (1.5 * buyume_yuzdesi), 30)
        tahmini_adil_fiyat = hisse_basi_kar * carpan
        if tahmini_adil_fiyat > guncel_fiyat * 3: tahmini_adil_fiyat = guncel_fiyat * 1.85 
        guvenli_alis_noktasi = tahmini_adil_fiyat * 0.75
        potansiyel = round(((tahmini_adil_fiyat / guncel_fiyat) - 1) * 100, 1)

        try:
            teknik_gecmis = hisse.history(period="1y")
            if len(teknik_gecmis) > 14:
                rsi_serisi = yerel_rsi_hesapla(teknik_gecmis['Close'], periyot=14)
                son_rsi = rsi_serisi.iloc[-1]
                if np.isnan(son_rsi): son_rsi = 50.0
            else:
                son_rsi = 50.0
        except Exception:
            son_rsi = 50.0

        pot_skor = min(max(potansiyel / 3, 0), 40)
        roe_skor = min(max(roe_val, 0), 40)
        borc_skor = 20 if net_borc_metni == "Nakit Zengini 💰" or (borc_favok and borc_favok < 2) else 5
        temettü_bonusu = min(temettü_verimi * 1.5, 10)
        
        toplam_ai_skor = round(pot_skor + roe_skor + borc_skor + temettü_bonusu, 1)
        if toplam_ai_skor > 100: toplam_ai_skor = 100.0

        ai_yorumu = yapay_zeka_yorum_uret(ticker_sembolu, potansiyel, roe_metni, borc_durumu, net_borc_metni, temettü_verimi, son_rsi)
        
        return {
            "Hisse": ticker_sembolu,
            "Güncel Fiyat (TL)": round(guncel_fiyat, 2),
            "AI Hedef Fiyat (TL)": round(tahmini_adil_fiyat, 2),
            "Güvenli Alış (TL)": round(guvenli_alis_noktasi, 2),
            "Potansiyel (%)": potansiyel,
            "Özsermaye Karlılığı (ROE)": roe_metni,
            "ROE_Değeri": roe_val,
            "Net Borç / FAVÖK": round(borc_favok, 2) if borc_favok else "Makul",
            "Borç Riski": borc_durumu,
            "Net Borç (TL)": net_borc_metni,
            "F/K Oranı": round(fk, 2),
            "Temettü Verimi (%)": round(temettü_verimi, 2),
            "Günlük Hacim (TL)": gunluk_hacim_tl,
            "RSI (14)": round(son_rsi, 2),
            "AI Skor": toplam_ai_skor,
            "AI Yorumu": ai_yorumu
        }
    except Exception:
        return None

# ==================== STREAMLIT ARAYÜZÜ ====================

strl.sidebar.header("🎯 Profesyonel Tarama Filtreleri")

min_hacim_filtresi = strl.sidebar.number_input(
    "Minimum Günlük Hacim Eşiği (TL)", 
    min_value=0, value=5000000, step=1000000
)

min_temettu_filtresi = strl.sidebar.slider(
    "Minimum Temettü Verimi (%)", 
    min_value=0.0, max_value=20.0, value=0.0, step=0.5
)

max_fk_filtresi = strl.sidebar.slider(
    "Maksimum F/K Oranı", 
    min_value=1.0, max_value=50.0, value=25.0, step=0.5
)

min_roe_filtresi = strl.sidebar.slider(
    "Minimum Özsermaye Karlılığı (ROE %)", 
    min_value=0.0, max_value=150.0, value=0.0, step=5.0
)

max_rsi_filtresi = strl.sidebar.slider(
    "🚀 Maksimum RSI Seviyesi", 
    min_value=20.0, max_value=100.0, value=100.0, step=2.0
)

sadece_nakit_zenginleri = strl.sidebar.checkbox(
    "Sadece Nakit Zengini Şirketleri Getir 💰", 
    value=False
)

strl.subheader("🔍 Tekil Şirket Analizi")
secilen_hisse = strl.selectbox("Analiz etmek istediğiniz BIST hissesini seçin:", tum_bist_kodlari)

if strl.button("🎯 Seçilen Hisseyi Analiz Et"):
    with strl.spinner("Analiz ediliyor..."):
        res = detayli_analiz_et(secilen_hisse)
        if res:
            col1, col2 = strl.columns(2)
            col1.metric("Güncel Fiyat", f"{res['Güncel Fiyat (TL)']} TL")
            col2.metric("AI Alım Skoru", f"{res['AI Skor']} / 100")
            strl.info(res["AI Yorumu"])
            strl.table(pd.DataFrame([res]))

strl.markdown("---")
strl.subheader("⚡ Tüm BIST Akıllı Toplu Tarama")

if strl.button("🚀 Tüm BIST'i Tara ve En İyi 10 Şirketi Bul"):
    filitreli_olmayacaklar = ["AKBNK", "ALBRK", "GARAN", "HALKB", "ISCTR", "ISDMR", "YKBNK", "VAKBN", "TSKB"]
    tarama_listesi = [h for h in tum_bist_kodlari if h not in filitreli_olmayacaklar]
    tum_sonuclar = []
    toplam_adet = len(tarama_listesi)
    
    ilerleme_cubugu = strl.progress(0)
    durum_yazisi = strl.empty()
    
    with ThreadPoolExecutor(max_workers=15) as executor:
        gelecek_gorevler = {executor.submit(detayli_analiz_et, hisse): hisse for hisse in tarama_listesi}
        for i, gorev in enumerate(as_completed(gelecek_gorevler)):
            res = gorev.result()
            if res:
                if res["Günlük Hacim (TL)"] >= min_hacim_filtresi and \
                   res["Temettü Verimi (%)"] >= min_temettu_filtresi and \
                   res["F/K Oranı"] <= max_fk_filtresi and \
                   res["ROE_Değeri"] >= min_roe_filtresi and \
                   res["RSI (14)"] <= max_rsi_filtresi and \
                   (not sadece_nakit_zenginleri or res["Net Borç (TL)"] == "Nakit Zengini 💰"):
                    tum_sonuclar.append(res)
            durum_yazisi.text(f"İşleniyor: {i+1}/{toplam_adet}")
            ilerleme_cubugu.progress((i + 1) / toplam_adet)
            
    if tum_sonuclar:
        df_en_iyi_10 = pd.DataFrame(tum_sonuclar).sort_values(by="AI Skor", ascending=False).head(10)
        df_goster = df_en_iyi_10.copy()
        csv_data = df_goster.to_csv(index=False).encode('utf-8')
        
        # Güncel pandas uyumlu formatlama
        renkli_tablo = df_goster.style.map(lambda x: 'background-color: #1ed760' if float(x) >= 85 else '', subset=["AI Skor"])
        strl.dataframe(renkli_tablo, use_container_width=True)
        
        strl.download_button("📊 Analiz Sonuçlarını İndir", data=csv_data, file_name="bist_radar.csv", mime="text/csv")
    else:
        strl.warning("Filtrelere uygun sonuç bulunamadı.")