from setuptools import setup
from rust_ext import build_rust, install_with_rust, RustModule

rust_modules = [
    RustModule(
            'helloyoujo',
            'helloyoujo/Cargo.toml',
    )
]

setup(
        name='hello-youjo',
        version='0.0.1',
        cmdclass={
            'build_rust': build_rust,
            'install_lib': install_with_rust,
        },
        options={
            'build_rust': {
                'modules': rust_modules,
            }
        }
)