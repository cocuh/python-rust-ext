#![crate_type = "dylib"]
use std::vec;
use std::thread;
use std::sync::{Arc,Mutex};
#[macro_use] extern crate cpython;

use cpython::{PyObject, PyResult, PyInt, Python, PyList, ExtractPyObject, ToPyObject};

py_module_initializer!(math, initmath, PyInit_math, |py, m| {
    try!(m.add(py, "__doc__", "Prime searcher with"));
    try!(m.add(py, "enum_prime", py_fn!(py, enum_prime(num:i32))));
    try!(m.add(py, "sleep_sort", py_fn!(py, sleep_sort(items:PyList))));
    Ok(())
});

fn enum_prime(py: Python, num: i32) -> PyResult<PyObject> {
    println!("hello youjo!");
    Ok(py.None())
}
fn sleep_sort(py:Python, items:PyList)->PyResult<PyList>{
    let mut vec = Vec::new();
    for item in items.iter(py) {
        let x :u32 = try!(item.extract(py));
        print!("{},", x);
        vec.push(x);
    }
    println!("");
    let result = Arc::new(Mutex::new(Vec::new()));
    let threads = vec.into_iter().map(|x|{
        let result = result.clone();
        thread::spawn(move||{
            thread::sleep_ms(x * 100);
            let mut result = result.lock().unwrap();
            result.push(x);
        })
    }).collect::<Vec<_>>();
    
    threads.into_iter().map(|x|{
        x.join();
    }).collect::<Vec<_>>();
    let res = result.lock().unwrap().to_py_object(py);
    Ok(res)
}