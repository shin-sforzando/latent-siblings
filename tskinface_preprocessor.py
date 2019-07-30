import shutil
import subprocess
import sys
from pathlib import Path

import click

SRC_DIR_PATH = Path('data/TSKinFace/cropped_FMSD_original')
PRE_DIR_PATH = Path('data/TSKinFace/preprocessed')
OUT_DIR_PATH = Path('data/TSKinFace/combined')
RESOLUTION = 256


def main():
    try:
        if subprocess.run('convert -version'.split()).returncode != 0:
            ''' Check ImageMagick'''
            click.secho('ImageMagick is not installed.', fg='red')
            sys.exit(1)

        PRE_DIR_PATH.mkdir(exist_ok=True)
        OUT_DIR_PATH.mkdir(exist_ok=True)

        for img_s in SRC_DIR_PATH.glob('*-S.jpg'):
            img_s = Path(img_s)
            img_s_no = img_s.stem.split('-')[0]
            click.secho(f'Image No.: {img_s_no}', fg='magenta')

            ''' Copy & Flop '''
            click.secho(f'Son: {img_s}', fg='blue')
            img_org_s_path: Path = PRE_DIR_PATH / f'{img_s_no}-original-S.jpg'
            click.secho(f'Copy: {shutil.copyfile(img_s, img_org_s_path)}', fg='green')
            resize_s = subprocess.run(f'mogrify -resize {RESOLUTION}x{RESOLUTION}! {img_org_s_path}'.split())
            click.secho(f'Resize: {resize_s}', fg='green')
            # img_flopped_s_path: Path = PRE_DIR_PATH / f'{img_s_no}-flopped-S.jpg'
            # flop_s = subprocess.run(f'convert -flop {img_org_s_path} {img_flopped_s_path}'.split())
            # click.secho(f'Flop: {flop_s}', fg='green')

            img_d = SRC_DIR_PATH / f'{img_s_no}-D.jpg'
            click.secho(f'Daughter: {img_d}', fg='blue')
            img_org_d_path: Path = PRE_DIR_PATH / f'{img_s_no}-original-D.jpg'
            click.secho(f'Copy: {shutil.copyfile(img_d, img_org_d_path)}', fg='green')
            resize_d = subprocess.run(f'mogrify -resize {RESOLUTION}x{RESOLUTION}! {img_org_d_path}'.split())
            click.secho(f'Resize: {resize_d}', fg='green')
            # img_flopped_d_path: Path = PRE_DIR_PATH / f'{img_s_no}-flopped-D.jpg'
            # flop_d = subprocess.run(f'convert -flop {img_org_d_path} {img_flopped_d_path}'.split())
            # click.secho(f'Flop: {flop_d}', fg='green')

            ''' Append '''
            img_osod_path: Path = OUT_DIR_PATH / f'{img_s_no}-SD.jpg'
            # img_osfd_path: Path = OUT_DIR_PATH / f'{img_s_no}-oSfD.jpg'
            osod = subprocess.run(f'convert +append {img_org_s_path} {img_org_d_path} {img_osod_path}'.split())
            click.secho(f'Append: {osod}', fg='cyan')
            # osfd = subprocess.run(f'convert +append {img_org_s_path} {img_flopped_d_path} {img_osfd_path}'.split())
            # click.secho(f'Append: {osfd}', fg='cyan')
            img_odos_path: Path = OUT_DIR_PATH / f'{img_s_no}-DS.jpg'
            # img_odfs_path: Path = OUT_DIR_PATH / f'{img_s_no}-oDfS.jpg'
            odos = subprocess.run(f'convert +append {img_org_d_path} {img_org_s_path} {img_odos_path}'.split())
            click.secho(f'Append: {odos}', fg='cyan')
            # # odfs = subprocess.run(f'convert +append {img_org_d_path} {img_flopped_s_path} {img_odfs_path}'.split())
            # # click.secho(f'Append: {odfs}', fg='cyan')
            # # img_fsod_path: Path = OUT_DIR_PATH / f'{img_s_no}-fSoD.jpg'
            # img_fsfd_path: Path = OUT_DIR_PATH / f'{img_s_no}-fSfD.jpg'
            # # fsod = subprocess.run(f'convert +append {img_flopped_s_path} {img_org_d_path} {img_fsod_path}'.split())
            # # click.secho(f'Append: {fsod}', fg='cyan')
            # fsfd = subprocess.run(f'convert +append {img_flopped_s_path} {img_flopped_d_path} {img_fsfd_path}'.split())
            # click.secho(f'Append: {fsfd}', fg='cyan')
            # # img_fdos_path: Path = OUT_DIR_PATH / f'{img_s_no}-fDoS.jpg'
            # img_fdfs_path: Path = OUT_DIR_PATH / f'{img_s_no}-fDfS.jpg'
            # # fdos = subprocess.run(f'convert +append {img_flopped_d_path} {img_org_s_path} {img_fdos_path}'.split())
            # # click.secho(f'Append: {fdos}', fg='cyan')
            # fdfs = subprocess.run(f'convert +append {img_flopped_d_path} {img_flopped_s_path} {img_fdfs_path}'.split())
            # click.secho(f'Append: {fdfs}', fg='cyan')

    except Exception as e:
        click.secho(f'Error: {e}', fg='red')
        sys.exit(1)


if __name__ == '__main__':
    main()
