import subprocess
import logging
import inspect

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
        result =subprocess.run(["volcano", "run", "-", "--stdout"], input=source.encode())
        
        print(result)
        
        return
    

    return wrapper