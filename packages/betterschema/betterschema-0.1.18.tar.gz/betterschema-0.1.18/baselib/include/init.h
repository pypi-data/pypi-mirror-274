#ifndef _INIT_H
#define _INIT_H

#include "schema.h"
#include <Python.h>

#define UNUSED(x) (void)(x)

int PySchema_ClassInit(PyObject *self, PyObject *args, PyObject *kwds);

#endif // _INIT_H