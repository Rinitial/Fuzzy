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


# Fuzzy Inference
def inferensi(mu_servis, mu_harga):
    rules = []
    rules.append((min(mu_servis["Bagus"], mu_harga["Murah"]), 100))
    rules.append((min(mu_servis["Bagus"], mu_harga["Sedang"]), 60))
    rules.append((min(mu_servis["Bagus"], mu_harga["Mahal"]), 60))
    rules.append((min(mu_servis["Biasa"], mu_harga["Murah"]), 60))
    rules.append((min(mu_servis["Biasa"], mu_harga["Sedang"]), 60))
    rules.append((min(mu_servis["Biasa"], mu_harga["Mahal"]), 40))
    rules.append((mu_servis["Buruk"], 20))
    return rules

# Defuzzifikasi
def defuzzifikasi(rules):
    pembilang = 0
    penyebut = 0
    for item in rules:
        mu = item[0]
        skor = item[1]
        pembilang = pembilang + (mu * skor)
        penyebut = penyebut + mu
    if penyebut == 0:
        return 0
    else:
        return pembilang / penyebut

# Fungsi Selection Sort manual berdasarkan Skor
# Fungsi Selection Sort manual berdasarkan Skor
def selection_sort(data):
    n = len(data)
    for i in range(n):
        max_idx = i
        for j in range(i + 1, n):
            if data[j]["Skor"] > data[max_idx]["Skor"]:
                max_idx = j
        temp = data[i]
        data[i] = data[max_idx]
        data[max_idx] = temp
    return data

# Main Program
def main():
    restoran = []

    # Membaca file secara manual dengan debug
    try:
        file = open('E:\\Python\\Fuzzy\\restoran.csv', 'r')
        lines = file.readlines()
        file.close()
    except:
        print("File restoran.csv tidak ditemukan.")
        return

    print(f"Jumlah baris yang dibaca: {len(lines)}")
    print(f"Isi baris pertama: {lines[0]}")

    # Menampilkan semua baris yang dibaca dengan format rapi
    print("\nIsi file yang dibaca:")
    
    # Menentukan lebar kolom berdasarkan jumlah karakter maksimum di setiap kolom
    header = lines[0].strip().split("\t" if "\t" in lines[0] else ",")
    print(f"{'ID Pelanggan':<15}{'Pelayanan':<15}{'Harga':<15}")
    print("-" * 45)

    for line in lines[1:]:
        line = line.strip()
        if line == "":
            continue

        # Cek separator otomatis
        if "\t" in line:
            kolom = line.split("\t")
        elif "," in line:
            kolom = line.split(",")
        else:
            continue

        if len(kolom) < 3:
            continue

        try:
            id_pelanggan = int(kolom[0].strip())
            pelayanan = int(kolom[1].strip())
            harga = int(kolom[2].strip())
        except:
            continue

        print(f"{id_pelanggan:<15}{pelayanan:<15}{harga:<15}")

    # Lewati header dan proses data
    for i in range(1, len(lines)):
        line = lines[i].strip()  # Menghapus whitespace ekstra di sekitar baris
        if line == "":
            continue

        # Cek otomatis separator (tab atau koma)
        if "\t" in line:
            kolom = line.split("\t")
        elif "," in line:
            kolom = line.split(",")
        else:
            continue  # Jika tidak ada pemisah yang dikenali, lewati

        if len(kolom) < 3:
            continue

        try:
            id_restoran = int(kolom[0].strip())
            kualitas_servis = float(kolom[1].strip())
            harga = float(kolom[2].strip())
        except:
            continue

        mu_servis = {}
        mu_servis["Buruk"] = servis_buruk(kualitas_servis)
        mu_servis["Biasa"] = servis_biasa(kualitas_servis)
        mu_servis["Bagus"] = servis_bagus(kualitas_servis)

        mu_harga = {}
        mu_harga["Murah"] = harga_murah(harga)
        mu_harga["Sedang"] = harga_sedang(harga)
        mu_harga["Mahal"] = harga_mahal(harga)

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

    restoran_terurut = selection_sort(restoran)

    # Output ke console dengan format yang lebih rapi
    print(f"\n{'ID Restoran':<15}{'Kualitas Servis':<20}{'Harga':<15}{'Skor':<10}")
    print("-" * 60)
    for resto in restoran_terurut:
        print(f"{resto['ID Restoran']:<15}{resto['Kualitas Servis']:<20}{resto['Harga']:<15}{resto['Skor']:<10}")

if __name__ == "__main__":
    main()
