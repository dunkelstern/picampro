#include <stdint.h>
#include <stdbool.h>
#include <math.h>

#include <Python.h>
#include <bcm_host.h>

typedef struct {
    // Python object
    PyObject base;

    // Internal attributes
    int scaled_height;
    int scaled_width;
    VC_RECT_T roi;
    uint8_t *capture_buffer;
    bool capture_ok;

    // DispmanX state
    DISPMANX_DISPLAY_HANDLE_T display;
    DISPMANX_MODEINFO_T display_info;
    DISPMANX_RESOURCE_HANDLE_T screen_resource;
} ScreenHistogram;

static PyTypeObject ScreenHistogram_type;
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

void ScreenHistogram_clear_capture(ScreenHistogram *self) {
    if (self->capture_buffer != NULL) {
        free(self->capture_buffer);
        self->capture_buffer = NULL;
    }
    if (self->screen_resource != 0) {
        vc_dispmanx_resource_delete(self->screen_resource);
        self->screen_resource = 0;
    }
    self->capture_ok = false;
}

PyObject *ScreenHistogram_new(PyTypeObject *subtype, PyObject *args, PyObject *kwargs) {
    ScreenHistogram *self = (ScreenHistogram *)ScreenHistogram_type.tp_alloc(subtype, 0);
    if (!self) {
        return NULL;
    }
    return (PyObject *)self;
}

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

    self->roi.x = 0;
    self->roi.y = 0;
    self->roi.width = self->display_info.width;
    self->roi.height = self->display_info.height;
    self->scaled_width = self->display_info.width;
    self->scaled_height = self->display_info.height;
    self->capture_ok = false;

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
    ScreenHistogram_clear_capture(self);
    vc_dispmanx_display_close(self->display);
    bcm_host_deinit();

    Py_TYPE(obj)->tp_free((PyObject*)self);
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
    uint32_t stride = self->scaled_width * 4;
    stride += (stride % 64 > 0) ? 64 - (stride % 64) : 0; // make it multiple of 64 bytes

    if (self->capture_buffer == NULL) {
        self->capture_buffer = calloc(stride * self->scaled_height, 1);
    }
    if (self->screen_resource == 0) {
        uint32_t image_handle;
        self->screen_resource = vc_dispmanx_resource_create(
            VC_IMAGE_RGBA32,
            self->scaled_width,
            self->scaled_height,
            &image_handle
        );
    }

    int failed = vc_dispmanx_snapshot(self->display, self->screen_resource, DISPMANX_SNAPSHOT_FILL);
    if (failed) {
        self->capture_ok = false;
        return Py_None;
    }

    VC_RECT_T rect;
    vc_dispmanx_rect_set(&rect, 0, 0, self->scaled_width, self->scaled_height);

    failed = vc_dispmanx_resource_read_data(
        self->screen_resource,
        &rect,
        self->capture_buffer,
        stride
    );
    if (failed) {
        self->capture_ok = false;
        return Py_None;
    }

    self->capture_ok = true;
    return Py_None;
}
PyObject *build_histogram(ScreenHistogram *self, float *pixel_sum, uint8_t num_bins) {
    PyObject* histogram = PyList_New(num_bins);

    // find max
    float max = 0;
    for(uint32_t i = 0; i < num_bins; i++) {
        if (pixel_sum[i] > max) {
            max = pixel_sum[i];
        }
    }

    for(uint32_t i = 0; i < num_bins; i++) {
        pixel_sum[i] = (logf(pixel_sum[i] + 1) / logf(max + 1) * 100.0);
    }

    // find min
    float min = 200.0;
    for(uint32_t i = 0; i < num_bins; i++) {
        if ((pixel_sum[i] > 10) && (pixel_sum[i] < min)) {
            min = pixel_sum[i];
        }
    }
    min -= 10;

    // make variation more visible
    for(uint32_t i = 0; i < num_bins; i++) {
        if (pixel_sum[i] > min) {
            pixel_sum[i] = (pixel_sum[i] - min) * (100.0 / (100.0 - min));
        }
    }

    for(uint8_t i = 0; i < num_bins; i++) {
        int result = PyList_SetItem(
            histogram,
            i,
            PyLong_FromUnsignedLong((int)pixel_sum[i])
        );
        if (result < 0) {
            // Exception already set by SetItem call
            return Py_None;
        }
    }

    return histogram;
}

