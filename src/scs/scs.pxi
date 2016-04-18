

def version():
    cdef const char* c_string = scs_version()
    return c_string


def solve(dict data, dict cone, dict sol, dict settings):
    """ Call the C function scs().

    cone - assume cone has numpy arrays where appropriate
    """
    cdef scs_int m, n

    A = data['A']    
    m, n = A.shape
    cdef AMatrix _A = make_amatrix(A.data, A.indices, A.indptr, m, n)

    cdef scs_float[:] b = data['b']
    cdef scs_float[:] c = data['c']

    cdef Settings _settings = settings

    cdef Data _data = Data(m, n, &_A, &b[0], &c[0], &_settings)

    cdef Sol _sol = make_sol(sol['x'], sol['y'], sol['s'])

    cdef Info _info

    _cone = Cone(**cone)

    cdef scs_int result = scs(&_data, &_cone._cone, &_sol, &_info)

    sol['info'] = _info

    return sol

# todo: lightweight wrapper object for cones is the way to go.
# don't want to put all the cone functionality in here, since we
# need to compile the class for each int/float combo
# rename to cone stuffer?
cdef class Cone:
    """
    - expects input to by numpy arrays where approrpiate
    """
    cdef:
        _Cone _cone

    def __cinit__(self,
                  scs_int f=0,
                  scs_int l=0,
                  scs_int[:] q=None,
                  scs_int[:] s=None,
                  scs_float[:] p=None,
                  scs_int ep=0,
                  scs_int ed=0):

        self._cone = _Cone(f=f, l=l, ep=ep, ed=ed,
                           q=NULL, qsize=0,
                           s=NULL, ssize=0,
                           p=NULL, psize=0)

        # todo: check for positive size?
        if q is not None:
            self._cone.qsize = q.shape[0]
            self._cone.q = &q[0]

        if s is not None:
            self._cone.ssize = s.shape[0]
            self._cone.s = &s[0]

        if p is not None:
            self._cone.psize = p.shape[0]
            self._cone.p = &p[0]



cdef Sol make_sol(scs_float[:] x, scs_float[:] y, scs_float[:] s):
    cdef Sol sol = Sol(&x[0], &y[0], &s[0])
    return sol

cdef AMatrix make_amatrix(scs_float[:] data, scs_int[:] ind, scs_int[:] indptr, scs_int m, scs_int n):
    # Amatrix is not really big, so there's no need to dynamically allocate it.
    # difference with C/python? don't need to make this dynamically declared?
    # maybe fill a local array and then memcopy to dynamically allocated array
    cdef AMatrix cA = AMatrix(&data[0], &ind[0], &indptr[0], m, n)
    return cA



# think about how much of this workspace is exposed to the user...
# rather than being used by the python layer
cdef class Workspace:
    cdef: #private by default, 'readonly' to make public
        Work * _work
        Settings settings

        readonly Info info
        AMatrix _A

        Data _data


    def __cinit__(self, dict data, dict cone, dict settings):
        cdef scs_int m, n
        self.settings = settings

        A = data['A']
        m,n = A.shape
        self._A = make_amatrix(A.data, A.indices, A.indptr, m, n)

        cdef scs_float[:] b = data['b']
        cdef scs_float[:] c = data['c']

        self._data = Data(m, n, &self._A, &b[0], &c[0], &self.settings)

        # make cython cone (really need to disambiguate)
        _cone = Cone(**cone)

        self._work = scs_init(&self._data, &_cone._cone, &self.info)

        if self._work == NULL:
            raise MemoryError("Memory error in allocating Workspace.")

    def __dealloc__(self):
        if self._work != NULL:
            scs_finish(self._work);

    # this is weird and inconsistent. why no cone?
    def solve(self, scs_float[:] b, scs_float[:] c, dict cone, dict sol, dict settings):
        self.settings = settings
        self._data.stgs = &self.settings
        self._data.b = &b[0]
        self._data.c = &c[0]
        
        cdef Sol _sol = make_sol(sol['x'], sol['y'], sol['s'])

        _cone = Cone(**cone)

        # write to sol and info
        scs_solve(self._work, &self._data, &_cone._cone, &_sol, &self.info)
