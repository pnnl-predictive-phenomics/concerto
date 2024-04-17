import pathlib
import logging

_log = logging.getLogger()
_path = pathlib.Path(__file__).parent
import cobra
cobra_config = cobra.Configuration()
orig_solver = cobra_config.solver
cobra_config.solver = "glpk_exact"
universal_model = cobra.io.load_json_model(
    _path.joinpath('universal_model_cobrapy.json').__str__()
)
cobra_config.solver = orig_solver