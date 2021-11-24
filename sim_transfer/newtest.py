import h5py
import os


filename = r'sim_file/node/1370/n1370_fps.tdr'
dataset = 'collection/geometry_0/state_0/dataset_6/values'


def PrintOnlyDataset(name, obj):
    if isinstance(obj, h5py.Dataset):
        print(name)
        head_tail = os.path.split(name)
        print(head_tail[0])
        if 'name' in f[head_tail[0]].attrs.keys():
            print(f[head_tail[0]].attrs['name'].decode('utf-8'))
        print('\t', obj)


with h5py.File(filename, "r") as f:
    # List all groups
    print(f.items())
    print(f.visititems(PrintOnlyDataset))
    print(f.keys())
    print(f['collection'].keys())
    print(f['collection']['tag_group_0'].keys())
    print(f['collection']['tag_group_0']['tag_group_0'].keys())
    print(f['collection']['tag_group_0']['tag_group_0']['tag_group_0'].keys())
    print(f['collection']['tag_group_0']['tag_group_0']['tag_group_0']['tag_20'])
    # print(f['collection']['tag_group_0']['tag_group_0'][()])


    print('-----------------')
    print(f['collection'].attrs.keys())
    print(f['collection/geometry_0/'].attrs.keys())
    for k in f['collection/geometry_0/'].attrs.keys():
        print('{} => {}'.format(k, f['collection/geometry_0/'].attrs[k]))
    print(f['collection/geometry_0/vertex'].attrs.keys())
    print('-----------------')
    print(f['collection/geometry_0/state_0/dataset_5/'].attrs.keys())
    for k in f['collection/geometry_0/state_0/dataset_5/'].attrs.keys():
        print('{} => {}'.format(k, f['collection/geometry_0/state_0/dataset_5/'].attrs[k]))

    print('-----------------')
    print(f['collection/geometry_0/state_0/dataset_1/'].attrs.keys())
    for k in f['collection/geometry_0/state_0/dataset_1/'].attrs.keys():
        print('{} => {}'.format(k, f['collection/geometry_0/state_0/dataset_1/'].attrs[k]))
    print(len(f['collection/geometry_0/state_0/dataset_1/values'][()]))


    # a_group_9key = list(f['collection']['tag_group_0']['tag_0'].keys())[0]

    # Get the data
    # data = list(f['collection']['tag_group_0']['tag_0'][a_group_key])

pass