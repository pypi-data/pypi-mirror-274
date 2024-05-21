from pathlib import Path

from satsure_core.satelite.raster import mask_cloud


class TestMaskCloudFunction:
    """test maskthecloud"""

    def test_mask_cloud_valid_input(self, datadir: Path, tmp_path: Path) -> None:
        """Test mask_cloud function with valid input parameters.

        Args:
            datadir (Path): _description_
            tmp_path (Path): _description_
        """

        input_file = datadir / "input3.tif"
        output_name = "masked_output.tif"
        cloud_mask_bands = [datadir / "input1.tif", datadir / "input2.tif"]
        cloud_mask_threshold = [100, 150]
        target_value = 50
        level = "L1C"
        output = mask_cloud(
            input_file=input_file,
            output_folder=tmp_path,
            output_name=output_name,
            cloud_mask_bands=cloud_mask_bands,
            cloud_mask_threshold=cloud_mask_threshold,
            target_value=target_value,
            level=level,
        )
        assert output == True
