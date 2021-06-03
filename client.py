import xmlrpc.client
import xmlrpc.client as xmlrpclib
import socket
import sys
import os
import struct

# Fungsi Untuk Mengirimkan FIle Ke Server
def upld(file_name):
    print("Uploading {}".format(file_name))
    try:
        clear()
        with open(file_name, "rb") as handle:
            data = xmlrpclib.Binary(handle.read())
            server.file_upload(data, file_name)
    except Exception as e:
        print(e)


# Fungsi untuk Mengunduh FIle Dari Server ke Client dan kemudian akan disimpan dengan nama hasilDownload.txt
def dwnl(file_name):
    print("Downloading {}".format(file_name))
    try:
        clear()
        with open("hasilDownload.txt", "wb") as handle:
            handle.write(server.file_download(file_name).data)
            handle.close()
    except Exception as e:
        print(e)


# getting server direktori file
def listFile():
    print("List File")
    try:
        data = server.list_file().data
        while True:
            clear()
            print("Data Di Server \n")
            print(data.decode("utf-8"))
            prompt = input("Ingin Menutup Menu (Y/N) : ")
            if prompt == "Y" or prompt == "y":
                break
    except Exception as e:
        print(e)


def menu():
    clear()
    print("\nSelamat Datang FTP client.\n")
    while True:
        clear()
        print("++++++++++++++ MENU ++++++++++++++++")
        print("\nGunakan Perintah Berikut Ini:")
        print("UPLD file_path : Upload file")
        print("LIST           : List files")
        print("DWLD file_path : Download file")
        print("QUIT           : Exit from Application")
        prompt = input("\nSilahkan Masukkan Command : ")
        if prompt[:4].upper() == "CONN":
            conn()
        elif prompt[:4].upper() == "UPLD":
            upld(prompt[5:])
        elif prompt[:4].upper() == "LIST":
            listFile()
        elif prompt[:4].upper() == "DWLD":
            dwnl(prompt[5:])
        elif prompt[:4].upper() == "QUIT":
            print("Quit")
            break
        else:
            clear()
            print("Command not recognised; please try again")


def main():
    global server
    global clear
    global f
    try:
        clear = lambda: os.system("cls")
        # Connect to Server
        server = xmlrpclib.ServerProxy("http://127.0.0.1:8000/")
        # Open Main Menu
        menu()
    except socket.error as e:
        print("Socket Error")
        print(e)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
