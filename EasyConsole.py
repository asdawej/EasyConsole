# !usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations

import cmd
import os
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
        Народы мира не хотят повтореная бедствий  войны. - Сталин
    =================================================================
    '''
    prompt = '<Console> '
    path_ptr = plb.Path('.').absolute()
    son_paths: list[plb.Path] = [x for x in path_ptr.iterdir()]
    path_num = len(son_paths)
    try:
        fp_const = open(r'ConstPaths.dat', 'rb')
    except:
        fp_const = open(r'ConstPaths.dat', 'wb')
        pkl.dump({}, fp_const)
        fp_const.close()
        fp_const = open(r'ConstPaths.dat', 'rb')
    const_def_tab: dict[plb.Path] = pkl.load(fp_const)
    fp_const.close()
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

    # ========== 路径操作命令 ==========

    def do_cd(self, arg: str):
        'Open and move to a directory'
        _args = parse(arg)
        if not _args:
            _tempptr = self.path_ptr
        else:
            _tempptr = self._pathptr_FromArg(_args[0])
        if not _tempptr:
            return False
        _tempptr: plb.Path
        if not _tempptr.is_dir():
            print('Not a directory')
            return False
        self.path_ptr = _tempptr
        self.son_paths = [x for x in self.path_ptr.iterdir()]
        self.path_num = len(self.son_paths)

    def do_ls(self, arg: str):
        'List all the files and directories under this path or a given path.'
        _args = parse(arg)
        if not _args:
            _tempptr = self.path_ptr
        else:
            _tempptr = self._pathptr_FromArg(_args[0])
        if not _tempptr:
            return False
        _tempptr: plb.Path
        if not _tempptr.is_dir():
            print('Not a directory')
            return False
        print_here(_tempptr)
        print_parent()
        for i, x in enumerate(_tempptr.iterdir()):
            print(i, x)

    # ========== 全局量定义命令 ==========

    def do_const(self, arg: str):
        'Define a constant path alias'
        _args = parse(arg)
        if len(_args) != 2 or not isinstance(_args[0], str):
            print('Wrong sytax')
            return False
        _tempptr = self._pathptr_FromArg(_args[1])
        if not _tempptr:
            return False
        _tempptr: plb.Path
        self.const_def_tab[_args[0]] = _tempptr.absolute()
        self.fp_const = open(r'ConstPaths.dat', 'wb')
        pkl.dump(self.const_def_tab, self.fp_const)
        self.fp_const.close()

    def do_let(self, arg: str):
        'Define a temporary path alias'
        _args = parse(arg)
        if len(_args) != 2 or not isinstance(_args[0], str):
            print('Wrong syntax')
            return False
        _tempptr = self._pathptr_FromArg(_args[1])
        if not _tempptr:
            return False
        _tempptr: plb.Path
        self.path_def_tab[_args[0]] = _tempptr.absolute()

    def do_del(self, arg: str):
        'Delete an alias'
        _args = parse(arg)
        _length = len(_args)
        if _length != 1 or not isinstance(_args[0], str):
            if _length != 2:
                print('Wrong syntax')
                return False
            elif _args[1] != 'const' and _args[1] != 'let':
                print('Wrong syntax')
                return False
        if _length == 1:
            _set = self._pathptr_FromAlias(_args[0])
        else:
            _set = _args[1]
        if _set == 'const':
            del self.const_def_tab[_args[0]]
        else:
            del self.path_def_tab[_args[0]]

    # ========== 指令执行命令 ==========

    def do_run(self, arg: str):
        'Run a pre-processed command line'
        _args = parse(arg)
        for i in range(len(_args)):
            if (_subs := self._pathptr_FromArg_Ex(_args[i])):
                _subs: plb.Path
                _args[i] = '"'+str(_subs.absolute())+'"'
            elif isinstance(_args[i], int):
                _args[i] = str(_args[i])
        _args: list[str]
        os.system(' '.join(_args))

    def do_cmd(self, arg: str):
        'Run a raw command line'
        os.system(arg)

    # ========== 命令预处理 ==========

    def precmd(self, line: str) -> str:
        return line.lower()

    def _pathptr_FromArg(self, _index: str | int) -> plb.Path | bool:
        if isinstance(_index, str):
            if not _index in self.path_def_tab:
                if not _index in self.const_def_tab:
                    print('Wrong alias')
                    return False
                else:
                    return self.const_def_tab[_index]
            else:
                return self.path_def_tab[_index]
        else:
            if _index < -1 or _index >= self.path_num:
                print('Wrong index')
                return False
            if _index == -1:
                return self.path_ptr.parent
            else:
                return self.son_paths[_index]

    def _pathptr_FromArg_Ex(self, _index: str | int) -> plb.Path | bool:
        if isinstance(_index, str):
            if not _index in self.path_def_tab:
                if not _index in self.const_def_tab:
                    return False
                else:
                    return self.const_def_tab[_index]
            else:
                return self.path_def_tab[_index]
        else:
            if _index < -1 or _index >= self.path_num:
                return False
            if _index == -1:
                return self.path_ptr.parent
            else:
                return self.son_paths[_index]

    def _pathptr_FromAlias(self, _alias: str) -> str | bool:
        if not isinstance(_alias, str):
            return False
        if not _alias in self.path_def_tab:
            if not _alias in self.const_def_tab:
                print('Wrong alias')
                return False
            else:
                return 'const'
        else:
            return 'let'

    def _pathptr_FromAlias_Ex(self, _alias: str) -> str | bool:
        if not isinstance(_alias, str):
            return False
        if not _alias in self.path_def_tab:
            if not _alias in self.const_def_tab:
                return False
            else:
                return 'const'
        else:
            return 'let'

API_TAB={
    'help':EasyConsole.do_help,
    'hello':EasyConsole.do_hello,
    'exit':EasyConsole.do_exit,
    'cd':EasyConsole.do_cd,
    'ls':EasyConsole.do_ls,
    'const':EasyConsole.do_const,
    'let':EasyConsole.do_let,
    'del':EasyConsole.do_del,
    'run':EasyConsole.do_run,
    'cmd':EasyConsole.do_cmd
}

def do(console:EasyConsole, topic:str, arg:str=''):
    'EasyConsole API'
    API_TAB[topic](console, arg)

if __name__ == '__main__':
    EasyConsole().cmdloop()
