import obsws_python as obsws
import typer

from elfobs import OmegaConf, config, console

app = typer.Typer()


def _connect_to_obs(lconf):
    url = lconf['url']
    port = lconf['port']
    password = lconf['password']
    client = obsws.ReqClient(host=url, port=port, password=password, timeout=3)
    return client


@app.callback()
def obs():
    """
    OBS Manipulation Systems
    """


@app.command()
def toggle_stream():
    ws = _connect_to_obs(config['obs'])
    ws.toggle_stream()
    console.print(f"Stream Active {ws.get_stream_status().output_active}")


@app.command()
def start_stream():
    ws = _connect_to_obs(config['obs'])
    ws.start_stream()
    console.print(f"Stream Active {ws.get_stream_status().output_active}")


@app.command()
def stop_stream():
    ws = _connect_to_obs(config['obs'])
    ws.stop_stream()
    console.print(f"Stream Active {ws.get_stream_status().output_active}")


@app.command()
def stream_status():
    ws = _connect_to_obs(config['obs'])
    console.print(ws.get_stream_status().output_active)


@app.command()
def scene_list():
    ws = _connect_to_obs(config['obs'])
    console.print(ws.get_scene_list().scenes)


@app.command()
def get_current_program_scene():
    ws = _connect_to_obs(config['obs'])
    console.print(ws.get_current_program_scene().current_program_scene_name)


@app.command()
def get_current_preview_scene():
    ws = _connect_to_obs(config['obs'])
    console.print(ws.get_current_preview_scene().current_program_scene_name)


@app.command()
def version():
    ws = _connect_to_obs(config['obs'])
    console.print(ws.get_version().obs_version)


@app.command()
def conf():
    """
    Show Obs Configuration
    """
    console.print(OmegaConf.to_yaml(config['obs']))
