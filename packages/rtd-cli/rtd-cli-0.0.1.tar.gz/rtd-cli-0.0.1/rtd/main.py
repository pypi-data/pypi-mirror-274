import json
from functools import partial
from os import getenv
from os.path import join, expanduser, exists
from sys import stdout, stderr

import click
import requests


URL_BASE = 'https://readthedocs.org/api/v3'
RTD_TOKEN_VAR = 'RTD_TOKEN'

err = partial(print, file=stderr)


def get_token():
    token = getenv(RTD_TOKEN_VAR)
    if token:
        return token
    config_dir = getenv('XDG_CONFIG_HOME', join(expanduser('~'), '.config'))
    rtd_config_dir = join(config_dir, 'rtd-cli')
    token_path = join(rtd_config_dir, 'token')
    if exists(token_path):
        with open(token_path, "r") as f:
            return f.read().strip()

    raise RuntimeError(f"Readthedocs API token not found in ${RTD_TOKEN_VAR} or {token_path}")


@click.group("rtd")
def cli():
    """Simple CLI wrapper for the Readthedocs REST API."""
    pass


@cli.command("api")
@click.option('-b', '--body', help='JSON string to send in the body of a PATCH request; if absent, a GET request is sent')
@click.option('-u', '--show-updated', is_flag=True, help="After a PATCH request (with -b/--body), send a GET to the same endpoint, to verify the updated state of the resource")
@click.argument("endpoint")
def api(body, show_updated, endpoint):
    """Make a request to the Readthedocs REST API.

    RTD API docs: https://docs.readthedocs.io/en/stable/api/v3.html
    """
    token = get_token()
    headers = { 'Authorization': f'token {token}' }
    url = join(URL_BASE, endpoint)
    if body:
        body_obj = json.loads(body)
        response = requests.patch(url, body_obj, headers=headers)
        response.raise_for_status()
        if response.status_code != 204:
            text = response.text
            err(text)

    if body and show_updated or not body:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        body = response.json()
        json.dump(body, stdout, indent=2)


def patch_cmd(name, obj, docstr):
    def cmd(project, no_show_updated, versions):
        for version in versions:
            body = json.dumps(obj)
            api.callback(body=body, show_updated=not no_show_updated, endpoint=f"projects/{project}/versions/{version}/")

    cmd.__doc__ = docstr

    for deco in [
        cli.command(name),
        click.option('-p', '--project'),
        click.option('-U', '--no-show-updated', is_flag=True),
        click.argument("versions", nargs=-1),
    ]:
        cmd = deco(cmd)


patch_cmd("deactivate", {"active": False}, "Deactivate one or more versions")
patch_cmd("hide", {"hidden": True}, "Hide one or more versions")
