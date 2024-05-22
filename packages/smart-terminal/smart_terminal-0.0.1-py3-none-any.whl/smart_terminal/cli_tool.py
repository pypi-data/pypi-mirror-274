import click
import subprocess
import json
import os
import ollama
from click_default_group import DefaultGroup

@click.group(cls=DefaultGroup, default='run')
def cli():
    pass

@cli.command()
@click.argument('args', nargs=-1)
def run(args):
    user_command = ' '.join(args)
    prompt = f'''Generate terminal command to {user_command}. Only respond
    with terminal command. If there are any fill-in-the-blank sections,
    surround them with square brackets: []. Include details about what
    should go inside of the blanks within the brackets.

    Here are some examples:

    Desired user command: create a new file
    Output: touch [file name]

    Desired user command: add a new file to git
    Output: git add [path to file]

    Desired user command: commit to git
    Output: git commit -m '[commit message]'
    '''

    config = load_config()
    model = config['model']
    generated_command = ollama.generate(model, prompt)['response']

    actual_command_fragments = []
    i = 0
    while i < len(generated_command):
        if generated_command[i] == '[':
            j = generated_command.find(']', i)
            input = generated_command[i + 1: j]
            value = click.prompt(input)
            actual_command_fragments.append(value)
            i = j + 1
        else:
            actual_command_fragments.append(generated_command[i])
            i += 1

    actual_command = ''.join(actual_command_fragments)
    click.echo(actual_command)

    if click.confirm('Do you want to run this command?', default=False):
        try:
            result = subprocess.run(actual_command, shell=True, check=True, text=True, capture_output=True)
            click.echo(result.stdout)
        except subprocess.CalledProcessError as e:
            click.echo(e.stderr if e.stderr else e.stdout)

@cli.command()
@click.argument('model', nargs=1, required=True)
def change(model):
    models = [m['name'].split(':')[0] for m in ollama.list()['models']]
    if model not in models:
        click.echo(f"Error: {model} is not an installed language model. Run 'ollama pull {model}' to install it.")
    else:
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        config = load_config()
        config['model'] = model
        save_config(config, config_path)
        click.echo(f"Model changed to {model}")

def load_config():
    path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(path, 'r') as file:
        return json.load(file)

def save_config(config, file_path):
    with open(file_path, 'w') as file:
        json.dump(config, file, indent=4)

cli.add_command(run)
cli.add_command(change)
