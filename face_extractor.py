from pathlib import Path

import click
import cv2

HAAR_XML = 'venv/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml'


@click.command()
@click.argument('f', type=click.Path(exists=True))
def crop(f):
    input_path = Path(f)
    click.secho(f'Input: {input_path}', fg='green')
    cascade = cv2.CascadeClassifier(HAAR_XML)
    image_color = cv2.imread(f)
    image_grey = cv2.imread(f, 0)
    faces = cascade.detectMultiScale(image_grey)
    click.secho(f'Captured Faces: {faces}', fg='blue')
    for idx, face in enumerate(faces):
        x, y, w, h = face
        click.secho(f'Captured Face => X: {x} Y: {y} W: {w} H: {h}', fg='blue')
        output_path = input_path.parent / f'cropped_{idx:03}.jpg'
        cv2.imwrite(str(output_path), image_color[y:y + h, x:x + w])
        click.secho(f'Output: {output_path}', fg='green')


if __name__ == '__main__':
    crop()
