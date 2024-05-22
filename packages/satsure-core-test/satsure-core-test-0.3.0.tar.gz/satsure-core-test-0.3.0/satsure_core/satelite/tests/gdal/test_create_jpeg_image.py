from pathlib import Path

from satsure_core.satelite.gdal import create_jpeg_image


class TestCreateJPEGImage:
    """create JPEG Images"""

    def test_create_jpeg_image(self, datadir: Path) -> None:
        """_summary_

        Args:
            datadir (Path): path of input
        """
        input_file = datadir / "input1.tif"
        output_file = datadir / "output_image.jpeg"
        create_jpeg_image(
            input_file=input_file, bands_position=("1"), output_file=str(output_file)
        )

        assert (
            output_file.suffix.lower() == ".jpg"
            or output_file.suffix.lower() == ".jpeg"
        )
        output_file.unlink()
