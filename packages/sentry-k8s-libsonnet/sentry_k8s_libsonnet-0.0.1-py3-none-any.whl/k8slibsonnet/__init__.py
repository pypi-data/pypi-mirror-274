from importlib import resources
from pathlib import Path
import static

def load(path: Path) -> str:
    inp_file = (resources.files(static) / "vendor" / str(path))
    with inp_file.open("rb") as f:
        return str(f.read())
