#include "utils.h"
#include "schema.h"

// Get the current thread frame global and local
int PySys_GetGlobalLocal(PyObject **pGlobal, PyObject **pLocal) {
  // Access the global and local dictionaries
  *pGlobal = PyEval_GetGlobals();
  *pLocal = PyEval_GetLocals();
  if (*pGlobal == NULL || *pLocal == NULL) {
    PyErr_SetString(PyExc_RuntimeError,
                    "Failed to get the global and local dictionaries");
    return 0;
  }
  return 1;
}

PyObject *PyObject_GetName(PyObject *obj) {
  return PyObject_GenericGetAttr(obj, PyUnicode_FromString("__name__"));
}

const char *PyObject_GetNameStr(PyObject *obj) {
  PyObject *name = PyObject_GetName(obj);
  if (name == NULL) {
    PyErr_SetString(PyExc_AttributeError, "__name__ not found");
    return NULL;
  }
  return PyUnicode_AsUTF8(name);
}

PyObject *PySchema_SetAnnotations(PyObject *obj, PyObject *annotations) {
  PyTypeObject *type;
  if (PyType_Check(obj) == 0) {
    type = Py_TYPE(obj);
  } else {
    // type object
    type = (PyTypeObject *)obj;
  }
  if (type == NULL) {
    fprintf(stderr, "Failed to get type in set annotations\n");
    return NULL;
  }

  if (PyDict_SetItemString(type->tp_dict, "__annotations__", annotations) ==
      -1) {
    PyErr_SetString(PyExc_RuntimeError, "Failed to set annotations");
    return NULL;
  }

  return annotations;
}

PyObject *PySchema_GetAnnotations(PyObject *obj) {
  PyTypeObject *type;
  if (PyType_Check(obj) == 0) {
    type = Py_TYPE(obj);
  } else {
    // type object
    type = (PyTypeObject *)obj;
  }
  if (type == NULL) {
    fprintf(stderr, "Failed to get type in get annotations\n");
    return NULL;
  }

  PyObject *annotations =
      PyDict_GetItemString(type->tp_dict, "__annotations__");
  if (annotations == NULL) {
    PyErr_SetString(PyExc_AttributeError, "__annotations__ not found");
    return NULL;
  } else {
    if (!PySchema_IsValidAnnotations(annotations)) {
      fprintf(stderr, "Invalid annotations\n");
      return NULL;
    }
  }

  return annotations;
}

int PySchema_IsAnnotationKeyOptional(PyObject *obj, const char *attr) {
  PyObject *annotations = PySchema_GetAnnotations(obj);
  if (annotations == NULL) {
    fprintf(stderr,
            "Failed to get annotations while getting annotation type\n");
    return 0;
  }

  PyObject *typeval = PyDict_GetItemString(annotations, attr);
  if (typeval == NULL) {
    fprintf(stderr, "Failed to get type while getting item %s\n", attr);
    return 0;
  }
  if (PyType_Check(typeval) == 0) {
    if (strcmp(Py_TYPE(typeval)->tp_name, "_UnionGenericAlias") == 0) {
      PyObject *args = PyObject_GetAttrString(typeval, "__args__");
      if (args == NULL) {
        fprintf(stderr, "Failed to get args\n");
        return 0;
      }
      // make sure it is a tuple
      if (!PyTuple_Check(args)) {
        fprintf(stderr, "Expected tuple\n");
        return 0;
      }

      // make sure the second element is None
      PyObject *second_element = PyTuple_GetItem(args, 1);
      if (second_element == NULL) {
        fprintf(stderr, "Failed to get second element\n");
        return 0;
      }

      return 1;
    }
  }
  return 0;
}

int PySchema_ContainAnnotationKey(PyObject *obj, const char *attr) {
  PyObject *annotations = PySchema_GetAnnotations(obj);
  if (annotations == NULL) {
    fprintf(stderr, "Failed to get annotations while checking annotation\n");
    return 0;
  }
  PyObject *attr_str = PyUnicode_FromString(attr);
  int has_attr = PyDict_Contains(annotations, attr_str);
  Py_DECREF(attr_str);
  return has_attr;
}

