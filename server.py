from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
from sys import argv
import os

# Fungsi yang digunakan untuk menerima file yang dikirimkan atau bila dilihat dari client melakukan proses upload
def receive_file(filedata, filename):
    # kita buat try dan except untuk mencegah jika terjadi eksepsi
    try:
        # pertama kita buka fileUpload di server yang menerima pengiriman dari client
        with open("fileUpload.txt", "wb") as handle:
            # filedata diterima dengan nama variabel json
            json = filedata.data
            # kemudian fileUpload.txt diupdate line data yang digunakan
            handle.write(json)
            # kita return True untuk mengakhiri proses
            return True
    except Exception as e:
        # print eksepsi yang terjadi untuk mengetahui kesalahan yang terjadi
        print(e)


# Fungsi yang digunakan untuk mengirimkan file dari server atau bila dilihat dari client melakukan proses download
def sendFile(fileDownload):
    # kita buat try dan except untuk mencegah jika terjadi eksepsi
    try:
        # kita baca file yang ingin kita download yang berada di server
        with open(fileDownload, "rb") as handle:
            # kita akan mengirimkan setiap apa yang dibaca pada file tersebut
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
    # server dinyalakan selamanya hingga ada interupsi untuk mematikan
    server.serve_forever()


if __name__ == "__main__":
    main()
