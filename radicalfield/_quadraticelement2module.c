#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <math.h> //sqrt



typedef struct {
    PyTypeObject* QuadraticElement2_Type;
    PyTypeObject* Fraction_Type;
} module_state;

static module_state*
get_module_state_by_type(PyTypeObject* type)
{
    return (module_state*)PyType_GetModuleState(type);
}



/* QuadraticElement2 */

typedef struct {
    PyObject_HEAD
    PyObject* a;
    PyObject* b;
} quadraticelement2object;

#define quadraticelement2object_CAST(op) ((quadraticelement2object*)(op))


/* Internal constructor: create a QuadraticElement2 with BORROWED refs to
   a and b (both ref-counts are incremented internally).
   Returns a new strong reference, or NULL on error. */
static PyObject*
qe2_make(PyTypeObject* type, PyObject* a, PyObject* b)
{
    quadraticelement2object* qe = quadraticelement2object_CAST(type->tp_alloc(type, 0));
    if(!qe) {
        return NULL;
    }
    qe->a = Py_NewRef(a);
    qe->b = Py_NewRef(b);
    //PyObject_GC_Track(qe);
    return (PyObject*)qe;
}

/* Convenience wrapper: same type as self (safe since IMMUTABLETYPE). */
#define QE2_MAKE(self, a, b) qe2_make(Py_TYPE(self), (a), (b))



PyDoc_STRVAR(quadraticelement2_doc,
"Element of the quadratic rationals $\\mathbb{K}\\left(\\sqrt{2}\\right)$.\n\
\n\
An instance represents an exact rational of the form\n\
\n\
$$\n\
    a+b\\sqrt{2} \\qquad a, b\\in\\mathbb{K}\n\
$$\n\
\n\
where currently $\\mathbb{K}$ is $\\mathbb{Z}$ (`int`)\n\
or $\\mathbb{Q}$ (`fractions.Fraction`).\n\
\n\
The immutable class supports exact conversion, ordering,\n\
algebraic conjugation, norm computation and arithmetic.\n\
\n\
Addition, subtraction & multiplication is closed,\n\
mixed coefficients are promoted.\n\
Inversion is closed for integers for a norm of $\\pm1$,\n\
otherwise it is promoted to rationals.\n\
Division is more often than necessary promoted to rationals.\n\
\n\
Parameters\n\
----------\n\
a : int or Fraction, default 0\n\
    Coefficient of $1$.\n\
b : int or Fraction, default 0\n\
    Coefficient of $\\sqrt{2}$.\n\
\n\
References\n\
----------\n\
- [Wikipedia - Quadratic integers](https://en.wikipedia.org/wiki/Quadratic_integer)\n\
\n\
C implementation.\n\
");

static PyObject*
quadraticelement2_new(PyTypeObject* subtype, PyObject* args, PyObject* kwds)
{
    module_state* state = get_module_state_by_type(subtype);
    quadraticelement2object* qe;
    PyObject* a = NULL;
    PyObject* b = NULL;
    
    static char* kwlist[] = {"a", "b", NULL};
    if(!PyArg_ParseTupleAndKeywords(args, kwds, "|OO:QuadraticElement2", kwlist, &a, &b)) {
        return NULL;
    }
    if(a) {
        if(PyLong_Check(a) || PyObject_TypeCheck(a, state->Fraction_Type)) {
            Py_INCREF(a);
        } else {
            PyErr_SetString(PyExc_TypeError, "coefficients must be int or fractions.Fraction.");
            return NULL;
        }
    } else {
        a = PyLong_FromLong(0);
        if(!a) {
            return NULL;
        }
    }
    if(b) {
        if(PyLong_Check(b) || PyObject_TypeCheck(b, state->Fraction_Type)) {
            Py_INCREF(b);
        } else {
            Py_DECREF(a);
            PyErr_SetString(PyExc_TypeError, "coefficients must be int or fractions.Fraction.");
            return NULL;
        }
    } else {
        b = PyLong_FromLong(0);
        if(!b) {
            Py_DECREF(a);
            return NULL;
        }
    }
    
    qe = (quadraticelement2object*)subtype->tp_alloc(subtype, 0);
    if(!qe) {
        Py_DECREF(a);
        Py_DECREF(b);
        return NULL;
    }
    
    qe->a = a;
    qe->b = b;
    //PyObject_GC_Track(qe);
    return (PyObject*)qe;
}



