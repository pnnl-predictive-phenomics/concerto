import cobra
import pathlib
import logging

_log = logging.getLogger()
_path = pathlib.Path(__file__).parent

universal_model = cobra.io.load_json_model(
    _path.joinpath('universal_model_cobrapy.json').__str__()
)