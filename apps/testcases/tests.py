import threading
import time


def thread_job():
    print('This is an added Thread,number is %s' % threading.current_thread())
    for i in range(10):
        time.sleep(0.1)
    print('T1 finish \n')


def T2_job():
    print('T2 start \n')
    print('T2 finish \n')


def main():
    add_threading = threading.Thread(target=thread_job())
    threadT2 = threading.Thread(target=T2_job())
    add_threading.start()
    threadT2.start()
    print('all done \n')


if __name__ == '__main__':
    main()
