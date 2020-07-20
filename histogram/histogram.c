#include <stdint.h>
#include <stdbool.h>

#include <Python.h>
#include <bcm_host.h>

typedef struct {
    // Python object
    PyObject base;

    // Internal attributes
    int scaled_height;
    int scaled_width;
    VC_RECT_T roi;
    bool capture_ready;
    void *capture_buffer;

    // DispmanX state
    DISPMANX_DISPLAY_HANDLE_T display;
    DISPMANX_MODEINFO_T display_info;
    DISPMANX_RESOURCE_HANDLE_T screen_resource;
    VC_RECT_T rect;
} ScreenHistogram;

int populate_module(PyObject *module);

// static PyObject *captureHistogram(PyObject *self, PyObject *args) {
//     PyObject* pyList = PyList_New(0);

//     /*
//             hr = PyList_Append(pyList, Py_BuildValue("s", pValue));
//             if (FAILED(hr)) {
//                 return pyList;
//             }
//     */

//     return pyList;
// }

int ScreenHistogram_init(PyObject *obj, PyObject *args, PyObject *kwargs) {
    ScreenHistogram *self = (ScreenHistogram *)obj;

    // Initialize API
    bcm_host_init();

    // Open display
    self->display = vc_dispmanx_display_open(0);
    if (!self->display) {
        PyErr_SetString(PyExc_RuntimeError, "vc_dispmanx_display_open failed! Make sure to have hdmi_force_hotplug=1 setting in /boot/config.txt or a display connected");
        return -1;
    }

    // get display info
    int ret = vc_dispmanx_display_get_info(self->display, &(self->display_info));
    if (ret) {
        PyErr_SetString(PyExc_RuntimeError, "vc_dispmanx_display_get_info failed!");
        return -1;
    }

    return 0;
}

static void ScreenHistogram_dealloc(PyObject *obj) {
    if (obj == NULL) {
        return;
    }

    // Fetch state, if we have none free was called on an un-initialized object
    ScreenHistogram *self = (ScreenHistogram *)obj;

    // Exceptions
    // Py_XDECREF(state->DispmanXInitializationError);

    // DispmanX
    vc_dispmanx_display_close(self->display);
    bcm_host_deinit();

    Py_TYPE(obj)->tp_free((PyObject*)self);
}

void ScreenHistogram_clear_capture(ScreenHistogram *self) {
    self->capture_ready = 0;
}

PyObject *ScreenHistogram_get_scaled_width(PyObject *obj, void *context) {
    ScreenHistogram *self = (ScreenHistogram *)obj;
    return PyLong_FromLong(self->scaled_width);
}

int ScreenHistogram_set_scaled_width(PyObject *obj, PyObject *value, void *context) {
    ScreenHistogram *self = (ScreenHistogram *)obj;
    if (!PyLong_Check(value)) {
        PyErr_SetString(PyExc_ValueError, "Parameter has to be a integer number");
        return -1;
    }
    self->scaled_width = PyLong_AsLong(value);
    ScreenHistogram_clear_capture(self);
    return 0;
}

PyObject *ScreenHistogram_get_scaled_height(PyObject *obj, void *context) {
    ScreenHistogram *self = (ScreenHistogram *)obj;
    return PyLong_FromLong(self->scaled_height);
}

int ScreenHistogram_set_scaled_height(PyObject *obj, PyObject *value, void *context) {
    ScreenHistogram *self = (ScreenHistogram *)obj;
    if (!PyLong_Check(value)) {
        PyErr_SetString(PyExc_ValueError, "Parameter has to be a integer number");
        return -1;
    }
    self->scaled_height = PyLong_AsLong(value);
    ScreenHistogram_clear_capture(self);
    return 0;
}

PyObject *ScreenHistogram_get_screen_width(PyObject *obj, void *context) {
    ScreenHistogram *self = (ScreenHistogram *)obj;
    return PyLong_FromLong(self->display_info.width);
}

