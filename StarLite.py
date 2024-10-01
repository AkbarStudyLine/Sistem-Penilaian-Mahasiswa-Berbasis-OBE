class Mahasiswa:
    def __init__(self, nama, nim):
        self.nama = nama
        self.nim = nim
        self.mata_kuliah_diambil = []

    def tambah_mata_kuliah(self, mata_kuliah):
        self.mata_kuliah_diambil.append(mata_kuliah)

class MataKuliah:
    def __init__(self, nama, kode, lo_list):
        self.nama = nama
        self.kode = kode
        self.lo_list = lo_list
        self.nilai_mahasiswa = {}

    def tambah_nilai(self, mahasiswa, lo_nilai):
        self.nilai_mahasiswa[mahasiswa.nim] = lo_nilai

    def hasil_akhir(self, mahasiswa):
        lo_nilai = self.nilai_mahasiswa.get(mahasiswa.nim, {})
        total_nilai = sum(lo_nilai.values()) / len(self.lo_list)
        return total_nilai >= 75  # 75% sebagai ambang batas ketercapaian LO

class Penilaian:
    def __init__(self):
        self.hasil_penilaian = []

    def evaluasi(self, mahasiswa, mata_kuliah):
        if mata_kuliah.hasil_akhir(mahasiswa):
            self.hasil_penilaian.append(f"{mahasiswa.nama} mencapai semua LO pada {mata_kuliah.nama}.")
        else:
            self.hasil_penilaian.append(f"{mahasiswa.nama} tidak mencapai semua LO pada {mata_kuliah.nama}.")

# Contoh penggunaan program:
mahasiswa1 = Mahasiswa("Andi", "12345")
mata_kuliah1 = MataKuliah("Pemrograman", "CS101", ["LO1", "LO2", "LO3"])

mahasiswa1.tambah_mata_kuliah(mata_kuliah1)
mata_kuliah1.tambah_nilai(mahasiswa1, {"LO1": 80, "LO2": 70, "LO3": 85})

penilaian = Penilaian()
penilaian.evaluasi(mahasiswa1, mata_kuliah1)

for hasil in penilaian.hasil_penilaian:
    print(hasil)
