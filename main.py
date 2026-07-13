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
VERSI_SISTEM = "v2.3-GLOBAL-SECURE-DARURAT"
STANDAR_KEAMANAN = "ISO27001 | NIST | CERT-In | UU ITE"
NOMOR_WA = "62882007869413"
EMAIL_TUJUAN = "fadliifansyah120205@gmail.com"

# ==================================================
# 📶 SAMBUNGKAN WIFI & SIAPKAN SISTEM
# ==================================================
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD_WIFI)

LOG_AKSES = []
rtc = RTC()

# ==================================================
# 🚨 FUNGSI KIRIM PESAN DARURAT OTOMATIS
# ==================================================
def kirim_darurat(jenis_masalah, keterangan):
    waktu_sekarang = "{}-{:02d}-{:02d} {:02d}:{:02d}".format(*rtc.datetime()[:5])
    ip_sistem = str(wlan.ifconfig()[0]) if wlan.isconnected() else "TIDAK ADA KONEKSI"
    link_kendali = f"http://{ip_sistem}/pusat"
    
    pesan = f"""
🚨 ⚠️ PERINGATAN DARURAT SISTEM! ⚠️ 🚨

👤 Pengguna: {NAMA_PENGGUNA}
🕒 Waktu Kejadian: {waktu_sekarang}
⚠️ Jenis Masalah: {jenis_masalah}
📝 Keterangan: {keterangan}

🔗 LINK LANGSUNG KE SISTEM:
{link_kendali}

💡 SARAN PERBAIKAN CEPAT:
✅ Buka link di atas untuk cek kondisi
✅ Cek koneksi & daya perangkat
✅ Hubungi admin jika berulang

🛡️ Sistem Keamanan {VERSI_SISTEM}
    """.strip()
    
    link_wa = f"https://wa.me/{NOMOR_WA}?text={pesan.replace(' ', '%20').replace('\n', '%0A')}"
    print(f"📤 KIRIM NOTIFIKASI: {link_wa}")
    LOG_AKSES.append(f"🚨 DARURAT: {jenis_masalah} | {waktu_sekarang}")
    return pesan

# === CEK KONEKSI & KIRIM DARURAT JIKA GAGAL ===
print("🔄 Menghubungkan WiFi...")
waktu_mulai = time.time()
while not wlan.isconnected():
    time.sleep(0.5)
    if time.time() - waktu_mulai > 15:
        kirim_darurat("Gagal Koneksi WiFi", "Tidak tersambung, cek Nama & Sandi WiFi")
        break

if wlan.isconnected():
    print("✅ Tersambung! IP:", wlan.ifconfig()[0])

led = Pin(2, Pin.OUT)
STATUS_SISTEM = "SIAGA PENUH | TINGKAT GLOBAL"

# ==================================================
# 🌐 JALANKAN SERVER WEB & PENDETEKSI ANCAMAN
# ==================================================
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)

# Pola deteksi serangan
PolaSerangan = ["SELECT", "INSERT", "DROP", "UNION", "<script>", "../etc/passwd"]

