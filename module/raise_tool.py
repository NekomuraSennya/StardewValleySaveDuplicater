import sys
from types import TracebackType

def clean_raise(exception = None):
    if exception is None: exception = RuntimeError('No active exception to reraise')
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
    sys.exit(1)