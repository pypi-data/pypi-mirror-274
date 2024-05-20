#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <inttypes.h>
#include <stdbool.h>
#include <stdio.h>
#include <sodium.h>
#include <stdlib.h>
#include <string.h>

PyModuleDef secret_mod;
PyType_Spec SecretSpec;

struct SecretRef {
    volatile int readers;
    Py_ssize_t bytes_len;
    char* data;
};

struct SecretModuleState{
    PyTypeObject* Secret;
};

inline static PyTypeObject* borrowSecretCls(PyObject* self) {
    PyTypeObject* cls;

    if (PyType_Check(self)) {
        cls = (PyTypeObject*)self;
    } else {
        cls = Py_TYPE(self);
    }

    PyObject* mod = PyType_GetModuleByDef(cls, &secret_mod);

    struct SecretModuleState* state = (struct SecretModuleState*)
        PyModule_GetState(mod);

    if (state == NULL) {
        return NULL;
    }

    return state->Secret;
}

inline static struct SecretRef* accessInternalStorage(PyObject* self) {
    PyTypeObject* cls = borrowSecretCls(self);

    if (cls == NULL) {
        return NULL;
    }

    return PyObject_GetTypeData(self, cls);
}


int m_clear(PyObject* mod) {
    struct SecretModuleState* state = PyModule_GetState(mod);
    if (state == NULL) {
        return -1;
    }

    Py_CLEAR(state->Secret);
    return 0;
}

int m_traverse(PyObject* mod, visitproc visit, void* arg) {
    struct SecretModuleState* state = PyModule_GetState(mod);
    if (state == NULL) {
        return -1;
    }

    Py_VISIT(state->Secret);
    return 0;
}

int exec_module(PyObject* mod) {
    if (sodium_init() < 0) {
        PyErr_SetString(PyExc_RuntimeError, "Could not load libsodium.");
        return -1;
    }

    PyTypeObject* type = (PyTypeObject*)PyType_FromModuleAndSpec(
        mod,
        &SecretSpec,
        NULL
    );

    if (type == NULL) {
        return -1;
    }

    int result = PyModule_AddType(mod, type);

    if (result == -1) {
        return result;
    }

    struct SecretModuleState* state = PyModule_GetState(mod);

    if (state == NULL) {
        return -1;
    }
    state->Secret = type;

    return 0;
}

PyModuleDef_Slot module_slots[] = {
    {.slot=Py_mod_exec, .value=exec_module},
    {0, NULL},
};

PyModuleDef secret_mod = {
    PyModuleDef_HEAD_INIT,
    .m_name="omniblack.secret",
    .m_doc=PyDoc_STR(
        "A module for handling secret data in a way to reduce leaks."
    ),
    .m_size=sizeof(PyTypeObject*),
    .m_traverse=m_traverse,
    .m_clear=m_clear,
    .m_slots=module_slots,
};

struct SecretRef* unlock_secret(PyObject* self) {
    struct SecretRef* self_slot = accessInternalStorage(self);

    if (self_slot == NULL) {
        return NULL;
    }

    volatile int reader_num = ++self_slot->readers;

    if (reader_num == 1) {
        sodium_mprotect_readonly(self_slot->data);
    }
    return self_slot;
}

void lock_secret(struct SecretRef* self) {
    volatile int readers_left = --self->readers;

    if (readers_left == 0) {
        sodium_mprotect_noaccess(self->data);
    }
}


PyObject *reveal(PyObject* self, PyObject* Py_UNUSED(unsused)) {
    struct SecretRef* secret = unlock_secret(self);

    if (secret == NULL) {
        return NULL;
    }

    PyObject* string = PyUnicode_DecodeUTF8(
        secret->data,
        secret->bytes_len,
        "strict"
    );

    lock_secret(secret);

    if (string == NULL) {
        return NULL;
    }

    return string;
}

PyObject* rich(PyObject* Py_UNUSED(self), PyObject* Py_UNUSED(arg)) {
    return PyUnicode_InternFromString("<[red]Secret Redacted[/]>");
}

