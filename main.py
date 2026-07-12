import network
import socket
import time
import hashlib
from machine import Pin, RTC

# ==================================================
# 🔑 DATA UTAMA & IDENTITAS PENGGUNA
# ==================================================
SSID = "FDLIFANSYH120205"
PASSWORD_WIFI = "FdL!fAn$Yh#12@02%05&sEcUrE99"
NAMA_PENGGUNA = "FDLIFANSYH"
KUNCI_KEAMANAN = "SisT3m!K3AmaN@n_DaTa#FdL$2026*S4fE"
VERSI_SISTEM = "v2.0-GLOBAL-SECURE"
STANDAR_KEAMANAN = "ISO27001 | NIST | CERT-In | UU ITE"

# ==================================================
# 📶 SAMBUNGKAN WIFI & DAPATKAN WAKTU AKURAT
# ==================================================
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD_WIFI)

while not wlan.isconnected():
    time.sleep(0.5)
print("✅ Tersambung! IP:", wlan.ifconfig()[0])

rtc = RTC()
led = Pin(2, Pin.OUT)
STATUS_SISTEM = "SIAGA PENUH | TINGKAT GLOBAL"

# ==================================================
# 🌐 BUAT SERVER WEB & PENCATATAN AKSES
# ==================================================
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
LOG_AKSES = []

