from pathlib import Path

import rasterio as rio
from satsure_core.satelite.raster import create_normalised_difference_index


class TestCreateNormalisedDifferenceIndex:
    """test create normalized index"""

    def test_create_normalised_difference_index(
        self, datadir: Path, tmp_path: Path
    ) -> None:
        """
        Test the creation of a normalised difference index image.
        """
        filename_band_A = datadir / "input1.tif"
        filename_band_B = datadir / "input2.tif"

        output_name = "ndi_output.tif"
        output_path = create_normalised_difference_index(
            filename_band_A=filename_band_A,
            filename_band_B=filename_band_B,
            output_folder=tmp_path,
            output_name=output_name,
            output_format="COG",
        )
        assert Path(output_path).exists()
        with rio.open(output_path) as src:
            data = src.read(1)
            profile = src.profile
            assert profile["dtype"] == "uint8"
            assert profile["compress"] == "lzw"
            assert profile["nodata"] == 0
