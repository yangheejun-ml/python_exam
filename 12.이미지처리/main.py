from myclass import MyImage
import argparse

p = argparse.ArgumentParser()
p.add_argument("-f", type=str)
p.add_argument("-e", type=str)
p.add_argument("-r", action="store_true")
p.add_argument("-rw", type=int, default=500)
p.add_argument("-rh", type=int, default=500)
args = p.parse_args()

if args.f and (args.e or args.r):
    myimg = MyImage(folder=args.f,
                    ext=args.e,
                    resize=args.r,
                    r_width=args.rw,
                    r_height=args.rh)
    cnt_resize, cnt_ext = myimg.start()
    print("리사이즈: {}, 포맷변경: {}".format(cnt_resize, cnt_ext))
else:
    print("사용법: python main.py -f <대상폴더> -e <변경될확장자> -r [리사이즈] -rw 500 -rh 500")