from pathlib import Path

import rasterio
from satsure_core.satelite.gdal import reproject


class TestReprojectRaster:
    """test reproject of the raster"""

    def test_reproject_raster(self, datadir: Path) -> None:
        """_summary_

        Args:
            datadir (Path): _description_
            tmp_path (Path): _description_
        """

        input_file = datadir / "input1.tif"
        output_file = datadir / "output_reproject.tif"
        target_crs = "EPSG:4326"
        reproject(input_file=input_file, output_file=output_file, target_crs=target_crs)
        with rasterio.open(output_file) as src:
            assert src.crs.to_string() == target_crs
        Path(output_file).unlink()