PyObject *tp_repr(PyObject* Py_UNUSED(self)) {
    return PyUnicode_InternFromString("<Secret Redacted>");
}

void tp_dealloc(PyObject* self) {
    struct SecretRef* self_slot = accessInternalStorage(self);

    if (self_slot == NULL) {
        return;
    }

    PyObject_GC_UnTrack(self);
    sodium_free(self_slot->data);

    PyTypeObject *tp = Py_TYPE(self);
    tp->tp_free(self);
    Py_DECREF(tp);
}

int tp_traverse(PyObject* self, visitproc visit, void *arg) {
    Py_VISIT(Py_TYPE(self));
    return 0;
}

int tp_clear(PyObject* Py_UNUSED(self)) {
    return 0;
}

Py_ssize_t code_points_len(const char* data, Py_ssize_t bytes_len) {
    Py_ssize_t len = 0;

    // ASCII is only 7 bits so the highest bit will never be set
    // For multibyte unicode codepoints the first byte's high bits
    // will be set to `11`, and the high bits of continuation bytes
    // will be set to `10`. Therefore (*data & 0xC0) will only be
    // 0x80 for continuation bytes, and count all bytes not starting
    // with `10` count all starting bytes and ASCII bytes
    // .. the number of bytes.
    for (int i = 0; i < bytes_len; i += 1) {
        len += (data[i] & 0xC0) != 0x80;
    }

    return len;
}

PyObject* prepare_new_secret(
    PyTypeObject* cls,
    const char* data,
    Py_ssize_t len
) {
    allocfunc tp_alloc = PyType_GetSlot(cls, Py_tp_alloc);
    PyObject* new_self = tp_alloc(cls, 0);

    if (new_self == NULL) {
        return NULL;
    }

    struct SecretRef* new_self_slot = accessInternalStorage(new_self);

    if (new_self_slot == NULL) {
        Py_DECREF(new_self);
        return NULL;
    }

    // The destination to copy to
    // + 1 for the null byte
    char* secret_buffer = sodium_malloc((size_t)len + 1);

    if (secret_buffer == NULL) {
        Py_DECREF(new_self);
        return PyErr_SetFromErrno(PyExc_MemoryError);
    }

    // Copy our secret into the new buffer
    strcpy(secret_buffer, data);

    // Copy the metadata into the new python object
    new_self_slot->bytes_len = len;
    new_self_slot->data = secret_buffer;

    // We are the reader. Setting it one means lock_secret will
    // correctly Re-protect the memory.
    new_self_slot->readers = 1;

    // Re-protect the new and old secret
    lock_secret(new_self_slot);

    return new_self;
}


PyObject* tp_new(PyTypeObject *subtype, PyObject *args, PyObject *kwds) {
    // Parse the args we were passed
    static char* names[] = {"", NULL};
    PyObject* object; // Borrowed reference
    bool parse_result = PyArg_ParseTupleAndKeywords(
        args,
        kwds,
        "O:Secret",
        names,
        &object
    );

    if (!parse_result) {
        return NULL;
    }

    PyTypeObject* cls = borrowSecretCls((PyObject*)subtype);

    // Coerce our argument to a python `str`
    // this is the same as calling `str` in object
    PyObject* string = PyObject_Str(object);
    if (string == NULL) {
        return NULL;
    }

    // Get the underlying character data in utf-8
    // this data shares the lifetime of `string`
    // NOTE: we can't zero this memory as it is controlled by python
    Py_ssize_t len;
    const char* data_buffer = PyUnicode_AsUTF8AndSize(string, &len);

    if (data_buffer == NULL) {
        Py_DECREF(string);
        return NULL;
    }

    PyObject* self = prepare_new_secret(cls, data_buffer, len);
    Py_DECREF(string);

    return self;
}

PyObject* copy(PyObject* self, PyObject* Py_UNUSED(arg)) {
    PyTypeObject* subtype = Py_TYPE(self);
    // Get the data to copy
    struct SecretRef* old_secret = unlock_secret(self);

    PyObject* new_self = prepare_new_secret(
        subtype,
        old_secret->data,
        old_secret->bytes_len
    );

    lock_secret(old_secret);
    return new_self;
}

