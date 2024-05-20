#include "schema.h"
#include "attr.h"
#include "init.h"
#include "string.h"
#include "utils.h"
#include <Python.h>

#define CLASS_NAME_MAX_LEN 64
#define CLASS_DEF_BUF_SIZE 1024

static PyObject *PySchema_lshift(PyObject *, PyObject *);

// a dict object to hold all created schema classes
static PyObject *registered_schemas = NULL;

static PyNumberMethods PySchema_NumberMethods = {
    .nb_lshift = (binaryfunc)PySchema_lshift,
};

int PySchema_IsPrimitiveType(PyObject *obj) {
  if ((PyTypeObject *)obj == &PyLong_Type ||
      (PyTypeObject *)obj == &PyFloat_Type ||
      (PyTypeObject *)obj == &PyUnicode_Type ||
      (PyTypeObject *)obj == &PyBool_Type ||
      (PyTypeObject *)obj == &PyList_Type ||
      (PyTypeObject *)obj == &PyDict_Type) {
    return 1;
  } else if (strcmp(Py_TYPE(obj)->tp_name, "types.GenericAlias") == 0) {
    // get the origin type
    PyObject *origin = PyObject_GetAttrString(obj, "__origin__");
    if (origin == NULL) {
      return 0;
    }
    // make sure it is either list or dict
    if ((PyTypeObject *)origin == &PyList_Type ||
        (PyTypeObject *)origin == &PyDict_Type) {
      // make sure the element type is also primitive
      PyObject *args = PyObject_GetAttrString(obj, "__args__");
      if (args == NULL) {
        return 0;
      }
      // check length of tuple, if 1, then it is a list
      // if 2, then it is a dict
      if (PyTuple_Size(args) == 1) {
        PyObject *element_type = PyTuple_GetItem(args, 0);
        if (element_type == NULL) {
          return 0;
        }
        return PySchema_IsPrimitiveType(element_type);
      } else if (PyTuple_Size(args) == 2) {
        PyObject *key_type = PyTuple_GetItem(args, 0);
        PyObject *value_type = PyTuple_GetItem(args, 1);
        if (key_type == NULL || value_type == NULL) {
          return 0;
        }
        return (PySchema_IsPrimitiveType(key_type) &&
                PySchema_IsPrimitiveType(value_type));
      }
    }
  } else if (strcmp(Py_TYPE(obj)->tp_name, "_UnionGenericAlias") == 0) {
    // get the __args__ attribute
    PyObject *args = PyObject_GetAttrString(obj, "__args__");
    if (args == NULL) {
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
    // make sure the second element is NoneType
    if ((PyTypeObject *)second_element != Py_TYPE(Py_None)) {
      fprintf(stderr, "Expected NoneType\n");
      fprintf(stderr, "Got: %s\n", PyObject_GetNameStr(second_element));
      return 0;
    }

    // get the first element of the tuple
    PyObject *element_type = PyTuple_GetItem(args, 0);
    if (element_type == NULL) {
      fprintf(stderr, "Failed to get element type\n");
      return 0;
    }

    return ((PyTypeObject *)element_type == &PyLong_Type ||
            (PyTypeObject *)element_type == &PyFloat_Type ||
            (PyTypeObject *)element_type == &PyUnicode_Type ||
            (PyTypeObject *)element_type == &PyBool_Type ||
            (PyTypeObject *)element_type == &PyList_Type ||
            (PyTypeObject *)element_type == &PyDict_Type);
  }
  return 0;
}

int PySchema_IsSchemaType(PyObject *obj) {
  if (!PyType_Check(obj)) {
    return 0;
  }
  // go through registered schemas and check if obj is in there
  PyObject *key, *value;
  Py_ssize_t pos = 0;
  while (PyDict_Next(registered_schemas, &pos, &key, &value)) {
    if (PyObject_RichCompareBool(obj, value, Py_EQ) == 1) {
      return 1;
    }
  }
  return 0;
}

void PySchema_Init(PyObject *module) {
  // init dict object to hold all created schema classes
  registered_schemas = PyDict_New();

  if (registered_schemas == NULL) {
    // exit if failed to create dict
    exit(1);
  }

  // add variable to module
  PyModule_AddObject(module, "__schemas__", PySchema_GetRegisteredSchemas());
}

PyObject *PySchema_GetRegisteredSchemas() { return registered_schemas; }

int PySchema_AddRegisteredSchema(const char *class_name, PyObject *schema) {
  if (PyDict_Contains(registered_schemas, PyUnicode_FromString(class_name)) ==
      1) {
    return 0;
  }
  PyDict_SetItem(registered_schemas, PyUnicode_FromString(class_name), schema);
  return 1;
}

int PySchema_ContainsSchemaKey(const char *class_name) {
  // check if class_name is in registered_schemas keys
  if (PyDict_Contains(registered_schemas, PyUnicode_FromString(class_name)) ==
      1) {
    return 1;
  }
  return 0;
}

PyObject *schema(PyObject *self, PyObject *args) {
  UNUSED(self);
  int err = 0;

  PyObject *obj;
  if (!PyArg_ParseTuple(args, "O", &obj)) {
    return NULL; // Failed to parse a Python object argument
  }

  // find all __annotations__
  PyObject *annotations = PySchema_GetAnnotations(obj);
  if (annotations == NULL) {
    return NULL;
  }

  // return a new python class definition
  char *cls_def_buf = (char *)malloc(CLASS_DEF_BUF_SIZE);
  if (cls_def_buf == NULL) {
    PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
    return NULL;
  }

  char class_name[CLASS_NAME_MAX_LEN];
  const char *obj_name = PyObject_GetNameStr(obj);
  if (obj_name == NULL) {
    PyErr_SetString(PyExc_AttributeError, "__name__ not found");
    err = 1;
    goto out;
  }
  strncpy(class_name, obj_name, CLASS_NAME_MAX_LEN);
  class_name[CLASS_NAME_MAX_LEN - 1] = '\0';
  if (strlen(class_name) == 0) {
    PyErr_SetString(PyExc_AttributeError, "__name__ not found");
    err = 1;
    goto out;
  }

  sprintf(cls_def_buf, "class %s: pass", class_name);

  PyObject *pGlobal, *pLocal;
  if (!PySys_GetGlobalLocal(&pGlobal, &pLocal)) {
    err = 1;
    goto out;
  }

  PyRun_String(cls_def_buf, Py_file_input, pGlobal, pLocal);
  PyObject *class = PyDict_GetItemString(pLocal, class_name);
  if (class == NULL) {
    PyErr_SetString(PyExc_RuntimeError,
                    sprintf_static("Failed to get class: %s", class_name));
    err = 1;
    goto out;
  }

  // add __setattr__ method to the class
  PyTypeObject *class_type = (PyTypeObject *)class;
  // change setattr and getattr to PySchema_ClassDefSetAttr and
  // PySchema_ClassDefGetAttr
  class_type->tp_setattro = PySchema_ClassDefSetAttr;
  class_type->tp_getattro = PySchema_ClassDefGetAttr;
  class_type->tp_init = PySchema_ClassInit;
  class_type->tp_as_number = &PySchema_NumberMethods;

  if (PySchema_SetAnnotations(class, annotations) == NULL) {
    PyErr_SetString(PyExc_RuntimeError, "Failed to set annotations");
    err = 1;
    goto out;
  }

  // if any of the values in annotation is also set in the class, then
  // set the value to the class
  PyObject *key, *value;
  Py_ssize_t pos = 0;
  while (PyDict_Next(annotations, &pos, &key, &value)) {
    PyObject *cls_value = PyObject_GenericGetAttr(class, key);
    if (cls_value != NULL) {
      if (PyObject_GenericSetAttr(class, key, cls_value) < 0) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to set attribute");
        err = 1;
        goto out;
      }
    } else {
      // set to none if the value is not set
      if (PyObject_GenericSetAttr(class, key, Py_None) < 0) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to set attribute");
        err = 1;
        goto out;
      }
    }
  }

  // go through all attributes in the class and check if they are schema classes
  // if they are, also create them inside the class
  pos = 0;
  PyTypeObject *obj_class = (PyTypeObject *)obj;
  while (PyDict_Next(obj_class->tp_dict, &pos, &key, &value)) {
    if (PySchema_IsSchemaType(value)) {
      if (PyObject_GenericSetAttr(class, key, value) < 0) {
        PyErr_SetString(PyExc_RuntimeError, "Failed to set attribute");
        err = 1;
        goto out;
      }
    }
  }

  if (!PyCallable_Check(class)) {
    PyErr_SetString(PyExc_RuntimeError, "Failed to create a callable class");
    err = 1;
    goto out;
  }

  // add the created class to the schema_classes list, the key is the class name
  PySchema_AddRegisteredSchema(class_name, class);

out:
  free(cls_def_buf);
  if (err) {
    return NULL;
  }
  // clear error
  PyErr_Clear();
  Py_INCREF(class);
  return class;
}

static PyObject *PySchema_lshift(PyObject *self, PyObject *value) {
  // in case of a dict
  if (PyDict_Check(value)) {
    // iterate all dict items and set them as attributes
    PyObject *key, *item;
    Py_ssize_t pos = 0;
    while (PyDict_Next(value, &pos, &key, &item)) {
      // if self object does not have the key attribute
      // then return error
      if (PyObject_GenericGetAttr(self, key) == NULL) {
        PyErr_SetString(PyExc_AttributeError, "Attribute not found");
        return NULL;
      }
      // set the attribute
      if (self->ob_type->tp_setattro(self, key, item) < 0) {
        return NULL;
      }
    }
  } else {
    // return not yet supported error
    PyErr_SetString(PyExc_NotImplementedError, "Not yet supported");
    return NULL;
  }
  // TODO: implement this
  return self;
}
