import streamlit as st
import urllib.parse
import re
import random
from datetime import datetime, timezone, timedelta

# Desain halaman web AI biar keren
st.set_page_config(page_title="Asisten AI Aliy", page_icon="🤖", layout="centered")
st.title("🤖 Asisten AI Aliy (Versi Web Big Update)")
st.write("Woi bro! Selamat datang di AI Aliy yang baru. Di sini lu bisa suruh gua buka aplikasi apa aja, curhat masalah hidup, hitung matematika, tanya kalender lengkap, sampe belajar sejarah bareng. Gass ketik di bawah!")

if "riwayat_chat" not in st.session_state:
    st.session_state.riwayat_chat = []

def proses_ai_web(perintah_asli):
    perintah = perintah_asli.lower().strip()
    respon_ai, redirect_url = "", None

    # 📱 1. FITUR: BUKA APLIKASI LEBIH LUAS TANPA BATAS
    if perintah.startswith("buka "):
        aplikasi = perintah.replace("buka ", "").strip()
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
        else:
            respon_ai = f"Gua coba tembus langsung ke aplikasi '{aplikasi}' di HP lu ya bro! Kalau gagal langsung kebuka, tombol di bawah bakal otomatis ngarahin lu ke halaman pencarian Play Store / App Store-nya."
            redirect_url = f"{aplikasi}://"

    # 🟢 2. FITUR KIRIM WHATSAPP AMAN
    elif perintah.startswith("kirim wa ke "):
        try:
            sisa_teks = perintah_asli[12:].strip()
            match_pesan = re.search(r'\s+pesan\s+', sisa_teks, flags=re.IGNORECASE)
            if match_pesan:
                start_idx, end_idx = match_pesan.span()
                nomor_hp = sisa_teks[:start_idx].strip()
                isi_pesan = sisa_teks[end_idx:].strip()
                if nomor_hp.startswith("0"): nomor_hp = "62" + nomor_hp[1:]
                respon_ai = f"Siap bro! Pesan kamu udah aku siapin buat dikirim ke nomor {nomor_hp}."
                pesan_encoded = urllib.parse.quote(isi_pesan)
                redirect_url = f"https://whatsapp.com{nomor_hp}&text={pesan_encoded}"
            else:
                respon_ai = "Formatnya salah bro. Yang bener gini contohnya: `kirim wa ke 0812xxx pesan woi mabar`"
        except:
            respon_ai = "Duh sorry bro, gagal ngeproses nomor WhatsApp-nya. Cek lagi kenedia ya."

    # 🧮 3. FITUR KALKULATOR
    elif perintah.startswith("hitung "):
        try:
            soal = perintah.replace("hitung ", "").strip()
            soal = soal.replace("×", "*").replace("x", "*").replace("X", "*").replace("÷", "/").replace(":", "/").replace("^", "**")
            if not re.match(r'^[\d+\-*/\s.()]*$', soal): raise ValueError()
            hasil = eval(soal)
            if isinstance(hasil, float) and hasil.is_integer(): hasil = int(hasil)
            respon_ai = f"Hasil akhir dari hitungan '{soal}' itu {hasil} bro! Gampang kan? Hehe."
        except ZeroDivisionError:
            respon_ai = "Duh bro, di matematika angka itu gak bisa dibagi sama nol (0) ya!"
        except:
            respon_ai = "Format hitungannya ngaco tuh bro. Pastiin lu cuma pake angka ama simbol tambah (+), kurang (-), kali (*), ato bagi (/) aja!"

    # 🕒 4. FITUR: WAKTU LENGKAP INDONESIA (JAM, HARI, TANGGAL, BULAN, TAHUN)
    elif any(x in perintah for x in ["jam berapa", "menit berapa", "waktu sekarang", "hari apa", "tanggal berapa", "tahun berapa", "bulan apa"]):
        waktu_wib = datetime.now(timezone.utc) + timedelta(hours=7)
        hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
        hari_ini = hari_list[waktu_wib.weekday()]
        bulan_list = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
        bulan_ini = bulan_list[waktu_wib.month - 1]
        tgl = waktu_wib.strftime("%d")
        thn = waktu_wib.strftime("%Y")
        jam = waktu_wib.strftime("%H:%M")
        respon_ai = f"Hari ini itu hari *{hari_ini}*, tanggal *{tgl} {bulan_ini} {thn}*. Nah kalau buat jamnya, sekarang udah menunjukkan pukul *{jam} WIB* bro. Lengkap kan kalender dari gua? Hehe."

    # 📜 5. FITUR: BELAJAR SEJARAH SERU
    elif "sejarah" in perintah or perintah.startswith("jelaskan "):
        if "majapahit" in perintah:
            respon_ai = "Wah, Majapahit itu kerajaan super power abad ke-14 kuno di Indonesia bro! Pusatnya di Jawa Timur. Yang paling terkenal itu Patih Gajah Mada dengan 'Sumpah Palapa'-nya. Dia bersumpah gak mau makan enak sebelum berhasil menyatukan seluruh Nusantara (Indonesia, Malaysia, Filipina sekarang). Gokil banget kan sejarah leluhur kita!"
        elif "perang dunia" in perintah or "pd" in perintah:
            respon_ai = "Perang Dunia itu sejarah kelam tapi seru buat dipelajari bro. PD 1 (1914) itu gara-gara pangeran Austria ditembak. Kalau PD 2 (1939) itu puncaknya pas aliansi Jerman pimpinan Hitler nyerang Polandia, terus berakhir pas kota Hiroshima-Nagasaki di Jepang dibom atom sama Amerika tahun 1945. Nah, momen itu juga yang dimanfaatin Indonesia buat langsung proklamasi kemerdekaan!"
        elif "soekarno" in perintah or "sukarno" in perintah:
            respon_ai = "Ir. Soekarno atau Bung Karno itu bapak Proklamator sekaligus Presiden pertama kita bro! Beliau itu singa podium, kalau pidato di depan negara asing semua langsung ciut. Bersama Bung Hatta, beliau yang berani bacain teks proklamasi 17 Agustus 1945 pas Jepang lagi kalah perang."
        else:
            respon_ai = "Gass kita belajar sejarah bro! Sejarah itu asyik, bukan cuma ngafalin tahun doang. Lu mau tahu sejarah apa nih? Coba ketik secara spesifik, misalnya: `sejarah majapahit`, `sejarah perang dunia`, atau `siapa soekarno`. Nanti gua ceritain secara detail dan seru!"

    # 🔍 6. FIX TOTAL GOOGLE SEARCH: FORMAT BARU ANTI-ERROR SPASI (LINE 131 AMAN)
    elif perintah.startswith("cari ") or perintah.startswith("apa ") or perintah.startswith("pengen cari "):
        query_final = perintah_asli
        for k in ["pengen cari ", "pengen cari", "cari ", "cari", "apa ", "apa"]:
            if perintah.startswith(k):
                query_final = perintah_asli[len(k):].strip()
                break
        if query_final:
            if perintah.startswith("apa "): query_final = "apa " + query_final
            respon_ai = f"Siap bro, gua cariin info tentang '{query_final}' langsung di Google ya!"
            redirect_url = f"https://google.com/search?q={urllib.parse.quote(query_final)}"
        else:
            respon_ai = "Mau cari apa di Google bro? Sebutin objek atau kalimatnya dong biar jelas."

    # 🆔 7. IDENTITAS JAWABAN PANJANG & SANTAI
    elif perintah in ["lu siapa", "kamu siapa", "siapa kamu"]:
        respon_ai = "Kenalin bro, aku AI Aliy! Program asisten virtual virtual santai yang dibikin pake Python khusus buat bantuin kamu sehari-hari. Tugas utama aku itu ringkas banget: bisa nemenin kamu ngobrol pas gabut, bantuin hitung matematika cepat, otomatis nyariin info apa aja di Google, sampe ngebuka semua jenis aplikasi di HP kamu tinggal sekali klik doang. Mantap kan?"

    # 💬 8. FITUR: JAWABAN RANDOM VARIATIF & CURHATAN
    else:
        sapaan_list = ["Halo juga bro! Senang banget bisa ketemu dan nyapa kamu lagi hari ini. Ada hal seru apa yang mau kita lakuin bareng hari ini?", "Yo bro! Whatsapp! Ada yang bisa dibantu hari ini? Gua lagi luang banget nih buat nemenin lu.", "Hai bro! Akhirnya lu ngechat gua lagi, hehe. Mau suruh gua ngapain hari ini? Tinggal sebut!"]
        kabar_list = ["Kabar sistemku aman terkendali bro, performa lagi kenceng-kencengnya dan siap tempur nemenin aktivitasmu! Kalau kabar kamu sendiri gimana?", "Gua sebagai AI selalu mantap bro, server lagi adem dan siap dengerin perintah lu. Semoga lu di sana juga sehat dan banyak duit ya!", "Kabar baik banget bro! Gimana hari-hari lu? Semoga dilancarkan semua urusan lu ya bro."]
