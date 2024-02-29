
from invoke import task, Context

from tasks import PROJECT_ROOT

@task
def compose_up(c:Context):
    c.run("docker compose up")