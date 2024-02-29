from invoke import task, Context, Config

@task
def from_invoke(c:Context, key:str):
    print(c.config[key])

@task
def project_name(c:Context, ):
    print(c.config.project_name)