import click
import requests
import subprocess
import os
import json
from pathlib import Path
import time

GITHUB_API_URL = "https://api.github.com"
VERSION = "1.0.2"
CONFIG_FILE = Path.home() / ".tempclone_config"

ASCII_ART = r"""
 /$$$$$$$$ /$$$$$$ /$$     /$$ /$$$$$$      /$$$$  /$$      /$$$$$  /$$  /$$ /$$$$$$
|__  $$__/| $$___/| $$$   /$$$| $$_  $$    /$$_ $$| $$     /$$_  $$| $$ | $$| $$___/
   | $$   | $$    | $$$$  $$$$| $$ \ $$   | $$ \_/| $$    | $$ \ $$| $$$| $$| $$    
   | $$   | $$$$  | $$ $$/$ $$| $$$$$$/   | $$    | $$    | $$ | $$| $$$$ $$| $$$$  
   | $$   | $$_/  | $$  $$| $$| $$___/    | $$    | $$    | $$ | $$| $$ $$$$| $$_/  
   | $$   | $$$$$$| $$ \/ | $$| $$        |  $$$$/| $$$$$$|  $$$$$/| $$\  $$| $$$$$$
   |__/   |______/|__/    |__/|__/         \____/ |______/ \_____/ |__/ \__/|______/
"""

def get_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}
    else:
        return {}

def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)

@click.group()
@click.version_option(version=VERSION, prog_name="tempclone", message=ASCII_ART + f"\nVersion: {VERSION}")
def cli():
    """CLI to automate the creation of new projects from GitHub templates."""
    pass

@click.command()
def configure():
    """Configure GitHub access token and user nickname.

    For more information on managing your personal access tokens, visit:
    https://docs.github.com/en/authentication/
    """
    token = click.prompt('Please enter your GitHub access token', hide_input=True)
    nickname = click.prompt('Please enter your GitHub nickname')
    
    config = get_config()
    config['token'] = token
    config['nickname'] = nickname
    save_config(config)
    click.echo("Configuration saved successfully.")

@click.command()
def list_templates():
    """List available templates on GitHub."""
    config = get_config()
    token = config.get('token')
    if not token:
        click.echo("Token not found. Run 'tempclone configure' to set up your access token.")
        return

    headers = {
        "Authorization": f"token {token}"
    }
    owner = click.prompt('Please enter the template repository owner (user or organization)', default=config.get('nickname'))

    templates = []
    page = 1
    while True:
        url = f"{GITHUB_API_URL}/users/{owner}/repos?page={page}&per_page=100"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            click.echo(f"Error listing templates: {response.json()}")
            return

        repos = response.json()
        if not repos:
            break

        templates.extend([repo['name'] for repo in repos if repo.get('is_template')])
        page += 1

    click.echo("Available templates:")
    for template in templates:
        click.echo(f"- {template}")

@click.command()
@click.argument('new_repo_name')
def new_project(new_repo_name):
    """Create a new project from a template."""
    config = get_config()
    token = config.get('token')
    if not token:
        click.echo("Token not found. Run 'tempclone configure' to set up your access token.")
        return

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.baptiste-preview+json"
    }

    owner = click.prompt('Please enter the template repository owner (user or organization)', default=config.get('nickname'))
    
    templates = []
    page = 1
    while True:
        url = f"{GITHUB_API_URL}/users/{owner}/repos?page={page}&per_page=100"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            click.echo(f"Error listing templates: {response.json()}")
            return

        repos = response.json()
        if not repos:
            break

        templates.extend([repo for repo in repos if repo.get('is_template')])
        page += 1

    click.echo("Available templates:")
    for i, template in enumerate(templates, 1):
        click.echo(f"{i}. {template['name']}")

    template_index = click.prompt("Select the template by number", type=int)
    template_repo = templates[template_index - 1]

    new_repo_data = {
        "owner": owner,
        "name": new_repo_name,
        "private": False  # or True if you want the repository to be private
    }

    create_url = f"{GITHUB_API_URL}/repos/{owner}/{template_repo['name']}/generate"
    response = requests.post(create_url, headers=headers, json=new_repo_data)
    
    if response.status_code == 201:
        new_repo = response.json()
        new_repo_clone_url = new_repo['clone_url'].replace('.git', '')  # Remove .git extension
        click.echo(f'New repository created: {new_repo_clone_url}')

        # Pause and check if the repository is ready
        click.echo('Waiting for the repository to be configured...')
        time.sleep(5)

        for _ in range(5):  # Try 5 times
            click.echo(f'Checking repository status: {new_repo_clone_url}')  # Debug output
            api_repo_url = new_repo_clone_url.replace('https://github.com/', 'https://api.github.com/repos/')
            response = requests.get(api_repo_url, headers=headers)
            if response.status_code == 200 and response.json().get('size') > 0:
                break
            click.echo('Waiting for the repository to be populated...')
            time.sleep(10)

        # Clone the new repository
        click.echo(f'Cloning the repository: {new_repo_clone_url}')
        subprocess.run(['git', 'clone', f"{new_repo_clone_url}.git", new_repo_name])

        click.echo(f"Project {new_repo_name} successfully set up!")
    else:
        click.echo(f"Error creating repository: {response.json()}")

cli.add_command(configure)
cli.add_command(list_templates)
cli.add_command(new_project)

if __name__ == '__main__':
    cli()
