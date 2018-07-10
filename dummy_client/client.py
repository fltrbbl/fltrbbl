import click
import json
import sys
import requests
from requests.auth import HTTPBasicAuth

HOST = 'http://localhost:8080'


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
def cli():
    pass


@click.command()
def dummyuser():
    d = dict(
        email='test@abc.de',
        password='password'
    )

auth = dict(username="testemail@abc.de", password='testpassword')


@cli.command()
@click.argument('resource')
def get(resource):
    response = requests.get(f'{HOST}/{resource}', auth=HTTPBasicAuth(auth['username'], auth['password']))
    try:
        print('response %s: %s' % (response.status_code, json.dumps(response.json(), indent=2, ensure_ascii=False)))
    except (ValueError, json.decoder.JSONDecodeError):
        print('response %s: %s' % (response.status_code, response.text))


@cli.command()
@click.argument('resource')
@click.option('--json', '-d', 'json_dict')
def post(resource, json_dict=''):
    if json_dict:
        d = resolve_json(json_dict)
    else:
        if not sys.stdin.isatty():
            print('reading stdin...')
            d = resolve_json(sys.stdin.read())
        else:
            print('no input found..?')
            exit(1)
    response = requests.post(f'{HOST}/{resource}', json=d, auth=HTTPBasicAuth(auth['username'], auth['password']))
    try:
        print('response %s: %s' % (response.status_code, json.dumps(response.json(), indent=2, ensure_ascii=False)))
    except (ValueError, json.decoder.JSONDecodeError):
        print('response %s: %s' % (response.status_code, response.text))

@cli.command()
@click.argument('resource')
@click.option('--json', '-d', 'json_dict')
def put(resource, json_dict=''):
    if json_dict:
        d = resolve_json(json_dict)
    else:
        if not sys.stdin.isatty():
            print('reading stdin...')
            d = resolve_json(sys.stdin.read())
        else:
            print('no input found..?')
            exit(1)
    response = requests.put(f'{HOST}/{resource}', json=d, auth=HTTPBasicAuth(auth['username'], auth['password']))
    try:
        print('response %s: %s' % (response.status_code, json.dumps(response.json(), indent=2, ensure_ascii=False)))
    except (ValueError, json.decoder.JSONDecodeError):
        print('response %s: %s' % (response.status_code, response.text))

@cli.command()
@click.argument('resource')
@click.option('--json', '-d', 'json_dict')
def delete(resource, json_dict=''):
    if json_dict:
        d = resolve_json(json_dict)
    else:
        if not sys.stdin.isatty():
            print('reading stdin...')
            d = resolve_json(sys.stdin.read())
        else:
            print('no input found..?')
            exit(1)
    response = requests.delete(f'{HOST}/{resource}', json=d, auth=HTTPBasicAuth(auth['username'], auth['password']))
    try:
        print('response %s: %s' % (response.status_code, json.dumps(response.json(), indent=2, ensure_ascii=False)))
    except (ValueError, json.decoder.JSONDecodeError):
        print('response %s: %s' % (response.status_code, response.text))

if __name__ == '__main__':
    cli()
