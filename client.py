import xmlrpc.client
import xmlrpc.client as xmlrpclib
import socket
import sys
import os
import struct


def conn():
    # Connect to the server
    print("Sending server request...")
    try:
        clear()
        server = xmlrpclib.ServerProxy("http://127.0.0.1:8000/")
        print("Status => Connection sucessful \n")
    except Exception as e:
        print("Status => Connection unsucessful. Make sure the server is online. \n")
        print(e)


def upld(file_name):
    print("Uploading {}".format(file_name))
    try:
        clear()
        with open(file_name, "rb") as handle:
            data = xmlrpclib.Binary(handle.read())
            server.file_upload(data, file_name)
    except Exception as e:
        print(e)


def dwnl(file_name):
    print("Downloading {}".format(file_name))
    try:
        clear()
        with open("hasilDownload.txt", "wb") as handle:
            handle.write(server.file_download(file_name).data)
            handle.close()
    except Exception as e:
        print(e)


def menu():
    clear()
    print("\nSelamat Datang FTP client.\n")
    while True:
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
            print("List")
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
    try:
        clear = lambda: os.system("cls")
        server = xmlrpclib.ServerProxy("http://127.0.0.1:8000/")
        menu()
    except socket.error as e:
        print("Socket Error")
        print(e)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
