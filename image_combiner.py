import subprocess
from pathlib import Path

import click


@click.command()
@click.argument('input_directory', type=click.Path(exists=True, dir_okay=True, file_okay=False))
@click.argument('output_directory', type=click.Path(exists=True, dir_okay=True, file_okay=False))
def cmd(input_directory, output_directory):
    input_directory_path = Path(input_directory)
    for idx, input_img in enumerate(input_directory_path.glob('*.jpg')):
        subprocess.run(f'convert +append data/blank_256x256.jpg {input_img} {output_directory}/{idx:03}.jpg'.split())


if __name__ == '__main__':
    cmd()
