from prettytable import PrettyTable

# Entitas: Mahasiswa
class Mahasiswa:
    def __init__(self, nama, nim, password, angkatan):
        self.nama = nama
        self.nim = nim
        self.password = password
        self.angkatan = angkatan
        self.krs = KRS()
        self.khs = KHS()

# Entitas: MataKuliah
class MataKuliah:
    def __init__(self, nama_mk, id_mk, sks, dosen, waktu):
        self.nama_mk = nama_mk
        self.id_mk = id_mk
        self.sks = sks
        self.dosen = dosen
        self.waktu = waktu

# Entitas: Dosen
class Dosen:
    def __init__(self, nama, nip, password):
        self.nama = nama
        self.nip = nip
        self.password = password
        self.mata_kuliah = []

    def beri_nilai(self, mk, mahasiswa, nilai):
        # Cek apakah dosen adalah pengampu mata kuliah ini
        if mk not in self.mata_kuliah:
            print(f"Dosen {self.nama} bukan pengampu mata kuliah {mk.nama_mk}. Tidak bisa memberi nilai.")
            return

        # Cari mata kuliah di KHS mahasiswa dan beri nilai spesifik pada mahasiswa
        for matkul in mahasiswa.khs.matkul_list:
            if matkul.id_mk == mk.id_mk:
                mahasiswa.khs.set_nilai(matkul.id_mk, nilai)
                print(f"Nilai {nilai} diberikan kepada {mahasiswa.nama} untuk {mk.nama_mk}")
                break
        else:
            print(f"{mahasiswa.nama} tidak mengambil mata kuliah ini")

# Entitas: Admin
class Admin:
    def __init__(self, nama, id_admin, password):
        self.nama = nama
        self.id_admin = id_admin
        self.password = password

# Entitas: KRS (Kartu Rencana Studi)
class KRS:
    def __init__(self):
        self.matkul_list = []
        self.total_sks = 0

    def tambah_matkul(self, matkul):
        if self.total_sks + matkul.sks <= 24:
            self.matkul_list.append(matkul)
            self.total_sks += matkul.sks
            print(f"{matkul.nama_mk} berhasil ditambahkan ke KRS!")
        else:
            print("Total SKS melebihi batas maksimal 24 SKS.")

    def hapus_matkul(self, matkul_id):
        for matkul in self.matkul_list:
            if matkul.id_mk == matkul_id:
                self.matkul_list.remove(matkul)
                self.total_sks -= matkul.sks
                print(f"{matkul.nama_mk} berhasil dihapus dari KRS!")
                return
        print("Mata kuliah tidak ditemukan di KRS.")

    def tampilkan_krs(self):
        table = PrettyTable()
        table.field_names = ["ID MataKuliah", "Nama MataKuliah", "SKS", "Dosen", "Waktu"]
        for matkul in self.matkul_list:
            table.add_row([matkul.id_mk, matkul.nama_mk, matkul.sks, matkul.dosen, matkul.waktu])
        print(table)

# Entitas: KHS (Kartu Hasil Studi)
class KHS:
    def __init__(self):
        self.matkul_list = []
        self.nilai_dict = {}  # Menyimpan nilai per mata kuliah
        self.ipk = 0.0
        self.ip_semester = 0.0

    def set_nilai(self, id_mk, nilai):
        self.nilai_dict[id_mk] = nilai

    def hitung_ip_semester(self):
        total_sks = 0
        total_nilai = 0
        for matkul in self.matkul_list:
            if matkul.id_mk in self.nilai_dict:
                nilai = self.nilai_dict[matkul.id_mk]
                total_nilai += nilai * matkul.sks
                total_sks += matkul.sks
        if total_sks > 0:
            self.ip_semester = total_nilai / total_sks

    def hitung_ipk(self):
        self.hitung_ip_semester()
        # Simplifikasi: IPK diambil dari IP semester ini saja
        self.ipk = self.ip_semester

    def tampilkan_khs(self):
        self.hitung_ip_semester()
        table = PrettyTable()
        table.field_names = ["ID MataKuliah", "Nama MataKuliah", "SKS", "Nilai"]
        for matkul in self.matkul_list:
            nilai = self.nilai_dict.get(matkul.id_mk, "Belum ada nilai")
            table.add_row([matkul.id_mk, matkul.nama_mk, matkul.sks, nilai])
        print(table)
        print(f"IP Semester: {self.ip_semester:.2f}")
        print(f"IPK: {self.ipk:.2f}")

