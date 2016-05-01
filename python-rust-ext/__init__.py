from distutils.cmd import Command
from distutils.command.install_lib import install_lib

import subprocess as sp
import sys


def execute_streaming_stdout(args):
    process = sp.Popen(args, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
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
        args = ['cargo', 'build', '--manifest-path', self.cargo_toml_path]
        if self.is_release:
            args.append('--release')
        if self.is_color_output:
            args.extend(['--color', 'always'])
        return args


class RustBuildCommand(Command):
    modules = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        pass

    def compile_module(self, module: RustModule):
        args = module.get_compile_command()

    @classmethod
    def register_module(cls, modules):
        if not isinstance(modules, [list, tuple]):
            modules = [modules]
        else:
            modules = modules
        res = cls._gen_new_class_if_needed()
        res.modules = modules
        return res

    @classmethod
    def set_options(cls, **kwargs):
        pass

    @classmethod
    def _gen_new_class_if_needed(cls): # XXX: improve this name
        if cls == RustBuildCommand:
            class _RestBuildCommand(cls):
                pass

            res = _RestBuildCommand
        else:
            res = cls
        return res


class install_rust_lib(install_lib):
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        pass

    def build(self):
        pass