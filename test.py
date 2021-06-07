from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
from sys import argv
import os

ACCOUNT_FILE = "dataClient.txt"


def counter_upload(account):
    return change_value(account)


def change_value(account):
    accnts = get_accounts_name(account)
    return True


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


akun = get_accounts_name("client6")
if akun == "":
    print("Tidak ada Akun")

