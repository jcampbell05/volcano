import subprocess
import logging
import inspect
import tempfile

logger = logging.getLogger(__name__)

def volcano(func):
    """
    Decorator that allows a Volcano script to be defined in a Python function
    and then ran when that function is called.

    Example:

    from volcano import volcano

    @volcano
    def my_script():
        print("Hello, world!")
    """
    def wrapper(*args, **kwargs):

        source_lines, _ = inspect.getsourcelines(func)
        source = "\n".join(source_lines)
        subprocess.run(["volcano", "run", "-", f"-m={func.__name__}"], input=source.encode())
    
    return wrapper