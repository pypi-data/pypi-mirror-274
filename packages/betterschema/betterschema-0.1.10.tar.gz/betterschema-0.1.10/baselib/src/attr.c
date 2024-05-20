#include "attr.h"
#include "init.h"
#include "utils.h"
#include "watch.h"

// getattr
PyObject *PySchema_ClassDefGetAttr(PyObject *self, PyObject *name) {
  // get self annotations
  if (PySchema_GetAnnotations(self) == NULL) {
    return NULL;
  }

  // get the name of the attribute
  PyObject *name_str = PyObject_Str(name);
  char name_str_c[100];
  sprintf(name_str_c, "%s", PyUnicode_AsUTF8(name_str));
  Py_DECREF(name_str);

  // check if the attribute is in the annotations
  int has_attr = PySchema_ContainAnnotationKey(self, name_str_c);
  if (!has_attr) {
    // check if the attribute has __ prefix
    if (name_str_c[0] == '_' && name_str_c[1] == '_') {
      return PyObject_GenericGetAttr(self, name);
    }
    PyErr_SetString(PyExc_AttributeError,
                    sprintf_static("Attribute %s not found while getting attr",
                                   name_str_c));
    return NULL;
  }

  PyObject *anno_type = PySchema_GetAnnotationType(self, name_str_c);
  if (anno_type == NULL) {
    return NULL;
  }
  if (PySchema_IsPrimitiveType(anno_type) || PySchema_IsSchemaType(anno_type)) {
    return PyObject_GenericGetAttr(self, name);
  }

  PyErr_SetString(
      PyExc_TypeError,
      sprintf_static("Unsupported type while getting attribute %s of type %s",
                     name_str_c, ((PyTypeObject *)anno_type)->tp_name));
  return NULL;
}

int PySchema_ValidDictType(PyObject *value, PyObject *anno_key_type,
                           PyObject *anno_value_type) {
  // make sure value is a dict type
  if (!PyDict_Check(value)) {
    PyErr_SetString(PyExc_TypeError, "Expected dict");
    return 0;
  }

  // make sure anno_key_type is a type
  if (!PyType_Check(anno_key_type)) {
    PyErr_SetString(PyExc_TypeError, "Expected type");
    return 0;
  }

  // make sure anno_value_type is a type
  if (!PyType_Check(anno_value_type)) {
    PyErr_SetString(PyExc_TypeError, "Expected type");
    return 0;
  }

  // iterate each item in value and check if the type is correct
  PyObject *key, *item;
  Py_ssize_t pos = 0;
  while (PyDict_Next(value, &pos, &key, &item)) {
    PyObject *key_type = PyObject_Type(key);
    PyObject *item_type = PyObject_Type(item);
    if (PyObject_RichCompareBool(anno_key_type, key_type, Py_EQ) == 0) {
      PyErr_SetString(PyExc_TypeError,
                      sprintf_static("Expected dict key type %s, got %s",
                                     PyObject_GetNameStr(anno_key_type),
                                     PyObject_GetNameStr(key_type)));
      return 0;
    }
    if (PyObject_RichCompareBool(anno_value_type, item_type, Py_EQ) == 0) {
      PyErr_SetString(PyExc_TypeError,
                      sprintf_static("Expected dict value type %s, got %s",
                                     PyObject_GetNameStr(anno_value_type),
                                     PyObject_GetNameStr(item_type)));
      return 0;
    }
  }
  return 1;
}

int PySchema_ValidListType(PyObject *value, PyObject *anno_element_type) {
  // make sure value is a list type
  if (!PyList_Check(value)) {
    PyErr_SetString(PyExc_TypeError, "Expected list");
    return 0;
  }

  // make sure anno_element_type is a type
  if (!PyType_Check(anno_element_type)) {
    PyErr_SetString(PyExc_TypeError, "Expected type");
    return 0;
  }

  // iterate each item in value and check if the type is correct
  Py_ssize_t len = PyList_Size(value);
  for (Py_ssize_t i = 0; i < len; i++) {
    PyObject *item = PyList_GetItem(value, i);
    PyObject *item_type = PyObject_Type(item);
    if (PyObject_RichCompareBool(anno_element_type, item_type, Py_EQ) == 0) {
      PyErr_SetString(PyExc_TypeError,
                      sprintf_static("Expected list element type %s, got %s",
                                     PyObject_GetNameStr(anno_element_type),
                                     PyObject_GetNameStr(item_type)));
      return 0;
    }
  }
  return 1;
}

