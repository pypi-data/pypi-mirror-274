import typer
from v4l2py.device import Device

from elfobs import OmegaConf, config, console

app = typer.Typer()


@app.callback()
def video():
    """
    Video Manipulation Systems
    """


@app.command()
def check():
    """
    Check the Video 4 Linux Device
    """
    cam = Device.from_id(config['video']['id'])
    cam.open()
    console.print(cam.info.card)
    cam.close()


@app.command()
def show():
    """
    Video Device information
    """
    cam = Device.from_id(config['video']['id'])
    cam.open()
    console.print(cam.info.card)


@app.command()
def conf():
    """
    Show Video Configuration
    """
    console.print(OmegaConf.to_yaml(config['video']))
