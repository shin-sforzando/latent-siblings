from pathlib import Path

import click
import cv2

'''
OpenCV HAAR XML Default Options

* venv/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml
* venv/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_alt.xml
* venv/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_alt2.xml
* venv/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_alt_tree.xml
* venv/lib/python3.7/site-packages/cv2/data/haarcascade_profileface.xml
'''

HAAR_XML = 'venv/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml'
INTERPOLATIONS = ['INTER_LINEAR', 'INTER_AREA', 'INTER_NEAREST', 'INTER_CUBIC', 'INTER_LANCZOS4']


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Face Extractor Version 1.0')
    ctx.exit()


@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('-r', '--resolution', type=int, default=64, show_default=True, help='Resolution to Export')
@click.option('-i', '--interpolation', type=click.Choice(INTERPOLATIONS), default=INTERPOLATIONS[4], show_default=True,
              help='Method of Interpolation')
@click.option('--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
def crop(input_path, resolution, interpolation):
    click.secho(f'Input: {input_path}', fg='green')
    resolution = (resolution, resolution)
    click.secho(f'Target Resolution: {resolution} [px]', fg='green')
    click.secho(f'Interpolation Method: {interpolation}', fg='green')
    cascade = cv2.CascadeClassifier(HAAR_XML)
    image_color = cv2.imread(input_path)
    image_grey = cv2.imread(input_path, 0)
    faces = cascade.detectMultiScale(image_grey)
    click.secho(f'Captured Faces: {faces}', fg='blue')
    for idx, face in enumerate(faces):
        x, y, w, h = face
        click.secho(f'Captured Face => X: {x} Y: {y} W: {w} H: {h}', fg='blue')
        output_path = Path(input_path).parent / f'cropped_{idx:03}.jpg'
        image_cropped = image_color[y:y + h, x:x + w]
        image_resized = cv2.resize(image_cropped, resolution, interpolation=getattr(cv2, interpolation))
        cv2.imwrite(str(output_path), image_resized)
        click.secho(f'Output: {output_path}', fg='green')


if __name__ == '__main__':
    crop()
