import glob
import os
from distutils.cmd import Command
from distutils.command.build_ext import build_ext
from distutils.command.install_lib import install_lib as _install_lib

import subprocess as sp
import sys


def execute_streaming_stdout(args, cwd=None):
    process = sp.Popen(args, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True, cwd=cwd)
    for line in iter(process.stdout.readline, ''):
        sys.stdout.write(line)
        sys.stdout.flush()
    for line in iter(process.stderr.readline, ''):
        sys.stderr.write(line)
        sys.stderr.flush()


class RustModule:
    def __init__(self, name, cargo_toml_path, is_release=False, color_output=True):
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
        paths= glob.glob(os.path.join(
            self.get_parent_path(),
            'target',
            'release' if self.is_release else 'debug',
            '*{ext}'.format(ext=self.get_ext())
        ))  # XXX: :poop:
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
    def initialize_options(self):
        self.modules = []
        self.parallel = None
        self.build_temp = None
        self.cargo_clean = False

    def finalize_options(self):
        self.set_undefined_options(
                'build',
                ('parallel', 'parallel'),
                ('build_temp', 'build_temp'),
        )

    def run(self):
        if self.cargo_clean:
            for module in self.modules:
                self.clean_module(module)

        for module in self.modules:
            self.compile_module(module)

        for module in self.modules:
            self.deploy(module)

    def clean_module(self, module):
        working_directory = module.get_parent_path()
        try:
            execute_streaming_stdout(['cargo', 'clean'], cwd=working_directory)
        except Exception as e:  # fixme:!!!!
            raise e

    def compile_module(self, module):
        args = module.get_compile_command()
        args = self.extend_command_args(args)

        working_directory = module.get_parent_path()

        try:
            execute_streaming_stdout(args, cwd=working_directory)
        except sp.CalledProcessError as e:
            # fixme: improve error message
            raise e
        except Exception as e:  # fixme: specify exceptions
            raise e
        return module

    def deploy(self, module):
        dylib_path = module.get_dylib_path()
        build_ext = self.get_finalized_command('build_ext')  # type: build_ext
        ext_fullpath = build_ext.get_ext_fullpath(module.name)
        self.mkpath(os.path.dirname(ext_fullpath))
        self.copy_file(dylib_path, ext_fullpath)

    def extend_command_args(self, args):
        if self.parallel:
            args.extend(['--jobs', '-1'])
        return args

build_rust = RustBuildCommand


class install_with_rust(_install_lib):
    def build(self):
        super(install_with_rust, self).build()
        self.run_command('build_rust')