# !usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

import cmd
import pickle as pkl
import pathlib as plb


def parse(arg: str) -> list[str | int]:
    _args = arg.split()
    for i in range(len(_args)):
        try:
            _args[i] = int(_args[i])
        except:
            continue
    return _args


def print_here(path: plb.Path):
    print(f'-*- {path} -*-')


def print_parent():
    print(-1, '..')


class EasyConsole(cmd.Cmd):
    intro = '''
    Welcome to EasyConsole, where we provide fast way to get a path.
    ================================================================
    '''
    prompt = '<Console> '
    path_ptr = plb.Path('.').absolute()
    son_paths: list[plb.Path] = [x for x in path_ptr.iterdir()]
    path_num = len(son_paths)
    fp_const=open(r'ConstPaths.dat', 'r+b')
    const_def_tab: dict[plb.Path] = pkl.load(fp_const)
    path_def_tab: dict[plb.Path] = {}

    # ========== 检测命令 ==========

    def do_hello(self, arg: str):
        'Say hello.'
        if not parse(arg):
            print('Hello world!')
        else:
            print(f'Hello, {arg}!')

    def do_exit(self, arg: str):
        'Exit console.'
        if not parse(arg):
            print('Bye bye!')
        else:
            print(f'Bye, {arg}!')
        self.fp_const.close()
        return True

    # ========== 主要功能 ==========

    def do_cd(self, arg: str):
        'Open and move to a directory'
        _args = parse(arg)
        if not _args:
            _tempptr = self.path_ptr
        elif isinstance(_args[0], str):
            if not _args[0] in self.const_def_tab:
                if not _args[0] in self.path_def_tab:
                    print('Wrong index')
                    return False
                else:
                    _tempptr = self.path_def_tab[_args[0]]
            else:
                _tempptr = self.const_def_tab[_args[0]]
        else:
            if _args[0] < -1 or _args[0] >= self.path_num:
                print('Wrong index')
                return False
            if _args[0] == -1:
                _tempptr = self.path_ptr.parent
            else:
                _tempptr = self.son_paths[_args[0]]
        if not _tempptr.is_dir():
            print('Not a directory')
            return False
        self.path_ptr=_tempptr
        self.son_paths: list[plb.Path] = [x for x in self.path_ptr.iterdir()]
        self.path_num = len(self.son_paths)

    def do_ls(self, arg: str):
        'List all the files and directories under this path or a given path.'
        _args = parse(arg)
        if not _args:
            _tempptr = self.path_ptr
        elif isinstance(_args[0], str):
            if not _args[0] in self.const_def_tab:
                if not _args[0] in self.path_def_tab:
                    print('Wrong index')
                    return False
                else:
                    _tempptr = self.path_def_tab[_args[0]]
            else:
                _tempptr = self.const_def_tab[_args[0]]
        else:
            if _args[0] < -1 or _args[0] >= self.path_num:
                print('Wrong index')
                return False
            if _args[0] == -1:
                _tempptr = self.path_ptr.parent
            else:
                _tempptr = self.son_paths[_args[0]]
        if not _tempptr.is_dir():
            print('Not a directory')
            return False
        print_here(_tempptr)
        print_parent()
        for i, x in enumerate(_tempptr.iterdir()):
            print(i, x)

    # ========== 命令预处理 ==========

    def precmd(self, line: str) -> str:
        return line.lower()
    


if __name__ == '__main__':
    EasyConsole().cmdloop()