// TODO: BUG: we need to process nested type such as Generic type in Optional
PyObject *PySchema_GetAnnotationType(PyObject *obj, const char *attr) {
  PyObject *annotations = PySchema_GetAnnotations(obj);
  if (annotations == NULL) {
    fprintf(stderr,
            "Failed to get annotations while getting annotation type\n");
    return NULL;
  }

  PyObject *typeval = PyDict_GetItemString(annotations, attr);
  if (typeval == NULL) {
    fprintf(stderr, "Failed to get type while getting item %s\n", attr);
    return NULL;
  }
  if (PyType_Check(typeval) == 0) {
    // check if it is a type.GenericAlias
    // or _UnionGenericAlias
    if (strcmp(Py_TYPE(typeval)->tp_name, "types.GenericAlias") == 0) {
      PyObject *origin = PyObject_GetAttrString(typeval, "__origin__");
      if (PyType_Check(origin) == 0) {
        fprintf(stderr, "Failed to get origin in anno type\n");
        return NULL;
      }
      // if it is a list or dict type, return typeval
      if ((PyTypeObject *)origin == &PyList_Type ||
          (PyTypeObject *)origin == &PyDict_Type) {
        return origin;
      }
    } else if (strcmp(Py_TYPE(typeval)->tp_name, "_UnionGenericAlias") == 0) {
      PyObject *args = PyObject_GetAttrString(typeval, "__args__");
      if (args == NULL) {
        fprintf(stderr, "Failed to get args\n");
        return NULL;
      }
      // make sure it is a tuple
      if (!PyTuple_Check(args)) {
        fprintf(stderr, "Expected tuple\n");
        return NULL;
      }

      // make sure the second element is None
      PyObject *second_element = PyTuple_GetItem(args, 1);
      if (second_element == NULL) {
        fprintf(stderr, "Failed to get second element\n");
        return NULL;
      }

      // return the first element
      return PyTuple_GetItem(args, 0);
    }
    return NULL;
  }

  return typeval;
}

// TODO: BUG: we need to process nested type such as Generic type in Optional
PyObject *PySchema_GetAnnotationElementType(PyObject *obj, const char *attr) {
  PyObject *annotations = PySchema_GetAnnotations(obj);
  if (annotations == NULL) {
    fprintf(stderr,
            "Failed to get annotations while getting annotation type\n");
    return NULL;
  }

  PyObject *typeval = PyDict_GetItemString(annotations, attr);
  if (typeval == NULL) {
    fprintf(stderr, "Failed to get type while getting item %s\n", attr);
    return NULL;
  }
  if (PyType_Check(typeval) == 0) {
    // check if it is a type.GerericAlias or _UnionGenericAlias
    if (strcmp(Py_TYPE(typeval)->tp_name, "types.GenericAlias") == 0) {
      PyObject *origin = PyObject_GetAttrString(typeval, "__origin__");
      if (PyType_Check(origin) == 0) {
        fprintf(stderr, "Failed to get origin in element type\n");
        return NULL;
      }
      // if it is a list or dict type, return typeval
      if ((PyTypeObject *)origin == &PyList_Type) {
        // get __args__[0] from typeval
        PyObject *args = PyObject_GetAttrString(typeval, "__args__");
        if (args == NULL) {
          fprintf(stderr, "Failed to get args\n");
          return NULL;
        }
        PyObject *element_type = PyTuple_GetItem(args, 0);
        if (element_type == NULL) {
          fprintf(stderr, "Failed to get element type\n");
          return NULL;
        }
        return element_type;
      } else if ((PyTypeObject *)origin == &PyDict_Type) {
        // return (key, value) tuple object
        PyObject *args = PyObject_GetAttrString(typeval, "__args__");
        if (args == NULL) {
          fprintf(stderr, "Failed to get args\n");
          return NULL;
        }
        PyObject *key_type = PyTuple_GetItem(args, 0);
        PyObject *value_type = PyTuple_GetItem(args, 1);
        if (key_type == NULL || value_type == NULL) {
          fprintf(stderr, "Failed to get key or value type\n");
          return NULL;
        }
        return PyTuple_Pack(2, key_type, value_type);
      }
    } else if (strcmp(Py_TYPE(typeval)->tp_name, "_UnionGenericAlias") == 0) {
      // get first element of the tuple
      PyObject *args = PyObject_GetAttrString(typeval, "__args__");
      if (args == NULL) {
        fprintf(stderr, "Failed to get args\n");
        return NULL;
      }
      // make sure it is a tuple
      if (!PyTuple_Check(args)) {
        fprintf(stderr, "Expected tuple\n");
        return NULL;
      }

      // make sure the second element is None
      PyObject *second_element = PyTuple_GetItem(args, 1);
      if (second_element == NULL) {
        fprintf(stderr, "Failed to get second element\n");
        return NULL;
      }
      // make sure the second element is NoneType
      if ((PyTypeObject *)second_element != Py_TYPE(Py_None)) {
        fprintf(stderr, "Expected NoneType\n");
        fprintf(stderr, "Got: %s\n", PyObject_GetNameStr(second_element));
        return NULL;
      }

      // get the first element of the tuple
      PyObject *element_type = PyTuple_GetItem(args, 0);
      if (element_type == NULL) {
        fprintf(stderr, "Failed to get element type\n");
        return NULL;
      }
      return element_type;
    }
  }

  return NULL;
}

