
from invoke import task, Context


@task
def gen_key(ctx:Context, email:str ="", path:str=""):
    """Generates a GPG key for the given email address.
    Automatically exports to `path` if given."""
    ctx.run("gpg --gen-key")
    if email and path:
        export_key(ctx,email,path)

@task
def export_key(ctx:Context, email:str, path:str):
    """Export public key of for email id."""
    ctx.run(f"gpg --armor --export {email} > {path}")


@task
def import_key(ctx:Context, path:str):
    """Import public key from selected file."""
    ctx.run(f"gpg  --import {path}")


@task
def dirs(ctx:Context, key:str=""):
    """List gpg configured directories."""
    ctx.run(f"gpgconf --list-dirs {key}")

