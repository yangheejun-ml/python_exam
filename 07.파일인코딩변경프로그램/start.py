import os
from chardet import detect
import argparse

def search_dir(dirname):
    result_list = []
    filenames = os.listdir(dirname)

    for filename in filenames:
        full_path = os.path.join(dirname, filename)
        if os.path.isdir(full_path):
            result_list.extend(search_dir(full_path))
        else:
            result_list.append(full_path)
    return result_list

def get_encoding_type(filepath):
    with open(filepath, "rb") as f:
        rawdata = f.read()
    
    codec = detect(rawdata)
    return codec["encoding"]


INCLUDE_EXT_LIST = [".txt", ".smi"]


parse = argparse.ArgumentParser()
parse.add_argument("-f", type=str)
parse.add_argument("-e", nargs="+")
args = parse.parse_args()

if args.f is not None:
    path = args.f
    filelists = search_dir(path)

    if args.e is not None:
        if len(args.e) > 0:
            INCLUDE_EXT_LIST = [e.lower() if e[0:1] == "." else ".{}".format(e.lower()) for e in args.e]
    for file in filelists:
        filename, ext = os.path.splitext(file)

        tempfile = filename + "_tmp" + ext

        if ext.lower() in INCLUDE_EXT_LIST:
            encoding = get_encoding_type(file)
            if encoding.lower().find("utf") < 0:
                try:
                    with open(file, "r") as read, open(tempfile, "w", encoding="utf-8") as write:
                        write.write(read.read())
                    os.unlink(file)
                    os.rename(tempfile, file)
                    print("{} 이 저장되었습니다.".format(file))
                except:
                    pass
                finally:
                    if os.path.exists(tempfile):
                        os.unlink(tempfile)