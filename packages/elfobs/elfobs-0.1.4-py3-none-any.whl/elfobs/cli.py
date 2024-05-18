import typer

from elfobs import OmegaConf, config, console
from elfobs.display import app as display_app
from elfobs.image import app as image_app
from elfobs.obs import app as obs_app
from elfobs.sched import app as sched_app
from elfobs.sound import app as sound_app
from elfobs.video import app as video_app

app = typer.Typer()
app.add_typer(image_app)
app.add_typer(sound_app)
app.add_typer(display_app)
app.add_typer(video_app)
app.add_typer(obs_app)
app.add_typer(sched_app)


@app.callback()
def elfobs():
    """
    El Faro OBS
    """
    pass


@app.command()
def conf():
    """
    Show Global Configuration
    """
    console.print(OmegaConf.to_yaml(config))


if __name__ == "__main__":
    app()
