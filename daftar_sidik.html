import machine
import time

# Sambungan sama seperti sistem utama
uart = machine.UART(0, baudrate=9600, tx=machine.Pin(4), rx=machine.Pin(5))

# Perintah standar sensor AS608
PAKET_KEPALA = b'\xEF\x01'
ALAMAT = b'\xFF\xFF\xFF\xFF'
KATA_KUNCI = b'\x00\x00\x00\x00'

def kirim_perintah(perintah):
    uart.write(PAKET_KEPALA + ALAMAT + KATA_KUNCI + bytes([len(perintah)+2]) + perintah)
    cek = sum(perintah) + len(perintah) + 2
    uart.write(bytes([cek//256, cek%256]))

def baca_hasil():
    time.sleep(0.1)
    if uart.any():
        return uart.read()
    return None

print("="*50)
print("  📝 PENDAFTARAN SIDIK JARI PEMILIK")
print("  NAMA: FADLI IFAN SYAH")
print("  ID YANG DIPAKAI: 1")
print("="*50)

# === LANGKAH PENDAFTARAN ===
print("\n👉 LANGKAH 1: Tempelkan jari kamu ke sensor...")
while True:
    kirim_perintah(b'\x01')  # Cek ada jari tidak
    res = baca_hasil()
    if res and res[9] == 0:
        print("✅ Jari terdeteksi! Lepaskan sebentar...")
        break
    time.sleep(0.2)

while True:
    kirim_perintah(b'\x03')  # Ambil gambar pertama
    res = baca_hasil()
    if res and res[9] == 0:
        print("✅ Gambar pertama diambil! Tempelkan lagi jari yang SAMA...")
        break
    time.sleep(0.2)

while True:
    kirim_perintah(b'\x01')
    res = baca_hasil()
    if res and res[9] == 0:
        break
    time.sleep(0.2)

while True:
    kirim_perintah(b'\x05')  # Ambil gambar kedua
    res = baca_hasil()
    if res and res[9] == 0:
        print("✅ Gambar kedua diambil! Sedang diproses...")
        break
    time.sleep(0.2)

kirim_perintah(b'\x07')  # Gabungkan jadi pola
res = baca_hasil()
if res and res[9] != 0:
    print("❌ GAGAL: Tekan jari lebih rata & sama posisinya! Ulangi lagi.")
    exit()

# ✅ SIMPAN DENGAN ID = 1 (sesuai kode sistemmu)
print(f"\n💾 Menyimpan dengan ID: 1 ...")
kirim_perintah(b'\x09\x00\x01')  # 00 01 = ID nomor 1
res = baca_hasil()

if res and res[9] == 0:
    print("\n✅✅✅ BERHASIL! SIDIK JARI SUDAH TERDAFTAR!")
    print(f"👤 Pemilik: FADLI IFAN SYAH")
    print(f"🆔 Nomor ID: 1")
    print("\n👉 Sekarang kamu bisa pakai kode sistem utamamu!")
    print("👉 Nyalakan ulang alat, lalu tempelkan jari ini untuk buka sistem.")
else:
    print("❌ Gagal simpan! Coba ulangi lagi.")
