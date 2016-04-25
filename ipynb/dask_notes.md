# dask processor tests

```python
import dask.array as da
x = da.random.normal(10, .1, size=(10000, 10000), chunks = (1000,1000))
y = (x+100).mean(axis=0)
y.compute()
dask.set_options(get=dask.async.get_sync)
```

Check out put with `top` and `htop`.
- Note that `top` only goes up to 100%, so when calling
a single-threaded program with GIL, will only
get up to 25% on my laptop.
- `htop` may show all cores active, or 50% on two cores (thread affinity issue?)

# test GIL for SCS
- see what SCS looks like in paralell

```python
import scs
from concurrent.futures import ThreadPoolExecutor
ex = ThreadPoolExecutor(max_workers=2)
datas = [scs.examples.l1(3000) for i in range(4)]
list(ex.map(lambda x: scs.solve(*x), datas))
```

what does this look like on kona64...?

- should i write a dummy func to capture C output?
- write two SCS versions, one with gil and one without?
- how is this handled in other projects?

- have dummy print function that aquires and releases the GIL to print progress?
https://groups.google.com/forum/#!topic/cython-users/Sm8Vcg8CPsg

- test performance of using verbose or not...


Serial solve time: 8.634671
Serial (notverbose) solve time: 8.419349
Parallel solve time: 5.480639
Parallel (not verbose) solve time: 5.276434






