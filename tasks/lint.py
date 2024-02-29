from glob import glob
from pathlib import Path

from invoke import task, Context

from tasks import PROJECT_ROOT


@task
def docker(c:Context, file:str=""):
    if not file:
        dockerfiles = (
            glob(f"**/Dockerfile",root_dir=PROJECT_ROOT)+
            glob(f"**/*.dockerfile",root_dir=PROJECT_ROOT)
        )
    elif Path(file).exists():
        dockerfiles = file
    else:
        dockerfiles = glob(f"**/{file}",root_dir=PROJECT_ROOT)
    for dockerfile in dockerfiles:
        with c.cd(PROJECT_ROOT):
            c.run(f"scripts/hadolint {dockerfile}")