import glob
import os
from distutils.cmd import Command
from distutils.command.install_lib import install_lib as _install_lib

import subprocess as sp
import sys


class RustCleanError(Exception):
    pass


class RustCompileError(Exception):
    pass


class RustDylibNotFound(Exception):
    pass


def execute_streaming_stdout(args, cwd=None):
    print('[python-rust-ext]execute "{}"'.format(' '.join(args)))
    process = sp.Popen(args, stdout=sp.PIPE, stderr=sp.PIPE,
            universal_newlines=True, cwd=cwd)
    for line in iter(process.stdout.readline, ''):
        sys.stdout.write(line)
        sys.stdout.flush()
    for line in iter(process.stderr.readline, ''):
        sys.stderr.write(line)
        sys.stderr.flush()
    process.wait()
    return process


class RustModule:
    def __init__(self, name, cargo_toml_path,
            is_release=False, color_output=True):
        self.name = name
        self.cargo_toml_path = cargo_toml_path
        self.is_release = is_release
        self.is_color_output = color_output

    def get_compile_command(self):
        args = ['cargo', 'build']
        if self.is_release:
            args.append('--release')
        if self.is_color_output:
            args.extend(['--color', 'always'])
        return args

    def get_parent_path(self):
        return os.path.dirname(self.cargo_toml_path)

    def get_dylib_path(self):
        paths = glob.glob(os.path.join(
            self.get_parent_path(),
            'target',
            'release' if self.is_release else 'debug',
            '*{ext}'.format(ext=self.get_ext())
        ))
        if len(paths) == 0:
            raise RustDylibNotFound()
        return paths[0]

    @staticmethod
    def get_ext():
        if sys.platform == 'win32':
            ext = '.dll'
        elif sys.platform == 'darwin':
            ext = '.dylib'
        else:
            ext = '.so'
        return ext


class RustBuildCommand(Command):
    description = "rust build command"
    user_options = [
        ('modules=', None, 'rust modules'),
    ]

    def initialize_options(self):
        self.modules = []
        self.build_temp = None
        self.cargo_clean = False

    def finalize_options(self):
        self.set_undefined_options(
                'build',
                ('build_temp', 'build_temp'),
        )

    def run(self):
        print('[python-rust-ext]modules {}'.format(
            ','.join([m.name for m in self.modules]))
        )
        if self.cargo_clean:
            for module in self.modules:
                self.clean_module(module)

        for module in self.modules:
            self.compile_module(module)

        for module in self.modules:
            self.deploy(module)

    def clean_module(self, module):
        working_directory = module.get_parent_path()
        process = None

        try:
            process = execute_streaming_stdout(
                    ['cargo', 'clean'],
                    cwd=working_directory,
            )
        except Exception as e:  # fixme:!!!!
            raise e

        if process and process.returncode != 0:
            raise RustCleanError()
        return module

    def compile_module(self, module):
        args = module.get_compile_command()
        args = self.extend_command_args(args)

        working_directory = module.get_parent_path()
        process = None

        try:
            process = execute_streaming_stdout(args, cwd=working_directory)
        except sp.CalledProcessError as e:
            # fixme: improve error message
            raise e
        except Exception as e:  # fixme: specify exceptions
            raise e

        if process and process.returncode != 0:
            raise RustCompileError()
        return module

    def deploy(self, module):
        dylib_path = module.get_dylib_path()
        build_ext = self.get_finalized_command('build_ext')  # type: build_ext
        ext_fullpath = build_ext.get_ext_fullpath(module.name)
        self.mkpath(os.path.dirname(ext_fullpath))
        self.copy_file(dylib_path, ext_fullpath)

    def extend_command_args(self, args):
        return args

build_rust = RustBuildCommand


class install_with_rust(_install_lib):
    def build(self):
        _install_lib.build(self)
        self.run_command('build_rust')
