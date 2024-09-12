from .utils import parse_carbsource_growth, create_carveme_mediadb_df

import pathlib
import logging

_log = logging.getLogger()
_path = pathlib.Path(__file__).parent
import cobra


def load_universal_model():
    """
    Load the universal model from the concerto package
    """
    # this allows loading of model without need for gurobi lic.
    cobra_config = cobra.Configuration()
    orig_solver = cobra_config.solver
    cobra_config.solver = "glpk_exact"
    universal_model = cobra.io.load_json_model(
        _path.joinpath('universal_model_cobrapy.json').__str__()
    )
    cobra_config.solver = orig_solver
    return universal_model

