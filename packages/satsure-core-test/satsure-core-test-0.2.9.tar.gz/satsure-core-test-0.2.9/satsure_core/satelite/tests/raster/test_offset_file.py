from pathlib import Path

import rasterio
from satsure_core.satelite.raster import offset_file


class TestOffsetFile:
    """Offset the file"""

    def test_offset_file(self, datadir: Path) -> None:
        """Test the offset_file function"""
        input_file = datadir / "input1.tif"
        output_file = datadir / "input1.tif"
        offset_file(
            input_file=str(input_file), output_file=str(output_file), offset=1000
        )

        with rasterio.open(output_file) as src:
            assert src.count == 1