PyObject* verify_password_against(PyObject* self, PyObject* args) {
    PyTypeObject* cls = borrowSecretCls(self);
    if (cls == NULL) {
        return NULL;
    }

    PyObject* other;
    if (!PyArg_ParseTuple(args, "O!:verifyPasswordAgainst", cls, &other)) {
        return NULL;
    }

    struct SecretRef* self_secret = unlock_secret(self);

    if (self_secret == NULL) {
        return NULL;
    }

    struct SecretRef* other_secret = unlock_secret(other);

    if (other_secret == NULL) {
        lock_secret(self_secret);
        return NULL;
    }

    PyThreadState* _save = NULL;

    if (self_secret->bytes_len >= 2000) {
        Py_UNBLOCK_THREADS;
    }

    const int verify_result = crypto_pwhash_str_verify(
        other_secret->data,
        self_secret->data,
        (unsigned long long)self_secret->bytes_len
    );

    if (self_secret->bytes_len >= 2000) {
        Py_BLOCK_THREADS;
    }

    lock_secret(self_secret);
    lock_secret(other_secret);

    return PyBool_FromLong(!verify_result);
}

PyObject* hash(PyObject* self, PyObject* Py_UNUSED(args)) {
    struct SecretRef* secret = unlock_secret(self);
    if (secret == NULL) {
        return NULL;
    }

    PyTypeObject* cls = borrowSecretCls(self);

    PyThreadState* _save = NULL;
    if (secret->bytes_len >= 2000) {
        Py_UNBLOCK_THREADS;
    }

    char out[crypto_pwhash_STRBYTES] = {};

    unsigned long long len = (unsigned long long)secret->bytes_len;
    int hash_result = crypto_pwhash_str(
        (char*)&out,
        secret->data,
        len,
        crypto_pwhash_OPSLIMIT_INTERACTIVE,
        crypto_pwhash_MEMLIMIT_INTERACTIVE
    );

    if (secret->bytes_len >= 2000) {
        Py_BLOCK_THREADS;
    }

    // We no longer need the secret
    lock_secret(secret);

    if (hash_result) {
        PyErr_SetString(PyExc_RuntimeError, "Could not hash password.");
        return NULL;
    }

    Py_ssize_t out_len = (Py_ssize_t)strlen(out);
    PyObject* hashed = prepare_new_secret(cls, out, out_len);

    sodium_memzero(out, crypto_pwhash_STRBYTES);

    return hashed;
}

PyObject* need_rehash(PyObject* self, PyObject* Py_UNUSED(arg)) {
    struct SecretRef* secret = unlock_secret(self);

    int check_result = crypto_pwhash_str_needs_rehash(
        secret->data,
        crypto_pwhash_OPSLIMIT_INTERACTIVE,
        crypto_pwhash_MEMLIMIT_INTERACTIVE
    );

    lock_secret(secret);

    return PyBool_FromLong(check_result);
}

PyObject* random_secret(PyTypeObject* cls, PyObject* args) {
    Py_ssize_t py_size;
    if (!PyArg_ParseTuple(args, "n:random_secret", &py_size)) {
        return NULL;
    }


    // If we are allocating and encoding a large chunk
    // let's release the GIL.
    // This may not be a good idea as somepoint we
    // should check to see if the cost of allocating and encoding
    // exceeds the cost of releasing and aquiring the GIL.
    PyThreadState* _save = NULL;
    if (py_size >= 2000) {
        Py_UNBLOCK_THREADS;
    }

    // Calculate the number of bytes needed
    // to get a base64 string of N-characters
    size_t num_of_bytes = (size_t)py_size / 4 * 3;

    unsigned char* new_data = sodium_malloc(num_of_bytes);

    if (new_data == NULL) {
        return PyErr_NoMemory();
    }

    randombytes_buf(new_data, num_of_bytes);

    size_t b64_maxlen = sodium_base64_encoded_len(
        num_of_bytes,
        sodium_base64_VARIANT_URLSAFE
    );

    char* b64_data = sodium_malloc(b64_maxlen);

    if (b64_data == NULL) {
        sodium_free(new_data);
        return PyErr_NoMemory();
    }

    sodium_bin2base64(
        b64_data,
        b64_maxlen,
        new_data,
        num_of_bytes,
        sodium_base64_VARIANT_URLSAFE
    );

    sodium_free(new_data);

    if (py_size >= 2000) {
        Py_BLOCK_THREADS;
    }

    PyObject* result = prepare_new_secret(
        cls,
        b64_data,
        // b64_maxlen include the trailling NULL
        // prepare_new_secret expects length to not include
        // the NULL
        (Py_ssize_t)b64_maxlen - 1
    );

    sodium_free(b64_data);

    return result;
}

