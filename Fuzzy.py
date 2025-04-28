# Program Sistem Pemilihan Restoran Terbaik berbasis Fuzzy Logic
# Dibuat sesuai ketentuan tugas CBR AI 2025
# Tidak menggunakan library eksternal

# Fungsi Membership Function untuk Servis
def servis_buruk(x):
    if x <= 40:
        return 1
    elif 40 < x < 60:
        return (60 - x) / 20
    else:
        return 0

def servis_biasa(x):
    if 40 < x < 60:
        return (x - 40) / 20
    elif 60 <= x <= 80:
        return (80 - x) / 20
    else:
        return 0

def servis_bagus(x):
    if x <= 60:
        return 0
    elif 60 < x < 80:
        return (x - 60) / 20
    else:
        return 1

# Fungsi Membership Function untuk Harga
def harga_murah(x):
    if x <= 30000:
        return 1
    elif 30000 < x < 40000:
        return (40000 - x) / 10000
    else:
        return 0

def harga_sedang(x):
    if 30000 < x < 40000:
        return (x - 30000) / 10000
    elif 40000 <= x <= 50000:
        return (50000 - x) / 10000
    else:
        return 0

def harga_mahal(x):
    if x <= 40000:
        return 0
    elif 40000 < x < 50000:
        return (x - 40000) / 10000
    else:
        return 1

# Fuzzy Inference (aturan logika fuzzy)
def inferensi(mu_servis, mu_harga):
    rules = []
    rules.append((min(mu_servis["Bagus"], mu_harga["Murah"]), 100))
    rules.append((min(mu_servis["Bagus"], mu_harga["Sedang"]), 80))
    rules.append((min(mu_servis["Bagus"], mu_harga["Mahal"]), 60))
    rules.append((min(mu_servis["Biasa"], mu_harga["Murah"]), 80))
    rules.append((min(mu_servis["Biasa"], mu_harga["Sedang"]), 60))
    rules.append((min(mu_servis["Biasa"], mu_harga["Mahal"]), 40))
    rules.append((mu_servis["Buruk"], 20))  # Semua kondisi buruk
    return rules

# Defuzzifikasi (menghitung nilai crisp dari aturan fuzzy)
def defuzzifikasi(rules):
    pembilang = 0
    penyebut = 0
    for item in rules:
        mu = item[0]
        skor = item[1]
        pembilang += (mu * skor)
        penyebut += mu
    if penyebut == 0:
        return 0
    else:
        return pembilang / penyebut

# Selection Sort untuk mengurutkan data berdasarkan skor (Descending)
def selection_sort(data):
    n = len(data)
    for i in range(n):
        max_idx = i
        for j in range(i + 1, n):
            if data[j]["Skor"] > data[max_idx]["Skor"]:
                max_idx = j
        data[i], data[max_idx] = data[max_idx], data[i]
    return data

# Menyimpan hasil ke file CSV
def simpan_ke_csv(restoran_terurut):
    try:
        file = open('peringkat.csv', 'w')
        file.write("ID Restoran,Kualitas Servis,Harga,Skor\n")
        for resto in restoran_terurut[:5]:
            line = f"{resto['ID Restoran']},{resto['Kualitas Servis']},{resto['Harga']},{resto['Skor']}\n"
            file.write(line)
        file.close()
        print("\nFile peringkat.csv berhasil dibuat!")
    except:
        print("\nGagal menyimpan file peringkat.csv.")

# Fungsi utama program
def main():
    restoran = []

    # Membaca file restoran.csv
    try:
        file = open('restoran.csv', 'r')
        lines = file.readlines()
        file.close()
    except:
        print("File restoran.csv tidak ditemukan.")
        return

    # Menampilkan data yang dibaca
    print(f"\n{'ID Restoran':<15}{'Kualitas Servis':<20}{'Harga':<15}")
    print("-" * 50)

    for line in lines[1:]:
        line = line.strip()
        if line == "":
            continue

        if "," in line:
            kolom = line.split(",")
        elif "\t" in line:
            kolom = line.split("\t")
        else:
            continue

        if len(kolom) < 3:
            continue

        try:
            id_restoran = int(kolom[0].strip())
            kualitas_servis = float(kolom[1].strip())
            harga = float(kolom[2].strip())
        except:
            continue

        print(f"{id_restoran:<15}{kualitas_servis:<20}{harga:<15}")

        # Fuzzifikasi
        mu_servis = {
            "Buruk": servis_buruk(kualitas_servis),
            "Biasa": servis_biasa(kualitas_servis),
            "Bagus": servis_bagus(kualitas_servis)
        }

        mu_harga = {
            "Murah": harga_murah(harga),
            "Sedang": harga_sedang(harga),
            "Mahal": harga_mahal(harga)
        }

        # Inferensi dan Defuzzifikasi
        rules = inferensi(mu_servis, mu_harga)
        skor = defuzzifikasi(rules)

        restoran.append({
            "ID Restoran": id_restoran,
            "Kualitas Servis": kualitas_servis,
            "Harga": harga,
            "Skor": round(skor, 2)
        })

    if len(restoran) == 0:
        print("Tidak ada data valid yang diproses.")
        return

    # Sorting restoran berdasarkan skor tertinggi
    restoran_terurut = selection_sort(restoran)

    # Menampilkan 5 restoran terbaik
    print(f"\n{'ID Restoran':<15}{'Kualitas Servis':<20}{'Harga':<15}{'Skor':<10}")
    print("-" * 70)
    for resto in restoran_terurut[:5]:
        print(f"{resto['ID Restoran']:<15}{resto['Kualitas Servis']:<20}{resto['Harga']:<15}{resto['Skor']:<10}")

    # Simpan hasil ke file peringkat.csv
    simpan_ke_csv(restoran_terurut)

# Jalankan program
if __name__ == "__main__":
    main()
