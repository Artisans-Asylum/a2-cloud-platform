
from invoke import task, Context

from tasks import PROJECT_ROOT

BOOTSTRAP_DEPS ={
    # dep   : command to install it 
    'docker': './scripts/install_docker.sh',
    'git-secret': 'apt install -y git-secret'
}

def check_or_install(c:Context, dep, install_cmd):
    print(f"Checking dependency on: {dep}")
    result = c.run(f"which {dep}")
    if result.return_code != 0:
        c.sudo(f"{install_cmd}")

@task 
def install_post_bootstrap(c: Context):
    """Install remaining dependencies after make bootstrap"""
    for dep in BOOTSTRAP_DEPS:
        check_or_install(c,dep,BOOTSTRAP_DEPS[dep])

@task 
def install_all(c: Context):
    """Install all deps"""
    with c.cd(PROJECT_ROOT):
        c.run("make deps")
    install_post_bootstrap(c)