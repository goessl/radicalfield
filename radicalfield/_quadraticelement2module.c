#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>



typedef struct {
    PyTypeObject* QuadraticElement2_Type;
} module_state;



/* QuadraticElement2 */


typedef struct {
    PyObject_HEAD
    PyObject* a;
    PyObject* b;
} quadraticelement2object;

#define quadraticelement2object_CAST(op) ((quadraticelement2object*)(op))



static PyObject*
quadraticelement2_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
    quadraticelement2object* qe;
    PyObject* a = NULL;
    PyObject* b = NULL;
    
    static char* kwlist[] = {"a", "b", NULL};
    if(!PyArg_ParseTupleAndKeywords(args, kwds, "|OO", kwlist, &a, &b)) {
        return NULL;
    }
    if(!a) {
        a = PyLong_FromLong(0);
        if(!a) {
            return NULL;
        }
    } else {
        Py_INCREF(a);
    }
    if(!b) {
        b = PyLong_FromLong(0);
        if(!b) {
            Py_DECREF(a);
            return NULL;
        }
    } else {
        Py_INCREF(b);
    }
    
    qe = (quadraticelement2object*)type->tp_alloc(type, 0);
    if(!qe) {
        Py_DECREF(a);
        Py_DECREF(b);
        return NULL;
    }
    
    qe->a = a;
    qe->b = b;
    return (PyObject*)qe;
}

static void
quadraticelement2_dealloc(PyObject* op)
{
    quadraticelement2object* qe = quadraticelement2object_CAST(op);
    PyTypeObject* tp = Py_TYPE(qe);
    PyObject_GC_UnTrack(qe);
    Py_XDECREF(qe->a);
    Py_XDECREF(qe->b);
    tp->tp_free(qe);
    Py_DECREF(tp);
}

static int
quadraticelement2_traverse(PyObject *op, visitproc visit, void* arg)
{
    quadraticelement2object* qe = quadraticelement2object_CAST(op);
    Py_VISIT(Py_TYPE(qe));
    Py_VISIT(qe->a);
    Py_VISIT(qe->b);
    return 0;
}

static int
quadraticelement2_clear(PyObject* op)
{
    quadraticelement2object* qe = quadraticelement2object_CAST(op);
    Py_CLEAR(qe->a);
    Py_CLEAR(qe->b);
    return 0;
}

static PyMemberDef quadraticelement2_members[] = {
    {"a", Py_T_OBJECT_EX, offsetof(quadraticelement2object, a), Py_READONLY, NULL},
    {"b", Py_T_OBJECT_EX, offsetof(quadraticelement2object, b), Py_READONLY, NULL},
    {NULL}  /* sentinel */
};

//https://docs.python.org/3/c-api/typeobj.html
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
    //{Py_tp_methods, quadraticelement2_methods},
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
    
    state->QuadraticElement2_Type = (PyTypeObject*)PyType_FromModuleAndSpec(mod, &quadraticelement2_spec, NULL);
    if(state->QuadraticElement2_Type == NULL) {
        return -1;
    }
    if(PyModule_AddType(mod, state->QuadraticElement2_Type) < 0) {
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
    Py_VISIT(state->QuadraticElement2_Type);
    return 0;
}

static int
module_clear(PyObject* mod)
{
    module_state* state = PyModule_GetState(mod);
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
    .m_methods = NULL,
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
