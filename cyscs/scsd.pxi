cdef extern from "glbopts.h":
    ctypedef double scs_float
    ctypedef long scs_int
    
    ctypedef SCS_PROBLEM_DATA c_Data "Data"
    ctypedef SCS_SETTINGS c_Settings "Settings"
    ctypedef SCS_SOL_VARS c_Sol "Sol"
    ctypedef SCS_INFO Info
    ctypedef SCS_WORK Work
    ctypedef SCS_CONE c_Cone "Cone"


cdef extern from "linSys.h":
    ctypedef A_DATA_MATRIX c_AMatrix "AMatrix"


cdef extern from "scs.h":
    scs_int scs(const c_Data* d, const c_Cone* k, c_Sol* sol, Info* info) nogil
    const char * scs_version()
    
    Work * scs_init(const c_Data* d, const c_Cone* k, Info* info) nogil
    scs_int scs_solve(Work* w, const c_Data* d, const c_Cone* k, c_Sol* sol, Info* info) nogil
    void scs_finish(Work * w) nogil

    struct SCS_SETTINGS:
        scs_int normalize
        scs_float scale
        scs_float rho_x

        scs_int max_iters
        scs_float eps
        scs_float alpha
        scs_float cg_rate
        scs_int verbose
        scs_int warm_start


    struct SCS_PROBLEM_DATA:
        # these cannot change for multiple runs for the same call to scs_init
        scs_int m, n # A has m rows, n cols
        c_AMatrix * A # A is supplied in data format specified by linsys solver

        # these can change for multiple runs for the same call to scs_init
        scs_float * b
        scs_float * c # dense arrays for b (size m), c (size n)

        c_Settings * stgs # contains solver settings specified by user

    # contains primal-dual solution arrays */
    struct SCS_SOL_VARS:
        scs_float * x
        scs_float * y
        scs_float * s


    # contains terminating information
    struct SCS_INFO:
        scs_int iter # number of iterations taken */
        char status[32] # status string, e.g. 'Solved' */
        scs_int statusVal # status as scs_int, defined in constants.h */
        scs_float pobj # primal objective */
        scs_float dobj # dual objective */
        scs_float resPri # primal equality residual */
        scs_float resDual # dual equality residual */
        scs_float resInfeas # infeasibility cert residual */
        scs_float resUnbdd # unbounded cert residual */
        scs_float relGap # relative duality gap */
        scs_float setupTime # time taken for setup phase */
        scs_float solveTime # time taken for solve phase */

    # workspace for SCS
    struct SCS_WORK:
        pass


cdef extern from "amatrix.h":
    struct A_DATA_MATRIX:
        # A is supplied in column compressed format
        scs_float * x  # A values, size: NNZ A 
        scs_int * i    # A row index, size: NNZ A 
        scs_int * p    # A column pointer, size: n+1 
        scs_int m, n   # m rows, n cols


cdef extern from "cones.h":
# NB: rows of data matrix A must be specified in this exact order
    struct SCS_CONE:
        scs_int f # number of linear equality constraints
        scs_int l # length of LP cone
        scs_int *q # array of second-order cone constraints */
        scs_int qsize # length of SOC array */
        scs_int *s # array of SD constraints */
        scs_int ssize # length of SD array */
        scs_int ep # number of primal exponential cone triples */
        scs_int ed # number of dual exponential cone triples */
        scs_int psize # number of (primal and dual) power cone triples */
        scs_float * p # array of power cone params, must be \in [-1, 1],
                       # negative values are interpreted as specifying the dual cone */
        scs_int z # number of linear equality constraints (primal zero, dual free)

