import xmlrpc.client
import xmlrpc.client as xmlrpclib
import socket
import sys
import os
import struct

# Fungsi Untuk Mengirimkan FIle Ke Server
def upld(file_name, clientName):
    # kita bersihkan command prompt agar rapi
    clear()
    # print untuk menandakan sedang berada di fungsi ana
    print("Uploading {}".format(file_name))
    try:
        # buka file yang ingin dikirim dan baca perbaris
        with open(file_name, "rb") as handle:
            # data yang dikirim merupakan baris data yang dibaca
            data = xmlrpclib.Binary(handle.read())
            # file dikirim menggunakan fungsi upload yang ada di server
            server.file_upload(data, file_name, clientName)
    except Exception as e:
        # jika terjadi eksepsi print eksepsinya
        print(e)


# Fungsi untuk Mengunduh FIle Dari Server ke Client dan kemudian akan disimpan dengan nama hasilDownload.txt
def dwnl(file_name, clientName):
    # membersihkan command prompt
    clear()
    print(clientName)
    # print untuk  menandai proses download
    try:
        # buka file yang baru hasilDownload untuk menerima file yang dikirim server
        print("Downloading {}".format(file_name))
        with open("download_{}".format(file_name), "wb") as handle:
            # tuliskan perbaris apa yang data yang diterima dari server
            handle.write(server.file_download(file_name, clientName).data)
            # penulisan di tutup
            handle.close()
    except Exception as e:
        # jika terjadi eksepsi print eksepsinya
        print(e)


# getting server direktori file
def listFile():
    # print untuk menandai menu yang digunakan
    print("List File")
    try:
        # lakukan looping agar data bisa ditampilkan
        while True:
            # bersihkan command prompt
            clear()
            # panggil data yang diterima dari server yang berupa list nama barang di server
            data = server.list_file().data
            # print kalimat untuk mempercantik aplikasi
            print("Data Di Server \n")
            # print data byte yang diterima dengan kita decode dulu ke format yang diketahui
            print(data.decode("utf-8"))
            # input untuk menu
            prompt = input("Ingin Menutup Menu (Y/N) : ")
            # jika Y maka kembali ke menu utama
            if prompt == "Y" or prompt == "y":
                break
    except Exception as e:
        # jika terjadi eksepsi maka print eksepsinya
        print(e)


# getting most active client
def cln():
    try:
        # looping menu
        while True:
            clear()
            print("List Client")
            # get data dari server mengenai client
            data = server.client_active()
            # sort max value dari dictionary dan mengembalikan key
            maxValue = max(data, key=data.get)
            # hasil data client dan nama client teraktif
            print("Akun yang terdaftar : {}".format(data))
            print("Akun yang teraktif : {}".format(maxValue))
            # input untuk menu
            prompt = input("Ingin Menutup Menu (Y/N) : ")
            # jika Y maka kembali ke menu utama
            if prompt == "Y" or prompt == "y":
                break
    # jika ada eksepsi
    except Exception as e:
        # print kesalahan
        print(e)


# fungsi yang digunakan untuk menampilkan menu dari aplikasi
def menu(clientName):
    # clear command prompt
    clear()
    # print kata sambutan
    print("\nSelamat Datang FTP client.\n")
    # lakukan looping terus hingga kondisi menghentikan aplikasi dan menu
    while True:
        # bersihkan command prompt
        clear()
        # print tampilan mempercantik menu
        print("++++++++++++++ MENU ++++++++++++++++")
        # penjelasan perintah yang dapat digunakan
        print("\nGunakan Perintah Berikut Ini:")
        # untuk melakukan upload bisa menggunakan UPLD dan file_pathnya
        print("UPLD file_path : Upload file")
        # untuk melihat list dapat menggunakan LIST
        print("LIST           : List files")
        # untuk melihat keaktifan client
        print("CLN           : Client Activity Record")
        # untuk melakukan download bisa menggunakan DWLD dan file_pathnya
        print("DWLD file_path : Download file")
        # untuk menutup menggunakan QUIT
        print("QUIT           : Exit from Application")
        # input menu
        prompt = input("\nSilahkan Masukkan Command : ")
        # kita ambil 4 kalimat awal yang dimasukkan dan kita uppercase untuk perintah sesuai keperluan menu
        if prompt[:4].upper() == "UPLD":
            # Upload file dengan file_path yang berada pada kalimat 5 keatas
            upld(prompt[5:], clientName)
        elif prompt[:4].upper() == "LIST":
            # buka fungsi listFile
            listFile()
        elif prompt[:4].upper() == "DWLD":
            # buka fungsi download
            dwnl(prompt[5:], clientName)
        elif prompt[:4].upper() == "CLN":
            cln()
        elif prompt[:4].upper() == "QUIT":
            # Tutup Aplikasi
            clear()
            break
        else:
            # bila tidak ditemukan command print pemberitahuan
            clear()
            print("Command not recognised; please try again")


# fungsionalitas utama
def main():
    # deklarasi global variabel yang dapat digunakan
    global server
    global clear
    global f
    global counterDownload
    global clientName
    # buat try and except mencegah eksepsi
    try:
        # buat fungsi untuk membersihkan command prompt windows dengan cls
        clear = lambda: os.system("cls")
        # Connect to Server
        server = xmlrpclib.ServerProxy("http://127.0.0.1:8000/")
        # lakukan login untuk memastikan data client ada dan dapat digunakan
        clientName = server.login_client(input("Silahkan Masukan ID anda : "))
        # buat kondisi bila data ada
        if clientName != "":
            # Open Main Menu
            menu(clientName)
        # jika data tidak ada
        else:
            # naikkan jadi Exception untuk menghentikan program
            raise Exception
    # jika socket connection error
    except socket.error as e:
        # print pemberitahuan
        print("Socket Error")
        print(e)
    # jika terjadi eksepsi lainnya
    except Exception as e:
        print("Terjadi Kesalahan")


if __name__ == "__main__":
    main()
