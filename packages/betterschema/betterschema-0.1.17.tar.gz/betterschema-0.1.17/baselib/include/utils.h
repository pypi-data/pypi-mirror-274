#ifndef _UTILS_H
#define _UTILS_H

#include "schema.h"
#include <Python.h>

int PySys_GetGlobalLocal(PyObject **pGlobal, PyObject **pLocal);

PyObject *PyObject_GetName(PyObject *obj);
const char *PyObject_GetNameStr(PyObject *obj);

// schema annotation related functions
PyObject *PySchema_GetAnnotations(PyObject *obj);
PyObject *PySchema_SetAnnotations(PyObject *obj, PyObject *annotations);

int PySchema_IsAnnotationKeyOptional(PyObject *obj, const char *attr);
int PySchema_ContainAnnotationKey(PyObject *obj, const char *attr);
PyObject *PySchema_GetAnnotationType(PyObject *obj, const char *attr);
PyObject *PySchema_GetAnnotationElementType(PyObject *obj, const char *attr);

int PySchema_IsValidAnnotations(PyObject *annotations);

void PySchema_PrintAnnotations(PyObject *obj);
void PySchema_PrintDir(PyObject *obj);
void PySchema_PrintTypeDict(PyTypeObject *type);

const char *sprintf_static(const char *fmt, ...);

#endif // _UTILS_H
