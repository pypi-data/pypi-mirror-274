from pathlib import Path

import rasterio
from satsure_core.satelite.raster import resample_file


class TestOffsetFile:
    """Offset the file"""

    def test_resample_file(self, datadir: Path) -> None:
        """Test the offset_file function"""
        input_file = datadir / "input1.tif"
        output_file = datadir / "input1.tif"
        resample_file(input_file=str(input_file), output_file=str(input_file))
        expected_pixel_width = 10
        expected_pixel_height = 10

        with rasterio.open(output_file) as src:
            assert src.count == 1
            assert src.res == (expected_pixel_width, expected_pixel_height)
