#ifndef _BASE_H
#define _BASE_H

#include <Python.h>

int PySchema_IsPrimitiveType(PyObject *obj);
int PySchema_IsSchemaType(PyObject *obj);

void PySchema_Init(PyObject *module);
PyObject *PySchema_GetRegisteredSchemas();
int PySchema_AddRegisteredSchema(const char *class_name, PyObject *schema);
int PySchema_ContainsSchemaKey(const char *class_name);

PyObject *schema(PyObject *self, PyObject *args);

#endif // _BASE_H
