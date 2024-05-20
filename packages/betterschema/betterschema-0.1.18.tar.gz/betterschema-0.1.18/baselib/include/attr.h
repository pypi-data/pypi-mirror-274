#ifndef _ATTR_H
#define _ATTR_H

#include "schema.h"
#include <Python.h>

int PySchema_ClassDefSetAttr(PyObject *, PyObject *, PyObject *);
PyObject *PySchema_ClassDefGetAttr(PyObject *self, PyObject *name);

#endif // _ATTR_H