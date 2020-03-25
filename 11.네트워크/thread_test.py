import time
import threading

def 주문받기():
    for i in range(5):
        print("주문받기 {}".format(i))
        time.sleep(1)

def 우편발송():
    for i in range(5):
        print("우편발송 {}".format(i))
        time.sleep(0.5)

th1 = threading.Thread(target=주문받기)
th2 = threading.Thread(target=우편발송)

th1.daemon = True
th2.daemon = True

th1.start()
th2.start()