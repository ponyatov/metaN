
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

    def __floordiv__(self, that):
        self.nest.append(that)
        return self

class Class(Object):
    def __init__(self, C):
        Object.__init__(self, C.__name__)

class Primitive(Object):
    pass

class String(Primitive):
    pass

class File(Object):
    def __floordiv__(self, that):
        if isinstance(that, str):
            return super().__floordiv__(String(that))
        else:
            return super().__floordiv__(that)

class Module(Object):
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

print(metaL)
