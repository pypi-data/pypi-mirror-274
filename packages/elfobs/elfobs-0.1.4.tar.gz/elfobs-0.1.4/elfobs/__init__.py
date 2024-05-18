import os

from omegaconf import OmegaConf
from rich.console import Console

console = Console()
user_home = os.path.expanduser('~')
default_config = user_home + '/.elfobs.yml'
try:
    OmegaConf.load(default_config)
except Exception:
    console.print("[white] Creating default config for ELF OBS...")
    conf_yaml = """
image:
  source: /home/aldo/Downloads/ElFaro.jpg
  date: today
  timezone: Europe/Madrid
  format: YYYY-MM-DD
  head: C/ Torres
  font: NotoSerif-Bold.ttf
  text_size: 12
  text_color: black
  position_x: 10
  position_y: 10
  output: /tmp/ElFaroWithDate.jpg
sound:
  input: alsa_input.pci-0000_00_1f.3.analog-stereo
display:
  default: None
video:
  id: 0
obs:
  url: localhost
  port: 4455
  password: Ch@ng3MENOW!.
    """
    conf = OmegaConf.create(conf_yaml)
    with open(default_config, 'w') as file:
        OmegaConf.save(config=conf, f=file)
        file.flush()
    console.print(
        f"[bold yellow] Please edit in => [bold green]{default_config}")
    console.print("[white] Enter for continue... ")
    input()
config = OmegaConf.load(default_config)
