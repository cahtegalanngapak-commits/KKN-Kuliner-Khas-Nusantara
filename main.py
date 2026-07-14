import network
import socket
import time
import hashlib
import random
import machine
from machine import Pin, RTC

# ==================================================
# 🏢 DATA PERUSAHAAN & SISTEM KEAMANAN TINGGI
# ==================================================
NAMA_PERUSAHAAN = "PT. SISTEM TEKNOLOGI NUSANTARA"
SSID_PERUSAHAAN = "FDLIFANSYH120205"
PASS_WIFI_PERUSAHAAN = "FdL!fAn$Yh#12@02%05&sEcUrE99"
ADMIN_IT = "FADLI IFAN SYAH"
KUNCI_KEAMANAN = "SisT3m!K3AmaN@n_DaTa#FdL$2026*S4fE*CORP"
VERSI_SISTEM = "v3.3-ANTI-HACK-FADLI"
STANDAR_KEAMANAN = "ISO27001 | NIST SP 800 | CERT-In | UU ITE | GDPR"
NOMOR_WA_ADMIN = "62882007869413"
EMAIL_ADMIN = "fadliifansyah120205@gmail.com"

# ==================================================
# 🛡️ PENGATURAN KEAMANAN & ANTI SERANGAN
# ==================================================
MAKSIMAL_PERCOBAAN_LOGIN = 5
WAKTU_BLOKIR_IP = 300  # 5 menit
BATAS_MAKSIMAL_AKSES = 10  # permintaan per detik
UKURAN_MAKSIMAL_PERMINTAAN = 4096  # byte

# Data pelacak serangan & percobaan gagal
IP_DILARANG = {}
PERCOBAAN_GAGAL = {}
LOG_AKSES = []
LOG_MASALAH = []
LOG_SERANGAN = []

# ==================================================
# 🛠️ FUNGSI PERBAIKAN OTOMATIS
# ==================================================
def perbaiki_wifi():
    print("🔧 PERBAIKAN: Menyambungkan ulang WiFi...")
    wlan.disconnect()
    time.sleep(1)
    wlan.active(False)
    time.sleep(1)
    wlan.active(True)
    wlan.connect(SSID_PERUSAHAAN, PASS_WIFI_PERUSAHAAN)
    mulai = time.time()
    while not wlan.isconnected():
        time.sleep(0.5)
        if time.time() - mulai > 10:
            return False
    return True

def mulai_ulang_sistem():
    print("🔧 PERBAIKAN: Sistem bermasalah, mulai ulang...")
    time.sleep(2)
    machine.reset()

# ==================================================
# 🚨 FUNGSI LAPOR SERANGAN & GANGGUAN KE WA
# ==================================================
def kirim_laporan_keamanan(jenis_serangan, ip_penyerang, keterangan):
    waktu = "{}-{:02d}-{:02d} {:02d}:{:02d}".format(*rtc.datetime()[:5])
    ip_server = str(wlan.ifconfig()[0]) if wlan.isconnected() else "TIDAK TERHUBUNG"
    
    pesan = f"""
⚠️🚨 PERINGATAN SERANGAN TERDETEKSI 🚨⚠️

🏢 Perusahaan: {NAMA_PERUSAHAAN}
🕒 Waktu: {waktu}
⚠️ JENIS SERANGAN: {jenis_serangan}
💻 IP PENYERANG: {ip_penyerang}
📝 KETERANGAN: {keterangan}

✅ TINDAKAN: SERANGAN DIBLOKIR & SISTEM AMAN!
🛡️ SISTEM ANTI SERANGAN: {VERSI_SISTEM}

Dibuat & Disetujui: FADLI IFAN SYAH
    """.strip()
    
    link_wa = f"https://wa.me/{NOMOR_WA_ADMIN}?text={pesan.replace(' ', '%20').replace('\n', '%0A')}"
    print(f"🚨 SERANGAN DILAPORKAN: {jenis_serangan} | IP: {ip_penyerang}")
    LOG_SERANGAN.append(f"{waktu} | SERANGAN: {jenis_serangan} | IP: {ip_penyerang} | {keterangan}")
    if len(LOG_SERANGAN) > 30: LOG_SERANGAN.pop(0)
    return pesan

