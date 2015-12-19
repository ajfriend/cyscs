import scs
from concurrent.futures import ThreadPoolExecutor
import time

workers = 2
blocks = 4
m = 1000
repeat = 1

ex = ThreadPoolExecutor(max_workers=workers)
datas = [scs.examples.l1(m, seed=i) for i in range(blocks)]


ts = []
for _ in range(repeat):
    start = time.time()
    a = list(map(lambda x: scs.solve(*x), datas))
    end = time.time()
    ts.append(end-start)
serial = min(ts)

ts = []
for _ in range(repeat):
    start = time.time()
    a = list(map(lambda x: scs.solve(*x, verbose=False), datas))
    end = time.time()
    ts.append(end-start)
serialnotverbose = min(ts)

ts = []
for _ in range(repeat):
    start = time.time()
    a = list(ex.map(lambda x: scs.solve(*x), datas))
    end = time.time()
    ts.append(end-start)
parallel = min(ts)

ts = []
for _ in range(repeat):
    start = time.time()
    a = list(ex.map(lambda x: scs.solve(*x, verbose=False), datas))
    end = time.time()
    ts.append(end-start)
parnotverbose = min(ts)

print('Serial solve time: %f'%serial)
print('Serial (notverbose) solve time: %f'%serialnotverbose)
print('Parallel solve time: %f'%parallel)
print('Parallel (not verbose) solve time: %f'%parnotverbose)