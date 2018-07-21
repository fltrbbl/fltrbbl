import click
import json
import sys
import requests
import os
from requests.auth import HTTPBasicAuth

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


@click.group()
@click.option('--host', default='http://localhost:8080')
@click.pass_context
def cli(ctx, host):
    ctx.obj['HOST'] = host


auth = dict(username="testemail@abc.de", password='testpassword')


@cli.command()
@click.argument('resource')
@click.pass_context
def get(ctx, resource):
    response = requests.get(f'{ctx.obj["HOST"]}/{resource}', auth=HTTPBasicAuth(auth['username'], auth['password']))
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
    response = requests.post(f'{ctx.obj["HOST"]}/{resource}', json=d, auth=HTTPBasicAuth(auth['username'], auth['password']))
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
    response = requests.put(f'{ctx.obj["HOST"]}/{resource}', json=d, auth=HTTPBasicAuth(auth['username'], auth['password']))
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
    response = requests.delete(f'{ctx.obj["HOST"]}/{resource}', json=d, auth=HTTPBasicAuth(auth['username'], auth['password']))
    try:
        print('response %s: %s' % (response.status_code, json.dumps(response.json(), indent=2, ensure_ascii=False)))
    except (ValueError, json.decoder.JSONDecodeError):
        print('response %s: %s' % (response.status_code, response.text))

if __name__ == '__main__':
    cli(obj={})
