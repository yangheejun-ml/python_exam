from PIL import Image
import os
import argparse

def search_dir(dirname):
    result_file_list = []

    filenames = os.listdir(dirname)
    for filename in filenames:
        full_path = os.path.join(dirname, filename)

        if os.path.isdir(full_path):
            if filename != "convert":
                result_file_list.extend(search_dir(full_path))
        else:
            result_file_list.append(full_path)
    return result_file_list

p = argparse.ArgumentParser()
p.add_argument("-f", type=str)
p.add_argument("-e", type=str)
args = p.parse_args()

if args.f is None or args.e is None:
    print("사용법: python changer.py -f <대상폴더> -e <변환될확장자>")
else:
    new_format = args.e
    if new_format[0] != ".":
        new_format = "." + new_format
    file_list = search_dir(args.f)
    for file in file_list:
        new_folder = os.path.split(file)[0] + "\\convert"
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)
        src_filename = os.path.splitext(file)[0]
        new_file = new_folder + "\\" + src_filename.split("\\")[-1] + new_format
        
        try:
            img = Image.open(file)
            img.verify()
            img.close()
            img = Image.open(file)
            img.save(new_file)
        except:
            pass