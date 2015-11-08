# make sure to also install psutil with memory_profiler
from memory_profiler import memory_usage
import numpy as np

# garbage collection before each memory_usage call does seem to give better estimates
import gc
from cvxpy import *
from collections import defaultdict

def cvx_solve():
    m = 128
    n = 10
    np.random.seed(1)
    A = np.random.randn(m, n)
    b = np.random.randn(m)

    # Construct the problem.
    x = Variable(n)
    objective = Minimize(norm(A*x - b))
    constraints = [0 <= x, x <= 1]
    prob = Problem(objective, constraints)
    prob.solve('SCS')

def dummy():
    a = defaultdict(list)
    n = 1000
    for i in np.random.randint(n,size=2*n):
        a[i] += [i*i]

# run a few times to get any ancillary objects created
cvx_solve()
dummy()
gc.collect()
r = memory_usage(-1, interval=0)
cvx_solve()
dummy()
gc.collect()
r = memory_usage(-1, interval=0)

n = 1000
a = np.zeros(n)
for i in range(n):
    # compare the output from running with cvx_solve or with dummy
    cvx_solve()
    #dummy()
    gc.collect()
    r = memory_usage(-1, interval=0)
    a[i] = r[0]

print (a.max() - a.min())/n