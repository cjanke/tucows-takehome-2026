# pytest automatically looks for conftest.py and when it finds one at the root,
# it adds that directory to the path. This means plain pytest tests/ -v will work correctly.