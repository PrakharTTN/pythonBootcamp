""" Q2) Explain the use of `from importlib import reload
    Importlib.reload(module)
"""

from importlib import reload
from customReloadModule import old

print("Text before reload: "+old.x)
old.x="Now I have been changed"
print("Text changed: "+old.x)
reload(old)
print("Text after reload: "+old.x)
