import sys
from types import TracebackType

is_silenced = False

def silent_excepthook(exctype, value, traceback):
    global is_silenced
    if is_silenced:
        pass
    else:
        sys.__excepthook__(exctype, value, traceback)
    
sys.excepthook = silent_excepthook

def silent_raise():
    global is_silenced
    is_silenced = True
    raise

def clean_raise(exception = None):
    except_class = exception.__class__
    
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
        
    traceback = None
    for f in frames:
        traceback = TracebackType(
            tb_next = traceback,
            tb_frame = f,
            tb_lasti = f.f_lasti,
            tb_lineno = f.f_lineno
        )
    
    sys.__excepthook__(type(exception), exception, traceback)
    silent_raise()