PyObject *ScreenHistogram_get_screen_height(PyObject *obj, void *context) {
    ScreenHistogram *self = (ScreenHistogram *)obj;
    return PyLong_FromLong(self->display_info.height);
}

PyObject *ScreenHistogram_get_roi(PyObject *obj, void *context) {
    ScreenHistogram *self = (ScreenHistogram *)obj;
    PyObject *tuple = PyTuple_New(4);
    PyTuple_SetItem(tuple, 0, PyLong_FromLong(self->roi.x));
    PyTuple_SetItem(tuple, 1, PyLong_FromLong(self->roi.y));
    PyTuple_SetItem(tuple, 2, PyLong_FromLong(self->roi.width));
    PyTuple_SetItem(tuple, 3, PyLong_FromLong(self->roi.height));
    return tuple;
}

int ScreenHistogram_set_roi(PyObject *obj, PyObject *value, void *context) {
    ScreenHistogram *self = (ScreenHistogram *)obj;
    if (!PyTuple_Check(value)) {
        PyErr_SetString(PyExc_ValueError, "Parameter has to be a 4-tuple of integer numbers");
        return -1;
    }
    for (int i = 0; i < 4; i++) {
        PyObject *item = PyTuple_GetItem(value, i);
        if (!PyLong_Check(item)) {
            PyErr_SetString(PyExc_ValueError, "Parameter has to be a 4-tuple of integer numbers");
            return -1;
        }
    }
    self->roi.x = PyLong_AsLong(PyTuple_GetItem(value, 0));
    self->roi.y = PyLong_AsLong(PyTuple_GetItem(value, 1));
    self->roi.width = PyLong_AsLong(PyTuple_GetItem(value, 2));
    self->roi.height = PyLong_AsLong(PyTuple_GetItem(value, 3));
    ScreenHistogram_clear_capture(self);
    return 0;
}

PyObject *ScreenHistogram_capture(PyObject *obj, PyObject *nul) {
    ScreenHistogram *self = (ScreenHistogram *)obj;
    return Py_None;
}

PyObject *ScreenHistogram_luminance(PyObject *obj, PyObject *kwargs) {
    ScreenHistogram *self = (ScreenHistogram *)obj;
    return Py_None;
}

PyObject *ScreenHistogram_red(PyObject *obj, PyObject *kwargs) {
    ScreenHistogram *self = (ScreenHistogram *)obj;
    return Py_None;
}

PyObject *ScreenHistogram_green(PyObject *obj, PyObject *kwargs) {
    ScreenHistogram *self = (ScreenHistogram *)obj;
    return Py_None;
}

PyObject *ScreenHistogram_blue(PyObject *obj, PyObject *kwargs) {
    ScreenHistogram *self = (ScreenHistogram *)obj;
    return Py_None;
}

struct PyMethodDef methods[] = {
    {"capture",             ScreenHistogram_capture,   METH_NOARGS,  "Capture screen into internal buffer"},
    {"luminance_histogram", ScreenHistogram_luminance, METH_KEYWORDS, "Calculate luminance histogram from captured buffer\n\n:param int num_bins: Number of bins to use, has to be power of two\n:returns: List with ``num_bins`` integers from 0-255"},
    {"red_histogram",       ScreenHistogram_red,       METH_KEYWORDS, "Calculate red intensity histogram from captured buffer\n\n:param int num_bins: Number of bins to use, has to be power of two\n:returns: List with ``num_bins`` integers from 0-255"},
    {"green_histogram",     ScreenHistogram_green,     METH_KEYWORDS, "Calculate green intensity histogram from captured buffer\n\n:param int num_bins: Number of bins to use, has to be power of two\n:returns: List with ``num_bins`` integers from 0-255"},
    {"blue_histogram",      ScreenHistogram_blue,      METH_KEYWORDS, "Calculate blue intensity histogram from captured buffer\n\n:param int num_bins: Number of bins to use, has to be power of two\n:returns: List with ``num_bins`` integers from 0-255"},
    {NULL, NULL, 0, NULL}
};

