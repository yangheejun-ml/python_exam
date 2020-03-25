import cv2
import numpy as np
from skimage.measure import compare_ssim
from PIL import Image, ImageFont, ImageDraw

cap = cv2.VideoCapture(1)
if cap.isOpened() == False:
    print("카메라를 오픈 할 수 없습니다.")

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

old_image = None
show_image = None

while True:
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

        old_image = frame
        cv2.imshow("CCTV", show_image)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()