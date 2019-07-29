import math
import shutil
from pathlib import Path

import click


# noinspection PyTypeChecker
import cv2


@click.command()
@click.argument('directory', type=click.Path(exists=True, dir_okay=True, file_okay=False))
@click.option('-s', '--split', default=0.2, help='Split ratio of train and validation')
def cmd(directory, split):
    if not 0.0 < split < 1.0:
        raise click.BadParameter('The split ratio must be greater than 0 and less than 1.')

    target_dir_path = Path(directory)
    all_jpg_path = list(target_dir_path.glob('*.jpg'))
    all_jpg_num: int = len(all_jpg_path)
    val_num: int = math.floor(all_jpg_num * split)
    click.secho(
        f'{all_jpg_num} JPG files will be split into {all_jpg_num - val_num} train data and {val_num} validation data.',
        fg='green')

    dataset_path = target_dir_path.parent / 'dataset'
    if dataset_path.exists():
        shutil.rmtree(dataset_path)  # Delete 'dataset' before splitting.
    train_path = dataset_path / 'train'
    val_path = dataset_path / 'val'
    test_path = dataset_path / 'test'

    ''' Create directories '''
    dataset_path.mkdir(exist_ok=True)
    train_path.mkdir(exist_ok=True)
    val_path.mkdir(exist_ok=True)
    test_path.mkdir(exist_ok=True)

    ''' Copy '''
    for idx, img_path in enumerate(all_jpg_path[:val_num]):
        shutil.copy(img_path, val_path / f'{idx:03}.jpg')
    for idx, img_path in enumerate(all_jpg_path[val_num:]):
        shutil.copy(img_path, train_path / f'{idx:03}.jpg')
    for idx, img_path in enumerate(Path('data/test').glob('*.jpg')):
        shutil.copy(img_path, test_path / f'{idx:03}.jpg')

    ''' Check '''
    for img in dataset_path.glob('**/*.jpg'):
        checking = cv2.imread(str(img))
        height, width, ch = checking.shape
        click.secho(f'Height: {height} Width: {width} Channel: {ch}', fg='cyan')
        if ch != 3:
            click.secho(f'Channel Error: {checking}', fg='red')

    ''' Archive '''
    shutil.make_archive(dataset_path, format='zip', root_dir=dataset_path)

    click.secho(f'{dataset_path}.zip was created.', fg='blue')


if __name__ == '__main__':
    cmd()
