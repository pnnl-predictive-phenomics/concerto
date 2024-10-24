import cobra
import logging
import pandas as pd
import pathlib
from concerto.utils import load_universal_model

_log = logging.getLogger()

_path = pathlib.Path(__file__).parent
_f_path = _path.joinpath('plate_to_bigg.csv').__str__()


def add_biolog_exchanges(model):
    """ Add missing BioLog exchanges to cobra model

    Adds missing BioLog exchanges from the plate to a cobra model. It grabs the
    reactions for the universal model, which should pull all annotations as
    well as metabolite information.


    Parameters
    ----------
    model : cobra.Model

    Returns
    -------
    cobra.Model
    """
    new_model = model
    not_found = set()
    added = set()

    # load in material needed to add biolog exchanges
    universal_model = load_universal_model()
    biolog_map = pd.read_csv(_f_path, index_col=False)

    for rxn in biolog_map.exchange:
        if rxn not in new_model.reactions:
            if rxn in universal_model.reactions:
                added.add(rxn)
                current_rxn = universal_model.reactions.get_by_id(rxn)
                metabolite = current_rxn.reactants[0]
                new_model.add_boundary(
                    metabolite,
                    type="exchange"
                )
            else:
                not_found.add(rxn)
    for i in not_found:
        _log.warning(f'{i} not found in universal model')
        print(f'{i} not found in universal model')
    _log.info(f"Added {len(added)} biolog exchange reactions")
    print(f"Added {len(added)} biolog exchange reactions")

    return new_model
