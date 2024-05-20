from distutils.core import run_setup
from distutils.unixccompiler import UnixCCompiler
from json import dump, load
from logging import getLogger
from os import environ, path
from shlex import join, split

from setuptools import Extension
from setuptools.command.build_ext import build_ext



ext = Extension(
    name='omniblack.secret',
    include_dirs=['/usr/include/python3.12'],
    extra_compile_args=[
        '-Wall',
        '-Werror',
        '-Wextra',
        '-Wfloat-equal',
        '-Wcast-align',
        '-Wconversion',
        '-Wdouble-promotion',
        '-Wduplicated-branches',
        '-Wduplicated-cond',
        '-Wformat-overflow',
        '-Wformat-truncation',
        '-Wformat=2',
        '-Wjump-misses-init',
        '-Wlogical-op',
        '-Wmisleading-indentation',
        '-Wnull-dereference',
        '-Wrestrict',
        '-Wshadow',
        '-Wsign-conversion',
        '-Wundef',
        '-Wunused',
        '-std=gnu17',
    ],
    libraries=['sodium'],
    sources=['secret.c'],
)


class CmdArgs(Exception):
    pass


class Compiler(UnixCCompiler):
    def spawn(self, cmd, **kwargs):
        raise CmdArgs(*cmd)


class Command(build_ext):
    def build_extensions(self):
        self.compiler.__class__ = Compiler
        return super().build_extensions()


if __name__ == '__main__':
    log = getLogger()
    log.disabled = True
    SRC = environ['SRC']
    dist = run_setup(path.join(SRC, 'setup.py'), stop_after='commandline')

    dist.cmdclass['build_ext'] = Command

    try:
        dist.run_command('build_ext')
    except CmdArgs as exc:
        cc_args = exc.args

        with open(path.join(SRC, 'compile_commands.json'), 'r+') as f:
            current = load(f)
            f.seek(0)
            f.truncate()
            f.seek(0)

            main_opts, = current
            main_opts['command'] = join(cc_args)
            main_opts['arguments'] = cc_args

            dump(current, f, ensure_ascii=False, indent=4, sort_keys=True)
