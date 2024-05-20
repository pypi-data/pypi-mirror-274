from metrics import *
from scaled_rope import *

help_text = """
上传步骤：
1.python setup.py check
2.python setup.py sdist build
3.twine upload dist/*
"""

def help():
    print(help_text)
