import requests
from bs4 import BeautifulSoup
import re
import json
import random
import os

def get_news():
    url = "https://www.usatoday.com"
    r = requests.get(url)
    bs = BeautifulSoup(r.text, "lxml")
    lists = bs.select("ul.hfwmm-list.hfwmm-4uphp-list.hfwmm-light-list > li > a")
    for li in lists:
        href = url + li["href"]
        
        r = requests.get(href)
        bs = BeautifulSoup(r.text, "lxml")
        texts = bs.select("div.asset-double-wide.double-wide.p402_premium > p.p-text")
        contents = [p.text for p in texts]
        contents = " ".join(contents)
        return contents.lower()
    return None

def naver_translate(word):
    try:
        url = "https://ac.dict.naver.com/enendict/ac?q={}&q_enc=utf-8&st=11001".format(word)
        r = requests.get(url)
        j = json.loads(r.text)
        return (j["items"][0][0][1][0])
    except:
        return None

def make_quize(news):
    match_pattern = re.findall(r'\b[a-z]{4,15}\b', news)

    frequency = {}
    quize_list = []

    for word in match_pattern:
        count = frequency.get(word, 0)
        frequency[word] = count + 1

    for word, count in frequency.items():
        if count > 1:
            kor = naver_translate(word)
            if kor is not None:
                quize_list.append({kor: word})

    return quize_list

def quize():
    quize_list = make_quize(get_news())
    random.shuffle(quize_list)

    chance = 5
    count = 0

    for q in quize_list:
        os.system("cls")
        count += 1
        kor = list(q.keys())[0]
        english = q.get(kor)

        print("*" * 90)
        print("문제: {}".format(kor))
        print("*" * 90)

        for j in range(chance):
            user_input = str(input("위의 뜻이 의미하는 단어를 입력하세요> ")).strip().lower()

            if user_input == english:
                print("정답입니다!! {} 문제 남음".format(len(quize_list) - count))
                os.system("pause")
                break
            else:
                n = chance - (j + 1)
                if j == 0:
                    print("{} 가 아닙니다. {} 번 기회가 남았습니다.".format(user_input, n))
                elif j == 1:
                    print("{} 가 아닙니다. {} 번 기회가 남았습니다. 힌트: {}로 시작".format(user_input, n, english[0]))
                elif j == 2:
                    hint = " _ " * int(len(english) - 2)
                    print("{} 가 아닙니다. {} 번 기회가 남았습니다. 힌트: {} {} {}로 시작".format(user_input, n, english[0], english[1], hint))
                elif j == 3:
                    hint = " _ " * int(len(english) - 3)
                    print("{} 가 아닙니다. {} 번 기회가 남았습니다. 힌트: {} {} {} {}로 시작".format(user_input, n, english[0], english[1], english[2], hint))
                else:
                    print("틀렸습니다.!! 정답은 {} 입니다.".format(english))
                    os.system("pause")

    print("더이상 문제가 없습니다.")

quize()