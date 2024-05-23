import numpy as np
import pickle
from importlib.resources import path
from composition_vectorizer.utilities import pymatgen_comp

with path('composition_vectorizer.orderings', '1d_orderings.pkl') as path:
    with open(path, 'rb') as fid:
        orders_dict = pickle.load(fid)


def featurizer_1d(comps, order, el_list = []):
        if order not in ['alphabet','periodic','pettifor','m-pettifor','user']:
           raise ValueError("order must be one of ['alphabet','periodic','pettifor','m-pettifor','user']")
        
        comps = pymatgen_comp(comps)
        if order in ['alphabet','periodic','pettifor','m-pettifor']:
            if len(el_list) == 0:
                for c in comps:
                    el_list += list(c.get_el_amt_dict().keys())
                el_list = list(set(el_list))
            eles = np.array(sorted(el_list,key = lambda x : orders_dict[order].index(x)))
        elif order == 'user' and len(el_list)!=0:
            eles = np.array(el_list)
        else:
            raise ValueError('user defined order needs to be followed by the list of elements')

        all_vecs = np.zeros([len(comps), len(eles)])
        for i, c in enumerate(comps):
            for k, v in c.get_el_amt_dict().items(): 
                j = np.argwhere(eles == k)
                all_vecs[i, j] = v

        all_vecs = all_vecs / np.sum(all_vecs, axis=1).reshape(-1, 1)
        all_vecs = np.array(all_vecs, dtype=np.float32)

        return (all_vecs,eles)

def decode_comp(val_list,order):
    return [''.join([f'{order[i]}{x[i]}' for i in range(len(order)) if x[i]!=0])for x in val_list]