//garbage collection
static int
quadraticelement2_traverse(PyObject* self, visitproc visit, void* arg)
{
    quadraticelement2object* qe = quadraticelement2object_CAST(self);
    Py_VISIT(Py_TYPE(self));
    Py_VISIT(qe->a);
    Py_VISIT(qe->b);
    return 0;
}

static int
quadraticelement2_clear(PyObject* self)
{
    quadraticelement2object* qe = quadraticelement2object_CAST(self);
    Py_CLEAR(qe->a);
    Py_CLEAR(qe->b);
    return 0;
}

static void
quadraticelement2_dealloc(PyObject* self)
{
    PyTypeObject* tp = Py_TYPE(self);
    PyObject_GC_UnTrack(self);
    (void)quadraticelement2_clear(self);
    tp->tp_free(self);
    Py_DECREF(tp);
}



static int
quadraticelement2_bool(PyObject* self)
{
    quadraticelement2object* qe = quadraticelement2object_CAST(self);
    int a_true = PyObject_IsTrue(qe->a);
    if(a_true) { //true or error
        return a_true;
    }
    return PyObject_IsTrue(qe->b);
}

PyDoc_STRVAR(quadraticelement2_is_rational_doc,
"Return whether this element has no sqrt(2) component.");

static PyObject*
quadraticelement2_is_rational(PyObject* self, PyObject* Py_UNUSED(args))
{
    quadraticelement2object* qe = quadraticelement2object_CAST(self);
    int b_false = PyObject_Not(qe->b);
    if(b_false < 0) {
        return NULL;
    }
    if(b_false) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

PyDoc_STRVAR(quadraticelement2_as_fraction_doc,
"Return this element as a fraction.");

static PyObject*
quadraticelement2_as_fraction(PyObject* self, PyObject* Py_UNUSED(args))
{
    quadraticelement2object* qe = quadraticelement2object_CAST(self);
    module_state* state = get_module_state_by_type(Py_TYPE(self));
    
    int b_false = PyObject_Not(qe->b);
    if(b_false < 0) {
        return NULL;
    }
    if(!b_false) {
        PyErr_SetString(PyExc_ValueError, "not a fraction (b != 0)");
        return NULL;
    }
    return PyObject_CallOneArg((PyObject*)state->Fraction_Type, qe->a);
}

PyDoc_STRVAR(quadraticelement2_is_integer_doc,
"Return whether this element is an integer.");

static PyObject*
quadraticelement2_is_integer(PyObject* self, PyObject* Py_UNUSED(args))
{
    quadraticelement2object* qe = quadraticelement2object_CAST(self);
    
    int b_false = PyObject_Not(qe->b);
    if(b_false < 0) {
        return NULL;
    }
    if(!b_false) {
        Py_RETURN_FALSE;
    }
    
    if(PyLong_Check(qe->a)) {
        Py_RETURN_TRUE;
    }
    static PyObject* name = NULL;
    if(!name) {
        name = PyUnicode_InternFromString("is_integer");
        if(!name) {
            return NULL;
        }
    }
    return PyObject_CallMethodNoArgs(qe->a, name);
}

static PyObject*
quadraticelement2_int(PyObject* self)
{
    quadraticelement2object* qe = quadraticelement2object_CAST(self);
    
    int b_false = PyObject_Not(qe->b);
    if(b_false < 0) {
        return NULL;
    }
    if(!b_false) {
        PyErr_SetString(PyExc_ValueError, "not an integer");
        return NULL;
    }
    
    if(PyLong_Check(qe->a)) {
        return Py_NewRef(qe->a);
    }
    
    static PyObject* name_is_integer = NULL;
    if(!name_is_integer) {
        name_is_integer = PyUnicode_InternFromString("is_integer");
        if(!name_is_integer) {
            return NULL;
        }
    }
    PyObject* a_is_integer = PyObject_CallMethodNoArgs(qe->a, name_is_integer);
    if(!a_is_integer) {
        return NULL;
    }
    int ok = PyObject_IsTrue(a_is_integer);
    Py_DECREF(a_is_integer);
    if(ok < 0) {
        return NULL;
    }
    if(!ok) {
        PyErr_SetString(PyExc_ValueError, "not an integer");
        return NULL;
    }
    return PyNumber_Long(qe->a);
}

static PyObject*
quadraticelement2_float(PyObject* self)
{
    quadraticelement2object* qe = quadraticelement2object_CAST(self);
    double fa = PyFloat_AsDouble(qe->a);
    if(fa==-1.0 && PyErr_Occurred()) {
        return NULL;
    }
    double fb = PyFloat_AsDouble(qe->b);
    if(fb==-1.0 && PyErr_Occurred()) {
        return NULL;
    }
    return PyFloat_FromDouble(fa + sqrt(2.0) * fb);
}

//_sympy_

static Py_hash_t
quadraticelement2_hash(PyObject* self)
{
    quadraticelement2object* qe = quadraticelement2object_CAST(self);
    
    int b_zero = PyObject_Not(qe->b);
    if(b_zero < 0) {
        return -1;
    }
    if(b_zero) {
        return PyObject_Hash(qe->a);
    }
    
    PyObject* tup = PyTuple_Pack(2, qe->a, qe->b);
    if(!tup) {
        return -1;
    }
    Py_hash_t h = PyObject_Hash(tup);
    Py_DECREF(tup);
    return h;
}



//__eq__
//__lt__

static PyObject* quadraticelement2_pos(PyObject* self);
static PyObject* quadraticelement2_neg(PyObject* self);
static PyObject*
quadraticelement2_abs(PyObject* self)
{
    PyObject* zero = PyLong_FromLong(0);
    if(!zero) {
        return NULL;
    }
    int lt = PyObject_RichCompareBool(self, zero, Py_LT);
    Py_DECREF(zero);
    if(lt < 0) {
        return NULL;
    }
    return lt ? quadraticelement2_neg(self) : quadraticelement2_pos(self);
}



PyDoc_STRVAR(quadraticelement2_norm_doc,
"Return the algebraic norm.");

static PyObject*
quadraticelement2_norm(PyObject* self, PyObject* Py_UNUSED(args))
{
    quadraticelement2object *qe = quadraticelement2object_CAST(self);
    PyObject* aa;
    PyObject* bb;
    PyObject* two_bb;
    PyObject* r;
    
    aa = PyNumber_Multiply(qe->a, qe->a);
    if(aa == NULL) {
        return NULL;
    }
    
    bb = PyNumber_Multiply(qe->b, qe->b);
    if(bb == NULL) {
        Py_DECREF(aa);
        return NULL;
    }
    
    two_bb = PyNumber_Add(bb, bb);
    Py_DECREF(bb);
    if(two_bb == NULL) {
        Py_DECREF(aa);
        return NULL;
    }
    
    r = PyNumber_Subtract(aa, two_bb);
    Py_DECREF(aa);
    Py_DECREF(two_bb);
    return r;
}

PyDoc_STRVAR(quadraticelement2_conjugate_doc,
"Return the algebraic conjugate.");

static PyObject*
quadraticelement2_conjugate(PyObject* self, PyObject* Py_UNUSED(args))
{
    quadraticelement2object* qe = quadraticelement2object_CAST(self);
    PyObject* neg_b = PyNumber_Negative(qe->b);
    if(!neg_b) {
        return NULL;
    }
    
    PyObject* r = QE2_MAKE(self, qe->a, neg_b);
    Py_DECREF(neg_b);
    return r;
}


PyDoc_STRVAR(quadraticelement2_conj_doc,
"Return the algebraic conjugate.");

static PyObject*
quadraticelement2_conj(PyObject* self, PyObject* Py_UNUSED(args))
{
    return quadraticelement2_conjugate(self, NULL);
}

static PyObject*
quadraticelement2_pos(PyObject* self)
{
    quadraticelement2object* qe = quadraticelement2object_CAST(self);
    PyObject* pos_a = PyNumber_Positive(qe->a);
    if(!pos_a){
        return NULL;
    }
    PyObject* pos_b = PyNumber_Positive(qe->b);
    if(!pos_b) {
        Py_DECREF(pos_a);
        return NULL;
    }
    PyObject* r = QE2_MAKE(self, pos_a, pos_b);
    Py_DECREF(pos_a);
    Py_DECREF(pos_b);
    return r;
}

static PyObject*
quadraticelement2_neg(PyObject* self)
{
    quadraticelement2object* qe = quadraticelement2object_CAST(self);
    PyObject* neg_a = PyNumber_Negative(qe->a);
    if(!neg_a){
        return NULL;
    }
    PyObject* neg_b = PyNumber_Negative(qe->b);
    if(!neg_b) {
        Py_DECREF(neg_a);
        return NULL;
    }
    PyObject* r = QE2_MAKE(self, neg_a, neg_b);
    Py_DECREF(neg_a);
    Py_DECREF(neg_b);
    return r;
}

//__add__
//__radd__
//__sub__
//__rsub__
//__mul__
//__rmul__
//inv
//__truediv__
//__rtruediv__

static PyObject*
quadraticelement2_str(PyObject* self)
{
    quadraticelement2object* qe = quadraticelement2object_CAST(self);
    
    PyObject* a_str = PyObject_Str(qe->a);
    if(!a_str) {
        return NULL;
    }
    
    static PyObject* str_plus = NULL;
    if(!str_plus) {
        str_plus = PyUnicode_InternFromString("+");
        if(!str_plus) {
            Py_DECREF(a_str);
            return NULL;
        }
    }
    PyObject* b_fmt = PyObject_Format(qe->b, str_plus);
    if(!b_fmt) {
        Py_DECREF(a_str);
        return NULL;
    }
    
    PyObject* r = PyUnicode_FromFormat("%U%U\xe2\x88\x9a" "2", a_str, b_fmt);
    Py_DECREF(a_str);
    Py_DECREF(b_fmt);
    return r;
}

static PyObject*
quadraticelement2_repr(PyObject* self)
{
    quadraticelement2object* qe = quadraticelement2object_CAST(self);
    return PyUnicode_FromFormat("QuadraticElement2(a=%R, b=%R)", qe->a, qe->b);
}

static PyObject*
quadraticelement2_repr_latex(PyObject* self, PyObject* Py_UNUSED(args))
{
    quadraticelement2object* qe = quadraticelement2object_CAST(self);
    
    PyObject* a_str = PyObject_Str(qe->a);
    if(!a_str) {
        return NULL;
    }
    
    PyObject* str_plus = PyUnicode_InternFromString("+");
    if(!str_plus) {
        Py_DECREF(a_str);
        return NULL;
    }
    PyObject* b_fmt = PyObject_Format(qe->b, str_plus);
    Py_DECREF(str_plus);
    if(!b_fmt) {
        Py_DECREF(a_str);
        return NULL;
    }
    
    PyObject* r = PyUnicode_FromFormat("%U%U\\sqrt{2}", a_str, b_fmt);
    Py_DECREF(a_str);
    Py_DECREF(b_fmt);
    return r;
}

static PyMemberDef quadraticelement2_members[] = {
    {"a", Py_T_OBJECT_EX, offsetof(quadraticelement2object, a), Py_READONLY, NULL},
    {"b", Py_T_OBJECT_EX, offsetof(quadraticelement2object, b), Py_READONLY, NULL},
    {NULL}  /* sentinel */
};

static PyMethodDef quadraticelement2_methods[] = {
    {"is_rational",  quadraticelement2_is_rational, METH_NOARGS, quadraticelement2_is_rational_doc},
    {"as_fraction",  quadraticelement2_as_fraction, METH_NOARGS, quadraticelement2_as_fraction_doc},
    {"is_integer",   quadraticelement2_is_integer,  METH_NOARGS, quadraticelement2_is_integer_doc},
    {"norm",         quadraticelement2_norm,        METH_NOARGS, quadraticelement2_norm_doc},
    {"conjugate",    quadraticelement2_conjugate,   METH_NOARGS, quadraticelement2_conjugate_doc},
    {"conj",         quadraticelement2_conj,        METH_NOARGS, quadraticelement2_conj_doc},
    {"_repr_latex_", quadraticelement2_repr_latex,  METH_NOARGS, NULL},
    {NULL, NULL, 0, NULL}
};

static PyType_Slot quadraticelement2_slots[] = {
    {Py_tp_dealloc, quadraticelement2_dealloc},
    //Py_tp_getattr
    //Py_tp_setattr
    {Py_tp_repr, quadraticelement2_repr},
    {Py_tp_hash, quadraticelement2_hash},
    //Py_tp_call
    {Py_tp_str, quadraticelement2_str},
    //Py_tp_getattro
    //Py_tp_setattro
    {Py_tp_doc, quadraticelement2_doc},
    {Py_tp_traverse, quadraticelement2_traverse},
    {Py_tp_clear, quadraticelement2_clear},
    //{Py_tp_richcompare, quadraticelement2_richcompare},
    //Py_tp_iter
    //Py_tp_iternext
    {Py_tp_methods, quadraticelement2_methods},
    {Py_tp_members, quadraticelement2_members},
    //Py_tp_getset
    //Py_tp_base
    //Py_tp_descr_get
    //Py_tp_descr_set
    //Py_tp_init
    //Py_tp_alloc
    {Py_tp_new, quadraticelement2_new},
    //Py_tp_free don't touch https://docs.python.org/3/howto/isolating-extensions.html#not-overriding-tp-free
    //Py_tp_is_gc
    //Py_tp_bases
    //Py_tp_del
    //Py_tp_finalize
    //Py_tp_vectorcall
    
    //{Py_nb_add,         quadraticelement2_add},
    //{Py_nb_subtract,    quadraticelement2_sub},
    //{Py_nb_multiply,    quadraticelement2_multiply},
    {Py_nb_negative,    quadraticelement2_neg},
    {Py_nb_positive,    quadraticelement2_pos},
    {Py_nb_absolute,    quadraticelement2_abs},
    {Py_nb_bool,        quadraticelement2_bool},
    {Py_nb_int,         quadraticelement2_int},
    {Py_nb_float,       quadraticelement2_float},
    //{Py_nb_true_divide, quadraticelement2_true_divide},
    
    {0, 0} /* sentinel */
};

static PyType_Spec quadraticelement2_spec = {
    .name = "radicalfield._quadraticelement2.QuadraticElement2",
    .basicsize = sizeof(quadraticelement2object),
    .flags = (Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC | Py_TPFLAGS_IMMUTABLETYPE),
    .slots = quadraticelement2_slots
};



/* module */

static int
module_exec(PyObject* mod)
{
    module_state* state = PyModule_GetState(mod);
    
    PyObject* fractions = PyImport_ImportModule("fractions");
    if(fractions == NULL) {
        return -1;
    }
    state->Fraction_Type = (PyTypeObject*)PyObject_GetAttrString(fractions, "Fraction");
    Py_DECREF(fractions);
    if(state->Fraction_Type == NULL) {
        return -1;
    }
    
    state->QuadraticElement2_Type = (PyTypeObject*)PyType_FromModuleAndSpec(mod, &quadraticelement2_spec, NULL);
    if(state->QuadraticElement2_Type == NULL) {
        Py_DECREF(state->Fraction_Type);
        return -1;
    }
    if(PyModule_AddType(mod, state->QuadraticElement2_Type) < 0) {
        Py_DECREF(state->Fraction_Type);
        Py_DECREF(state->QuadraticElement2_Type);
        return -1;
    }
    
    return 0;
}

static struct PyModuleDef_Slot module_slots[] = {
    {Py_mod_exec, module_exec},
    {0, NULL}
};

static int
module_traverse(PyObject* mod, visitproc visit, void* arg)
{
    module_state* state = PyModule_GetState(mod);
    Py_VISIT(state->Fraction_Type);
    Py_VISIT(state->QuadraticElement2_Type);
    return 0;
}

static int
module_clear(PyObject* mod)
{
    module_state* state = PyModule_GetState(mod);
    Py_CLEAR(state->Fraction_Type);
    Py_CLEAR(state->QuadraticElement2_Type);
    return 0;
}

static void
module_free(void* mod)
{
    (void)module_clear((PyObject*)mod);
}

static struct PyModuleDef module = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "radicalfield._quadraticelement2",
    //.m_doc = module_doc,
    .m_size = sizeof(module_state),
    //.m_methods = NULL,
    .m_slots = module_slots,
    .m_traverse = module_traverse,
    .m_clear = module_clear,
    .m_free = module_free
};

PyMODINIT_FUNC
PyInit__quadraticelement2(void)
{
    return PyModuleDef_Init(&module);
}
