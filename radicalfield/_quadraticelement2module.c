#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>



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


PyDoc_STRVAR(quadraticelement2_doc,
"Element of the quadratic rationals $\\mathbb{K}\\left(\\sqrt{2}\\right)$.\n\
\n\
An instance represents an exact rational of the form\n\
\n\
$$\n\
    a+b\\sqrt{2} \\qquad a, b\\in\mathbb{K}\n\
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
C implementation.\n\
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
");

static PyObject*
quadraticelement2_new(PyTypeObject* subtype, PyObject* args, PyObject* kwds)
{
    module_state* state = get_module_state_by_type(subtype);
    quadraticelement2object* qe;
    PyObject* a = NULL;
    PyObject* b = NULL;
    
    static char* const* kwlist[] = {"a", "b", NULL};
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
    PyObject_GC_Track(qe);
    return (PyObject*)qe;
}



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



PyDoc_STRVAR(quadraticelement2_is_rational_doc,
"Return whether this element has no sqrt(2) component.")

static PyObject*
quadraticelement2_is_rational(PyObject* self, PyObject* Py_UNUSED(args))
{
    quadraticelement2object* qe = quadraticelement2object_CAST(self);
    int is_zero = PyObject_Not(qe->b);
    if(is_zero < 0) {
        return NULL;
    }
    if(is_zero) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}


PyDoc_STRVAR(quadraticelement2_norm_doc,
"Return the algebraic norm.")

static PyObject*
quadraticelement2_norm(PyObject* self, PyObject* Py_UNUSED(args))
{
    quadraticelement2object *qe = quadraticelement2object_CAST(self);
    PyObject* aa = NULL;
    PyObject* bb = NULL;
    PyObject* two_bb = NULL;
    PyObject* result = NULL;
    
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
    if(two_bb == NULL) {
        Py_DECREF(aa);
        Py_DECREF(bb);
        return NULL;
    }
    
    result = PyNumber_Subtract(aa, two_bb);
    Py_DECREF(aa);
    Py_DECREF(bb);
    Py_DECREF(two_bb);
    return result;
}



static PyMemberDef quadraticelement2_members[] = {
    {"a", Py_T_OBJECT_EX, offsetof(quadraticelement2object, a), Py_READONLY, NULL},
    {"b", Py_T_OBJECT_EX, offsetof(quadraticelement2object, b), Py_READONLY, NULL},
    {NULL}  /* sentinel */
};

static PyMethodDef quadraticelement2_methods[] = {
    {"is_rational", quadraticelement2_is_rational, METH_NOARGS, quadraticelement2_is_rational_doc},
    {"norm",        quadraticelement2_norm,        METH_NOARGS, quadraticelement2_norm_doc},
    {NULL, NULL, 0, NULL}
};

static PyType_Slot quadraticelement2_slots[] = {
    {Py_tp_dealloc, quadraticelement2_dealloc},
    //Py_tp_getattr
    //Py_tp_setattr
    //Py_tp_repr
    //Py_tp_hash
    //Py_tp_call
    //Py_tp_str
    //Py_tp_getattro
    //Py_tp_setattro
    //{Py_tp_doc, quadraticelement2_doc},
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
    
    //number, ...
    
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