# Sistem Login
class Sistem:
    def __init__(self):
        self.mahasiswa_list = []
        self.dosen_list = []
        self.admin_list = []
        self.matakuliah_list = []

     # Menambahkan data awal
        self.init_data_awal()

    def init_data_awal(self):
        # Menambahkan objek Mahasiswa
        mhs1 = Mahasiswa("Muhammad Akbar Ilham", "2305176048", "pass123", "2023")
        mhs2 = Mahasiswa("Muhammad Gim Nastiar", "2305176077", "pass456", "2023")
        mhs3 = Mahasiswa("Zaky Zaidan Akmal", "2305176052", "pass456", "2023")
        self.mahasiswa_list.extend([mhs1, mhs2, mhs3])

        # Menambahkan objek Dosen 
        dosen1 = Dosen("Bapak Ramaulvi M.Akhyar, S.Kom., M.Kom", "D123", "dosenpass")
        dosen2 = Dosen("Ibu Dewi Rosita, M.kom", "D456", "dosenpass")
        self.dosen_list.extend([dosen1, dosen2])

        # Menambahkan objek Admin
        admin1 = Admin("Admin", "A001", "adminpass")
        self.admin_list.append(admin1)

        # Menambahkan MataKuliah
        mk1 = MataKuliah("Algoritma Pemrograman 2", "MK001", 3, "Bapak Ramaulvi M.Akhyar, S.Kom., M.Kom", "Senin 08:00")
        mk2 = MataKuliah("Database", "MK002", 3, "Ibu Dewi Rosita, M.kom", "Selasa 10:00")
        self.matakuliah_list.extend([mk1, mk2])

        # # Menambahkan mata kuliah ke dosen pengampu
        dosen1.mata_kuliah.append(mk1)
        dosen2.mata_kuliah.append(mk2)

    def login(self, role):
        for _ in range(3): # Memberi 3 kali Kesempatan untuk login
            
            nim_or_nip = input(f"Masukkan {role} NIM/NIP: ")
            password = input("Masukkan Password: ")

            if role == "mahasiswa":
                for mahasiswa in self.mahasiswa_list:
                    if mahasiswa.nim == nim_or_nip and mahasiswa.password == password:
                        print(f"Selamat datang, {mahasiswa.nama}")
                        return mahasiswa
            elif role == "dosen":
                for dosen in self.dosen_list:
                    if dosen.nip == nim_or_nip and dosen.password == password:
                        print(f"Selamat datang, {dosen.nama}")
                        return dosen
            elif role == "admin":
                for admin in self.admin_list:
                    if admin.id_admin == nim_or_nip and admin.password == password:
                        print(f"Selamat datang, {admin.nama}")
                        return admin

        print("Login gagal, username atau password salah.")
        return None

    def daftar_mahasiswa(self):
        nama = input("Nama: ")
        nim = input("NIM: ")
        password = input("Password: ")
        angkatan = input("Angkatan: ")
        mahasiswa = Mahasiswa(nama, nim, password, angkatan)
        self.mahasiswa_list.append(mahasiswa)
        print("Pendaftaran mahasiswa berhasil!")

    def daftar_dosen(self):
        nama = input("Nama: ")
        nip = input("NIP: ")
        password = input("Password: ")
        dosen = Dosen(nama, nip, password)
        self.dosen_list.append(dosen)
        print("Pendaftaran dosen berhasil!")

    def daftar_admin(self):
        nama = input("Nama: ")
        id_admin = input("ID Admin: ")
        password = input("Password: ")
        admin = Admin(nama, id_admin, password)
        self.admin_list.append(admin)
        print("Pendaftaran admin berhasil!")