struct PyGetSetDef getters_setters[] = {
    {"scaled_width",  ScreenHistogram_get_scaled_width,  ScreenHistogram_set_scaled_width,  "Internal capture buffer width", NULL},
    {"scaled_height", ScreenHistogram_get_scaled_height, ScreenHistogram_set_scaled_height, "Internal capture buffer height", NULL},
    {"screen_width",  ScreenHistogram_get_screen_width,  NULL,                              "Screen width", NULL},
    {"screen_height", ScreenHistogram_get_screen_height, NULL,                              "Screen height", NULL},
    {"roi",           ScreenHistogram_get_roi,           ScreenHistogram_set_roi,           "Region of interest for screen capture", NULL},
    {NULL, NULL, NULL, NULL, NULL}
};

static PyTypeObject ScreenHistogram_type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "rpi_display_histogram.ScreenHistogram",     /* tp_name */
    sizeof(ScreenHistogram),                    /* tp_basicsize */
    0,                                          /* tp_itemsize */
    (destructor) ScreenHistogram_dealloc,       /* tp_dealloc */
    NULL,                                       /* tp_print */
    NULL,                                       /* tp_getattr */
    NULL,                                       /* tp_setattr */
    NULL,                                       /* tp_reserved */
    NULL,                                       /* tp_repr */
    NULL,                                       /* tp_as_number */
    NULL,                                       /* tp_as_sequence */
    NULL,                                       /* tp_as_mapping */
    NULL,                                       /* tp_hash */
    NULL,                                       /* tp_call */
    NULL,                                       /* tp_str */
    NULL,                                       /* tp_getattro */
    NULL,                                       /* tp_setattro */
    NULL,                                       /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                         /* tp_flags */
    "Screen Capture Histogram generator",       /* tp_doc */
    NULL,                                       /* tp_traverse */
    NULL,                                       /* tp_clear */
    NULL,                                       /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    NULL,                                       /* tp_iter */
    NULL,                                       /* tp_iternext */
    methods,                                    /* tp_methods */
    NULL,                                       /* tp_members */
    getters_setters,                            /* tp_getset */
    NULL,                                       /* tp_base */
    NULL,                                       /* tp_dict */
    NULL,                                       /* tp_descr_get */
    NULL,                                       /* tp_descr_set */
    0,                                          /* tp_dictoffset */
    ScreenHistogram_init,                       /* tp_init */
    NULL,                                       /* tp_alloc */
    NULL,                                       /* tp_new */
    NULL,                                       /* tp_free */
    NULL,                                       /* tp_is_gc */
    NULL,                                       /* tp_bases */
    NULL,                                       /* tp_mro */
    NULL,                                       /* tp_cache */
    NULL,                                       /* tp_subclasses */
    NULL,                                       /* tp_weaklist */
    NULL,                                       /* tp_del */
    0,                                          /* tp_version_tag */
    NULL                                        /* tp_finalize */
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "rpi_display_histogram",
    "Captures screenshots and returns a histogram of the contents",
    0,
    NULL,        /* m_methods */
    NULL,        /* m_slots */
    NULL,        /* traverse */
    NULL,        /* clear */
    NULL         /* free */
};

PyMODINIT_FUNC PyInit_rpi_display_histogram(void) {
    if (PyType_Ready(&ScreenHistogram_type) < 0) {
        return NULL;
    }

    PyObject *module = PyModule_Create(&moduledef);
    if (module == NULL) {
        return NULL;
    }

    Py_INCREF(&ScreenHistogram_type);
    if (PyModule_AddObject(module, "ScreenHistogram", (PyObject *)&ScreenHistogram_type) < 0) {
        Py_DECREF(&ScreenHistogram_type);
        Py_DECREF(module);
        return NULL;
    }

    return module;
}
