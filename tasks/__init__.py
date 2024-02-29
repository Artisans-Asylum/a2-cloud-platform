# Invoke tasks module for automation of project tasks.

import sys
from pathlib import Path
from glob import glob

PROJECT_ROOT = Path(__file__).parent.parent
VENV_PKG_ROOT = Path(glob('.venv/lib/**/site-packages',
                               root_dir=str(PROJECT_ROOT))[0])

# enable: import cloud-platform
# enable: import tasks
sys.path.append(str(PROJECT_ROOT))

# enable poetry venv package(s) import
sys.path.append(str(VENV_PKG_ROOT))

# Import task modules 
from . import const
from . import deps
from . import lint
from . import docker

# Add task modules into invoke collections
from invoke import Collection
ns = Collection()
ns.add_collection(const)
ns.add_collection(deps)
ns.add_collection(docker)
ns.add_collection(lint)
