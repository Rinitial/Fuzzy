# Fungsi keanggotaan fuzzy untuk servis
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

# Fungsi keanggotaan fuzzy untuk harga
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

# Nilai skala linguistik (poin no. 5)
nilai_skala = {
    'sangat_rendah': 20,
    'rendah': 40,
    'sedang': 60,
    'tinggi': 80,
    'sangat_tinggi': 100
}

# Inferensi dengan label linguistik
def inferensi_label(mu_servis, mu_harga):
    rules = []
    rules.append((min(mu_servis["Bagus"], mu_harga["Murah"]), "sangat_tinggi"))
    rules.append((min(mu_servis["Bagus"], mu_harga["Sedang"]), "tinggi"))
    rules.append((min(mu_servis["Bagus"], mu_harga["Mahal"]), "sedang"))
    rules.append((min(mu_servis["Biasa"], mu_harga["Murah"]), "tinggi"))
    rules.append((min(mu_servis["Biasa"], mu_harga["Sedang"]), "sedang"))
    rules.append((min(mu_servis["Biasa"], mu_harga["Mahal"]), "rendah"))
    rules.append((min(mu_servis["Buruk"], mu_harga["Murah"]), "sedang"))
    rules.append((min(mu_servis["Buruk"], mu_harga["Sedang"]), "rendah"))
    rules.append((min(mu_servis["Buruk"], mu_harga["Mahal"]), "sangat_rendah"))
    return rules

# Defuzzifikasi menggunakan skala linguistik
def defuzzifikasi_linguistik(rules):
    pembilang = 0.0
    penyebut = 0.0
    for derajat, label in rules:
        nilai = nilai_skala.get(label, 0)
        pembilang += derajat * nilai
        penyebut += derajat
    if penyebut == 0:
        return 0
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

# Simpan ke CSV
def simpan_ke_csv(restoran_terurut):
    try:
        file = open('peringkat.csv', 'w')
        file.write("ID Restoran,Kualitas Servis,Harga,Skor\n")
        for resto in restoran_terurut[:5]:
            file.write(f"{resto['ID Restoran']},{resto['Kualitas Servis']},{resto['Harga']},{resto['Skor']}\n")
        file.close()
        print("\nFile peringkat.csv berhasil disimpan.")
    except:
        print("\nGagal menyimpan file peringkat.csv.")

# Fungsi utama
def main():
    restoran = []

    try:
        file = open('restoran.csv', 'r')
        lines = file.readlines()
        file.close()
    except:
        print("File restoran.csv tidak ditemukan.")
        return

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

        if harga < 25000 or harga > 55000:
            continue

        print(f"{id_restoran:<15}{kualitas_servis:<20}{harga:<15}")

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

        rules = inferensi_label(mu_servis, mu_harga)
        skor = defuzzifikasi_linguistik(rules)

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

    print(f"\n{'ID Restoran':<15}{'Kualitas Servis':<20}{'Harga':<15}{'Skor':<10}")
    print("-" * 60)
    for resto in restoran_terurut[:5]:
        print(f"{resto['ID Restoran']:<15}{resto['Kualitas Servis']:<20}{resto['Harga']:<15}{resto['Skor']:<10}")

    simpan_ke_csv(restoran_terurut)

if __name__ == "__main__":
    main()
