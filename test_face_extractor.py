from click.testing import CliRunner

from face_extractor import crop


def test_crop():
    runner = CliRunner()
    result = runner.invoke(crop, 'data/TSKinFace/cropped_FMSD_original/0001-D.jpg')
    assert result.exit_code == 0


if __name__ == '__main__':
    test_crop()
