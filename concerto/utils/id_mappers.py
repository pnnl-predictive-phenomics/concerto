import os.path

import pandas as pd
import pathlib
from concerto.storage import id_mapping_dir
_path = pathlib.Path(id_mapping_dir)
_chem_path =_path.joinpath('chem_xref.tsv.gz').__str__()
_reactions_path = _path.joinpath('reac_xref.tsv').__str__()


def download_metabolite_ids_xref():
    """
    This function downloads a file from the metanex website and saves it as a .tsv file.
    """
    url = 'https://www.metanetx.org/cgi-bin/mnxget/mnxref/chem_xref.tsv'
    chem_df = pd.read_csv(
        url,
        delimiter='\t',
        comment='#',
        names=['source', 'ID', 'description'],
        # engine='c'
    )
    chem_df.drop(columns=['description'], inplace=True)
    chem_df.to_csv(_chem_path, sep='\t', index=True)


def download_reaction_xref():
    url = 'https://www.metanetx.org/cgi-bin/mnxget/mnxref/reac_xref.tsv'
    reactions_df = pd.read_csv(
        url,
        delimiter='\t',
        comment='#',
        names=['source', 'ID', 'description'],
        engine='c'
    )
    reactions_df.drop(columns=['description'], inplace=True)
    reactions_df.to_csv(_reactions_path, sep='\t', index=True)


def download_reaction_properties():
    url = 'https://www.metanetx.org/cgi-bin/mnxget/mnxref/reac_prop.tsv'

    reactions_df = pd.read_csv(
        url,
        delimiter='\t',
        comment='#',
        names=['MNX_ID', 'equation',  'source_db', 'ec_number', 'equation_balanced', 'transport_reaction'],
        engine='c'
    )
    reactions_df.drop(columns=['description'], inplace=True)
    reactions_df.to_csv(_reactions_path, sep='\t', index=True)


def load_reactions_xref():
    """
    This function loads the .tsv file downloaded from the metanex website into a pandas DataFrame.
    """
    if not os.path.exists(_reactions_path):
        download_reaction_xref()
    reactions_df = pd.read_csv(
        _reactions_path,
        delimiter='\t',
        comment='#',
        names=['source', 'ID']
    )
    return reactions_df


def load_chem_xref():
    """
    This function loads the .tsv file downloaded from the metanex website into a pandas DataFrame.
    """
    if not os.path.exists(_chem_path):
        download_metabolite_ids_xref()
    return pd.read_csv(
            _chem_path,
            delimiter='\t',
            comment='#',
            names=['source', 'ID'], index_col=0,
        )


def generate_dict(df, source):
    """
    This function generates a dictionary from a DataFrame where the source column starts with a specific string.

    Parameters:
    df (DataFrame): The DataFrame to generate the dictionary from.
    source (str): The string that the source column should start with.

    Returns:
    dict: A dictionary where the keys are the IDs and the values are the sources.
    """
    source_df = df.loc[df.source.str.startswith(source)].copy()
    source_df['source'] = source_df['source'].str.lstrip(source + ':')
    source_df = source_df.loc[source_df['source'] != '']
    return source_df.set_index('ID').to_dict()['source']


def generate_id_mapping_dict(df, source, target):
    """
    This function generates a mapping dictionary from a DataFrame where the source column starts with a specific string.

    Parameters:
    df (DataFrame): The DataFrame to generate the dictionary from.
    source (str): The string that the source column should start with.
    target (str): The string that the target column should start with.

    Returns:
    dict: A dictionary where the keys are the sources and the values are the targets.
    """
    source_dict = generate_dict(df, source)
    target_dict = generate_dict(df, target)
    source_to_target = {j: target_dict[i] for i, j in source_dict.items() if i in target_dict}
    return source_to_target


class MetanexMapper:
    def __init__(self):
        self.chem_df = load_chem_xref()
        self.mnx_to_bigg = generate_id_mapping_dict(self.chem_df, 'bigg', 'mnx')
        self.bigg_to_mnx = generate_id_mapping_dict(self.chem_df, 'mnx', 'bigg')
        self.id_sources = self.chem_df.source.str.split(':').str[0].unique()

    def print_id_sources(self):
        """
        This function prints the unique sources in the DataFrame.
        """
        for id in sorted(self.id_sources):
            print(id)

    def get_bigg_id(self, mnx_id):
        """
        This function returns the BiGG ID for a given MetaNetX ID.

        Parameters:
        mnx_id (str): The MetaNetX ID for which the BiGG ID is to be retrieved.

        Returns:
        str: The BiGG ID for the given MetaNetX ID.
        """
        return self.mnx_to_bigg.get(mnx_id, None)

    def get_mnx_id(self, bigg_id):
        """
        This function returns the MetaNetX ID for a given BiGG ID.

        Parameters:
        bigg_id (str): The BiGG ID for which the MetaNetX ID is to be retrieved.

        Returns:
        str: The MetaNetX ID for the given BiGG ID.
        """
        return self.bigg_to_mnx.get(bigg_id, None)

    def generate_dict(self, source, target):
        return generate_id_mapping_dict(self.chem_df, source, target)


class ReactionMapper(object):
    def __init__(self):
        self.reactions_df = load_reactions_xref()
        self.id_sources = self.reactions_df.source.str.split(':').str[0].unique()

    def print_id_sources(self):
        """
        This function prints the unique sources in the DataFrame.
        """
        for id in sorted(self.id_sources):
            print(id)
    def generate_dict(self, source, target):
        return generate_id_mapping_dict(self.reactions_df, source, target)


if __name__ == '__main__':
    rxn_mapper = ReactionMapper()
    rxn_mapper.print_id_sources()
    dics = rxn_mapper.generate_dict('bigg.reaction', 'metacyc.reaction')
    print(dics)

