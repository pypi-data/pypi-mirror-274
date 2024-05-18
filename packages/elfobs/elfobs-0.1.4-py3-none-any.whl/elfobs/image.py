from importlib import resources as impresources

import pendulum
import typer
from PIL import Image, ImageDraw, ImageFont

from elfobs import OmegaConf, config, console

from . import fonts

app = typer.Typer()


def _get_date():
    tz = config['image']['timezone']
    outformat = config['image']['format']
    typedate = config['image']['date']
    if typedate == 'today':
        result = pendulum.today(tz)
    elif typedate == 'tomorrow':
        result = pendulum.tomorrow(tz)
    elif typedate == 'yesterday':
        result = pendulum.yesterday(tz)
    else:
        result = pendulum.now(tz)
    return result.format(outformat)


@app.callback()
def image():
    """
    Image Manipulation Systems
    """


@app.command()
def conf():
    """
    Show Image Configuration
    """
    console.print(OmegaConf.to_yaml(config['image']))


@app.command()
def output(show: bool = False):
    """
    Print the output that will put over image
    """
    head = config['image']['head']
    body = _get_date()
    output = head + "\n" + body
    if show:
        console.print(output)
    else:
        return output


@app.command()
def create():
    """
    Create the image
    """
    source_image = Image.open(config['image']['source'])
    draw = ImageDraw.Draw(source_image)
    conf_font = config['image']['font']
    text_size = config['image']['text_size']
    text_color = config['image']['text_color']
    font_source = impresources.files(fonts) / conf_font
    font = ImageFont.truetype(str(font_source), text_size)
    text = output()
    x = config['image']['position_x']
    y = config['image']['position_y']
    position = (x, y)
    draw.text(position, text, fill=text_color, font=font)
    source_image.save(config['image']['output'])


if __name__ == "__main__":
    app()
