from pathlib import Path

from satsure_core.satelite.gdal import get_projection


class TestGetProjection:
    """test get projection"""

    def test_get_projection(self, datadir: Path) -> None:
        """get the projection

        Args:
            datadir (Path): input path
        """
        input_file = datadir / "input1.tif"
        projection = get_projection(str(input_file))
        assert projection == "EPSG:32644"