int PySchema_IsValidAnnotations(PyObject *annotations) {
  PyObject *key, *value;
  PyObject *schema = PySchema_GetRegisteredSchemas();
  Py_ssize_t pos = 0;

  if (schema == NULL) {
    return 0;
  }

  while (PyDict_Next(annotations, &pos, &key, &value)) {
    // print key and value
    int res = (PySchema_IsPrimitiveType(value) || PySchema_IsSchemaType(value));
    if (res == 0) {
      PyErr_SetString(
          PyExc_TypeError,
          sprintf_static("Invalid type %s", PyObject_GetNameStr(value)));
      return 0;
    }
  }

  return 1;
}

void PySchema_PrintAnnotations(PyObject *obj) {
  PyObject *annotations = PySchema_GetAnnotations(obj);
  if (annotations == NULL) {
    return;
  }
  PyObject *key, *value;
  Py_ssize_t pos = 0;
  while (PyDict_Next(annotations, &pos, &key, &value)) {
    PyObject *key_str = PyObject_Str(key);
    PyObject *value_str =
        PyObject_GenericGetAttr(value, PyUnicode_FromString("__name__"));
    fprintf(stderr, "key: %s, value: %s\n", PyUnicode_AsUTF8(key_str),
            PyUnicode_AsUTF8(value_str));
    Py_DECREF(key_str);
    Py_DECREF(value_str);
  }
}

void PySchema_PrintDir(PyObject *obj) {
  PyObject *dir = PyObject_Dir(obj);
  if (dir == NULL) {
    return;
  }
  Py_ssize_t len = PyList_Size(dir);
  for (Py_ssize_t i = 0; i < len; i++) {
    PyObject *attr = PyList_GetItem(dir, i);
    PyObject *attr_str = PyObject_Str(attr);
    fprintf(stderr, "attr: %s\n", PyUnicode_AsUTF8(attr_str));
    Py_DECREF(attr_str);
  }
  Py_DECREF(dir);
}

void PySchema_PrintTypeDict(PyTypeObject *type) {
  PyObject *dict = type->tp_dict;
  PyObject *key, *value;
  Py_ssize_t pos = 0;
  // print type __name__
  PyObject *type_name = PyObject_GetName((PyObject *)type);
  fprintf(stderr, "Type: %s\n", PyUnicode_AsUTF8(type_name));
  Py_DECREF(type_name);
  while (PyDict_Next(dict, &pos, &key, &value)) {
    PyObject *key_str = PyObject_Str(key);
    PyObject *value_str = PyObject_Str(value);
    fprintf(stderr, "key: %s, value: %s\n", PyUnicode_AsUTF8(key_str),
            PyUnicode_AsUTF8(value_str));
    Py_DECREF(key_str);
    Py_DECREF(value_str);
  }
}

const char *sprintf_static(const char *fmt, ...) {
  static char buffer[1 << 10];
  va_list args;
  va_start(args, fmt);
  vsprintf(buffer, fmt, args);
  va_end(args);
  return buffer;
}