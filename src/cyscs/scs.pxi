def version():
    """Return the current version of the underlying SCS C library.
    """
    cdef const char* c_string = scs_version()
    return c_string


def solve(dict data, dict cone, dict sol, dict settings):
    """ Call the C function scs().

    cone - assume cone has numpy arrays where appropriate
    """
    cdef:
        c_AMatrix c_A
        c_Settings c_settings
        Info c_info

    c_data = stuff_c_data(data, settings, &c_A, &c_settings)
    c_sol = stuff_c_sol(sol)
    c_cone = stuff_c_cone(cone)

    with nogil:
        # write to sol and info
        scs(&c_data, &c_cone, &c_sol, &c_info)

    sol['info'] = c_info

    return sol


cdef class Workspace:
    """ Maintain SCS _work and c_Data structs to keep a reference to the A matrix.
    Maintain c_settings and b and c only coincidentally, since they are part
    of the c_data struct; expect that b, c, and settings will be passed
    in from the Python level, and that the Python level will manage wether
    those things change between solves.

    This class is designed to be as minimal a wrapper around the C SCS workspace
    struct as possible, and we delegate as much logic as possible up to the
    python level.

    Assume that data, cone, and settings have the appropriate formats
    to be directly converted for use in C.
    """
    cdef: #private by default, 'readonly' to make public
        Work * _work
        c_Settings c_settings
        c_AMatrix c_A
        c_Data c_data

        readonly Info c_info

    def __cinit__(self, dict data, dict cone, dict settings):
        self.c_data = stuff_c_data(data, settings, &self.c_A, &self.c_settings)
        c_cone = stuff_c_cone(cone)

        with nogil:
            self._work = scs_init(&self.c_data, &c_cone, &self.c_info)

        if self._work == NULL:
            raise MemoryError("Memory error in allocating Workspace.")

    def __dealloc__(self):
        if self._work != NULL:
            with nogil:
                scs_finish(self._work);

    def solve(self, scs_float[:] b, scs_float[:] c, dict cone, dict sol, dict settings):
        self.c_settings = settings
        self.c_data.b = &b[0]
        self.c_data.c = &c[0]
        
        c_sol = stuff_c_sol(sol)
        c_cone = stuff_c_cone(cone)

        with nogil:
            # write to sol and info
            scs_solve(self._work, &self.c_data, &c_cone, &c_sol, &self.c_info)


cdef c_Data stuff_c_data(dict data, dict settings,
                         c_AMatrix* c_A, c_Settings* c_settings):
    """ Returns a filled-out C struct for SCS c_Data.

    Cython cdef functions return by *value*, not by reference,
    but this struct is lightweight enough (contains pointers to larger objects)
    to pass around by value.

    Needs pointers to existing c_A and c_settings which are guaranteed to
    persist as long as this c_Data struct.

    Expects:
    - data['b'], data['c'] to be numpy arrays
    - data['A'] a scipy.sparse CSC matrix
    """
    cdef:
        scs_int m, n
        scs_float[:] b = data['b']
        scs_float[:] c = data['c']

    # Cython dereferences with var_name[0]
    c_A[0] = stuff_c_amatrix(data['A'])
    m,n = c_A.m, c_A.n # dot notation even though a pointer to a struct (Cython thing)
    c_settings[0] = settings

    return c_Data(m, n, c_A, &b[0], &c[0], c_settings)


cdef c_Cone stuff_c_cone(dict cone):
    """ Returns a filled-out C struct for SCS c_Cone.

    Cython cdef functions return by *value*, not by reference,
    but this struct is lightweight enough (contains pointers to larger objects)
    to pass around by value.

    Expects s,q,p to be numpy arrays.
    """
    cdef:
        c_Cone c_cone
        scs_int[:] q
        scs_int[:] s
        scs_float[:] p

    c_cone = c_Cone(f=0, l=0, ep=0, ed=0,
                    q=NULL, qsize=0,
                    s=NULL, ssize=0,
                    p=NULL, psize=0)

    c_cone.f = cone.get('f', 0)
    c_cone.l = cone.get('l', 0)
    c_cone.ep = cone.get('ep', 0)
    c_cone.ed = cone.get('ed', 0)

    if 'q' in cone:
        q = cone['q']
        c_cone.qsize = q.shape[0]
        c_cone.q = &q[0]

    if 's' in cone:
        s = cone['s']
        c_cone.ssize = s.shape[0]
        c_cone.s = &s[0]

    if 'p' in cone:
        p = cone['p']
        c_cone.psize = p.shape[0]
        c_cone.p = &p[0]

    return c_cone    



cdef c_Sol stuff_c_sol(dict sol):
    """ Returns a filled-out C struct for SCS c_Sol.

    Cython cdef functions return by *value*, not by reference,
    but this struct is lightweight enough (contains pointers to larger objects)
    to pass around by value.

    Expects x,y,s to be numpy arrays.
    """
    cdef:
        scs_float[:] x = sol['x']
        scs_float[:] y = sol['y']
        scs_float[:] s = sol['s']

    return c_Sol(&x[0], &y[0], &s[0])

cdef c_AMatrix stuff_c_amatrix(A):
    """ Returns a filled-out C struct for SCS c_Amatrix.

    Cython cdef functions return by *value*, not by reference,
    but this struct is lightweight enough (contains pointers to larger objects)
    to pass around by value.

    Expects A to be a scipy.sparse CSC matrix.
    """
    cdef:
        scs_int m, n
        scs_float[:] data
        scs_int[:] ind
        scs_int[:] indptr
        c_AMatrix c_A

    m, n = A.shape
    data = A.data
    ind = A.indices
    indptr = A.indptr

    return c_AMatrix(&data[0], &ind[0], &indptr[0], m, n)

