from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
from sys import argv
import os

ACCOUNT_FILE = "dataClient.txt"


# Fungsi yang digunakan untuk menerima file yang dikirimkan atau bila dilihat dari client melakukan proses upload
def receive_file(filedata, filename, clientName):
    # kita buat try dan except untuk mencegah jika terjadi eksepsi
    try:
        # pertama kita buka fileUpload di server yang menerima pengiriman dari client
        with open("upload_{}_{}".format(clientName, filename), "wb") as handle:
            # filedata diterima dengan nama variabel json
            json = filedata.data
            # kemudian fileUpload.txt diupdate line data yang digunakan
            handle.write(json)
            # kita return True untuk mengakhiri proses
            counter_data(clientName)
            return True
    except Exception as e:
        # print eksepsi yang terjadi untuk mengetahui kesalahan yang terjadi
        print(e)


# Fungsi yang digunakan untuk mengirimkan file dari server atau bila dilihat dari client melakukan proses download
def sendFile(fileDownload, clientName):
    # kita buat try dan except untuk mencegah jika terjadi eksepsi
    try:
        # kita baca file yang ingin kita download yang berada di server
        with open(fileDownload, "rb") as handle:
            # kita akan mengirimkan setiap apa yang dibaca pada file tersebut
            counter_data(clientName)
            return xmlrpc.client.Binary(handle.read())
            # kemudian pembacaan kita tutup
            handle.close()
    except Exception as e:
        # print eksepsi yang terjadi untuk mengetahui kesalahan yang terjadi
        print(e)


# Fungsi untuk menampilkan list data yang berada di server
def listFile():
    # kita buat try dan except untuk mencegah jika terjadi eksepsi
    try:
        # pertama kita get data file yang berada di direktori menggunakan os.listdir()
        arr = os.listdir()
        # kemudian kita buat file yang menuliskan data byte yang dibaca sebelumnya agar bisa dikirim
        with open("listDirektori.txt", "w+") as f:
            # setiap item yang berada di arr nanti akan di tuliskan ke file direktori tersebut
            for item in arr:
                # lakukan write setiap item
                f.write("%s\n" % item)
            # kita tutup bila sudah di tulis
            f.close
        # selanjutnya kita buka file List Direktori tersebut untuk mengirimkan data Direktori di server
        with open("listDirektori.txt", "rb") as handle:
            # Lakukan Pengiriman data tersebut perbaris data yang ada di file listdirektori
            return xmlrpc.client.Binary(handle.read())
            # kita tutup proses pengiriman dan pembacaan
            handle.close()
    except Exception as e:
        # print eksepsi yang terjadi untuk mengetahui kesalahan yang terjadi
        print(e)


# Print Data Keaktifan User
def most_active_client():
    try:
        accnts = get_accounts_data()
    except Exception as e:
        print(e)
    return accnts


# get data akun untuk pertama kali saat login
def get_accounts_name(akun_name):
    accnts = ""
    try:
        fileData = open(ACCOUNT_FILE, "r")
        for line in fileData:
            value = line.rstrip().partition(",")
            if value[0] == akun_name:
                accnts = value[0]
        fileData.close()
    except IOError:
        print("Gagal membuka {}".format(ACCOUNT_FILE))
    return accnts


# +++++++++++++++++++++++++++++++++++++++++COUNTER UPLOAD DAN DOWNLOAD++++++++++++++++++++++++++++++++++++++++++++++

# melakukan counter_data untuk setiap upload dan download client
def counter_data(account):
    return change_value(account)


# merubah value counter
def change_value(account):
    akun = get_accounts_data()
    try:
        akun[account] += 1
        write_to_database(akun)
        return True
    except (KeyError):
        return False


# mengambil keseluruhan data untuk diupdate
def get_accounts_data():
    accnts = {}
    try:
        fileData = open(ACCOUNT_FILE, "r")
        for line in fileData:
            value = line.rstrip().partition(",")
            accnts[value[0]] = int(value[2])
        fileData.close()
    except IOError:
        print("Gagal membuka {}".format(ACCOUNT_FILE))
    return accnts


# update data di file penyimpanan akun
def write_to_database(akun):
    try:
        f = open(ACCOUNT_FILE, "w")
        for key, val in akun.items():
            f.write("{},{}\n".format(key, val))
        f.close()
    except IOError:
        print("Gagal menambahkan counter {} ".format(ACCOUNT_FILE))
    return True


def main():
    # kita buat try untuk mencegah eksepsi ketika menjalankan aplikasi
    try:
        # cek jika argument yang dimasukkan di command prompt kurang dari 2 maka raise Index Error
        if len(argv) != 2:
            raise IndexError()
        # catat nomor port pada kalimat kedua yang dimasukan pada command prompt
        port_num = int(argv[1])
    # jika terjadi indexerror maka lakukan tahapan print cara menjalankan
    except IndexError:
        print("Gunakan Perintah> python server.py 'port'")
        # tutup koneksi server tidak dinyalakan
        exit()

    # buat try dan except ketika melakukan koneksi ke jaringan
    try:
        # server menggunakan jaringan localhost yang dapat diganti dengan port sesuai keperluan dari user
        server = SimpleXMLRPCServer(("127.0.0.1", port_num), allow_none=True)
        # print koneksi dibangun pada port berapa
        print("Listening On Port ", port_num)
    # jika terjadi eksepsi
    except Exception as e:
        # print eksepsi apa yang terjadi
        print(e)
        # print pesan gagal
        print("Gagal menggunakan jaringan")
        # tutup koneksi
        exit()

    # proses registrasi fungsi agar dapat digunakan pada sisi client
    server.register_introspection_functions()
    # receive file akan dikenali client sebagai fungsi upload
    server.register_function(receive_file, "file_upload")
    # receive file akan dikenali client sebagai fungsi download
    server.register_function(sendFile, "file_download")
    # receive file akan dikenali client sebagai fungsi list file
    server.register_function(listFile, "list_file")
    # fungsi untuk melakukan login
    server.register_function(get_accounts_name, "login_client")
    # fungsi untuk melakukan cek keaktifan
    server.register_function(most_active_client, "client_active")
    # server dinyalakan selamanya hingga ada interupsi untuk mematikan
    server.serve_forever()


if __name__ == "__main__":
    main()
