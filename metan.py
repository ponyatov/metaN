

import os, sys

## graph

class Object:
    def __init__(self, V):
        self.val = V
        self.slot = {}
        self.nest = []

    ## dump

    def __repr__(self): return self.dump()

    def dump(self, done=[], depth=0, prefix=''):
        # header
        tree = self._pad(depth) + self.head(prefix)
        # cycles
        if not depth:
            done = []
        if self in done:
            return tree + ' _/'
        else:
            done.append(self)
        # slot{}s
        for i in self.slot:
            tree += self.slot[i].dump(done, depth + 1, '%s = ' % i)
        # nest[]ed
        idx = 0
        for j in self.nest:
            tree += j.dump(done, depth + 1, '%s: ' % idx)
            idx += 1
        # subtree
        return tree

    def _pad(self, depth): return '\n' + '\t' * depth

    def head(self, prefix=''):
        return '%s<%s:%s> @%x' % (
            prefix, self._type(), self._val(), id(self))

    def _type(self): return self.__class__.__name__.lower()
    def _val(self): return '%s' % self.val

    ## operator

    def __getitem__(self, key):
        return self.slot[key]

    def __setitem__(self, key, that):
        self.slot[key] = that
        return self

    def __lshift__(self, that):
        return self.__setitem__(that._type(), that)

    def __rshift__(self, that):
        return self.__setitem__(that.val, that)

    def __floordiv__(self, that):
        if isinstance(that, str):
            return self // String(that)
        if isinstance(that, list):
            for i in that:
                self // i
            return self
        self.nest.append(that)
        return self

    ## eval

    def eval(self, ctx): raise Error((self))

## error

class Error(Object, BaseException):
    pass

## primitive

class Primitive(Object):
    def eval(self, ctx): return self

class Symbol(Primitive):
    pass

class String(Primitive):
    pass

class Number(Primitive):
    def __init__(self, V):
        Primitive.__init__(self, float(V))

class Integer(Primitive):
    def __init__(self, V):
        Primitive.__init__(self, int(V))

    def add(self, that, ctx):
        return Integer(self.val + that.val)

## active

class Active(Object):
    pass

class Op(Active):
    def eval(self, ctx):
        if len(self.nest) == 2:
            lval = self.nest[0].eval(ctx)
            rval = self.nest[1].eval(ctx)
        if self.val == '+':
            return lval.add(rval, ctx)
        raise Error((self))

## I/O

class IO(Object):
    pass

class Dir(IO):
    def __init__(self, V):
        IO.__init__(self, V)
        try:
            os.mkdir(self.val)
        except FileExistsError:
            pass

    def __floordiv__(self, that):
        if issubclass(that.__class__, File):
            filename = '%s/%s' % (self.val, that.val)
            print('filename', filename)
            that.fh = open(filename, 'w')
        return IO.__floordiv__(self, that)

class File(IO):
    def __init__(self, V):
        IO.__init__(self, V)
        self.fh = None

    def __floordiv__(self, that):
        # raise Error((self))
        if self.fh != None:
            raise Error((self))
            self.fh.write("'%s' % that.val")
            self.fh.flush()
        return IO.__floordiv__(self, that)

class Makefile(File):
    def __init__(self, V='Makefile'):
        File.__init__(self, V)

## meta

class Meta(Object):
    pass

class Class(Meta):
    def __init__(self, C):
        Object.__init__(self, C.__name__)

class Module(Meta):
    pass

class Section(Object):
    pass


MODULE = 'metaL'
TITLE = '[meta]programming [L]anguage'
ABOUT = 'homoiconic metaprogramming system'
AUTHOR = 'Dmitry Ponyatov'
EMAIL = 'dponyatov@gmail.com'
YEAR = 2020
LICENSE = 'MIT'
GITHUB = 'https://github.com/ponyatov/metaL'

metaL = Module(MODULE)

readme = File('README.md')
metaL // readme
readme // ('#  %s' % metaL.val)
readme // ('## %s' % TITLE)
readme // ''
readme // ABOUT
readme // ''
readme // ('(c) %s <<%s>> %s %s' % (AUTHOR, EMAIL, YEAR, LICENSE))
readme // ''

mk = File('Makefile')
metaL // mk

ini = File('metaL.ini')
metaL // ini

giti = File('.gitignore')
metaL // giti

py = File('metaL.py')
metaL // py

graph = Section('graph')
py // graph

obj = Class(Object)
graph // obj

primitive = Class(Primitive)
obj // primitive
# primitive['super'] = obj
prim = Section(primitive.val.lower())
graph // prim
prim // primitive

string = Class(String)
# string['super'] = primitive
primitive // string

# print(metaL)

hello = Object('Hello')
world = Symbol('World')
left = Object('left')
right = Object('right')
# print(hello // world << left >> right)

dj = Module('django')
djdir = dj['dir'] = Dir(dj.val)
djmk = dj['mk'] = (djdir // Makefile())
djmk // ('''

CWD     = $(CURDIR)
MODULE  = $(notdir $(CWD))
OS     ?= $(shell uname -s)

NOW = $(shell date +%%d%%m%%y)
REL = $(shell git rev-parse --short=4 HEAD)

PIP = $(CWD)/bin/pip3
PY  = $(CWD)/bin/python3

''' % ()).split('\n')
print(djmk)

# https://github.com/ponyatov/SICPy/wiki/1.1.1--Expressions/_edit

Number(486)

ctx = Object('context')

add = Op('+') // Integer(137) // Integer(349)
print(add)
print(add.eval(ctx))
