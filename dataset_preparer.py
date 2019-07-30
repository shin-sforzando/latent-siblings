import math
import shutil
import subprocess
from pathlib import Path

import click
import cv2

RESOLUTION = 256
BLANK_IMG_PATH: Path = Path('data/white_256x256.jpg')


# noinspection PyTypeChecker
@click.command()
@click.argument('directory', type=click.Path(exists=True, dir_okay=True, file_okay=False))
@click.option('-s', '--split', default=0.01, help='Split ratio of train and test')
def cmd(directory, split):
    if not 0.0 < split < 1.0:
        raise click.BadParameter('The split ratio must be greater than 0 and less than 1.')

    target_dir_path = Path(directory)
    all_jpg = list(target_dir_path.glob('*.jpg'))
    all_jpg_num: int = len(all_jpg)
    split_test_num: int = math.floor(all_jpg_num * split)
    prepared_test_path = Path('data/test')
    prepared_test_jpg = list(prepared_test_path.glob('*.jpg'))
    prepared_test_num: int = len(prepared_test_jpg)

    dataset_path = target_dir_path.parent / 'dataset'
    if dataset_path.exists():
        shutil.rmtree(dataset_path)  # Delete 'dataset' before splitting.
    train_path = dataset_path / 'train'
    test_path = dataset_path / 'test'

    ''' Create directories '''
    dataset_path.mkdir(exist_ok=True)
    train_path.mkdir(exist_ok=True)
    test_path.mkdir(exist_ok=True)

    ''' Copy '''
    for idx, img_path in enumerate(all_jpg[split_test_num:]):
        shutil.copy(img_path, train_path / f'{idx:03}.jpg')
    for idx, img_path in enumerate(all_jpg[:split_test_num]):
        shutil.copy(img_path, test_path / f'{idx:03}.jpg')
    for idx, img_path in enumerate(prepared_test_jpg):
        shutil.copy(img_path, test_path / f'{split_test_num + idx:03}.jpg')

    for img in dataset_path.glob('**/*.jpg'):
        ''' Normalize '''
        normalized = subprocess.run(f'mogrify -normalize {img}'.split())
        click.secho(f'Normalized: {normalized}', fg='green')

        ''' Strip EXIF '''
        stripped = subprocess.run(f'mogrify -strip {img}'.split())
        click.secho(f'Stripped: {stripped}', fg='green')

        ''' Check '''
        checking = cv2.imread(str(img))
        height, width, ch = checking.shape
        click.secho(f'{img}: {height}x{width}/{ch}[ch]', fg='cyan')
        if height != RESOLUTION:
            click.secho(f'Height Error: {checking}', fg='red')
        if width != RESOLUTION * 2:
            click.secho(f'Width Error: {checking}', fg='red')
        if ch != 3:
            click.secho(f'Channel Error: {checking}', fg='red')

    click.secho(
        f'Preprocessed {all_jpg_num} JPG files were split into {all_jpg_num - split_test_num} train data and {split_test_num} test data. And prepared {prepared_test_num} JPG were added into test data. Then {split_test_num + prepared_test_num} JPG are used for test.',
        fg='green')

    ''' Archive '''
    shutil.make_archive(dataset_path, format='zip', root_dir=dataset_path)

    click.secho(f'{dataset_path}.zip was created.', fg='blue')


if __name__ == '__main__':
    cmd()
