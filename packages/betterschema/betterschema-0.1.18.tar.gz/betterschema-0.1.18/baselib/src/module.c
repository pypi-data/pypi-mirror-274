#include "attr.h"
#include "init.h"
#include "schema.h"
#include "utils.h"
#include "watch.h"
#include <Python.h>

static PyMethodDef Methods[] = {
    {"schema", schema, METH_VARARGS,
     "Create a schema class from defined class"},
    {"watch", watch, METH_VARARGS, "Watch variable changes"},
    {NULL, NULL, 0, NULL} // Sentinel
};

static struct PyModuleDef module = {PyModuleDef_HEAD_INIT,
                                    "betterschema", // Name of the module
                                    "betterschema module for Python C API",
                                    -1,
                                    Methods,
                                    NULL,
                                    NULL,
                                    NULL,
                                    NULL};

PyMODINIT_FUNC PyInit_baselib(void) {
  PyObject *m = PyModule_Create(&module);
  if (m == NULL) {
    exit(1);
  }

  // init dict object to hold all created schema classes
  PySchema_Init(m);
  PyWatch_Init(m);

  return m;
}
