from invoke import task, Context, Config

from tasks import PROJECT_ROOT

@task
def from_invoke(c:Context, key:str):
    print(c.config[key])

@task
def project_name(c:Context, ):
    print(c.config.project_name)

@task
def project_root(_):
    print(PROJECT_ROOT)