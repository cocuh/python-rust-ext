#![crate_type = "dylib"]
#[macro_use]
extern crate cpython;

use cpython::{PyObject, PyResult, PyModule, Python, PyTuple, PyDict};

py_module_initializer!(hello, inithello, PyInit_hello, |py, m| {
    try!(m.add(py, "__doc__", "This module is youjo hello module."));
    try!(m.add(py, "run", py_fn!(py, run(*args, **kwargs))));
    try!(m.add(py, "val", py_fn!(py, val())));
    Ok(())
});

fn run(py: Python, args: &PyTuple, kwargs: &PyDict) -> PyResult<PyObject> {
    println!("hello youjo!");
    for arg in args.iter(py) {
        println!("Rust got {}", arg);
    }
    Ok(py.None())
}

fn val(_: Python) -> PyResult<i32> {
    Ok(42)
}
