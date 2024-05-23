import pymatgen.core as mg

def pymatgen_comp(comp_input):
    # Check if the input is a string (single composition)
    if isinstance(comp_input, str):
        return [mg.Composition(comp_input)]
    # Check if the input is a list or array
    elif isinstance(comp_input, (list, tuple)):
        return [mg.Composition(x) for x in comp_input]
    else:
        raise TypeError("Input must be a string or a list/tuple of strings.")