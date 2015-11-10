import numpy as np
cimport numpy as cnp # todo: what do i need cimport numpy for?
# use the python malloc/free to have the memory attributed to python.
#from cpython.mem cimport PyMem_Malloc, PyMem_Free
from cpython.object cimport Py_EQ, Py_NE


def version():
    cdef const char* c_string = scs_version()
    return c_string


def solve(dict data, Cone cone, dict sol, dict settings):
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
    # todo: validate input data: -1 <= p <= 1; q,s have positive integer elements,...
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

        if q is None:
            q = []
        self.q = np.array(q, dtype=np.int64)
        self.q.flags.writeable = False
        self._cone.q = <scs_int *>self.q.data
        self._cone.qsize = len(self.q)

        if s is None:    
            s = []
        self.s = np.array(s, dtype=np.int64)
        self.s.flags.writeable = False
        self._cone.s = <scs_int *>self.s.data
        self._cone.ssize = len(self.s)

        if p is None:
            p = []
        self.p = np.array(p, dtype=np.float64)
        self.p.flags.writeable = False
        self._cone.p = <scs_float *>self.p.data
        self._cone.psize = len(self.p)

            
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

    def __richcmp__(x, y, int op):
        cdef:
            Cone a, b
        if op == Py_EQ:
            if isinstance(x, Cone) and isinstance(y, Cone):
                a = x
                b = y
                if a._cone.f != b._cone.f:
                    return False
                if a._cone.l != b._cone.l:
                    return False
                if a._cone.ep != b._cone.ep:
                    return False
                if a._cone.ed != b._cone.ed:
                    return False
                if (a.q != b.q).any():
                    return False
                if (a.s != b.s).any():
                    return False
                if (a.p != b.p).any():
                    return False

                return True
            else:
                return False

        elif op == Py_NE:
            return not (x == y)
        else:
            raise SyntaxError("Can only compare Cone to another Cone for equality.")
        
cdef class Workspace:
    cdef: #private by default, 'readonly' to make public
        Work * _work
        Settings settings

        readonly Info info
        AMatrix _A

        Data _data
        # could probably move Cone up to python
        Cone cone


    def __cinit__(self, dict data, dict cone, dict settings):
        self.settings = settings

        A = data['A']
        cdef scs_int m, n
        m,n = A.shape

        self._A = make_amatrix(A.data, A.indices, A.indptr, m, n)

        cdef scs_float[:] b = data['b']
        cdef scs_float[:] c = data['c']

        self._data = Data(m, n, &self._A, &b[0], &c[0], &self.settings)

        # todo: do i convert at this point?
        self.cone = Cone(**cone)

        self._work = scs_init(&self._data, &self.cone._cone, &self.info)

        if self._work == NULL: 
            raise MemoryError("Memory error in allocating Workspace.")

    def __dealloc__(self):
        if self._work != NULL:
            scs_finish(self._work);

    # todo: reduce the signature to just the data that we actualy need
    # dont need all of data, just b, c
    def solve(self, dict data, dict sol, dict settings):
        cdef scs_float[:] b = data['b']
        cdef scs_float[:] c = data['c']

        self.settings = settings
        self._data.stgs = &self.settings
        self._data.b = &b[0]
        self._data.c = &c[0]
        
        cdef Sol _sol = make_sol(sol['x'], sol['y'], sol['s'])

        cdef scs_int status
        status = scs_solve(self._work, &self._data, &self.cone._cone, &_sol, &self.info)

        print 'info: ', self.info
        #return status, sol
