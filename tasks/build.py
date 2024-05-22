from glob import glob
from pathlib import Path

from invoke import task, Context, Config

from tasks import PROJECT_ROOT


@task
def make(c:Context, target:str):
    with c.cd(PROJECT_ROOT):
        c.run(f"make {target}")

@task
def j2(c:Context, dir=PROJECT_ROOT):
    yasha_ext = PROJECT_ROOT/'extensions/yasha.py'
    if not isinstance(dir,Path):
        dir = Path(dir)
    assert dir.is_dir()
    for j2_file in dir.glob('**/*.j2'):
        expected_output = j2_file.parent / j2_file.stem 
        with c.cd(j2_file.parent):
            c.run(" ".join([
                "poetry run yasha",
                f"--extensions {yasha_ext.absolute()}",
                "--mode pedantic",
                str(j2_file.name)
            ]))
        if expected_output.relative_to(PROJECT_ROOT) \
            not in (PROJECT_ROOT/'.gitignore').read_text('utf-8').splitlines():
            with c.cd(PROJECT_ROOT):
                c.run(f"echo {expected_output.relative_to(PROJECT_ROOT) } >> .gitignore")


@task
def clean(c:Context):
    for j2_file in glob(
        pathname='**.j2',
        root_dir=PROJECT_ROOT.absolute(),
        recursive=True
    ):
        j2_path = Path(j2_file)
        j2_out = j2_path.parent / j2_path.stem
        if j2_out.exists():
            c.run(f"rm {j2_out}")
    make(c, "clean")