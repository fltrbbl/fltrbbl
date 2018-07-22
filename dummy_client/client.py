import click
import json
import sys
import requests
import os
from requests.auth import HTTPBasicAuth
import cchardet


def check_encoding(r):
    # https://github.com/requests/requests/issues/2359
    # fix weird long parsing time for bigger responses
    if r.encoding is None:
        # Requests detects the encoding when the item is GET'ed using
        # HTTP headers, and then when r.text is accessed, if the encoding
        # hasn't been set by that point. By setting the encoding here, we
        # ensure that it's done by cchardet, if it hasn't been done with
        # HTTP headers. This way it is done before r.text is accessed
        # (which would do it with vanilla chardet). This is a big
        # performance boon.
        r.encoding = cchardet.detect(r.content)['encoding']


def resolve_json(path_or_json: str):
    if path_or_json.startswith('@'):
        path = path_or_json[1:]
        if os.path.isfile(path):
            with open(path, 'r') as f:
                d = json.load(f)
        else:
            raise Exception('file not found')
    else:
        d = json.loads(path_or_json)

    return d


credentials_file = 'credentials.json'


def store_creds(host, token):
    if not os.path.isfile(credentials_file):
        creds = {}
    else:
        with open(credentials_file, 'r') as f:
            creds = json.load(f)

    creds[host] = token
    with open(credentials_file, 'w+') as f:
        json.dump(creds, f)


def get_creds(host):
    if not os.path.isfile(credentials_file):
        creds = {}
    else:
        with open(credentials_file, 'r') as f:
            creds = json.load(f)
    if not creds.get(host, False):
        print('no credentials found, log in first!')
        exit(1)
    return creds[host]


@click.group()
@click.option('--host', default='http://localhost:8080')
@click.pass_context
def cli(ctx, host):
    ctx.obj['HOST'] = host


auth = dict(username="testemail@abc.de", password='testpassword')


@cli.command()
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
@click.pass_context
def login(ctx, username, password):
    response = requests.get(f'{ctx.obj["HOST"]}/user/token', auth=HTTPBasicAuth(auth['username'], auth['password']))
    check_encoding(response)
    try:
        if response.ok:
            store_creds(ctx.obj['HOST'], response.json()['token'])
    except (ValueError, json.decoder.JSONDecodeError):
        print('response %s: %s' % (response.status_code, response.text))


@cli.command()
@click.argument('resource')
@click.pass_context
def get(ctx, resource):
    response = requests.get(f'{ctx.obj["HOST"]}/{resource}',
                            headers=dict(Authorization='Token: %s' % get_creds(ctx.obj['HOST'])))
    try:
        print('response %s: %s' % (response.status_code, json.dumps(response.json(), indent=2, ensure_ascii=False)))
    except (ValueError, json.decoder.JSONDecodeError):
        print('response %s: %s' % (response.status_code, response.text))


@cli.command()
@click.argument('resource')
@click.option('--json', '-d', 'json_dict')
@click.pass_context
def post(ctx, resource, json_dict=''):
    if json_dict:
        d = resolve_json(json_dict)
    else:
        if not sys.stdin.isatty():
            print('reading stdin...')
            d = resolve_json(sys.stdin.read())
        else:
            print('no input found..?')
            exit(1)
    response = requests.post(f'{ctx.obj["HOST"]}/{resource}', json=d,
                             headers=dict(Authorization='Token: %s' % get_creds(ctx.obj['HOST'])))
    try:
        print('response %s: %s' % (response.status_code, json.dumps(response.json(), indent=2, ensure_ascii=False)))
    except (ValueError, json.decoder.JSONDecodeError):
        print('response %s: %s' % (response.status_code, response.text))


@cli.command()
@click.argument('resource')
@click.option('--json', '-d', 'json_dict')
@click.pass_context
def put(ctx, resource, json_dict=''):
    if json_dict:
        d = resolve_json(json_dict)
    else:
        if not sys.stdin.isatty():
            print('reading stdin...')
            d = resolve_json(sys.stdin.read())
        else:
            print('no input found..?')
            exit(1)
    response = requests.put(f'{ctx.obj["HOST"]}/{resource}', json=d,
                            headers=dict(Authorization='Token: %s' % get_creds(ctx.obj['HOST'])))
    try:
        print('response %s: %s' % (response.status_code, json.dumps(response.json(), indent=2, ensure_ascii=False)))
    except (ValueError, json.decoder.JSONDecodeError):
        print('response %s: %s' % (response.status_code, response.text))


@cli.command()
@click.argument('resource')
@click.option('--json', '-d', 'json_dict')
@click.pass_context
def delete(ctx, resource, json_dict=''):
    if json_dict:
        d = resolve_json(json_dict)
    else:
        if not sys.stdin.isatty():
            print('reading stdin...')
            d = resolve_json(sys.stdin.read())
        else:
            print('no input found..?')
            exit(1)
    response = requests.delete(f'{ctx.obj["HOST"]}/{resource}', json=d,
                               headers=dict(Authorization='Token: %s' % get_creds(ctx.obj['HOST'])))
    try:
        print('response %s: %s' % (response.status_code, json.dumps(response.json(), indent=2, ensure_ascii=False)))
    except (ValueError, json.decoder.JSONDecodeError):
        print('response %s: %s' % (response.status_code, response.text))


if __name__ == '__main__':
    cli(obj={})
