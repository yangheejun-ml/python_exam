'''
한글 = ((초성 * 21) + 중성) * 28 + 종성 + 44032

초성 = ((x - 44032) / 28) / 21
중성 = ((x - 44032) / 28) % 21
종성 = (x - 44032) % 28
'''


import time
import random
import os

CHO = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", 
        "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
JUNG = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ", "ㅙ", 
        "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"]
JONG = ["", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", 
        "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", 
        "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]

def break_korean(string):
    word_list = list(string)
    break_word = []
    for k in word_list:
        if ord(k) >= ord("가") and ord(k) <= ord("힣"):
            # 유니코드상 몇번째 글자인지 인덱스를 구합니다.
            char_index = ord(k) - ord('가')

            # 초성 = (유니코드인덱스 / 28) / 21
            char1 = int((char_index / 28) / 21)
            break_word.append(CHO[char1])

            # 중성 = (인덱스 / 28) % 21
            char2 = int((char_index / 28) % 21)
            break_word.append(JUNG[char2])

            # 종성 = 인덱스 % 28
            char3 = int(char_index % 28)

            if char3 > 0:
                break_word.append(JONG[char3])
        else:
            break_word.append(k)
    return break_word

WORD_LIST = [
    "남박사의 파이썬 100% 실전 프로그래밍 강좌",
    "파이썬에서 ord() 함수는 문자의 유니코드 값을 알아오는 함수로 10진수 값을 리턴합니다.",
    "chr(x)는 x에 유니코드 10진수 값을 입력하면 해당하는 문자를 리턴합니다.",
    "UTF-8은 유니코드를 8비트 기반으로 저장하는 인코딩 방식입니다.",
    "CP949는 윈도우에서 사용하기 위해 EUC-KR을 확장해서 만든 문자셋 입니다.",
    "파이썬은 코드가 짧고 유연하여 가독성과 생산성이 좋은 프로그래밍 언어 입니다.",
    "코딩하세요 코딩~~",
    "독도는 우리땅"
]

random.shuffle(WORD_LIST)

for q in WORD_LIST:
    os.system("cls")
    start_time = time.time()
    user_input = str(input(q + '\n')).strip()
    end_time = time.time() - start_time

    src = break_korean(q)
    tar = break_korean(user_input)

    if user_input == "/exit":
        break

    correct = 0
    for i, c in enumerate(tar):
        if i >= len(src):
            break
        if c == src[i]:
            correct += 1

    tot_len = len(src)
    c = correct / tot_len * 100
    e = (tot_len - correct) / tot_len * 100
    speed = (correct / end_time) * 60

    print("속도: {:0.2f} 정확도: {:0.2f} 오타율: {:0.2f}".format(speed, c, e))
    os.system("pause")

