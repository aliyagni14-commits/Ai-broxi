# Ai-broxi
import streamlit as st
import urllib.parse
import re
from datetime import datetime

# Desain halaman web AI biar keren
st.set_page_config(page_title="Asisten AI Aliy", page_icon="🤖", layout="centered")
st.title("🤖 Asisten AI Aliy (Versi Web Update)")
st.write("Woi bro! Ketik apa aja di bawah bebas, mau suruh buka aplikasi atau nanya-nanya santai, langsung pencet Enter aja!")

# Memori riwayat chat biar gak ilang pas di-refresh
if "riwayat_chat" not in st.session_state:
    st.session_state.riwayat_chat = []

def proses_ai_web(perintah_asli):
    perintah = perintah_asli.lower().strip()
    respon_ai, redirect_url = "", None

    # 📱 1. SISTEM BARU: DETEKSI SEMUA PERINTAH BUKA APLIKASI SECARA LUAS
    if perintah.startswith("buka "):
        aplikasi = perintah.replace("buka ", "").strip()
        
        # Daftar aplikasi populer yang deep link-nya udah pasti cocok
        if aplikasi == "whatsapp":
            respon_ai, redirect_url = "Siap bro, gass buka WhatsApp!", "https://whatsapp.com"
        elif aplikasi == "google":
            respon_ai, redirect_url = "Oke, ini beranda Google ya bro.", "https://google.com"
        elif aplikasi == "roblox":
            respon_ai, redirect_url = "Mantap, selamat main Roblox bro! Semoga seru.", "roblox://"
        elif aplikasi == "duolingo":
            respon_ai, redirect_url = "Waktunya belajar nih, jangan sampai putus streak Duolingo kamu!", "duolingo://"
        elif aplikasi in ["youtube", "yt"]:
            respon_ai, redirect_url = "Gass nonton YouTube, enjoy videonya bro!", "vnd.youtube://"
        elif aplikasi == "tiktok":
            respon_ai, redirect_url = "Membuka TikTok, selamat scroll fyp sampai puas bro!", "snssdk1128://"
        elif aplikasi in ["mobile legends", "ml", "mlbb"]:
            respon_ai, redirect_url = "Buka ML nih! Mabar gass, semoga gak ketemu tim beban ya bro.", "mobilelegends://"
        elif aplikasi in ["free fire", "ff"]:
            respon_ai, redirect_url = "Buka Free Fire, bersiap booyah pertandingan kali ini bro!", "freefire://"
        elif aplikasi == "capcut":
            respon_ai, redirect_url = "Siap, gass ngedit video di CapCut biar makin estetik kreasimu.", "capcut://"
        elif aplikasi == "chatgpt":
            respon_ai, redirect_url = "Membuka ChatGPT resmi, silakan nanya yang rumit-rumit di sana bro.", "https://chatgpt.com"
        elif aplikasi == "spotify":
            respon_ai, redirect_url = "Buka Spotify, dengerin lagu favorit biar makin santai bro.", "spotify://"
        elif aplikasi == "instagram":
            respon_ai, redirect_url = "Membuka Instagram, selamat liat-liat story ato reels bro!", "instagram://app"
        elif aplikasi == "facebook":
            respon_ai, redirect_url = "Membuka Facebook buat kamu bro.", "fb://"
            
        # PENCARIAN OTOMATIS JIKA APLIKASI TIDAK ADA DI DAFTAR (Buka Aplikasi Lebih Luas)
        else:
            respon_ai = f"Aplikasi '{aplikasi}' belum ada di daftar mentahku bro, tapi tenang! Aku buatin link pencarian skema deep link otomatis ke Google biar kamu tetep bisa akses."
            redirect_url = f"https://google.com/search?q={urllib.parse.quote('open ' + aplikasi + ' app deep link android')}"

    # 🟢 2. PERBAIKAN TOTAL FITUR WHATSAPP (ANTI ERROR LINE 30 31)
    elif perintah.startswith("kirim wa ke "):
        try:
            sisa_teks = perintah_asli[12:].strip()
            match_pesan = re.search(r'\s+pesan\s+', sisa_teks, flags=re.IGNORECASE)
            if match_pesan:
                start_idx, end_idx = match_pesan.span()
                nomor_hp = sisa_teks[:start_idx].strip()
                isi_pesan = sisa_teks[end_idx:].strip()
                
                if nomor_hp.startswith("0"): 
                    nomor_hp = "62" + nomor_hp[1:]
                
                respon_ai = f"Siap bro! Pesan kamu udah aku siapin buat dikirim ke nomor {nomor_hp}."
                pesan_encoded = urllib.parse.quote(isi_pesan)
                redirect_url = f"https://whatsapp.com{nomor_hp}&text={pesan_encoded}"
            else: 
                respon_ai = "Formatnya salah bro. Yang bener gini contohnya: `kirim wa ke 0812xxx pesan woi mabar`"
        except: 
            respon_ai = "Duh sorry bro, gagal ngeproses nomor WhatsApp-nya. Cek lagi kodenya ya."

        # 🕒 INFO JAM REAL-TIME (SUDAH DI-FIX BIAR AKURAT JAM INDONESIA)
    elif "jam berapa" in perintah or "menit berapa" in perintah or "waktu sekarang" in perintah:
        import pytz
        zona_waktu = pytz.timezone('Asia/Jakarta')
        waktu_sekarang = datetime.now(zona_waktu).strftime("%H:%M")
        respon_ai = f"Sekarang jam {waktu_sekarang} WIB bro. Jangan sampai keasyikan main terus lupa waktu ya, hehe."

    # 🔍 4. FITUR PENCARIAN GOOGLE OTOMATIS
    elif perintah.startswith("cari ") or perintah.startswith("apa ") or perintah.startswith("pengen cari "):
        keyword = perintah
        for k in ["pengen cari ", "cari ", "apa "]:
            if keyword.startswith(k): keyword = keyword.replace(k, "", 1).strip(); break
        if keyword:
            q_final = "apa " + keyword if perintah.startswith("apa ") else keyword
            respon_ai, redirect_url = f"Siap bro, aku cariin info tentang '{q_final}' langsung di Google ya!", f"https://google.com/search?q={urllib.parse.quote(q_final)}"
        else: 
            respon_ai = "Mau cari apa di Google bro? Sebutin objek atau kalimatnya dong biar jelas."

    # 🆔 5. IDENTITAS JAWABAN PANJANG & SANTAI
    elif perintah in ["lu siapa", "kamu siapa", "siapa kamu"]:
        respon_ai = "Kenalin bro, aku AI Aliy! Program asisten virtual santai yang dibikin pake Python khusus buat bantuin kamu sehari-hari. Tugas utama aku itu ringkas banget: bisa nemenin kamu ngobrol pas gabut, bantuin hitung matematika cepat, otomatis nyariin info apa aja di Google, sampe ngebuka semua jenis aplikasi di HP kamu tinggal sekali klik doang. Mantap kan?"

    # 💬 6. JAWABAN PERTANYAAN RANDOM (BAHASA SANTAI TONGKRONGAN)
    else:
        if "wait" in perintah or "tunggu" in perintah or "sebentar" in perintah: 
            respon_ai = "Aman bro, santai aja gua tungguin kok! Gak usah buru-buru ketiknya, kalau udah lu tinggal kirim perintah baru lagi aja di sini."
        elif "halo" in perintah or "hai" in perintah or "p" in perintah: 
            respon_ai = "Halo juga bro! Senang banget bisa ketemu dan nyapa kamu lagi hari ini. Gimana nih, ada hal seru apa yang mau kita lakuin bareng hari ini? Aku siap bantu!"
        elif "kabar" in perintah: 
            respon_ai = "Kabar sistemku aman terkendali bro, performa lagi kenceng-kencengnya dan siap tempur nemenin aktivitasmu! Kalau kabar kamu sendiri gimana? Semoga hari ini seru dan menyenangkan ya!"
        elif "bosan" in perintah or "gabut" in perintah: 
            respon_ai = "Lagi gabut banget ya bro? Mending lu ketik perintah 'buka youtube' buat nonton video seru, 'buka roblox' ama 'buka ml' biar bisa mabar game ama temen tongkrongan lu!"
        elif "terima kasih" in perintah or "makasih" in perintah: 
            respon_ai = "Sama-sama bro! Udah jadi tugas wajib bagi asisten keren kayak gua buat bantuin lu. Kalau butuh bantuan lain tinggal ketik aja ya, santai aja."
        else: 
            respon_ai = f"Wah, jujur di otak keduaku belum ada jawaban khusus buat kalimat '{perintah_asli}' ini bro. Tapi tenang aja, mending lu ketik perintah 'cari {perintah_asli}' biar langsung gua cariin jawaban paling lengkap dan akurat di internet lewat Google otomatis!"

    return respon_ai, redirect_url

# Input chat di halaman web
input_user = st.text_input("Ketik pesan atau perintah buat AI Aliy di sini bro:", key="user_input")
if input_user:
    jawaban, link_tujuan = proses_ai_web(input_user)
    st.session_state.riwayat_chat.insert(0, {"user": input_user, "ai": jawaban, "link": link_tujuan})

st.write("---")
st.subheader("📜 Riwayat Obrolan Kita:")
for chat in st.session_state.riwayat_chat:
    st.markdown(f"**👦 Kamu:** {chat['user']}")
    st.markdown(f"**🤖 AI Aliy:** {chat['ai']}")
    if chat['link']: 
        st.link_button("👉 KLIK DI SINI BUAT BUKA APLIKASI / LINK", chat['link'])
    st.write("---")
