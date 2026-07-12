import network
import socket
import time
from machine import Pin

# === 🔑 ISI NAMA WIFI & SANDI KAMU ===
SSID = "FDLIFANSYAH120205"
PASSWORD = "TGLFDLIFANSYAH"

# === 📶 SAMBUNGKAN WIFI ===
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    time.sleep(0.5)
print("✅ Tersambung! Alamat IP Pico W:", wlan.ifconfig()[0])

# === 🌐 BUAT SERVER WEB ===
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

# === 💡 KENDALI PERANGKAT (PIN 2 KE LED/ALARM) ===
led = Pin(2, Pin.OUT)
STATUS_SISTEM = "SIAP & AMAN"

while True:
    conn, addr = s.accept()
    req = conn.recv(2048).decode()
    print("Akses dari:", addr)

    # === 🎛️ PERINTAH KENDALI ===
    if "/nyala" in req:
        led.value(1)
        STATUS_SISTEM = "🔴 SISTEM BERJALAN AKTIF"
    if "/mati" in req:
        led.value(0)
        STATUS_SISTEM = "🟢 SISTEM SIAP SIAGA"

    # === 📄 TAMPILAN HTML LENGKAP & TERGABUNG ===
    html = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistem Keamanan Data - Pico W</title>
    <style>
        * {box-sizing: border-box; font-family: Arial, sans-serif; margin: 0; padding: 0;}
        body {background: #050510; color: #e2e8f0; padding: 20px; max-width: 650px; margin: 0 auto;}
        h2 {text-align: center; color: #22d3ee; margin: 20px 0;}
        h3 {color: #38bdf8; margin-bottom: 10px;}
        .kartu {background: #111827; border-radius: 12px; padding: 18px; margin-bottom: 15px; border-left: 4px solid #38bdf8;}
        .nama-alat, .judul {font-weight: bold; font-size: 18px; color: #60a5fa; margin-bottom: 8px;}
        .isi, .fungsi {font-size: 15px; line-height: 1.7; color: #cbd5e1;}
        .etis {border-left-color: #22c55e;}
        .penting, .peringatan {background: #331a1a; border-left-color: #f87171; padding: 15px; border-radius: 8px; margin-top: 20px;}
        .aman {background: #1a332e; border-left-color: #4ade80; padding: 15px; border-radius: 8px; margin-top: 15px;}
        .cek {color: #4ade80;}
        .tombol {padding: 18px 35px; font-size: 20px; border: none; border-radius: 12px; margin: 10px; cursor: pointer; font-weight: bold; width: 45%;}
        .on {background: #ef4444; color: white;}
        .off {background: #22c55e; color: white;}
        .status {text-align: center; padding: 15px; border-radius: 10px; font-size: 20px; font-weight: bold; margin: 20px 0;}
        .lapis {border-radius: 999px; margin: 10px auto; padding: 12px; text-align: center; font-weight: bold;}
        .l1 {width: 98%; background: #1e3a5f; border: 2px solid #3b82f6;}
        .l2 {width: 88%; background: #1e4d5f; border: 2px solid #22d3ee;}
        .l3 {width: 78%; background: #1e5f55; border: 2px solid #34d399;}
        .l4 {width: 68%; background: #1e5f3f; border: 2px solid #4ade80;}
        .l5 {width: 58%; background: #4f5f1e; border: 2px solid #a3e635;}
        .l6 {width: 48%; background: #5f3f1e; border: 2px solid #fbbf24; color: #111;}
        .inti {width: 38%; background: #7f1d1d; border: 3px solid #f87171; color: white; box-shadow: 0 0 20px #ef4444;}
        .garis {border: none; border-top: 2px solid #334155; margin: 30px 0;}
        .info-ip {text-align: center; color: #94a3b8; margin-top: 20px;}
    </style>
</head>
<body>

<h1 style="text-align:center; color:#22d3ee; font-size:28px;">🛡️ SISTEM KEAMANAN DATA</h1>
<p style="text-align:center; color:#94a3b8;">Raspberry Pi Pico W - Standar Keamanan Tingkat Dunia</p>

<div class="status aman">""" + STATUS_SISTEM + """</div>

<div style="text-align:center; margin:20px 0;">
    <a href="/nyala"><button class="tombol on">🔴 AKTIFKAN SISTEM</button></a>
    <a href="/mati"><button class="tombol off">🟢 SIAGA</button></a>
</div>

<hr class="garis">

<h2>🔐 HACKING YANG BENAR & BERETIKAL</h2>
<div class="kartu etis">
    <div class="judul">✅ PRINSIP KERJA</div>
    <div class="isi">
        Tujuan: <strong>Melindungi & Memperbaiki Keamanan Data</strong><br>
        ✅ Selalu ada IZIN TERTULIS<br>
        ✅ Cari celah → Lapor → Perbaiki<br>
        ✅ Aman, Halal, & Dihargai
    </div>
</div>

<hr class="garis">

<h2>🏢 PERTAHANAN BERALAPIS DATA</h2>
<div class="lapis l1">1️⃣ FISIK: Pagar, CCTV, Akses Bertingkat</div>
<div class="lapis l2">2️⃣ JARINGAN: Firewall, Penyaring Ancaman</div>
<div class="lapis l3">3️⃣ AKSES: Verifikasi Ganda, Hak Sesuai Peran</div>
<div class="lapis l4">4️⃣ PERANGKAT: Enkripsi Penuh, Pembaruan Otomatis</div>
<div class="lapis l5">5️⃣ PENYIMPANAN: Enkripsi Ganda, Cadangan Aman</div>
<div class="lapis l6">6️⃣ APLIKASI: Uji Celah, Perbaikan Rutin</div>
<div class="lapis inti">💎 INTI DATA: Terisolasi & Terlindungi Penuh</div>

<hr class="garis">

<h2>📋 PERLINDUNGAN DATA LENGKAP</h2>
<div class="kartu">
    <h3>🔒 1. Enkripsi Data</h3>
    <p class="cek">✅ Saat dikirim & disimpan: berubah jadi kode acak, tak terbaca jika dicuri</p>
    <p class="cek">✅ Kunci keamanan disimpan terpisah, tak bisa diambil lewat perangkat lunak</p>
</div>

<div class="kartu">
    <h3>💾 2. Cadangan & Pemulihan</h3>
    <p class="cek">✅ Data disalin di lokasi berbeda — tetap ada walau bencana/kerusakan</p>
    <p class="cek">✅ Diperiksa rutin agar bisa dipulihkan kapan saja</p>
</div>

<div class="kartu">
    <h3>🛡️ 3. Uji Keamanan Rutin</h3>
    <p class="cek">✅ Cari celah keamanan secara berkala sebelum orang jahat menemukannya</p>
    <p class="cek">✅ Lapor lengkap & perbaiki segera agar sistem makin kuat</p>
</div>

<div class="peringatan">
    <strong>⚠️ PERINGATAN HUKUM:</strong><br>
    ✅ Gunakan hanya pada milik sendiri atau yang sudah berizin resmi<br>
    ❌ Tanpa izin = Melanggar UU ITE & Privasi → Denda & Penjara
</div>

<div class="info-ip">📍 Alamat IP Alat: """ + str(wlan.ifconfig()[0]) + """</div>

</body>
</html>
    """
    conn.send(html)
    conn.close()