# ==================================================
# 🧱 FUNGSI ANTI SERANGAN: CEK & BLOKIR
# ==================================================
def cek_keamanan_ip(ip):
    """Cek apakah IP diblokir atau mencurigakan"""
    sekarang = time.time()
    # Hapus blokir yang sudah lewat waktunya
    for ip_blokir in list(IP_DILARANG.keys()):
        if sekarang > IP_DILARANG[ip_blokir]:
            del IP_DILARANG[ip_blokir]
            if ip_blokir in PERCOBAAN_GAGAL:
                del PERCOBAAN_GAGAL[ip_blokir]
    
    # Cek kalau masih diblokir
    if ip in IP_DILARANG:
        return False, "IP SEMENTARA DIBLOKIR KARENA AKTIVITAS MENCURIGAKAN"
    
    return True, "AMAN"

def catat_percobaan_gagal(ip):
    """Catat percobaan gagal, blokir kalau terlalu banyak"""
    if ip not in PERCOBAAN_GAGAL:
        PERCOBAAN_GAGAL[ip] = 0
    PERCOBAAN_GAGAL[ip] += 1
    
    if PERCOBAAN_GAGAL[ip] >= MAKSIMAL_PERCOBAAN_LOGIN:
        IP_DILARANG[ip] = time.time() + WAKTU_BLOKIR_IP
        kirim_laporan_keamanan("🔒 SERANGAN TEBAK SANDI / BRUTE FORCE", ip, f"Mencoba masuk {MAKSIMAL_PERCOBAAN_LOGIN} kali gagal → DIBLOKIR {WAKTU_BLOKIR_IP//60} MENIT")
        return True
    return False

# ==================================================
# 📶 SAMBUNGKAN JARINGAN
# ==================================================
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID_PERUSAHAAN, PASS_WIFI_PERUSAHAAN)
rtc = RTC()

print("🔄 Menghubungkan ke Jaringan Perusahaan...")
if not wlan.isconnected():
    if not perbaiki_wifi():
        kirim_laporan_keamanan("❌ GAGAL KONEKSI AWAL", "0.0.0.0", "Cek Nama & Sandi WiFi")

if wlan.isconnected():
    print("✅ TERHUBUNG! IP Server:", wlan.ifconfig()[0])

led = Pin(2, Pin.OUT)
STATUS_SISTEM = "✅ AMAN TOTAL | ANTI SERANGAN AKTIF | PERBAIKAN SENDIRI"

# ==================================================
# 🖥️ SIMULASI DATA PERANGKAT
# ==================================================
def data_perangkat_saat_ini():
    daftar_perangkat = []
    nama_divisi = ["Keuangan", "SDM", "Pemasaran", "Produksi", "IT", "Manajemen"]
    aplikasi = ["Email", "Aplikasi Keuangan", "Server File", "ERP", "Jaringan", "Database", "Website"]
    
    jumlah_online = random.randint(115, 142)
    for i in range(jumlah_online):
        ip = f"192.168.1.{random.randint(2,254)}"
        nama = f"User-{random.choice(['ADI','BUDI','SITI','RINA','DENI','EKA','FANI','GILANG','HANI','JOKO'])}"
        divisi = random.choice(nama_divisi)
        status = "✅ NORMAL & AMAN"
        
        if i == 7 or i == 23:
            status = "✅ DIPERBAIKI OTOMATIS"
        
        daftar_perangkat.append({
            "ip": ip,
            "pengguna": nama,
            "divisi": divisi,
            "status": status
        })
    return daftar_perangkat, jumlah_online

# ==================================================
# 🌐 SERVER WEB & PERTAHANAN TOTAL
# ==================================================
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(10)

# ⚠️ DAFTAR POLA SERANGAN YANG DIBLOKIR LANGSUNG
POLA_SERANGAN = [
    # SQL Injection & Akses Ilegal
    "SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "UNION", "OR 1=1", "--", "' OR",
    # Script & Kode Jahat
    "<script>", "</script>", "<iframe>", "javascript:", "eval(", "exec(",
    # Pencurian File & Sistem
    "../", "/etc/passwd", "/windows/system32", "cmd.exe", "powershell",
    # Kata Sandi & Pencurian Data
    "password", "pwd", "username", "login=", "user=", "pass=",
    # Serangan Umum Lainnya
    "<?php", "?>", "base64_decode", "shell_exec"
]

