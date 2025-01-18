import os
import click
import base64
import requests
import sys
import subprocess
from process_isolation import import_isolated
import pycdlib

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
@click.option('--choice', type=click.Choice(['Enter', 'Dont enter']), prompt='Enter your choice')
def pakvenv(choice):
    print("You are about to enter a virtual environment in Pakbox, ONLY use this if you are using an untrusted app!")
    if choice == 'Enter':
        context = import_isolated.default_context()
        context.ensure_started()
        untrusted = context.load_module('untrusted', path=['.'])
    elif choice == 'Dont enter':
        print("Exiting...")
        sys.exit()

def createiso(folder_path, iso_name):
    # Initialize a new ISO object
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=4)

    # Add a directory to the ISO
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            iso_path = os.path.relpath(file_path, folder_path).replace(os.sep, '/')
            iso.add_file(file_path, iso_path)
    
    # Write the ISO to a file
    iso.write(f'{iso_name}.iso')
    iso.close()
    print(f"ISO created as {iso_name}.iso")

def open_file(file_path):
    if sys.platform == "win32":
        # For Windows
        subprocess.Popen(f'explorer /select,"{file_path}"')
    else:
        # For macOS and Linux
        os.system(f'open --reveal -- {file_path}')

def execute_user_command():
    command = input("Enter the command you want to execute: ")
    os.system(command)

if __name__ == '__main__':
    user = input("Enter the GitHub username: ")
    repo_name = input("Enter the repository name: ")
    path_to_file = input("Enter the path to the file: ")
    install(user, repo_name, path_to_file)
    pakvenv()
    folder_path = input("Enter the path to the folder you want to add to the ISO: ")
    iso_name = input("Enter the name of the ISO file: ")
    createiso(folder_path, iso_name)
    open_file_path = input("Enter the file path to open: ")
    open_file(open_file_path)
    execute_user_command()
