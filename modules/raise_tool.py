import sys
from types import TracebackType
import dis

is_silenced = False

def silent_excepthook(exctype, value, traceback):
    global is_silenced
    if is_silenced:
        pass
    else:
        sys.__excepthook__(exctype, value, traceback)
    
sys.excepthook = silent_excepthook

def silent_raise(exception):
    global is_silenced
    is_silenced = True
    raise exception

def clean_raise(exception = None, lasti_move = 0):
    def is_inside_try():
        try:
            frame = sys._getframe(2)
        except ValueError:
            return False
        
        while frame is not None:
            lasti = frame.f_lasti
            code = frame.f_code.co_code
            
            i = lasti + 2
            search_limit = i + 2048
            
            while i < len(code) and i < search_limit:
                op = code[i]
                opname = dis.opname[op]
                
                if opname == 'PUSH_EXC_INFO':
                    return True
                    
                if opname in ('RETURN_VALUE', 'RETURN_CONST') and i > lasti + 10:
                    break
                    
                i += 2
            frame = frame.f_back
            
        return False
    
    if exception is None: exception = RuntimeError('No active exception to reraise')
    exception.__traceback__ = None
    try:
        frame = sys._getframe(2)
    except ValueError:
        frame = sys._getframe(1)
        exception = RuntimeError('clean_raise() cannot be called from the global scope')
    frames = []
    
    while frame is not None:
        frames.append(frame)
        frame = frame.f_back
        
    f = frames[0]
    
    traceback = None
    for f in frames:
        code = f.f_code.co_code
        lasti = f.f_lasti
        direction = 2 if lasti_move > 0 else -2
        i = lasti + 2
        step = abs(lasti_move)
        
        while i < len(code) and step != 0:
            op = code[i]
            opname = dis.opname[op]
            
            i += direction
            lasti += direction
            
            if opname == 'CACHE':
                continue
            
            step -=1
        
        traceback = TracebackType(
            tb_next = traceback,
            tb_frame = f,
            tb_lasti = lasti,
            tb_lineno = f.f_lineno
        )
    if not is_inside_try():
        sys.__excepthook__(type(exception), exception, traceback)
    silent_raise(exception)
