def servis_buruk(x):
    a, b, c = 0, 25, 50
    if x <= a or x >= c:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)

def servis_biasa(x):
    a, b, c = 50, 70, 90
    if x <= a or x >= c:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)

def servis_bagus(x):
    a, b, c = 70, 85, 100
    if x <= a or x >= c:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)

def harga_murah(x):
    a, b, c = 25000, 30000, 35000
    if x <= a or x >= c:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)

def harga_sedang(x):
    a, b, c = 35000, 42500, 50000
    if x <= a or x >= c:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)

def harga_mahal(x):
    a, b, c = 45000, 50000, 55000
    if x <= a or x >= c:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)


# Fuzzy Inference (aturan logika fuzzy)
def inferensi(n_service, n_harga):
    rules = []
    rules.append((min(n_service["Bagus"], n_harga["Murah"]), 100))
    rules.append((min(n_service["Bagus"], n_harga["Sedang"]), 80))
    rules.append((min(n_service["Bagus"], n_harga["Mahal"]), 60))
    rules.append((min(n_service["Biasa"], n_harga["Murah"]), 80))
    rules.append((min(n_service["Biasa"], n_harga["Sedang"]), 60))
    rules.append((min(n_service["Biasa"], n_harga["Mahal"]), 40))
    rules.append((min(n_service["Buruk"],n_harga["Murah"]), 40)) 
    rules.append((min(n_service["Buruk"],n_harga["Sedang"]), 20))  
    rules.append((min(n_service["Buruk"],n_harga["Mahal"]), 0))  
    return rules

# Defuzzifikasi 
def defuzzifikasi(rules):
    pembilang = 0
    penyebut = 0
    for i in rules:
        n_anggota = i[0]
        skor = i[1]
        pembilang += (n_anggota * skor)
        penyebut += n_anggota
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
        file = open('E:\\Python\\Fuzzy\\restoran.csv', 'r')
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

        # Mengecek apakah harga berada dalam rentang yang diinginkan (25.000 - 55.000)
        if harga < 25000 or harga > 55000:
            continue  # Lewatkan data yang tidak sesuai rentang harga

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
    print("-" * 55)
    for resto in restoran_terurut[:5]:
        print(f"{resto['ID Restoran']:<15}{resto['Kualitas Servis']:<20}{resto['Harga']:<15}{resto['Skor']:<10}")

    # Simpan hasil ke file peringkat.csv
    simpan_ke_csv(restoran_terurut)


if __name__ == "__main__":
    main()
