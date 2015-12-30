import scs
from concurrent.futures import ThreadPoolExecutor
import time

"""
Set up a list of several SCS problems and map `scs.solve` over that list.

Compare the compute time of Python's serial `map` with a multithreaded map
from concurrent.futures. Also test times with and without verbose printing.
"""

workers = 2 # size of the threadpool
num_problems = 4
m = 1000 # size of L1 problem
repeat = 2 # number of times to repeat timing

ex = ThreadPoolExecutor(max_workers=workers)
data = [scs.examples.l1(m, seed=i) for i in range(num_problems)]

def time_scs(mapper, **kwargs):
    """ Map `scs.solve` over the global `data` and return timing results

    Maps with `mapper`, which may be a parallel map, such as
    `concurrent.futures.ThreadPoolExecutor.map`

    Pass `kwargs` onto `scs.solve` to, for example, toggle verbose output
    """
    ts = []
    for _ in range(repeat):
        start = time.time()
        # `mapper` will usually return a generator instantly
        # need to consume the entire generator to find the actual compute time
        # calling `list` consumes the generator. an empty `for` loop would also work
        a = list(mapper(lambda x: scs.solve(*x, **kwargs), data))
        end = time.time()
        ts.append(end-start)
    return min(ts)

serial = time_scs(map)
serialnotverbose = time_scs(map, verbose=False)
parallel = time_scs(ex.map)
parnotverbose = time_scs(ex.map, verbose=False)

print('Serial solve time: %f'%serial)
print('Serial (not verbose) solve time: %f'%serialnotverbose)
print('Parallel solve time: %f'%parallel)
print('Parallel (not verbose) solve time: %f'%parnotverbose)