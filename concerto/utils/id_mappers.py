import pandas as pd


def download_files_from_metanex():
    """
    This function downloads a file from the metanex website and saves it as a .tsv file.
    """
    url = 'https://www.metanex.org/cgi-bin/mnxget/mnxref/chem_xref.tsv'
    chem_df = pd.read_csv(
        url,
        delimiter='\t',
        comment='#',
        names=['source', 'ID', 'description']
    )
    chem_df.to_csv('chem_xref.tsv', sep='\t', index=True)

    url = 'https://www.metanetx.org/cgi-bin/mnxget/mnxref/reac_xref.tsv'
    reactions_df = pd.read_csv(
        url,
        delimiter='\t',
        comment='#',
        names=['source', 'ID', 'description']
    )
    reactions_df.to_csv('reac_xref.tsv', sep='\t', index=True)


def load_chem_xref():
    """
    This function loads the .tsv file downloaded from the metanex website into a pandas DataFrame.
    """
    chem_df = pd.read_csv(
        'chem_xref.tsv',
        delimiter='\t',
        comment='#',
        names=['source', 'ID', 'description']
    )
    return chem_df


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