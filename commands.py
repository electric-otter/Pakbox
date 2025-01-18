import os
import click
import base64
import requests
from process_isolation import import_isolated

user_input():

def install(user, repo_name, path_to_file):
    giturl = f'https://api.github.com/repos/{user}/{repo_name}/contents/{path_to_file}'
    req = requests.get(giturl)
    if req.status_code == requests.codes.ok:
        req = req.json()  # the response is a JSON
        content = base64.b64decode(req['content'])
        # Decoded content can be saved to a file or used as needed
        file_path = os.path.join(os.getcwd(), path_to_file)
        with open(file_path, 'wb') as file:
            file.write(content)
        print(f"Content written to {file_path}")
    else:
        print('Content was not found. May not install')

@click.command()
@click.option('--choice', type=click.Choice(['Enter', 'Dont enter']))
def pakvenv(choice):
    print("You are about to enter a virtual environment in Pakbox, ONLY use this if you are using an untrusted app!")
    if choice == 'Enter':
        context = import_isolated.default_context()
        context.ensure_started()
        untrusted = context.load_module('untrusted', path=['.'])

if __name__ == '__main__':
    pakvenv()
