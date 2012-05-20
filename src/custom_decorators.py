import time

# This in itself seems to add 300-400ms :-/ (FIXME)
# Should only enabled in debug mode (TODO: enforce this)
class Timer(object):
    """Log the time taken for a view."""
    def __init__(self):
        import logging
        self.logger = logging.getLogger("debugger")

    def __call__(self, func):
        """Turn the object into a decorator"""
        def wrapper(*arg, **kwargs):
            t1 = time.time()                #start time
            res = func(*arg, **kwargs)      #call the original function
            t2 = time.time()                #stop time
            t = (t2-t1)*1000.0              #time in milliseconds
            self.logger.debug("%s:%s" % (func.__name__, t)) 
            return res 
        return wrapper
timer = Timer()