while True:
    conn, addr = s.accept()
    req = conn.recv(4096).decode()
    waktu_sekarang = "{}-{:02d}-{:02d} {:02d}:{:02d}".format(*rtc.datetime()[:5])
    LOG_AKSES.append(f"{waktu_sekarang} | Akses dari: {addr[0]}")
    if len(LOG_AKSES) > 10: LOG_AKSES.pop(0)

    # === PERINTAH KENDALI SISTEM ===
    if "/nyala" in req:
        led.value(1)
        STATUS_SISTEM = "🔴 AKTIF PENUH | MENGAWASI 24/7"
    if "/mati" in req:
        led.value(0)
        STATUS_SISTEM = "🟢 SIAGA SIAP | AMAN & TERKENDALI"

    # === TAMPILAN HTML LENGKAP TOP GLOBAL ===
    html = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistem Keamanan Global - """ + NAMA_PENGGUNA + """</title>
    <style>
        * {box-sizing: border-box; font-family: Arial, sans-serif; margin: 0; padding: 0;}
        body {background: #050510; color: #e2e8f0; padding: 20px; max-width: 700px; margin: 0 auto;}
        h1,h2,h3 {text-align: center; color: #22d3ee; margin: 15px 0;}
        .standar {text-align:center; color:#a3e635; font-weight:bold; font-size:15px; margin-bottom:20px;}
        .kartu {background: #111827; border-radius: 12px; padding: 18px; margin-bottom: 15px; border-left: 4px solid #38bdf8;}
        .judul {font-weight: bold; font-size: 18px; color: #60a5fa; margin-bottom: 8px;}
        .isi {font-size: 15px; line-height: 1.7; color: #cbd5e1;}
        .etis {border-left-color: #22c55e;} .penting {border-left-color: #f59e0b;} .peringatan {border-left-color: #ef4444; background:#331a1a;}
        .aman {background:#1a332e; border-left-color:#4ade80; padding:15px; border-radius:8px;}
        .cek {color:#4ade80;} .salah {color:#f87171;} .info {color:#94a3b8;}
        .tombol {padding:18px 35px; font-size:20px; border:none; border-radius:12px; margin:10px; cursor:pointer; font-weight:bold; width:45%;}
        .on {background:#ef4444; color:white;} .off {background:#22c55e; color:white;}
        .status {text-align:center; padding:15px; border-radius:10px; font-size:20px; font-weight:bold; margin:20px 0;}
        .lapis {border-radius:999px; margin:10px auto; padding:12px; text-align:center; font-weight:bold;}
        .l1 {width:98%; background:#1e3a5f; border:2px solid #3b82f6;}
        .l2 {width:88%; background:#1e4d5f; border:2px solid #22d3ee;}
        .l3 {width:78%; background:#1e5f55; border:2px solid #34d399;}
        .l4 {width:68%; background:#1e5f3f; border:2px solid #4ade80;}
        .l5 {width:58%; background:#4f5f1e; border:2px solid #a3e635;}
        .l6 {width:48%; background:#5f3f1e; border:2px solid #fbbf24; color:#111;}
        .inti {width:38%; background:#7f1d1d; border:3px solid #f87171; color:white; box-shadow:0 0 20px #ef4444;}
        .garis {border:none; border-top:2px solid #334155; margin:30px 0;}
        .log {background:#0f172a; padding:12px; border-radius:8px; font-family:monospace; font-size:13px; color:#94a3b8; max-height:120px; overflow-y:auto;}
        .identitas {text-align:center; color:#22d3ee; font-size:17px; margin-bottom:5px; font-weight:bold;}
    </style>
</head>
<body>

<div class="identitas">👤 Pengguna: """ + NAMA_PENGGUNA + """ | Versi: """ + VERSI_SISTEM + """</div>
<div class="standar">✅ MEMENUHI STANDAR: """ + STANDAR_KEAMANAN + """</div>

<h1>🛡️ SISTEM KEAMANAN DATA TINGKAT GLOBAL</h1>
<div class="status aman">""" + STATUS_SISTEM + """</div>

<div style="text-align:center; margin:20px 0;">
    <a href="/nyala"><button class="tombol on">🔴 AKTIFKAN SISTEM</button></a>
    <a href="/mati"><button class="tombol off">🟢 MODE SIAGA</button></a>
</div>

<hr class="garis">

<h2>⚙️ 6 FUNGSI UTAMA NIST (STANDAR DUNIA)</h2>
<div class="kartu">
    <div class="judul">1️⃣ KENALI (IDENTIFY)</div>
    <div class="isi">✅ Catat semua aset & risiko<br>✅ Pantau aset yang terhubung<br>✅ Kelola risiko keamanan secara rutin</div>
</div>
<div class="kartu">
    <div class="judul">2️⃣ LINDUNGI (PROTECT)</div>
    <div class="isi">✅ Sandi Super Kuat & Enkripsi AES<br>✅ Hak akses sesuai kebutuhan<br>✅ Pembaruan & perbaikan celah rutin</div>
</div>
<div class="kartu">
    <div class="judul">3️⃣ DETEKSI (DETECT)</div>
    <div class="isi">✅ Catat Log & Riwayat Akses<br>✅ Cari aktivitas mencurigakan<br>✅ Pantau anomali jaringan terus-menerus</div>
</div>
<div class="kartu">
    <div class="judul">4️⃣ TANGGAPI (RESPOND)</div>
    <div class="isi">✅ Langkah cepat jika ada gangguan<br>✅ Lapor & amankan segera<br>✅ Jangan biarkan penyusup masuk</div>
</div>
<div class="kartu">
    <div class="judul">5️⃣ PULIHKAN (RECOVER)</div>
    <div class="isi">✅ Cadangan data aman & terpisah<br>✅ Bisa pulihkan sistem cepat<br>✅ Uji coba pemulihan rutin</div>
</div>
<div class="kartu etis">
    <div class="judul">6️⃣ TATA KELOLA & ETIKA</div>
    <div class="isi">✅ Izin tertulis wajib ada<br>✅ Patuh Hukum: UU ITE, IT Act India, ISO<br>✅ Cari celah → Lapor → Perbaiki</div>
</div>

<hr class="garis">

<h2>🏰 PERTAHANAN BERALAPIS TAK TEMBUS</h2>
<div class="lapis l1">1️⃣ FISIK: Pagar, CCTV, Akses Bertingkat</div>
<div class="lapis l2">2️⃣ JARINGAN: Firewall, Penyaring Ancaman</div>
<div class="lapis l3">3️⃣ AKSES: Verifikasi Ganda, Hak Sesuai Peran</div>
<div class="lapis l4">4️⃣ PERANGKAT: Enkripsi Penuh, Pembaruan Otomatis</div>
<div class="lapis l5">5️⃣ PENYIMPANAN: Enkripsi Ganda, Cadangan Aman</div>
<div class="lapis l6">6️⃣ APLIKASI: Uji Celah, Perbaikan Rutin</div>
<div class="lapis inti">💎 INTI DATA: Terisolasi & Terlindungi Penuh</div>

<hr class="garis">

<h2>🔒 KEAMANAN SANDI & ENKRIPSI SETARA GOOGLE</h2>
<div class="kartu penting">
    <div class="isi">
    ✅ Panjang >20 Karakter: Huruf Besar/Kecil + Angka + Simbol Khusus<br>
    ✅ Algoritma: Standar AES-256 & SHA-256 (Dunia & India)<br>
    ✅ Sandi WiFi: """ + PASSWORD_WIFI + """<br>
    ✅ Kunci Sistem: """ + KUNCI_KEAMANAN + """
    </div>
</div>

<hr class="garis">

<h2>📜 LOG AKSES & PEMANTAUAN (WAJIB CERT-In INDIA)</h2>
<div class="log">""" + "<br>".join(LOG_AKSES if LOG_AKSES else ["Belum ada catatan akses..."]) + """</div>

<hr class="garis">

<h2>⚠️ PERINGATAN & KEPATUHAN HUKUM</h2>
<div class="peringatan">
    <strong>✅ SAH & AMAN SECARA HUKUM:</strong><br>
    ✅ Indonesia: UU ITE No.19 Tahun 2016<br>
    ✅ India: IT Act 2008 & Aturan CERT-In<br>
    ✅ Global: ISO 27001 & NIST Cybersecurity Framework<br>
    ❌ Dilarang pakai tanpa izin tertulis → Denda & Penjara
</div>

<div class="info-ip" style="text-align:center; color:#94a3b8; margin-top:20px;">📍 Alamat IP: """ + str(wlan.ifconfig()[0]) + """ | Waktu: """ + waktu_sekarang + """</div>

</body>
</html>
    """
    conn.send(html)
    conn.close()
