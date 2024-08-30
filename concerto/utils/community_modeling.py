import numpy as np
import tellurium as te
import pandas as pd
import libsbml
from mira.metamodel import Distribution
from mira.modeling.amr.petrinet import AMRPetriNetModel
from mira.modeling import Model
from pathlib import Path



def save_SBML_from_smetana_df(smetana_df, seed=0, initial_bounds=(0,1), smbl_file='test_SBML.xml'):
    """
    Create an Antimony string based on the data in smetana_df and save it as an SBML (.xml) file.

    For each row of the smetana data:
    - donor-to-compound reaction: donor -> compound; rate: k_d*donor    
    - compound-to-receiver reaction: compound -> receiver; k_r*compound
    - use uniform initial values for the model variables (donor, compound, receiver)
    - k_d = scs and k_r = mus for that row 
    """
    np.random.seed(seed)

    reaction_list = []
    parameter_list = []
    initial_values_set = set()

    for index, row in smetana_df.iterrows():
        donor_reaction = f'\t{row.donor} -> {row.compound}; k_d{index}*{row.donor}'
        receiver_reaction = f'\t{row.compound} -> {row.receiver}; k_r{index}*{row.compound}'
        reaction_list.extend([donor_reaction, receiver_reaction])
        parameter_list.extend([f'\tk_d{index}={row.scs}', f'\tk_r{index}={row.mus}'])
        initial_values_set.add(row.donor)
        initial_values_set.add(row.compound)
        initial_values_set.add(row.receiver)

    initial_values_string = "\n".join([f"\t{name}={np.random.uniform(initial_bounds[0],initial_bounds[1])}" for name in initial_values_set])
    species_names_string = "\n".join([f'\t{species} is "{species}"' for species in initial_values_set])

    reaction_string = "\n".join(reaction_list)
    parameter_string = "\n".join(parameter_list)

    antimony_str = f"""
    model smetana
    {reaction_string}
    {parameter_string}
    {initial_values_string}
    {species_names_string}
    end
    """
    
    rr_model = te.loada(antimony_str)
    rr_model.exportToSBML(smbl_file)


# def update_SBML_for_MIRA(original_sbml_file, updated_sbml_file):
#     """Updates the SBML file to ensure that the species name, initial concentrations, and has_only_substance_units are set."""
#     d = libsbml.readSBMLFromFile(original_sbml_file)
#     m = d.getModel()
#     for species in m.getListOfSpecies():
#         print(f"species name: {species.name}, id: {species.id}, initial_concentration: {species.initial_concentration}, initial_amount: {species.initial_amount}, has_only_substance_units: {species.has_only_substance_units}")
        
#         species.name = species.id
#         species.initial_concentration = species.initial_amount
#         species.has_only_substance_units = False
#         print(f"species name: {species.name}, id: {species.id}, initial_concentration: {species.initial_concentration}, initial_amount: {species.initial_amount}, has_only_substance_units: {species.has_only_substance_units}")
#     libsbml.writeSBMLToFile(d,updated_sbml_file)
def update_SBML_for_MIRA(original_sbml_file, updated_sbml_file):
    """Updates the SBML file to ensure that the species name, initial concentrations, and has_only_substance_units are set."""
    
    # Read the SBML file
    document = libsbml.readSBMLFromFile(original_sbml_file)
    model = document.getModel()
    
    for species in model.getListOfSpecies():
        # Check if species has a valid ID
        if not species.isSetId() or not species.getId():
            raise ValueError("A species found without a valid ID.")
        
        # Set the species name to the ID if the name is not valid
        if not species.isSetName() or not species.getName():
            species.setName(species.getId())
        
        # Set initial concentration using initial amount if not already valid
        if not species.isSetInitialConcentration() or species.getInitialConcentration() <= 0:
            if species.isSetInitialAmount() and species.getInitialAmount() >= 0:
                species.setInitialConcentration(species.getInitialAmount())
            else:
                raise ValueError(f"Species '{species.getId()}' does not have a valid initial concentration or amount.")
        
        # Set has_only_substance_units to False
        species.setHasOnlySubstanceUnits(False)
    
    # Write the updated SBML file
    libsbml.writeSBMLToFile(document, updated_sbml_file)

def set_uniform_priors_for_MIRA_model_rate_constants(mira_model, min=1e-3, max=1):
    "Assigns a uniform(min,max) distribution for rate constants (parameters starting with 'k')."

    prior_dist = Distribution(
                    type= "Uniform1",
                    parameters= {"minimum": min,"maximum": max }     
                     )

    for name,parameter in mira_model.parameters.items():
        if name.startswith('k'): # only assign priors for rate constants
            parameter.distribution = prior_dist
    return mira_model


def convert_MIRA_model_to_petrinet_AMRPetriNetModel(mira_model, petrinet_model_filename):
    "Converts a MIRA model into a PetriNet Model (.JSON) and saves it."
    # Create a Path object and remove extension
    file_path = Path(petrinet_model_filename)
    file_root = file_path.stem
    petrinet_model = AMRPetriNetModel(Model(mira_model))
    petrinet_model.to_json_file(
                petrinet_model_filename,
                name=file_root,
                description=file_root,
                indent=2,
            )