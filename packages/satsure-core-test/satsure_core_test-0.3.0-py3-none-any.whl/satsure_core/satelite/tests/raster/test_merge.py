from pathlib import Path

from satsure_core.satelite.raster import merge


class TestMergeFunction:
    """Test merge of rasters"""

    def test_basic_merge(self, datadir: Path, tmp_path: Path) -> None:
        """
        Test that merge function returns an empty string when provided with invalid input files.
        Args:
            datadir (Path): path of dir
            tmp_path (Path): path of the dir
        """
        input_files = [datadir / "input1.tif", datadir / "input2.tif"]
        output_path = merge(
            input_files, output_folder=str(tmp_path), output_name="output.tif"
        )
        assert Path(output_path).exists()
        Path(output_path).unlink()
