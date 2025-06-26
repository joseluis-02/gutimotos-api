# Python
import importlib
from pathlib import Path

module_dir = Path(__file__).resolve().parent
package_path = "apps.measures.admin"

for file in module_dir.glob("*.py"):
    if file.name != "__init__.py":
        module_name = f"{package_path}.{file.stem}"
        importlib.import_module(module_name)