// setattr
int PySchema_ClassDefSetAttr(PyObject *self, PyObject *name, PyObject *value) {
  // get self annotations
  if (PySchema_GetAnnotations(self) == NULL) {
    return -1;
  }

  // get the name of the attribute
  PyObject *name_str = PyObject_Str(name);
  char name_str_c[100];
  sprintf(name_str_c, "%s", PyUnicode_AsUTF8(name_str));
  Py_DECREF(name_str);

  // check if the attribute is in the annotations
  int has_attr = PySchema_ContainAnnotationKey(self, name_str_c);
  if (!has_attr) {
    PyErr_SetString(
        PyExc_AttributeError,
        sprintf_static("Attribute \"%s\" not found while setting attr",
                       name_str_c));
    return -1;
  }

  PyObject *right_type = PyObject_Type(value);
  if (right_type == NULL) {
    return -1;
  }
  PyObject *anno_type = PySchema_GetAnnotationType(self, name_str_c);
  if (anno_type == NULL) {
    return -1;
  }
  if (PySchema_IsPrimitiveType(anno_type)) {
    if (PyObject_RichCompareBool(anno_type, right_type, Py_EQ) == 0) {
      PyErr_SetString(PyExc_TypeError,
                      sprintf_static("Expected %s, got %s",
                                     PyObject_GetNameStr(anno_type),
                                     PyObject_GetNameStr(right_type)));
      return -1;
    }
    // if dict or list, make sure the element type is correct
    if ((PyTypeObject *)anno_type == &PyList_Type) {
      // make sure the right side element type is correct
      PyObject *anno_element_type =
          PySchema_GetAnnotationElementType(self, name_str_c);
      if (anno_element_type == NULL) {
        return -1;
      }

      if (!PySchema_ValidListType(value, anno_element_type)) {
        return -1;
      }
    } else if ((PyTypeObject *)anno_type == &PyDict_Type) {
      // get key type and value type from return tuple
      PyObject *anno_element_tuple =
          PySchema_GetAnnotationElementType(self, name_str_c);
      if (anno_element_tuple == NULL) {
        return -1;
      }
      PyObject *anno_key_type = PyTuple_GetItem(anno_element_tuple, 0);
      PyObject *anno_value_type = PyTuple_GetItem(anno_element_tuple, 1);
      // iterate each item in value and check if the type is correct
      if (!PySchema_ValidDictType(value, anno_key_type, anno_value_type)) {
        return -1;
      }
    }

    PyObject *old_value = PyObject_GenericGetAttr(self, name);
    if (PyObject_GenericSetAttr(self, name, value) < 0) {
      return -1;
    } else {
      // trigger watch event
      if (PyWatch_OnAttributeUpdate(self, name_str_c, old_value, value) < 0) {
        return -1;
      }
    }
    return 0;
  } else if (PySchema_IsSchemaType(anno_type)) {
    // create a new instance of the class and initialize it
    PyObject *instance = PyObject_CallObject(anno_type, PyTuple_Pack(1, value));
    if (instance == NULL) {
      return -1;
    }
    PyObject *old_value = PyObject_GenericGetAttr(self, name);
    if (PyObject_GenericSetAttr(self, name, instance) < 0) {
      return -1;
    } else {
      // trigger watch event
      if (PyWatch_OnAttributeUpdate(self, name_str_c, old_value, instance) <
          0) {
        return -1;
      }
    }
    return 0;
  }

  PyErr_SetString(
      PyExc_TypeError,
      sprintf_static("Unsupported type while setting attribute %s of type %s",
                     name_str_c, ((PyTypeObject *)anno_type)->tp_name));
  return -1;
}