Py_ssize_t sq_length(PyObject* self) {
    struct SecretRef* secret = unlock_secret(self);

    if (secret == NULL) {
        return -1;
    }

    Py_ssize_t len = code_points_len(secret->data, secret->bytes_len);
    lock_secret(secret);
    return len;
}

PyMethodDef methods[] = {
    {
        .ml_name="__copy__",
        .ml_meth=(PyCFunction)copy,
        .ml_flags=METH_NOARGS,
        .ml_doc=PyDoc_STR("Return a copy of the secret."),
    },
    {
        .ml_name="__deepcopy__",
        .ml_meth=(PyCFunction)copy,
        .ml_flags=METH_O,
        .ml_doc=PyDoc_STR("Return a copy of the secret."),
    },
    {
        .ml_name="__rich__",
        .ml_meth=(PyCFunction)rich,
        .ml_flags=METH_NOARGS,
        .ml_doc=PyDoc_STR("Return a string `rich` can pretty print.")
    },
    {
        .ml_name="reveal",
        .ml_meth=(PyCFunction)reveal,
        .ml_flags=METH_NOARGS,
        .ml_doc=PyDoc_STR("Return the secret in the form of a string.")
    },
    {
        .ml_name="verify_password_against",
        .ml_meth=(PyCFunction)verify_password_against,
        .ml_flags=METH_VARARGS,
        .ml_doc=PyDoc_STR("Check if this password matches `hashedPassword`."),
    },
    {
        .ml_name="hash",
        .ml_meth=(PyCFunction)hash,
        .ml_flags=METH_NOARGS,
        .ml_doc=PyDoc_STR("Return the hash of this secret."),
    },
    {
        .ml_name="need_rehash",
        .ml_meth=(PyCFunction)need_rehash,
        .ml_flags=METH_NOARGS,
        .ml_doc=PyDoc_STR(
            "Check if this hash need to be recreated. \n"
            "NOTE: this always returns true if `self` is not in libsodium's "
            "stored password format."
        ),
    },
    {
        .ml_name="random_secret",
        .ml_meth=(PyCFunction)random_secret,
        .ml_flags=METH_VARARGS | METH_CLASS,
        .ml_doc=PyDoc_STR("Return a new random url safe base64 string."),
    },
    {.ml_name=NULL},
};

PyType_Slot type_slots[] = {
    {
        .slot=Py_tp_doc,
        .pfunc=PyDoc_STR("A secret stored safely in memory."),
    },
    {
        .slot=Py_tp_repr,
        .pfunc=tp_repr,
    },
    {
        .slot=Py_tp_new,
        .pfunc=tp_new,
    },
    {
        .slot=Py_tp_methods,
        .pfunc=methods,
    },
    {
        .slot=Py_tp_dealloc,
        .pfunc=tp_dealloc,
    },
    {
        .slot=Py_tp_traverse,
        .pfunc=tp_traverse,
    },
    {
        .slot=Py_tp_clear,
        .pfunc=tp_clear,
    },
    {
        .slot=Py_sq_length,
        .pfunc=sq_length,
    },
    {0, 0}
};

PyType_Spec SecretSpec = {
    .name="omniblack.secret.Secret",
    .basicsize=-(Py_ssize_t)sizeof(struct SecretRef),
    .flags=Py_TPFLAGS_IMMUTABLETYPE | Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,
    .slots=type_slots,
};


PyMODINIT_FUNC PyInit_secret(void) {
    return PyModuleDef_Init(&secret_mod);
}
