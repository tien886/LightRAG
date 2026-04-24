import sys
import os
import importlib.util

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

enum_init = os.path.join(project_root, "enum", "__init__.py")
if os.path.exists(enum_init):
    spec = importlib.util.spec_from_file_location("enum", enum_init)
    local_enum = importlib.util.module_from_spec(spec)
    
    sys.modules["enum"] = local_enum
    spec.loader.exec_module(local_enum)
