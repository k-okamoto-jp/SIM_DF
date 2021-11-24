import h5py
import pandas as pd
import numpy as np

hdfpath = r'sim_file/node/2704/n2704_0013_des.tdr'
datasets = ['collection/geometry_0/offset',
            'collection/geometry_0/region_0/elements_0',
            'collection/geometry_0/region_0/material_properties_0/cell angle',
            'collection/geometry_0/region_0/material_properties_0/cell dimension',
            'collection/geometry_0/region_1/elements_0',
            'collection/geometry_0/region_2/elements_0',
            'collection/geometry_0/state_0/dataset_0/values',
            'collection/geometry_0/state_0/dataset_1/values',
            'collection/geometry_0/state_0/dataset_10/values',
            'collection/geometry_0/state_0/dataset_11/values',
            'collection/geometry_0/state_0/dataset_12/values',
            'collection/geometry_0/state_0/dataset_13/values',
            'collection/geometry_0/state_0/dataset_14/values',
            'collection/geometry_0/state_0/dataset_15/values',
            'collection/geometry_0/state_0/dataset_16/values',
            'collection/geometry_0/state_0/dataset_17/values',
            'collection/geometry_0/state_0/dataset_18/values',
            'collection/geometry_0/state_0/dataset_19/values',
            'collection/geometry_0/state_0/dataset_2/values',
            'collection/geometry_0/state_0/dataset_20/values',
            'collection/geometry_0/state_0/dataset_21/values',
            'collection/geometry_0/state_0/dataset_22/values',
            'collection/geometry_0/state_0/dataset_23/values',
            'collection/geometry_0/state_0/dataset_24/values',
            'collection/geometry_0/state_0/dataset_25/values',
            'collection/geometry_0/state_0/dataset_26/values',
            'collection/geometry_0/state_0/dataset_27/values',
            'collection/geometry_0/state_0/dataset_28/values',
            'collection/geometry_0/state_0/dataset_29/values',
            'collection/geometry_0/state_0/dataset_3/values',
            'collection/geometry_0/state_0/dataset_30/values',
            'collection/geometry_0/state_0/dataset_31/values',
            'collection/geometry_0/state_0/dataset_32/values',
            'collection/geometry_0/state_0/dataset_33/values',
            'collection/geometry_0/state_0/dataset_34/values',
            'collection/geometry_0/state_0/dataset_35/values',
            'collection/geometry_0/state_0/dataset_36/values',
            'collection/geometry_0/state_0/dataset_37/values',
            'collection/geometry_0/state_0/dataset_38/values',
            'collection/geometry_0/state_0/dataset_39/values',
            'collection/geometry_0/state_0/dataset_4/values',
            'collection/geometry_0/state_0/dataset_40/values',
            'collection/geometry_0/state_0/dataset_41/values',
            'collection/geometry_0/state_0/dataset_42/values',
            'collection/geometry_0/state_0/dataset_43/values',
            'collection/geometry_0/state_0/dataset_44/values',
            'collection/geometry_0/state_0/dataset_45/values',
            'collection/geometry_0/state_0/dataset_46/values',
            'collection/geometry_0/state_0/dataset_47/values',
            'collection/geometry_0/state_0/dataset_48/values',
            'collection/geometry_0/state_0/dataset_49/values',
            'collection/geometry_0/state_0/dataset_5/values',
            'collection/geometry_0/state_0/dataset_50/values',
            'collection/geometry_0/state_0/dataset_51/values',
            'collection/geometry_0/state_0/dataset_52/values',
            'collection/geometry_0/state_0/dataset_53/values',
            'collection/geometry_0/state_0/dataset_54/values',
            'collection/geometry_0/state_0/dataset_55/values',
            'collection/geometry_0/state_0/dataset_56/values',
            'collection/geometry_0/state_0/dataset_57/values',
            'collection/geometry_0/state_0/dataset_58/values',
            'collection/geometry_0/state_0/dataset_59/values',
            'collection/geometry_0/state_0/dataset_6/values',
            'collection/geometry_0/state_0/dataset_60/values',
            'collection/geometry_0/state_0/dataset_61/values',
            'collection/geometry_0/state_0/dataset_62/values',
            'collection/geometry_0/state_0/dataset_63/values',
            'collection/geometry_0/state_0/dataset_7/values',
            'collection/geometry_0/state_0/dataset_8/values',
            'collection/geometry_0/state_0/dataset_9/values',
            'collection/geometry_0/state_0/overlay_0/overlay_element_0/loop_0/vertex indices',
            'collection/geometry_0/state_0/overlay_0/overlay_element_0/vertex',
            'collection/geometry_0/state_0/overlay_1/overlay_element_0/loop_0/vertex indices',
            'collection/geometry_0/state_0/overlay_1/overlay_element_0/vertex',
            'collection/geometry_0/state_0/overlay_2/overlay_element_0/loop_0/vertex indices',
            'collection/geometry_0/state_0/overlay_2/overlay_element_0/vertex',
            'collection/geometry_0/state_0/overlay_3/overlay_element_0/loop_0/vertex indices',
            'collection/geometry_0/state_0/overlay_3/overlay_element_0/vertex',
            'collection/geometry_0/state_0/overlay_4/overlay_element_0/loop_0/vertex indices',
            'collection/geometry_0/state_0/overlay_4/overlay_element_0/vertex',
            'collection/geometry_0/state_0/string_stream_0/characters',
            'collection/geometry_0/transformation/A',
            'collection/geometry_0/transformation/b',
            'collection/geometry_0/vertex',
            'collection/pi/data'
            ]


def PrintOnlyDataset(name, obj):
    if isinstance(obj, h5py.Dataset):
        print(name)


with h5py.File(hdfpath, 'r') as f:
    f.visititems(PrintOnlyDataset)
    for dataset in datasets:
        # print('name:\t', dataset, ',\traw dataset:\t', f[dataset])
        try:
            print('max value:\t', f[dataset][()].max(),
              ',\tmin value:\t', f[dataset][()].min(), )
        except TypeError:
            print('no max/min value')
        # print('with value:\t', f[dataset][()])

pass
