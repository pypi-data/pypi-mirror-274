import alsaaudio
import typer

from elfobs import OmegaConf, config, console

app = typer.Typer()


@app.callback()
def sound():
    """
    Sound Manipulation Systems
    """


@app.command()
def playback():
    """
    List of playback devices
    """
    devices = alsaaudio.pcms(pcmtype=alsaaudio.PCM_PLAYBACK)
    console.print(devices)


@app.command()
def capture():
    """
    List of capture devices
    """
    devices = alsaaudio.pcms(pcmtype=alsaaudio.PCM_CAPTURE)
    console.print(devices)


@app.command()
def cards():
    """
    List of sound cards
    """
    devices = alsaaudio.cards()
    console.print(devices)


@app.command()
def mixer():
    """
    Mixer information
    """
    devices = alsaaudio.Mixer()
    console.print("Card Name: ", devices.cardname())
    console.print("Mixer: ", devices.mixer())
    console.print("Mixer ID: ", devices.mixerid())
    console.print("Mixer Capability: ", devices.getenum())
    console.print("Volume: ", devices.getvolume())


@app.command()
def conf():
    """
    Show Sound Configuration
    """
    console.print(OmegaConf.to_yaml(config['sound']))