# Main program
sistem = Sistem()

# Tambahkan MataKuliah contoh
# sistem.matakuliah_list.append(MataKuliah("Algoritma Pemrograman", "MK001", 3, "Bapak Ramaulvi M.Akhyar, S.Kom., M.Kom", "Senin 08:00"))
# sistem.matakuliah_list.append(MataKuliah("Database", "MK002", 3, "Ibu Dewi Rosita, M.kom ", "Selasa 10:00"))

def main():
    while True:
        print("\n--- Sistem Informasi Akademik ---")
        print("1. Login Mahasiswa")
        print("2. Login Dosen")
        print("3. Login Admin")
        print("4. Daftar Mahasiswa")
        print("5. Daftar Dosen")
        print("6. Daftar Admin")
        print("7. Keluar")
        pilihan = input("Pilih opsi: ")

        if pilihan == "1":
            mahasiswa = sistem.login("mahasiswa")
            if mahasiswa:
                while True:
                    print("\n--- Menu Mahasiswa ---")
                    print("1. Isi KRS")
                    print("2. Cetak KHS")
                    print("3. Logout")
                    pilihan_mhs = input("Pilih opsi: ")
                    
                    if pilihan_mhs == "1":
                        print("\nDaftar MataKuliah:")
                        for mk in sistem.matakuliah_list:
                            print(f"{mk.id_mk} - {mk.nama_mk}, {mk.sks} SKS, Dosen: {mk.dosen}, Waktu: {mk.waktu}")
                        id_mk = input("Masukkan ID MataKuliah yang ingin diambil: ")
                        for mk in sistem.matakuliah_list:
                            if mk.id_mk == id_mk:
                                mahasiswa.krs.tambah_matkul(mk)
                                mahasiswa.khs.matkul_list.append(mk)
                                break
                        else:
                            print("MataKuliah tidak ditemukan.")
                    elif pilihan_mhs == "2":
                        mahasiswa.khs.tampilkan_khs()
                    elif pilihan_mhs == "3":
                        break

        elif pilihan == "2":
            dosen = sistem.login("dosen")
            if dosen:
                while True:
                    print("\n--- Menu Dosen ---")
                    print("1. Beri Nilai")
                    print("2. Logout")
                    pilihan_dosen = input("Pilih opsi: ")

                    if pilihan_dosen == "1":
                        for mk in dosen.mata_kuliah:
                            print(f"{mk.id_mk} - {mk.nama_mk}")
                        id_mk = input("Masukkan ID MataKuliah: ")
                        for mk in sistem.matakuliah_list:
                            if mk.id_mk == id_mk:
                                nim_mhs = input("Masukkan NIM Mahasiswa: ")
                                for mhs in sistem.mahasiswa_list:
                                    if mhs.nim == nim_mhs:
                                        nilai = float(input("Masukkan Nilai: "))
                                        dosen.beri_nilai(mk, mhs, nilai)
                                        break
                                break
                    elif pilihan_dosen == "2":  # Handle logout
                        print(f"Selamat tinggal, {dosen.nama}.")
                        break  # Break out of the loop to log out


        elif pilihan == "3":
            admin = sistem.login("admin")
            if admin:
                print("Admin dapat mengelola semua data. Fitur ini akan dikembangkan lebih lanjut.")

        elif pilihan == "4":
            sistem.daftar_mahasiswa()

        elif pilihan == "5": 
            sistem.daftar_dosen()

        elif pilihan == "6":
            sistem.daftar_admin()

        elif pilihan == "7":
            break

if __name__ == "__main__":
    main()
