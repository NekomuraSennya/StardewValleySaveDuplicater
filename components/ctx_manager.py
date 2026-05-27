import sys, os, time
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from modules.raise_tool import clean_raise
from typing import Iterable
import dis

class Variables_dict:
    def __init__(self, __iterable: Iterable | dict = None, **kwargs):
        self._data = {}
        try:
            if __iterable is None:
                self._data = dict(**kwargs)
            else:
                self._data = dict(__iterable, **kwargs)
        except Exception as e:
            clean_raise(e)
    
    def update(self, m):
        self._data.update(m)
        
    def items(self):
        return dict(self._data).items()
    
    def __or__(self, value):
        if type(value) == dict:
            return dict(self._data) | value
        else:
            clean_raise(TypeError(f"unsupported operand type(s) for |: 'dict' and '{type(value).__name__}'"))
            
    def __ior__(self, other):
        try:
            self.update(other)
            return self
        except Exception as e:
            clean_raise(e)
        
    def __eq__(self, value):
        if isinstance(value, Variables_dict):
            return self._data == value._data
        return False
    
    def __contains__(self, item):
        if item in self._data:
            return True
        else:
            return False
    
    def __getitem__(self, key):
        return self._data[key]
    
    def __setitem__(self, key, value):
        try:
            self._data[key] = value
        except KeyError as e:
            clean_raise(e)
    
    def __delitem__(self, name):
        try:
            del self._data[name]
        except KeyError as e:
            clean_raise(e)
    
    def __iter__(self):
        for key, value in self._data.items():
            yield key, value
            
    def __len__(self):
        return len(dict(self._data))
    
    def __repr__(self):
        return repr(self._data)
    
    def __str__(self):
        return str(self._data)
    
class Var:
    def __init__(self):
        self.ctx = Variables_dict()
        
    def add(self, *args):
        if len(args) == 0:
            clean_raise(TypeError(f'Var.add() needs an argument'))
        frame = sys._getframe(1)
        lasti = frame.f_lasti
        
        code = frame.f_code.co_code
        
        names = []
        
        i = lasti + 2
        search_jimit = i + 2048
        while i < len(code) and i < search_jimit:
            op = code[i]
            opname = dis.opname[op]
            
            if opname in ('STORE_NAME', 'STORE_FAST', 'STORE_GLOBAL', 'STORE_DEREF'):
                arg = code[i+1]
                if opname == 'STORE_FAST':
                    names.append(frame.f_code.co_varnames[arg])
                else:
                    names.append(frame.f_code.co_names[arg])
                    
                next_op = code[i+2]
                if dis.opname[next_op] not in ('STORE_NAME', 'STORE_FAST', 'STORE_GLOBAL', 'STORE_DEREF'):
                    break
            i += 2
        
        if len(names) == 0:
            clean_raise(SyntaxError('Var.add() cannot be called when not assigning a value'))
        
        if len(args) == 1 and len(names) == 1:
            self.ctx.update({names[0]: args[0]})
            return args[0]
        elif len(names) > 1:
            for k, v in zip(names, args*len(names)):
                print(k, v)
                self.ctx.update({k: v})
            return args
        else:
            for k, v in zip(names, args):
                print(k, v)
                self.ctx.update({k: v})
            return args
    
    
    def remove(self, *args):
        deleted = 0
        for name in args:
            if name in self.ctx:
                del self.ctx[name]
                deleted += 1
        return deleted
    
    def exist(self, name):
        return name in self.ctx
    
    def __repr__(self):
        return repr(self.ctx)
    
    def __str__(self):
        return str(self.ctx)
    
var = Var()
ctx = var.ctx