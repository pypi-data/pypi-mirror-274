#include "watch.h"
#include "init.h"

#include <Python.h>

// a dict object that maps class names to another dict which maps attribute name
// strings to functions
static PyObject *watched_classes = NULL;

void PyWatch_Init(PyObject *m) {
  // init dict object to hold all watched classes
  watched_classes = PyDict_New();
  if (watched_classes == NULL) {
    // exit if failed to create dict
    exit(1);
  }

  // add variable to module
  PyModule_AddObject(m, "__watches__", PyWatch_GetWatchDict());
}

PyObject *PyWatch_GetWatchDict() { return watched_classes; }

int PyWatch_AddWatchedAttribute(PyObject *class, const char *attr,
                                PyObject *func) {
  // make sure class is a class
  if (!PyType_Check(class)) {
    return 0;
  }
  // make sure func is a function
  if (!PyFunction_Check(func)) {
    return 0;
  }
  // get the dict for the class
  PyObject *class_dict = PyDict_GetItem(watched_classes, class);
  if (class_dict == NULL) {
    // create a new dict for the class
    class_dict = PyDict_New();
    PyDict_SetItem(watched_classes, class, class_dict);
  }

  // check if there is already an item with the same key
  // if not add a new list to the dict
  PyObject *func_list = PyDict_GetItem(class_dict, PyUnicode_FromString(attr));
  if (func_list == NULL) {
    func_list = PyList_New(0);
    PyDict_SetItem(class_dict, PyUnicode_FromString(attr), func_list);
  } else {
    // make sure it is a list
    if (!PyList_Check(func_list)) {
      return 0;
    }
  }

  // add the function to the list
  PyList_Append(func_list, func);
  return 1;
}

PyObject *watch(PyObject *self, PyObject *args) {
  UNUSED(self);
  // check if there are 2 arguments
  if (PyTuple_Size(args) != 2) {
    PyErr_SetString(PyExc_TypeError, "Expected 2 arguments");
    return NULL;
  }

  // parse arguments
  // first argument is a list of tuples
  // second argument is a function
  PyObject *list_of_tuples = PyTuple_GetItem(args, 0);
  PyObject *func = PyTuple_GetItem(args, 1);

  // check the number of arguments supported by the function is the same as the
  // number of tuples
  if (PyFunction_Check(func) == 0) {
    PyErr_SetString(PyExc_TypeError, "Expected a function");
    return NULL;
  }
  PyObject *code = PyFunction_GetCode(func);
  if (code == NULL) {
    PyErr_SetString(PyExc_TypeError, "Expected a function");
    return NULL;
  }
  PyObject *argcount = PyObject_GetAttrString(code, "co_argcount");
  if (argcount == NULL) {
    PyErr_SetString(PyExc_TypeError, "Expected a function");
    return NULL;
  }
  if (PyLong_Check(argcount) == 0) {
    PyErr_SetString(PyExc_TypeError,
                    "Expected a function with an integer argcount");
    return NULL;
  }
  // we only support 4 arguments for now
  // 1st argument is the instance of the class
  // 2nd argument is the attribute name
  // 3rd argument is the old value
  // 4th argument is the new value
  if (PyLong_AsLong(argcount) != 4) {
    PyErr_SetString(PyExc_TypeError, "Expected a function with 4 arguments");
    return NULL;
  }

  // if (PyLong_AsLong(argcount) != PyList_Size(list_of_tuples)) {
  //   char buf[100];
  //   snprintf(buf, 100, "Expected a function with %ld arguments but got %ld",
  //            PyList_Size(list_of_tuples), PyLong_AsLong(argcount));
  //   PyErr_SetString(PyExc_TypeError, buf);
  //   return NULL;
  // }

  // go through the list of tuples, make sure
  // the first element of each tuple is a class
  // and the second element is a string
  for (int i = 0; i < PyList_Size(list_of_tuples); i++) {
    PyObject *tuple = PyList_GetItem(list_of_tuples, i);
    if (!PyTuple_Check(tuple)) {
      PyErr_SetString(PyExc_TypeError, "Expected a tuple");
      return NULL;
    }
    if (PyTuple_Size(tuple) != 2) {
      PyErr_SetString(PyExc_TypeError, "Expected a tuple of size 2");
      return NULL;
    }
    PyObject *class = PyTuple_GetItem(tuple, 0);
    PyObject *attr = PyTuple_GetItem(tuple, 1);
    if (!PyType_Check(class)) {
      PyErr_SetString(PyExc_TypeError, "Expected a class");
      return NULL;
    }
    if (!PyUnicode_Check(attr)) {
      PyErr_SetString(PyExc_TypeError, "Expected a string");
      return NULL;
    }

    // add watch function
    if (!PyWatch_AddWatchedAttribute(class, PyUnicode_AsUTF8(attr), func)) {
      PyErr_SetString(PyExc_RuntimeError, "Failed to add watch function");
      return NULL;
    }
  }

  // clear the error
  PyErr_Clear();
  return func;
}

// This function is called when an attribute is updated
// it will trigger all the watch functions for the attribute
// if error occurs, it will return negative value
int PyWatch_OnAttributeUpdate(PyObject *instance, const char *attr,
                              const PyObject *old_value,
                              const PyObject *new_value) {
  PyObject *class = PyObject_Type(instance);
  if (class == NULL) {
    return -1;
  }
  PyObject *class_dict = PyDict_GetItem(watched_classes, class);
  if (class_dict == NULL) {
    return 0;
  }

  PyObject *func_list = PyDict_GetItem(class_dict, PyUnicode_FromString(attr));
  if (func_list == NULL) {
    return 0;
  }

  // call all the functions in the list
  for (int i = 0; i < PyList_Size(func_list); i++) {
    PyObject *func = PyList_GetItem(func_list, i);
    if (func == NULL) {
      return -1;
    }
    PyObject *args = PyTuple_Pack(4, instance, PyUnicode_FromString(attr),
                                  old_value, new_value);
    if (args == NULL) {
      return -1;
    }
    PyObject *result = PyObject_CallObject(func, args);
    if (result == NULL) {
      return -1;
    }
    Py_DECREF(result);
  }

  return 0;
}