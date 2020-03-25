import ftplib
from tqdm import tqdm
import os

def is_file(ftp, filename):
    current = ftp.pwd()
    try:
        ftp.cwd(filename)
    except:
        ftp.cwd(current)
        return True
    ftp.cwd(current)
    return False

FTP_SERVER = "127.0.0.1"
FTP_PORT = 6500
FTP_ID = "ftp_user"
FTP_PASS = "123456"

ftp = ftplib.FTP()
ftp.encoding = 'euc-kr'
ftp.connect(FTP_SERVER, FTP_PORT)
print(ftp.login(FTP_ID, FTP_PASS))

while True:
    current = ftp.pwd()
    cmd = input("FTP {}> ".format(current))
    args = cmd.split(" ")
    if len(args) <= 0:
        continue

    command = args[0]
    del args[0]
    if command == "exit":
        break
    if command == "dir" or command == "ls":
        lists = ftp.nlst()
        for l in lists:
            if is_file(ftp, l):
                print(l)
            else:
                print("{}{}/".format(current, l))
    elif command == "cd":
        target = args[0]
        if not is_file(ftp, target):
            ftp.cwd(target)
    elif command == "mkdir" or command == "mk":
        target = args[0]
        ftp.mkd(target)
    elif command == "delete" or command == "del":
        target = args[0]
        ftp.delete(target)
    elif command == "up":
        target = args[0]
        size = os.path.getsize(target)
        filename = target.split("\\")[-1]
        with open(target, "rb") as file:
            with tqdm(unit="blocks", unit_scale=True, leave=False, miniters=1, desc="Uploading....", total=size) as tq:
                def callback(data):
                    tq.update(len(data))
                ftp.storbinary("STOR " + filename, file, 2048, callback=callback)
    elif command == "down":
        target = args[0]
        with open(target, "wb") as file:
            size = ftp.size(target)
            with tqdm(unit='blocks', unit_scale=True, leave=False, miniters=1, desc="Donwloading...", total=size) as tq:
                def callback(data):
                    tq.update(len(data))
                    file.write(data)
                ftp.retrbinary("RETR " + target, callback=callback)

ftp.close()