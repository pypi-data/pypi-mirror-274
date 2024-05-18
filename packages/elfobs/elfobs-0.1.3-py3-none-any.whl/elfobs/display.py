import subprocess
from shlex import split

import typer

from elfobs import OmegaConf, config, console

app = typer.Typer()


def process_command(cmd: str):
    output = subprocess.check_output(split(cmd)).decode("utf8")
    list_outputs = output.split('\n')
    list_providers = [
        x.lower().rstrip("\n")[x.rfind("name:") + 5:]
        for x in list_outputs[1:-1]
    ]
    return list_providers


@app.callback()
def display():
    """
    Display Manipulation Systems
    """


@app.command()
def providers():
    """
    Show Display Providers
    """
    command = "xrandr --listproviders"
    console.print(process_command(command))


@app.command()
def monitors():
    """
    Show Monitors
    """
    command = "xrandr --listmonitors"
    console.print(process_command(command))


@app.command()
def active_monitors():
    """
    Show Active Monitors
    """
    command = "xrandr --listactivemonitors"
    console.print(process_command(command))


@app.command()
def conf():
    """
    Show Display Configuration
    """
    console.print(OmegaConf.to_yaml(config['display']))
