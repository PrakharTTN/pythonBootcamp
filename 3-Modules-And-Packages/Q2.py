from importlib import reload
from Q2 import old

print("Text before reload: "+old.x)
old.x="Now I have been changed"
print("Text changed: "+old.x)
reload(old)
print("Text after reload: "+old.x)
