import telepot
import logging
import module
import os

import cv2
import numpy as np
from skimage.measure import compare_ssim
from PIL import Image, ImageFont, ImageDraw

import threading
import time

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = "텔레그램토큰"

run_thread = False
send_frame = False

def send_frame_to_telegram(chat_id, frame):
    cv2.imwrite("_tmp.jpg", frame)
    bot.sendPhoto(chat_id, open("_tmp.jpg", mode="rb"))

def capture_cam(chat_id):
    global run_thread, send_frame
    cap = cv2.VideoCapture(1)
    if cap.isOpened() == False:
        print("카메라를 오픈 할 수 없습니다.")

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    old_image = None
    show_image = None

    while run_thread:
        ret, frame = cap.read()
        if ret == True:
            show_image = frame.copy()
            
            if old_image is not None:
                grayA = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                grayB = cv2.cvtColor(old_image, cv2.COLOR_BGR2GRAY)
                (score, diff) = compare_ssim(grayA, grayB, full=True)
                diff = (diff * 255).astype("uint8")
                cv2.imshow("DIFF", diff)
                text = "유사도: {:0.9f}".format(score)

                font = ImageFont.truetype("malgun.ttf", 17)
                text_w, text_h = font.getsize(text)
                w = show_image.shape[1]
                h = show_image.shape[0]
                X_POS = w - text_w - 10
                Y_POS = h - text_h - 10

                pil_image = Image.fromarray(show_image)
                draw = ImageDraw.Draw(pil_image)
                draw.text((X_POS, Y_POS), text, (255,255,255), font=font)
                show_image = np.array(pil_image)

                if score < 0.90:
                    cv2.rectangle(show_image, (0, 0), (w, h), (0, 0, 255), 6)
                    send_frame_to_telegram(chat_id, show_image)

                if send_frame:
                    send_frame_to_telegram(chat_id, show_image)
                    send_frame = False

            old_image = frame
            cv2.imshow("CCTV", show_image)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()


def handler(msg):
    global run_thread, send_frame
    content_type, chat_Type, chat_id, msg_date, msg_id = telepot.glance(msg, long=True)

    if content_type == "text":
        str_message = msg["text"]
        if str_message[0:1] == "/":
            args = str_message.split(" ")
            command = args[0]
            del args[0]

            if command == "/dir" or command == "/목록":
                filepath = " ".join(args)
                if filepath.strip() == "":
                    bot.sendMessage(chat_id, "/dir [대상폴더] 로 입력해주세요.")
                else:
                    filelist = module.get_dir_list(filepath)
                    bot.sendMessage(chat_id, filelist)
            elif command == "/weather" or command == "/날씨":
                w = " ".join(args)
                weather = module.get_weather(w)
                bot.sendMessage(chat_id, weather)
            elif command == "/money":
                w = " ".join(args)
                output = module.money_translate(w)
                bot.sendMessage(chat_id, output)
            elif command == "/c":
                send_frame = True
            elif command == "/mon":
                if args[0] == "start":
                    if not run_thread:
                        print("감시시작")
                        run_thread = True
                        t = threading.Thread(target=capture_cam, args=(chat_id, ))
                        t.daemon = True
                        t.start()
                        bot.sendMessage(chat_id, "감시를 시작했습니다.")
                    else:
                        bot.sendMessage(chat_id, "현재 감시가 동작 중입니다.")
                elif args[0] == "stop":
                    print("감시종료")
                    run_thread = False
                    bot.sendMessage(chat_id, "감시를 중지합니다.")
            elif command[0:4] == "/get":
                filepath = " ".join(args)
                if os.path.exists(filepath):
                    try:
                        if command == "/getfile":
                            bot.sendDocument(chat_id, open(filepath, "rb"))
                        elif command == "/getimage":
                            bot.sendPhoto(chat_id, open(filepath, "rb"))
                        elif command == "/getaudio":
                            bot.sendAudio(chat_id, open(filepath, "rb"))
                        elif command == "/getvideo":
                            bot.sendVideo(chat_id, open(filepath, "rb"))
                    except Exception as e:
                        bot.sendMessage(chat_id, "파일 전송 실패 {}".format(e))
                else:
                    bot.sendMessage(chat_id, "파일이 존재하지 않습니다.")

bot = telepot.Bot(TELEGRAM_TOKEN)
bot.message_loop(handler, run_forever=True)