PyObject *ScreenHistogram_fast_luminance(PyObject *obj, PyObject *args, PyObject *kwargs) {
    ScreenHistogram *self = (ScreenHistogram *)obj;
    uint32_t num_bins = 64;

    PyArg_ParseTupleAndKeywords(args, kwargs, "|i", (char *[]){"num_bins", NULL}, &num_bins);

    uint32_t stride = self->scaled_width * 4;
    stride += (stride % 64 > 0) ? 64 - (stride % 64) : 0; // make it multiple of 64 bytes

    float pixel_sum[num_bins + 1];
    memset(&pixel_sum, 0, sizeof(float) * num_bins);
    uint8_t denominator = ceilf(255.0 / (float)num_bins);

    // count pixels
    for(uint32_t y = 0; y < self->roi.height; y++) {
        for(uint32_t x = 0; x < self->roi.width; x++) {
            uint8_t red = self->capture_buffer[y * stride + x * 4];
            uint8_t green = self->capture_buffer[y * stride + x * 4 + 1];
            uint8_t blue = self->capture_buffer[y * stride + x * 4 + 2];
            uint16_t lum = (red + red + red + blue + green + green + green + green) >> 3;
            uint8_t idx = lum / denominator;
            pixel_sum[idx]++;
        }
    }

    return build_histogram(self, pixel_sum, num_bins);
}

// reverses the rgb gamma
#define inverseGamma(t) (((t) <= 0.0404482362771076) ? ((t)/12.92) : powf(((t) + 0.055)/1.055, 2.4))

//CIE L*a*b* f function (used to convert XYZ to L*a*b*)  http://en.wikipedia.org/wiki/Lab_color_space
#define LABF(t) ((t >= 8.85645167903563082e-3) ? powf(t,0.333333333333333) : (841.0/108.0)*(t) + (4.0/29.0))


uint8_t luminance(uint8_t ri, uint8_t gi, uint8_t bi) {
    float y;
    float r = ri/255.0;
    float g = gi/255.0;
    float b = bi/255.0;

    r = inverseGamma(r);
    g = inverseGamma(g);
    b = inverseGamma(b);

    y = 0.2125862307855955516 * r + 0.7151703037034108499 * g + 0.07220049864333622685 * b;
    y = LABF(y);

    return (uint8_t)((116.0 * y - 16.0) * 2.55);
}

PyObject *ScreenHistogram_luminance(PyObject *obj, PyObject *args, PyObject *kwargs) {
    ScreenHistogram *self = (ScreenHistogram *)obj;
    uint32_t num_bins = 64;

    PyArg_ParseTupleAndKeywords(args, kwargs, "|i", (char *[]){"num_bins", NULL}, &num_bins);

    uint32_t stride = self->scaled_width * 4;
    stride += (stride % 64 > 0) ? 64 - (stride % 64) : 0; // make it multiple of 64 bytes

    float pixel_sum[num_bins + 1];
    memset(&pixel_sum, 0, sizeof(float) * num_bins);
    uint8_t denominator = ceilf(255.0 / (float)num_bins);

    // count pixels
    for(uint32_t y = 0; y < self->roi.height; y++) {
        for(uint32_t x = 0; x < self->roi.width; x++) {
            uint8_t red = self->capture_buffer[y * stride + x * 4];
            uint8_t green = self->capture_buffer[y * stride + x * 4 + 1];
            uint8_t blue = self->capture_buffer[y * stride + x * 4 + 2];
            pixel_sum[luminance(red, green, blue) / denominator]++;
        }
    }

    return build_histogram(self, pixel_sum, num_bins);
}

PyObject *ScreenHistogram_red(PyObject *obj, PyObject *args, PyObject *kwargs) {
    ScreenHistogram *self = (ScreenHistogram *)obj;
    uint32_t num_bins = 64;

    PyArg_ParseTupleAndKeywords(args, kwargs, "|i", (char *[]){"num_bins", NULL}, &num_bins);

    uint32_t stride = self->scaled_width * 4;
    stride += (stride % 64 > 0) ? 64 - (stride % 64) : 0; // make it multiple of 64 bytes

    float pixel_sum[num_bins + 1];
    memset(&pixel_sum, 0, sizeof(float) * num_bins + 1);
    uint8_t denominator = ceilf(255.0 / (float)num_bins);

    // count pixels
    for(uint32_t y = 0; y < self->roi.height; y++) {
        for(uint32_t x = 0; x < self->roi.width; x++) {
            uint8_t red = self->capture_buffer[y * stride + x * 4];
            pixel_sum[red / denominator]++;
        }
    }

    return build_histogram(self, pixel_sum, num_bins);
}

