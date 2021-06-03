from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
from sys import argv
import os


def receive_file(filedata, filename):
    try:
        with open("fileUpload.txt", "wb") as handle:
            json = filedata.data
            handle.write(json)
            return True
    except Exception as e:
        print(e)


def sendFile(fileDownload):
    try:
        with open(fileDownload, "rb") as handle:
            return xmlrpc.client.Binary(handle.read())
            handle.close()
    except Exception as e:
        print(e)


def listFile():
    try:
        with open("listDirektori.txt", "rb") as handle:
            return xmlrpc.client.Binary(handle.read())
            handle.close()
    except Exception as e:
        print(e)


def main():
    try:
        if len(argv) != 2:
            raise IndexError()
        port_num = int(argv[1])
    except IndexError:
        print("Gunakan Perintah> python server.py 'port'")
        exit()

    try:
        server = SimpleXMLRPCServer(("127.0.0.1", port_num), allow_none=True)
        print("Listening On Port ", port_num)
        arr = os.listdir()
        with open("listDirektori.txt", "w+") as f:
            for item in arr:
                f.write("%s\n" % item)
            f.close
    except Exception as e:
        print(e)
        print("Gagal menggunakan jaringan")
        exit()

    server.register_introspection_functions()
    server.register_function(receive_file, "file_upload")
    server.register_function(sendFile, "file_download")
    server.register_function(listFile, "list_file")
    server.serve_forever()


if __name__ == "__main__":
    main()
