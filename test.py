import time
# from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process, Semaphore, Pool
import requests


def loder(i, sem):
    """直接请求ts文件的url然后在写入到本地"""
    sem.acquire()  # 获取钥匙
    url = 'https://doubanzyv3.tyswmp.com:888/2018/12/12/UEtWtHwTc0UniIDQ/out%03d.ts' % i  # %03d 左边补0方式
    html = requests.get(url).content

    with open(r"D:\txsp_test\%s%03d.ts" % ("a", i), "wb") as f:
        f.write(html)
    sem.release()


if __name__ == "__main__":
    start_time = time.time()
    print(start_time)
    sem = Semaphore(5)
    # pool = Pool(5)
    p_l = []
    for i in range(400):
        p = Process(target=loder, args=(i, sem))
        p.start()
        p_l.append(p)
    for i in p_l:
        i.join()
    print(time.time()-start_time)


"""
    pool = Pool(4)
    # pool = ThreadPoolExecutor(max_workers=16)
    # for i in range(2238):
    #     pool.apply_async(loder, (i,))
    pool.map(loder, range(400))
    pool.join()
    pool.close()
    # pool.shutdown()
    pool_time = time.time()-start_time
    print(pool_time)
"""

# >>> multiprocessing ——> 196.01457595825195  默认开启4个进程
# >>> multiprocessing ——> 196.01457595825195  默认开启16个进程
# >>> threading ——> 174.57704424858093  默认开启4个线程
# >>> threading ——> 202.30066895484924  默认开启40个线程（网络卡顿）
# >>> threading ——> 155.5946135520935  默认开启16个线程