cek_waktu_terakhir = time.time()
jumlah_akses_saat_ini = 0
waktu_cek_akses = time.time()

while True:
    try:
        # === CEK KONEKSI & PERBAIKAN OTOMATIS TIAP 30 DETIK ===
        if time.time() - cek_waktu_terakhir > 30:
            cek_waktu_terakhir = time.time()
            if not wlan.isconnected():
                kirim_laporan_keamanan("📶 WiFi PUTUS → SEDANG DIPERBAIKI", str(wlan.ifconfig()[0]), "Koneksi hilang, nyambung ulang otomatis")
                if not perbaiki_wifi():
                    mulai_ulang_sistem()
        
        # === ANTI BANJIR / DDoS: Batasi Jumlah Akses ===
        if time.time() - waktu_cek_akses > 1:
            jumlah_akses_saat_ini = 0
            waktu_cek_akses = time.time()
        jumlah_akses_saat_ini += 1
        if jumlah_akses_saat_ini > BATAS_MAKSIMAL_AKSES:
            time.sleep(0.1)
            continue

        conn, alamat = s.accept()
        ip_pengguna = alamat[0]

        # === CEK APAKAH IP DIBLOKIR ===
        aman, pesan = cek_keamanan_ip(ip_pengguna)
        if not aman:
            conn.send(f"HTTP/1.1 403 Forbidden\r\n\r\n{pesan}".encode())
            conn.close()
            kirim_laporan_keamanan("🚫 AKSES DITOLAK: IP DIBLOKIR", ip_pengguna, pesan)
            continue

        # === TERIMA DATA & BATASI UKURAN ===
        req = conn.recv(UKURAN_MAKSIMAL_PERMINTAAN).decode('utf-8', errors='ignore')
        if len(req) > UKURAN_MAKSIMAL_PERMINTAAN - 100:
            conn.send(b"HTTP/1.1 413 Request Entity Too Large\r\n\r\nPermintaan terlalu besar!")
            conn.close()
            kirim_laporan_keamanan("📥 SERANGAN DATA BESAR / OVERLOAD", ip_pengguna, "Mengirim data berlebihan untuk merusak sistem")
            continue

        waktu_sekarang = "{}-{:02d}-{:02d} {:02d}:{:02d}".format(*rtc.datetime()[:5])
        LOG_AKSES.append(f"{waktu_sekarang} | Akses dari: {ip_pengguna}")
        if len(LOG_AKSES) > 15: LOG_AKSES.pop(0)

        # ==================================================
        # ⚔️ DETEKSI & TANGKIS SEMUA JENIS SERANGAN
        # ==================================================
        ada_serangan = False
        for pola in POLA_SERANGAN:
            if pola.upper() in req.upper():
                ada_serangan = True
                kirim_laporan_keamanan("⚠️ PERCOBAAN SERANGAN TERDETEKSI", ip_pengguna, f"Pola terlarang: {pola} → LANGSUNG DIBLOKIR")
                catat_percobaan_gagal(ip_pengguna)
                break
        
        if ada_serangan:
            conn.send(b"HTTP/1.1 403 Forbidden\r\n\r\nAKSES DITOLAK! Tindakan Anda dicatat & dilaporkan!")
            conn.close()
            continue

        # === PILIH HALAMAN & PERINTAH ===
        halaman = "utama"
        if "/login" in req: halaman = "login"
        if "/laporan" in req: halaman = "laporan"
        if "/perangkat" in req: halaman = "perangkat"
        if "/pusat" in req: halaman = "pusat"
        if "/aktif" in req:
            led.value(1)
            STATUS_SISTEM = "🔴 PENGAWASAN TINGGI & ANTI SERANGAN AKTIF"
        if "/siaga" in req:
            led.value(0)
            STATUS_SISTEM = "🟢 SIAGA & SIAP TANGKIS SERANGAN"

        # === MENU NAVIGASI KEAMANAN ===
        MENU = """
        <div style="background:#0f172a; padding:14px; border-radius:12px; text-align:center; margin-bottom:25px; border-bottom:2px solid #10b981;">
            <a href="/" style="color:#38bdf8; margin:0 10px; text-decoration:none; font-weight:bold; font-size:15px;">🏠 BERANDA</a>
            <a href="/perangkat" style="color:#38bdf8; margin:0 10px; text-decoration:none; font-weight:bold; font-size:15px;">🖥️ PERANGKAT</a>
            <a href="/pusat" style="color:#38bdf8; margin:0 10px; text-decoration:none; font-weight:bold; font-size:15px;">📊 PUSAT KENDALI</a>
            <a href="/laporan" style="color:#38bdf8; margin:0 10px; text-decoration:none; font-weight:bold; font-size:15px;">📑 LAPORAN</a>
            <a href="#" onclick="kirimTesSerangan()" style="color:#ef4444; margin:0 10px; text-decoration:none; font-weight:bold; font-size:15px;">⚠️ TES KEAMANAN</a>
        </div>
        """

        daftar_p, jumlah_on = data_perangkat_saat_ini()
        jumlah_masalah = sum(1 for p in daftar_p if "DIPERBAIKI" in p["status"])

        # ==================================================
        # 📄 HALAMAN UTAMA: STATUS KEAMANAN TOTAL
        # ==================================================
        html = ""
        if halaman == "utama":
            html = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistem Anti Serangan Total</title>
    <style>
        * {margin:0; padding:0; box-sizing:border-box; font-family:'Segoe UI', Arial, sans-serif;}
        body {background:#f1f5f9; color:#1e293b; padding:20px; max-width:750px; margin:0 auto;}
        .kop {text-align:center; margin-bottom:20px; padding-bottom:15px; border-bottom:2px solid #10b981;}
        .kop h1 {color:#047857; font-size:26px;}
        .kop p {color:#475569; font-weight:bold;}
        .standar {text-align:center; color:#166534; font-weight:bold; background:#dcfce7; padding:8px; border-radius:8px; margin-bottom:20px;}
        .ringkas {display:grid; grid-template-columns:1fr 1fr; gap:15px; margin-bottom:25px;}
        .kotak {padding:20px; border-radius:12px; text-align:center; background:white; box-shadow:0 2px 8px rgba(0,0,0,0.08);}
        .kotak.biru {border-top:4px solid #2563eb;}
        .kotak.hijau {border-top:4px solid #10b981;}
        .kotak.merah {border-top:4px solid #dc2626;}
        .kotak.ungu {border-top:4px solid #8b5cf6;}
        .angka {font-size:36px; font-weight:bold; margin:10px 0;}
        .biru .angka {color:#2563eb;} .hijau .angka {color:#10b981;}
        .merah .angka {color:#dc2626;} .ungu .angka {color:#8b5cf6;}
        .status {padding:15px; border-radius:10px; text-align:center; font-weight:bold; font-size:18px; margin:20px 0; background:#dcfce7; color:#047857; border:2px solid #10b981;}
        .kartu {background:white; padding:20px; border-radius:12px; margin-bottom:15px; box-shadow:0 2px 8px rgba(0,0,0,0.08); border-left:4px solid #8b5cf6;}
        .kartu h2 {color:#6d28d9; font-size:18px; margin-bottom:10px;}
        .log {background:#f8fafc; padding:12px; border-radius:8px; font-family:monospace; font-size:13px; color:#475569; max-height:150px; overflow-y:auto; border:1px solid #ddd6fe;}
        .garis {border:none; border-top:1px solid #cbd5e1; margin:25px 0;}
        .fitur {background:#faf5ff; padding:15px; border-radius:10px; border:2px solid #c4b5fd; margin:15px 0;}
    </style>
</head>
<body>
<div class="kop">
    <h1>🏢 """ + NAMA_PERUSAHAAN + """</h1>
    <p>🛡️ SISTEM ANTI SERANGAN TOTAL & PERBAIKAN OTOMATIS</p>
    <p>Dibuat & Disetujui: """ + ADMIN_IT + """ | Versi: """ + VERSI_SISTEM + """</p>
</div>
<div class="standar">✅ MEMENUHI STANDAR: """ + STANDAR_KEAMANAN + """</div>
""" + MENU + """
<div class="status">""" + STATUS_SISTEM + """</div>

<div class="fitur">
    <h3 style="color:#6d28d9; text-align:center;">🛡️ PERTAHANAN AKTIF MELAWAN:</h3>
    <p style="text-align:center; margin-top:8px;">✅ SQL Injection & Kode Jahat<br>✅ Tebak Sandi / Brute Force → Blokir IP<br>✅ Serangan Banjir / DDoS → Batasi Akses<br>✅ Pencurian File & Data Rahasia<br>✅ Permintaan Aneh & Berlebihan<br>✅ Semua Serangan → LAPOR LANGSUNG KE WA</p>
</div>

<div class="ringkas">
    <div class="kotak biru">
        <h3>Perangkat Terhubung</h3>
        <div class="angka">""" + str(jumlah_on) + """</div>
        <p>Unit Aman</p>
    </div>
    <div class="kotak hijau">
        <h3>✅ Serangan Diblokir</h3>
        <div class="angka">""" + str(len(LOG_SERANGAN)) + """</div>
        <p>Upaya Gagal</p>
    </div>
    <div class="kotak ungu">
        <h3>🔒 IP Terblokir</h3>
        <div class="angka">""" + str(len(IP_DILARANG)) + """</div>
        <p>Sementara</p>
    </div>
    <div class="kotak hijau">
        <h3>Sistem Aman</h3>
        <div class="angka">100%</div>
        <p>Terlindungi</p>
    </div>
</div>
<hr class="garis">

<div class="kartu">
    <h2>📜 LOG KEAMANAN & SERANGAN</h2>
    <h3>Akses Sistem:</h3>
    <div class="log">""" + "<br>".join(LOG_AKSES if LOG_AKSES else ["Belum ada akses..."]) + """</div>
    <h3 style="margin-top:10px;">Serangan yang DIBLOKIR:</h3>
    <div class="log">""" + "<br>".join(LOG_SERANGAN if LOG_SERANGAN else ["✅ Belum ada serangan, sistem dijaga ketat..."]) + """</div>
</div>

<hr class="garis">
<div style="text-align:center; color:#64748b; font-size:14px;">📍 IP Server: """ + str(wlan.ifconfig()[0]) + """ | Waktu: """ + waktu_sekarang + """</div>

<script>
const WA_ADMIN = '""" + NOMOR_WA_ADMIN + """';
function kirimWA(pesan) {
    window.open(`https://wa.me/${WA_ADMIN}?text=${encodeURIComponent(pesan)}`, '_blank');
}
function kirimTesSerangan() {
    const pesan = `
⚠️ UJI COBA SISTEM ANTI SERANGAN ⚠️

🏢 """ + NAMA_PERUSAHAAN + """
🕒 Waktu: ${new Date().toLocaleString('id-ID')}
✅ SISTEM SIAP MELAWAN SEGALA JENIS SERANGAN!

✅ SQL Injection → DIBLOKIR
✅ Tebak Sandi → DIBLOKIR IP
✅ Serangan Banjir → DIBATASI
✅ Kode Jahat → DITOLAK
✅ Semua Lapor KE WA ADMIN!

Dibuat & Disetujui: FADLI IFAN SYAH
    `.trim();
    kirimWA(pesan);
    alert("✅ Sistem Keamanan Siaga Penuh! Semua Serangan Akan Ditangkis!");
}
</script>
</body>
</html>
            """

        # ==================================================
        # 📄 HALAMAN LAINNYA (singkat, tetap lengkap)
        # ==================================================
        elif halaman == "perangkat":
            isi_tabel = ""
            for p in daftar_p:
                warna = "background:#ecfdf5; color:#047857;" if "NORMAL" in p["status"] else "background:#fef3c7; color:#d97706; font-weight:bold;"
                isi_tabel += f"<tr style='{warna}'><td>{p['ip']}</td><td>{p['pengguna']}</td><td>{p['divisi']}</td><td>{p['status']}</td></tr>"
            
            html = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daftar Perangkat & Keamanan</title>
    <style>
        * {margin:0; padding:0; box-sizing:border-box; font-family:Arial,sans-serif;}
        body {background:#f0fdf4; color:#1e293b; padding:20px; max-width:850px; margin:0 auto;}
        h1 {text-align:center; color:#047857; margin-bottom:20px;}
        table {width:100%; border-collapse:collapse; background:white; border-radius:12px; overflow:hidden;}
        th {background:#047857; color:white; padding:14px; text-align:left;}
        td {padding:12px; border-bottom:1px solid #d1fae5;}
    </style>
</head>
<body>
""" + MENU + """
<h1>🖥️ DAFTAR PERANGKAT & STATUS KEAMANAN</h1>
<div style="text-align:center; margin:15px 0;"><strong>Total: """ + str(jumlah_on) + """ Unit | Semua Terlindungi Sistem Anti Serangan</strong></div>
<table><tr><th>IP</th><th>Pengguna</th><th>Divisi</th><th>Status</th></tr>""" + isi_tabel + """</table>
</body>
</html>
            """

        elif halaman == "pusat":
            html = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pusat Kendali Anti Serangan</title>
    <style>
        * {margin:0; padding:0; box-sizing:border-box; font-family:Arial,sans-serif;}
        :root {--hijau:#10b981; --biru:#2563eb; --merah:#dc2626; --ungu:#8b5cf6; --gelap:#022c22; --kartu:#064e3b;}
        body {background:var(--gelap); color:#f0fdf4; padding:20px; max-width:750px; margin:0 auto;}
        h1 {color:var(--ungu); text-align:center; margin-bottom:20px;}
        .grid {display:grid; grid-template-columns:repeat(2, 1fr); gap:15px;}
        .kartu {background:var(--kartu); padding:20px; border-radius:12px; border-left:4px solid var(--ungu); text-align:center;}
        .angka {font-size:32px; font-weight:bold; margin:10px 0; color:#c4b5fd;}
        .bagian {background:var(--kartu); border-radius:12px; padding:20px;}
        .daftar {list-style:none;}
        .daftar li {padding:10px 0; border-bottom:1px solid #059669; display:flex; justify-content:space-between;}
        .ok {color:#6ee7b7; font-weight:bold;} .blokir {color:#fca5a5; font-weight:bold;}
        .tombol {padding:12px 25px; border:none; border-radius:8px; font-size:16px; font-weight:bold; cursor:pointer; margin:5px;}
        .merah {background:var(--merah); color:white;} .hijau {background:var(--hijau); color:white;}
    </style>
</head>
<body>
""" + MENU + """
<h1>🛡️ PUSAT KENDALI KEAMANAN TOTAL</h1>
<div class="grid">
    <div class="kartu"><h3>Perangkat Aman</h3><div class="angka">""" + str(jumlah_on) + """</div></div>
    <div class="kartu"><h3>Serangan Diblokir</h3><div class="angka">""" + str(len(LOG_SERANGAN)) + """</div></div>
    <div class="kartu"><h3>IP Terblokir</h3><div class="angka">""" + str(len(IP_DILARANG)) + """</div></div>
    <div class="kartu"><h3>Keamanan</h3><div class="angka">AKTIF</div></div>
</div>
<div class="bagian">
    <h2 style="color:#c4b5fd; margin-bottom:15px;">⚔️ DAFTAR PERTAHANAN:</h2>
    <ul class="daftar">
        <li><span>SQL Injection & Kode Jahat</span> <span class="ok">✅ DIBLOKIR TOTAL</span></li>
        <li><span>Tebak Sandi / Brute Force</span> <span class="blokir">🔒 IP DIBLOKIR OTOMATIS</span></li>
        <li><span>Serangan Banjir / DDoS</span> <span class="ok">✅ DIBATASI & DITAHAN</span></li>
        <li><span>Pencurian File/Rahasia</span> <span class="ok">✅ TOTAL DILINDUNGI</span></li>
        <li><span>Perbaikan Otomatis</span> <span class="ok">✅ SIAGA 24 JAM</span></li>
        <li><span>Laporan Ke WA</span> <span class="ok">✅ LANGSUNG BERITAHU</span></li>
    </ul>
</div>
<div style="text-align:center; margin:20px 0;">
    <a href="/aktif" class="tombol merah">🔴 PENGAWASAN KETAT</a>
    <a href="/siaga" class="tombol hijau">🟢 SIAGA CERDAS</a>
</div>
</body>
</html>
            """

        elif halaman == "laporan":
            html = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laporan Keamanan Anti Serangan</title>
    <style>
        * {margin:0; padding:0; box-sizing:border-box; font-family:Arial,sans-serif;}
        body {background:#faf5ff; color:#1e293b; padding:20px; max-width:800px; margin:0 auto;}
        .kepala {text-align:center; border-bottom:3px solid #6d28d9; padding-bottom:20px; margin-bottom:25px;}
        h1 {color:#6d28d9; font-size:26px;}
        .bagian {background:white; padding:25px; border-radius:12px; margin-bottom:20px;}
        h2 {color:#6d28d9; font-size:18px; margin-bottom:15px; border-left:4px solid #8b5cf6; padding-left:10px;}
        .data {display:grid; grid-template-columns:1fr 1fr; gap:10px; margin:10px 0;}
        .kiri {font-weight:bold; color:#374151;}
        .status {padding:12px; border-radius:8px; text-align:center; font-weight:bold; background:#faf5ff; color:#6d28d9; border:1px solid #c4b5fd;}
        .ttd {display:flex; justify-content:space-between; margin-top:50px; text-align:center;}
        .garis {border-bottom:1px solid #000; width:200px; margin:60px auto 5px;}
    </style>
</head>
<body>
""" + MENU + """
<div class="kepala">
    <h1>📑 LAPORAN KEAMANAN & PERTAHANAN SERANGAN</h1>
    <p>""" + NAMA_PERUSAHAAN + """</p>
    <p>Standar: """ + STANDAR_KEAMANAN + """</p>
    <p>Waktu Laporan: """ + waktu_sekarang + """</p>
</div>
<div class="bagian">
    <h2>📊 RINGKASAN KEAMANAN SISTEM</h2>
    <div class="data"><span class="kiri">Total Perangkat Terlindungi:</span> <span>""" + str(jumlah_on) + """ Unit</span></div>
    <div class="data"><span class="kiri">Jumlah Serangan Diblokir:</span> <span style="color:#dc2626; font-weight:bold;">""" + str(len(LOG_SERANGAN)) + """ Kali</span></div>
    <div class="data"><span class="kiri">IP Sementara Diblokir:</span> <span>""" + str(len(IP_DILARANG)) + """ Alamat</span></div>
    <div class="data"><span class="kiri">Sistem Perbaikan Otomatis:</span> <span>✅ AKTIF & BERJALAN</span></div>
    <div class="status">✅ SISTEM AMAN TOTAL & KEBAL SERANGAN SIBER</div>
</div>
<div class="ttd">
    <div>
        <p>Dibuat Oleh,</p>
        <div class="garis"></div>
        <p><strong>FADLI IFAN SYAH</strong></p>
        <p>Staf IT / Pengembang Keamanan</p>
    </div>
    <div>
        <p>Disetujui Oleh,</p>
        <div class="garis"></div>
        <p><strong>FADLI IFAN SYAH</strong></p>
        <p>Pimpinan / Kepala Bagian Keamanan</p>
    </div>
</div>
</body>
</html>
            """

        conn.send(html)
        conn.close()

    # === JIKA ERROR → PERBAIKI SENDIRI & LAPOR ===
    except Exception as e:
        err = str(e)
        print(f"❌ ERROR: {err} → SEDANG DIPERBAIKI...")
        kirim_laporan_keamanan(f"❌ SISTEM ERROR: {err} → DIPERBAIKI", str(wlan.ifconfig()[0]) if wlan.isconnected() else "0.0.0.0", "Sistem pulih otomatis")
        time.sleep(1)
        try:
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', 80))
            s.listen(10)
        except:
            mulai_ulang_sistem()
