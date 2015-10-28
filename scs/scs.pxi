import numpy as np
cimport numpy as cnp # todo: what do i need cimport numpy for?
# use the python malloc/free to have the memory attributed to python.
#from cpython.mem cimport PyMem_Malloc, PyMem_Free

def version():
    cdef char* c_string = scs_version()
    return c_string


# IDEA: scs_solve interface is simple, the cached interface is a little more
# complicated, with the data input only updating what's necessary.

# maybe I don't even need the c function scs? maybe just do it for error checking?

# todo: assume 64bit int, and double.
# todo: do we have to convert CSC to 64 bit int?
# todo: coppying of data and ownership issues....

# todo: check for correct data format and convert if needed (all python)
# make direct and indirect versions, and call the appropriate one
# split into python and cython modules (as little code as possible in cython?)


def solve(dict data, Cone cone, dict settings):
    """ Call the C function scs().

    """
    A = data['A']
    cdef scs_int m, n 
    m, n = A.shape

    cdef AMatrix _A = make_amatrix(A.data, A.indices, A.indptr, m, n)

    cdef scs_float[:] b = data['b']
    cdef scs_float[:] c = data['c']

    cdef Settings _settings = settings

    cdef Data _data = Data(m, n, &_A, &b[0], &c[0], &_settings)

    # todo: sol prep should be done at python level?
    sol = dict(x=np.zeros(n), y=np.zeros(m), s=np.zeros(m))
    cdef Sol _sol = make_sol(sol['x'], sol['y'], sol['s'])

    cdef Info _info

    cdef scs_int result = scs(&_data, &cone._cone, &_sol, &_info)

    sol['info'] = _info

    return sol



cdef Sol make_sol(scs_float[:] x, scs_float[:] y, scs_float[:] s):
    cdef Sol sol = Sol(&x[0], &y[0], &s[0])
    return sol

cdef AMatrix make_amatrix(scs_float[:] data, scs_int[:] ind, scs_int[:] indptr, scs_int m, scs_int n):
    # Amatrix is not really big, so there's no need to dynamically allocate it.
    # difference with C/python? don't need to make this dynamically declared?
    # maybe fill a local array and then memcopy to dynamically allocated array
    cdef AMatrix cA = AMatrix(&data[0], &ind[0], &indptr[0], m, n)
    return cA

cdef class Cone:
    cdef:
        _Cone _cone
        cnp.ndarray q, s, p
    
    def __cinit__(self, scs_int f=0, scs_int l=0, q=None, s=None, p=None, scs_int ep=0, scs_int ed=0):
        self._cone = _Cone(f=f,l=l,ep=ep,ed=ed,
                              q=NULL,
                              qsize=0,
                              s=NULL,
                              ssize=0,
                              p=NULL,
                              psize=0)

        #todo: get rid of the weird branch for empty arrays
        # just have the pointer point to the empyt numpy array memory with zero size
        if q is not None and len(q) > 0:
            self.q = np.array(q, dtype=np.int64)
            self.q.flags.writeable = False
            self._cone.q = <scs_int *>self.q.data
            self._cone.qsize = len(self.q)
        else:
            self.q = np.array([], dtype=np.int64)
            
        if s is not None and len(s) > 0:
            self.s = np.array(s, dtype=np.int64)
            self.s.flags.writeable = False
            self._cone.s = <scs_int *>self.s.data
            self._cone.ssize = len(self.s)
        else:
            self.s = np.array([], dtype=np.int64)
            
        if p is not None and len(p) > 0:
            self.p = np.array(p, dtype=np.float64)
            self.p.flags.writeable = False
            self._cone.p = <scs_float *>self.p.data
            self._cone.psize = len(self.p)
        else:
            self.p = np.array([], dtype=np.float64)
            
    def __len__(self):
        cdef scs_int total = 0
        total += self._cone.f
        total += self._cone.l
        total += 3*self._cone.ep
        total += 3*self._cone.ed
        total += sum(self.q)
        total += sum((self.s*(self.s+1))/2)
        total += 3*self._cone.psize
        return total

            
    def todict(self):
        # todo: do i need the empty lists?
        d = {}
        if self._cone.f > 0:
            d['f'] = self._cone.f

        if self._cone.l > 0:
            d['l'] = self._cone.l

        if self._cone.ep > 0:
            d['ep'] = self._cone.ep

        if self._cone.ed > 0:
            d['ed'] = self._cone.ed

        if self._cone.qsize > 0:
            d['q'] = self.q
        
        if self._cone.ssize > 0:
            d['s'] = self.s
            
        if self._cone.psize > 0:
            d['p'] = self.p

        return d
    
    def __repr__(self):
        d = self.todict()
        s = 'Cone('
        s += ', '.join('{}={}'.format(k, self.array_repr(d[k])) for k in d)
        s += ')'
        return s

    def array_repr(self, item):
        if isinstance(item, int):
            return item
        else:
            return list(item)
    
    def __str__(self):
        return repr(self)
        

