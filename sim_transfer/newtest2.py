import h5py
import numpy as np

a = [6, 3, 4, 5]
b = [6, 3]

print(all(i in a for i in b)) # Checks if all items are in the list
print(any(i in a for i in b)) # Checks if any item is in the list


arr = np.random.randn(1000)

with h5py.File('groups.hdf5', 'w') as f:
    g = f.create_group('Base_Group')
    d = g.create_dataset('default', data=arr)

    f.attrs['User'] = 'Me'
    f.attrs['OS'] = 'Windows'

    g.attrs['Date'] = 'today'
    g.attrs['Time'] = 'now'

    d.attrs['attr1'] = 1.0
    d.attrs['attr2'] = 22.2

    for k in f.attrs.keys():
        print('{} => {}'.format(k, f.attrs[k]))
    for k in g.attrs.keys():
        print('{} => {}'.format(k, g.attrs[k]))
    for k in d.attrs.keys():
        print('{} => {}'.format(k, d.attrs[k]))