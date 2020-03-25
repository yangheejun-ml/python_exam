from PIL import Image
import os

class MyImage:
    def __init__(self, **kwargs):
        self.folder = kwargs.get("folder", None)
        self.resize = kwargs.get("resize", False)

        self.r_width = kwargs.get("r_width", 500)
        self.r_height = kwargs.get("r_height", 500)

        self.ext = kwargs.get("ext", None)

        self.newfolder = "__convert__"
        self.path_separator = "\\"
    
    def is_valid_image(self, filename):
        try:
            img = Image.open(filename)
            img.verify()
            img.close()
            return True
        except:
            return False
    
    def search_dir(self, dirname):
        result_file_list = []

        filenames = os.listdir(dirname)
        for filename in filenames:
            full_path = os.path.join(dirname, filename)

            if os.path.isdir(full_path):
                if filename == self.newfolder:
                    continue
                result_file_list.extend(self.search_dir(full_path))
            else:
                result_file_list.append(full_path)
        return result_file_list
    
    def change_format(self, img, filename, ext):
        new_folder = os.path.split(filename)[0] + self.path_separator + self.newfolder
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)
        
        src_filename = os.path.splitext(filename)[0]
        new_filename = new_folder + self.path_separator + src_filename.split(self.path_separator)[-1] + ext
        img.save(new_filename)
        
    def resize_image(self, filename):
        img = Image.open(filename)
        width, height = img.size
        if width < height:
            aspect = height / self.r_height
            new_width = int(width / aspect)
            new_height = self.r_height
        else:
            aspect = width / self.r_width
            new_width = self.r_width
            new_height = int(height / aspect)
        
        new_size = (new_width, new_height)
        return img.resize(new_size)

    def start(self):
        cnt_resize = 0
        cnt_format = 0

        if self.ext is None and self.resize is False:
            return (cnt_resize, cnt_format)
        
        file_list = self.search_dir(self.folder)

        for file in file_list:
            if not self.is_valid_image(file):
                continue
            if self.resize:
                img = self.resize_image(file)
                cnt_resize += 1
            else:
                img = Image.open(file)

            if self.ext is None:
                ext = str(file.split(self.path_separator)[-1]).split(".")[-1]
            else:
                ext = self.ext
                cnt_format += 1

            if ext[0] != ".":
                ext = "." + ext
            self.change_format(img, file, ext)
        return (cnt_resize, cnt_format)