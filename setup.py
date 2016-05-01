from setuptools import setup


setup(
    name='python-rust-ext',
    version='0.0.1',
    author='cocuh',
    author_email='cocuh.kk@gmail.com',
    packages=['rust_ext'],
    test_suite='nose.collector',
    tests_require=['nose'],
)