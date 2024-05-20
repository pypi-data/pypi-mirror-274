#ifndef _WATCH_H

#define _WATCH_H

#include <Python.h>

void PyWatch_Init(PyObject *module);

PyObject *PyWatch_GetWatchDict();

PyObject *watch(PyObject *self, PyObject *args);

int PyWatch_OnAttributeUpdate(PyObject *instance, const char *attr,
                              const PyObject *old_value,
                              const PyObject *new_value);

#endif // _WATCH_H