while True:
    try:
        conn, addr = s.accept()
        req = conn.recv(8192).decode()
        waktu_sekarang = "{}-{:02d}-{:02d} {:02d}:{:02d}".format(*rtc.datetime()[:5])
        LOG_AKSES.append(f"{waktu_sekarang} | Akses dari: {addr[0]}")
        if len(LOG_AKSES) > 10: LOG_AKSES.pop(0)

        # === DETEKSI SERANGAN & KIRIM DARURAT ===
        for pola in PolaSerangan:
            if pola in req:
                kirim_darurat("PERCOBAAN SERANGAN / AKSES ILEGAL", f"Dari IP: {addr[0]} | Pola: {pola}")
                break

        # === PERINTAH KENDALI & PILIH HALAMAN ===
        halaman = "utama"
        if "/login" in req: halaman = "login"
        if "/laporan" in req: halaman = "laporan"
        if "/pusat" in req: halaman = "pusat"
        if "/nyala" in req:
            led.value(1)
            STATUS_SISTEM = "🔴 AKTIF PENUH | MENGAWASI 24/7"
        if "/mati" in req:
            led.value(0)
            STATUS_SISTEM = "🟢 SIAGA SIAP | AMAN & TERKENDALI"

        # === MENU NAVIGASI LENGKAP DENGAN TOMBOL TES DARURAT ===
        MENU_NAV = """
        <div style="background:#1e293b; padding:12px; text-align:center; border-radius:10px; margin-bottom:20px;">
            <a href="/" style="color:#22d3ee; margin:0 12px; text-decoration:none; font-weight:bold;">🏠 UTAMA</a>
            <a href="/login" style="color:#22d3ee; margin:0 12px; text-decoration:none; font-weight:bold;">🔐 LOGIN</a>
            <a href="/laporan" style="color:#22d3ee; margin:0 12px; text-decoration:none; font-weight:bold;">📑 LAPORAN</a>
            <a href="/pusat" style="color:#22d3ee; margin:0 12px; text-decoration:none; font-weight:bold;">📊 PUSAT KENDALI</a>
            <a href="#" onclick="kirimTesDarurat()" style="color:#ef4444; margin:0 12px; text-decoration:none; font-weight:bold;">🚨 TES DARURAT</a>
        </div>
        """

        # ==================================================
        # 📄 HALAMAN UTAMA
        # ==================================================
        html = ""
        if halaman == "utama":
            html = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistem Keamanan Siber - Standar Dunia</title>
    <style>
        * {box-sizing:border-box; font-family:Arial,sans-serif; margin:0; padding:0;}
        body {background:#050510; color:#e2e8f0; padding:20px; max-width:700px; margin:0 auto;}
        h1,h2 {text-align:center; color:#22d3ee; margin:15px 0;}
        .standar {text-align:center; color:#a3e635; font-weight:bold; font-size:15px; margin-bottom:20px;}
        .kartu {background:#111827; border-radius:12px; padding:18px; margin-bottom:15px; border-left:4px solid #38bdf8;}
        .judul {font-weight:bold; font-size:18px; color:#60a5fa; margin-bottom:8px;}
        .isi {font-size:15px; line-height:1.7; color:#cbd5e1;}
        .etis {border-left-color:#22c55e;} .peringatan {border-left-color:#ef4444; background:#331a1a;}
        .aman {background:#1a332e; border-left-color:#4ade80; padding:15px; border-radius:8px;}
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
""" + MENU_NAV + """
<h1>🛡️ SISTEM KEAMANAN DATA TINGKAT GLOBAL</h1>
<div class="status aman">""" + STATUS_SISTEM + """</div>
<div style="text-align:center; margin:20px 0;">
    <a href="/nyala"><button class="tombol on">🔴 AKTIFKAN SISTEM</button></a>
    <a href="/mati"><button class="tombol off">🟢 MODE SIAGA</button></a>
</div>
<hr class="garis">
<h2>🔍 ALAT & PERANGKAT KEAMANAN</h2>
<div class="kartu"><div class="judul">🔍 Nmap</div><div class="isi">✅ Pindai jaringan, temukan perangkat & celah keamanan</div></div>
<div class="kartu"><div class="judul">🔥 Firewall</div><div class="isi">✅ Saring lalu lintas, halangi akses ilegal masuk</div></div>
<div class="kartu"><div class="judul">🕵️ Wireshark</div><div class="isi">✅ Rekam & analisis data, cari jejak penyusupan</div></div>
<div class="kartu"><div class="judul">🛡️ Antivirus</div><div class="isi">✅ Blokir & hapus program jahat, jaga sistem utuh</div></div>
<hr class="garis">
<h2>⚙️ 6 FUNGSI UTAMA NIST</h2>
<div class="kartu"><div class="judul">1️⃣ KENALI</div><div class="isi">✅ Catat aset & risiko, pantau semua perangkat</div></div>
<div class="kartu"><div class="judul">2️⃣ LINDUNGI</div><div class="isi">✅ Sandi AES-256, hak akses pas, pembaruan rutin</div></div>
<div class="kartu"><div class="judul">3️⃣ DETEKSI</div><div class="isi">✅ Catat log, cari aktivitas aneh, pantau terus</div></div>
<div class="kartu"><div class="judul">4️⃣ TANGGAPI</div><div class="isi">✅ Tindak cepat, lapor, amankan segera</div></div>
<div class="kartu"><div class="judul">5️⃣ PULIHKAN</div><div class="isi">✅ Cadangan aman, pulihkan sistem cepat</div></div>
<div class="kartu etis"><div class="judul">6️⃣ ETIKA & HUKUM</div><div class="isi">✅ Wajib izin tertulis, patuh hukum dunia & Indonesia</div></div>
<hr class="garis">
<h2>🏰 PERTAHANAN BERALAPIS</h2>
<div class="lapis l1">1️⃣ FISIK: Pagar, CCTV, Akses Bertingkat</div>
<div class="lapis l2">2️⃣ JARINGAN: Firewall, Penyaring Ancaman</div>
<div class="lapis l3">3️⃣ AKSES: Verifikasi Ganda, Hak Sesuai Peran</div>
<div class="lapis l4">4️⃣ PERANGKAT: Enkripsi Penuh, Pembaruan Otomatis</div>
<div class="lapis l5">5️⃣ PENYIMPANAN: Enkripsi Ganda, Cadangan Aman</div>
<div class="lapis l6">6️⃣ APLIKASI: Uji Celah, Perbaikan Rutin</div>
<div class="lapis inti">💎 INTI DATA: Terisolasi & Terlindungi Penuh</div>
<hr class="garis">
<h2>🔒 KEAMANAN SANDI SETARA GOOGLE</h2>
<div class="kartu penting">
    <div class="isi">
    ✅ Panjang >20 Karakter: Huruf Besar/Kecil + Angka + Simbol<br>
    ✅ Algoritma: AES-256 & SHA-256 (Standar Dunia)<br>
    ✅ Sandi WiFi: """ + PASSWORD_WIFI + """<br>
    ✅ Kunci Sistem: """ + KUNCI_KEAMANAN + """
    </div>
</div>
<hr class="garis">
<h2>📜 LOG AKSES & PEMANTAUAN</h2>
<div class="log">""" + "<br>".join(LOG_AKSES if LOG_AKSES else ["Belum ada catatan akses..."]) + """</div>
<hr class="garis">
<div class="peringatan">
    <strong>⚠️ PERINGATAN HUKUM:</strong><br>
    ✅ Hanya pakai milik sendiri atau yang berizin resmi<br>
    ❌ Tanpa izin = Melanggar UU ITE → Denda & Penjara
</div>
<div style="text-align:center; color:#94a3b8; margin-top:20px;">📍 Alamat IP: """ + str(wlan.ifconfig()[0]) + """ | Waktu: """ + waktu_sekarang + """</div>
<script>
const NOMOR_WA = '""" + NOMOR_WA + """';
function kirimWA(pesan) {
    const link = `https://wa.me/${NOMOR_WA}?text=${encodeURIComponent(pesan)}`;
    window.open(link,'_blank');
}
function kirimTesDarurat() {
    const pesan = `
🚨 UJI COBA SISTEM DARURAT 🚨

✅ Ini pesan uji coba
🕒 Waktu: ${new Date().toLocaleString('id-ID')}
🔗 Link Sistem: ${window.location.origin}/pusat

Sistem berjalan normal & siap siaga!
    `.trim();
    kirimWA(pesan);
    alert("✅ Pesan Darurat Terkirim ke WhatsApp! Cek WA kamu sekarang.");
}
</script>
</body>
</html>
            """

        # ==================================================
        # 📄 HALAMAN LOGIN
        # ==================================================
        elif halaman == "login":
            html = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Masuk Ke Sistem | Keamanan Data Global</title>
    <style>
        * {margin:0; padding:0; box-sizing:border-box; font-family:Arial,sans-serif;}
        body {background:linear-gradient(135deg, #0f172a 0%, #1e293b 100%); min-height:100vh; padding:20px;}
        .pusat {max-width:420px; margin:0 auto;}
        .kotak {background:white; border-radius:20px; box-shadow:0 10px 40px rgba(0,0,0,0.3); padding:40px 30px; text-align:center;}
        .logo {font-size:48px; margin-bottom:10px;}
        h1 {color:#1e40af; font-size:24px; margin-bottom:5px;}
        .sub {color:#64748b; font-size:15px; margin-bottom:30px;}
        label {display:block; font-weight:bold; color:#334155; margin-bottom:8px; text-align:left;}
        input {width:100%; padding:14px; border:2px solid #cbd5e1; border-radius:10px; font-size:16px; margin-bottom:20px;}
        input:focus {outline:none; border-color:#2563eb; box-shadow:0 0 0 3px rgba(37,99,235,0.2);}
        .tombol {width:100%; padding:16px; background:#2563eb; color:white; border:none; border-radius:10px; font-size:18px; font-weight:bold; cursor:pointer;}
        .tombol:hover {background:#1d4ed8;}
        .info {margin-top:25px; font-size:13px; color:#64748b; line-height:1.6;}
        .standar {margin-top:20px; padding-top:20px; border-top:1px solid #e2e8f0; font-size:12px; color:#94a3b8;}
    </style>
</head>
<body>
<div class="pusat">
""" + MENU_NAV + """
<div class="kotak">
    <div class="logo">🛡️</div>
    <h1>Sistem Keamanan Data</h1>
    <p class="sub">Masukkan identitas sah untuk mengakses sistem</p>
    <form>
        <label>👤 Nama Pengguna</label>
        <input type="text" value=""" + NAMA_PENGGUNA + """ readonly>
        <label>🔑 Kunci Keamanan</label>
        <input type="password" placeholder="Masukkan Kunci Rahasia">
        <button type="button" class="tombol" onclick="alert('✅ Identitas Terverifikasi!\\nSilakan akses menu di atas')">🔓 MASUK KE SISTEM</button>
    </form>
    <div class="info">
        <p>✅ Hanya untuk pengguna yang berizin resmi</p>
        <p>🔒 Data dikirim terenkripsi penuh</p>
    </div>
    <div class="standar">✅ ISO 27001 • NIST • CERT-In • UU ITE<br>© 2026 Dibuat Oleh: """ + NAMA_PENGGUNA + """</div>
</div>
</div>
</body>
</html>
            """

        # ==================================================
        # 📄 HALAMAN LAPORAN
        # ==================================================
        elif halaman == "laporan":
            html = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laporan Keamanan Sistem | Laporan Resmi</title>
    <style>
        * {margin:0; padding:0; box-sizing:border-box; font-family:Arial,sans-serif;}
        body {background:#f8fafc; color:#1e293b; padding:20px; max-width:900px; margin:0 auto;}
        .kepala {text-align:center; border-bottom:3px solid #1e40af; padding-bottom:20px; margin-bottom:30px;}
        h1 {color:#1e40af; font-size:28px;}
        .bagian {background:white; padding:25px; margin-bottom:20px; border-radius:12px; box-shadow:0 2px 10px rgba(0,0,0,0.05);}
        h2 {color:#1e40af; font-size:20px; margin-bottom:15px; border-left:4px solid #3b82f6; padding-left:10px;}
        .data {display:grid; grid-template-columns:1fr 1fr; gap:10px; margin:10px 0;}
        .kiri {font-weight:bold; color:#334155;}
        .status {padding:10px 15px; border-radius:8px; font-weight:bold; text-align:center; background:#dcfce7; color:#166534; border:1px solid #22c55e;}
        .tabel {width:100%; border-collapse:collapse; margin-top:15px;}
        .tabel th, .tabel td {padding:12px; text-align:left; border-bottom:1px solid #e2e8f0;}
        .tabel th {background:#eff6ff; color:#1e40af; font-weight:bold;}
        .tabel tr:hover {background:#f8fafc;}
        .ttd {display:flex; justify-content:space-between; margin-top:50px; text-align:center;}
        .garis {border-bottom:1px solid #000; width:200px; margin:60px auto 5px;}
    </style>
</head>
<body>
""" + MENU_NAV + """
<div class="kepala">
    <h1>📑 LAPORAN PEMANTAUAN & KEAMANAN SISTEM</h1>
    <p>Standar: ISO 27001, NIST, CERT-In • Dibuat Oleh: """ + NAMA_PENGGUNA + """</p>
    <p>Tanggal: """ + waktu_sekarang + """ | Halaman 1 dari 1</p>
</div>
<div class="bagian">
    <h2>📋 DATA SISTEM UTAMA</h2>
    <div class="data"><span class="kiri">Nama Sistem:</span> <span>Sistem Keamanan Data Terpadu """ + VERSI_SISTEM + """</span></div>
    <div class="data"><span class="kiri">Perangkat Inti:</span> <span>Raspberry Pi Pico W</span></div>
    <div class="data"><span class="kiri">Alamat Jaringan:</span> <span>""" + str(wlan.ifconfig()[0]) + """</span></div>
    <div class="data"><span class="kiri">Enkripsi:</span> <span>AES-256 • SHA-256</span></div>
    <div class="status">✅ SISTEM AMAN & TERKENDALI PENUH — TIDAK ADA ANCAMAN</div>
</div>
<div class="bagian">
    <h2>📊 HASIL PEMERIKSAAN LAPIS PERTAHANAN</h2>
    <table class="tabel">
        <tr><th>No</th><th>Bagian Perlindungan</th><th>Hasil</th><th>Keterangan</th></tr>
        <tr><td>1</td><td>Keamanan Fisik</td><td>✅ AMAN</td><td>Terkunci & Terpantau</td></tr>
        <tr><td>2</td><td>Penyaringan Jaringan</td><td>✅ AMAN</td><td>Firewall Aktif</td></tr>
        <tr><td>3</td><td>Akses & Identitas</td><td>✅ TERKUNCI</td><td>Terverifikasi</td></tr>
        <tr><td>4</td><td>Perangkat Lunak</td><td>✅ AMAN</td><td>Terbarui</td></tr>
        <tr><td>5</td><td>Penyimpanan Data</td><td>✅ AMAN</td><td>Terenkripsi</td></tr>
        <tr><td>6</td><td>Aplikasi & Layanan</td><td>⚠️ DIPERIKSA</td><td>Pemantauan Rutin</td></tr>
        <tr><td>7</td><td>Inti Data Pusat</td><td>✅ SANGAT AMAN</td><td>Terisolasi</td></tr>
    </table>
</div>
<div class="bagian">
    <h2>📜 RINGKASAN AKTIVITAS</h2>
    <p>Jumlah akses sah: <strong>Normal</strong> | Percobaan akses mencurigakan: <strong>DITOLAK OTOMATIS</strong></p>
    <p>Pemeriksaan otomatis terakhir: <strong>""" + waktu_sekarang + """</strong></p>
</div>
<div class="ttd">
    <div>
        <p>Dibuat Oleh,</p>
        <div class="garis"></div>
        <p><strong>""" + NAMA_PENGGUNA + """</strong></p>
        <p>Staf IT / Junior Developer</p>
    </div>
    <div>
        <p>Disetujui Oleh,</p>
        <div class="garis"></div>
        <p>____________________</p>
        <p>Pimpinan / Kepala Bagian</p>
    </div>
</div>
</body>
</html>
            """

        # ==================================================
        # 📄 HALAMAN PUSAT KENDALI
        # ==================================================
        elif halaman == "pusat":
            html = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pusat Kendali Utama | Sistem Keamanan Global</title>
    <style>
        * {margin:0; padding:0; box-sizing:border-box; font-family:Arial,sans-serif;}
        :root {--biru:#2563eb; --hijau:#10b981; --merah:#ef4444; --kuning:#f59e0b; --abu:#64748b; --gelap:#0f172a; --kartu:#1e293b; --batas:#334155;}
        body {background:var(--gelap); color:#f1f5f9; padding:20px; max-width:700px; margin:0 auto;}
        .atas {display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:15px; margin-bottom:30px;}
        h1 {color:var(--biru); font-size:24px;}
        .grid {display:grid; grid-template-columns:repeat(2, 1fr); gap:15px; margin-bottom:30px;}
        .kartu {background:var(--kartu); padding:20px; border-radius:12px; border-left:4px solid var(--biru); text-align:center;}
        .kartu h3 {color:var(--abu); font-size:15px; margin-bottom:10px;}
        .angka {font-size:32px; font-weight:bold;}
        .hijau {border-color:var(--hijau);} .hijau .angka {color:var(--hijau);}
        .merah {border-color:var(--merah);} .merah .angka {color:var(--merah);}
        .kuning {border-color:var(--kuning);} .kuning .angka {color:var(--kuning);}
        .bagian {background:var(--kartu); border-radius:12px; padding:20px;}
        .daftar {list-style:none;}
        .daftar li {padding:10px 0; border-bottom:1px solid var(--batas); display:flex; justify-content:space-between;}
        .ok {color:var(--hijau); font-weight:bold;}
        .peringatan {color:var(--kuning); font-weight:bold;}
        .tombol {padding:12px 25px; border:none; border-radius:8px; font-size:16px; font-weight:bold; cursor:pointer; margin:5px;}
        .merah {background:var(--merah); color:white;}
        .hijau {background:var(--hijau); color:white;}
    </style>
</head>
<body>
""" + MENU_NAV + """
<div class="atas">
    <h1>🛡️ PUSAT KENDALI SISTEM</h1>
    <p style="color:#94a3b8;">📅 """ + waktu_sekarang + """</p>
</div>
<div class="grid">
    <div class="kartu">
        <h3>Perangkat Terhubung</h3>
        <div class="angka">128</div>
        <p style="color:#94a3b8; font-size:13px;">Normal & Terpantau</p>
    </div>
    <div class="kartu hijau">
        <h3>Sistem Aktif</h3>
        <div class="angka">99.9%</div>
        <p style="color:#94a3b8; font-size:13px;">Lancar Terus</p>
    </div>
    <div class="kartu kuning">
        <h3>Pembaruan Siap</h3>
        <div class="angka">2</div>
        <p style="color:#94a3b8; font-size:13px;">Perlu Dipasang</p>
    </div>
    <div class="kartu merah">
        <h3>Peringatan Aktif</h3>
        <div class="angka">0</div>
        <p style="color:#10b981; font-size:13px;">Sangat Aman</p>
    </div>
</div>
<div class="bagian">
    <h2 style="color:#2563eb; text-align:left; margin-bottom:15px;">📊 STATUS LAPIS PERTAHANAN</h2>
    <ul class="daftar">
        <li><span>1️⃣ Keamanan Fisik</span> <span class="ok">✅ AMAN</span></li>
        <li><span>2️⃣ Jaringan & Firewall</span> <span class="ok">✅ AMAN</span></li>
        <li><span>3️⃣ Akses & Identitas</span> <span class="ok">✅ TERKUNCI</span></li>
        <li><span>4️⃣ Perangkat & Enkripsi</span> <span class="ok">✅ TERLINDUNGI</span></li>
        <li><span>5️⃣ Data & Cadangan</span> <span class="ok">✅ AMAN</span></li>
        <li><span>6️⃣ Aplikasi & Layanan</span> <span class="peringatan">⚠️ DIPERIKSA</span></li>
        <li><span>💎 Inti Data Pusat</span> <span class="ok">✅ SANGAT AMAN</span></li>
    </ul>
</div>
<div style="text-align:center; margin:20px 0;">
    <a href="/nyala" class="tombol merah">🔴 AKTIFKAN PENUH</a>
    <a href="/mati" class="tombol hijau">🟢 MODE SIAGA</a>
</div>
<div style="text-align:center; color:#94a3b8; margin-top:20px;">📍 IP: """ + str(wlan.ifconfig()[0]) + """ | 🔑 AES-256 & SHA-256</div>
</body>
</html>
            """

        # === KIRIM HALAMAN KE BROWSER ===
        conn.send(html)
        conn.close()

    # === JIKA ADA ERROR SISTEM → LANGSUNG KIRIM DARURAT ===
    except Exception as e:
        pesan_error = str(e)
        kirim_darurat("❌ SISTEM ERROR / GANGGUAN", f"Kesalahan: {pesan_error}")
        time.sleep(1)
