# python-rust-ext
Python distutils helper for Rust Extension [![Build Status](https://travis-ci.org/cocuh/python-rust-ext.svg?branch=master)](https://travis-ci.org/cocuh/python-rust-ext)

# install
```
$ pip install git+https://github.com/cocuh/python-rust-ext
```

# how to use it
write setup.py like follows.

```python
from setuptools import setup
from rust_ext import build_rust, install_with_rust, RustModule

rust_modules = [
    RustModule(
            'youjo.hello',      # module name
            'hello/Cargo.toml', # module's cargo file(relative path from setup.py)
    ),
]

setup(
        name='rust-ext-example',
        version='0.0.1',
        cmdclass={
            'build_rust': build_rust,
            'install_lib': install_with_rust,
        }, # required
        options={
            'build_rust': {
                'modules': rust_modules,
            }
        }, # required
        zip_safe=False, # required
)
```

use it!

```
import youjo.hello

youjo.hello.run()
```


# TODO
- [ ] documentation

# relate works
- [rust-cpython](https://github.com/dgrunwald/rust-cpython)
    - Rust library of rust-python bridge.
    - You should use it, unless you love writing python c extension on rust. See example.
- [rust-python-ext](https://github.com/novocaine/rust-python-ext/)
    - Pioneer of Python distutils helper.
