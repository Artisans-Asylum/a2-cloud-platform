
from secrets import token_urlsafe
from pathlib import Path
from invoke import task, Context

# REF: https://sobolevn.me/git-secret/

@task
def tell(ctx:Context, email:str):
    ctx.run(f"git secret tell {email}")

@task
def cat(ctx:Context, path:str):
    ctx.run(f"git secret cat {path}")

@task
def xclip(ctx:Context, path:str):
    ctx.run(f"git secret cat {path} | xclip -in")

@task
def add(ctx:Context, path:str):
    ctx.run(f"git secret add {path}")
    ctx.run("git secret hide -mF")

@task
def re_encrypt(ctx:Context):
    ctx.run("git secret reveal")
    # re-create encrypted and delete plaintext
    ctx.run("git secret hide -dc")  

@task
def create(ctx:Context, path:str, data="", nbytes=32):
    assert nbytes>=16, "Too few bytes for secure password token."
    file = Path(path)
    if file.exists():
        file.unlink()
    file.write_text(
        data=data if data else token_urlsafe(nbytes),
        encoding='utf-8')
    add(ctx,file)

@task
def rotate(ctx:Context):
    ctx.run("git secret reveal")
    for path in ctx.run("git secret list").stdout.splitlines():
        if Path(path).exists():
            create(ctx,path)
    ctx.run("git secret hide -d")