PyObject *ScreenHistogram_green(PyObject *obj, PyObject *args, PyObject *kwargs) {
    ScreenHistogram *self = (ScreenHistogram *)obj;
    uint32_t num_bins = 64;

    PyArg_ParseTupleAndKeywords(args, kwargs, "|i", (char *[]){"num_bins", NULL}, &num_bins);

    uint32_t stride = self->scaled_width * 4;
    stride += (stride % 64 > 0) ? 64 - (stride % 64) : 0; // make it multiple of 64 bytes

    float pixel_sum[num_bins + 1];
    memset(&pixel_sum, 0, sizeof(float) * num_bins + 1);
    uint8_t denominator = ceilf(255.0 / (float)num_bins);

    // count pixels
    for(uint32_t y = 0; y < self->roi.height; y++) {
        for(uint32_t x = 0; x < self->roi.width; x++) {
            uint8_t green = self->capture_buffer[y * stride + x * 4 + 1];
            pixel_sum[green / denominator]++;
        }
    }

    return build_histogram(self, pixel_sum, num_bins);
}

PyObject *ScreenHistogram_blue(PyObject *obj, PyObject *args, PyObject *kwargs) {
    ScreenHistogram *self = (ScreenHistogram *)obj;
    uint32_t num_bins = 64;

    PyArg_ParseTupleAndKeywords(args, kwargs, "|i", (char *[]){"num_bins", NULL}, &num_bins);

    uint32_t stride = self->scaled_width * 4;
    stride += (stride % 64 > 0) ? 64 - (stride % 64) : 0; // make it multiple of 64 bytes

    float pixel_sum[num_bins + 1];
    memset(&pixel_sum, 0, sizeof(float) * num_bins + 1);
    uint8_t denominator = ceilf(255.0 / (float)num_bins);

    // count pixels
    for(uint32_t y = 0; y < self->roi.height; y++) {
        for(uint32_t x = 0; x < self->roi.width; x++) {
            uint8_t blue = self->capture_buffer[y * stride + x * 4 + 2];
            pixel_sum[blue / denominator]++;
        }
    }

    return build_histogram(self, pixel_sum, num_bins);
}

struct PyMethodDef methods[] = {
    {"capture",                  (PyCFunction)ScreenHistogram_capture,   METH_NOARGS,  "Capture screen into internal buffer"},
    {"fast_luminance_histogram", (PyCFunction)ScreenHistogram_fast_luminance, METH_VARARGS | METH_KEYWORDS, "Calculate faster luminance histogram from captured buffer\n\n:param int num_bins: Number of bins to use, has to be power of two\n:returns: List with ``num_bins`` integers from 0-100"},
    {"luminance_histogram",      (PyCFunction)ScreenHistogram_luminance, METH_VARARGS | METH_KEYWORDS, "Calculate luminance histogram from captured buffer\n\n:param int num_bins: Number of bins to use, has to be power of two\n:returns: List with ``num_bins`` integers from 0-100"},
    {"red_histogram",            (PyCFunction)ScreenHistogram_red,       METH_VARARGS | METH_KEYWORDS, "Calculate red intensity histogram from captured buffer\n\n:param int num_bins: Number of bins to use, has to be power of two\n:returns: List with ``num_bins`` integers from 0-100"},
    {"green_histogram",          (PyCFunction)ScreenHistogram_green,     METH_VARARGS | METH_KEYWORDS, "Calculate green intensity histogram from captured buffer\n\n:param int num_bins: Number of bins to use, has to be power of two\n:returns: List with ``num_bins`` integers from 0-100"},
    {"blue_histogram",           (PyCFunction)ScreenHistogram_blue,      METH_VARARGS | METH_KEYWORDS, "Calculate blue intensity histogram from captured buffer\n\n:param int num_bins: Number of bins to use, has to be power of two\n:returns: List with ``num_bins`` integers from 0-100"},
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
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "rpi_display_histogram.ScreenHistogram",
    .tp_doc       = "Screen Capture Histogram generator",
    .tp_basicsize = sizeof(ScreenHistogram),
    .tp_itemsize  = 0,
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_methods   = methods,
    .tp_getset    = getters_setters,
    .tp_new       = ScreenHistogram_new,
    .tp_init      = ScreenHistogram_init,
    .tp_dealloc   = (destructor) ScreenHistogram_dealloc
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    .m_name = "rpi_display_histogram",
    .m_doc  = "Captures screenshots and returns a histogram of the contents",
    .m_size = -1
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
