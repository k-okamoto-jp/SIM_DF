import h5py
import pandas as pd
import numpy as np
import glob
import os
from tqdm import tqdm

datasets_list = []


def GetListOnlyDataset(name, obj):
    if isinstance(obj, h5py.Dataset):
        if 'offset' not in name:
            datasets_list.append(name)


def GetDictFromList(d_list, f):
    dataset_dict = {}
    for dataset in d_list:
        head_tail = os.path.split(dataset)
        if all(i in f[head_tail[0]].attrs.keys()
               for i in ['name', 'number of vertices']):
            colname = f[head_tail[0]].attrs['name'].decode('utf-8')
            vnum = f[head_tail[0]].attrs['number of vertices']
            # print(colname, dataset, vnum)
            dataset_dict[colname] = [dataset, vnum]
        if all(i in f[head_tail[0]].attrs.keys()
               for i in ['name', 'number of values']):
            colname = f[head_tail[0]].attrs['name'].decode('utf-8')
            vnum = f[head_tail[0]].attrs['number of values']
            # print(colname, dataset, vnum)
            dataset_dict[colname] = [dataset, vnum]

    return dataset_dict


def search_mid_end(text, text_start, text_mid, text_end):
    """
        text内のtext_startキーワード以降から検索を開始し、
        最初のtext_midキーワードからtext_endキーワードまでのテキストを返す。
        キーワードは含まない。
    """
    index_start = text.find(text_start)
    index_mid = text.find(text_mid, index_start + 1)
    index_end = text.find(text_end, index_mid + 1)
    ex_text = text[index_mid + 1:index_end]

    return ex_text


def TransDataXY(data):
    data_x = data[0::2]
    data_y = data[1::2]
    data_abs = [(x ** 2 + y ** 2) ** 0.5 for (x, y) in zip(data_x, data_y)]

    return data_abs


def MakeCrossSection(
        path, df_project, col_list, datasets,
        save=True, output='df_cross_section.csv'):
    """
    測定条件をまとめたDataFrameを作成する。

    hdfpaths: HDFファイルへのパスのリスト
    datasets: HDFファイルから抽出したい情報パスのディクショナリー。
              keyはDataFrameのコラム名。
    """

    # node_list[i]にi番目のcol_listのnodeデータ格納
    node_list = [list(df_project[col_list[0]].values),
                 list(df_project[col_list[1]].values),
                 list(df_project[col_list[2]].values)
                 ]

    # 空のdict作成。
    # このheaderというdictにdatasetsで指定した情報をHDFから読み取り追加
    header = {'Node_ID': [], 'X': [], 'Y': []}
    for i in range(len(datasets)):
        for j in range(len(datasets[i])):
            header[datasets[i][j]] = []

    print('searching n*_fps.tdr files')

    hdfpaths = glob.glob(path + r'\**\n*_fps.tdr', recursive=True)
    hdfpaths += glob.glob(path + r'\**\n*_0012_des.tdr', recursive=True)
    hdfpaths += glob.glob(path + r'\**\n*_0013_des.tdr', recursive=True)

    print('No. of files:', len(hdfpaths))  # 確認用
    # print('files:', hdfpaths)

    hdfpath_dict = {}
    for hdfpath in tqdm(hdfpaths):
        if 'fps' in hdfpath:
            try:
                node = int(
                    search_mid_end(
                        text=hdfpath,
                        text_start='node', text_mid='n', text_end='_fps.tdr')
                )
                if node in node_list[0]:
                    hdfpath_dict[node] = hdfpath

            except ValueError:
                pass

        if '_0012_des.tdr' in hdfpath:
            try:
                node = int(
                    search_mid_end(
                        text=hdfpath,
                        text_start='node',
                        text_mid='n',
                        text_end='_0012_des.tdr')
                )
                if node in node_list[1]:
                    hdfpath_dict[node] = hdfpath

            except ValueError:
                pass

        if '_0013_des.tdr' in hdfpath:
            try:
                node = int(
                    search_mid_end(
                        text=hdfpath,
                        text_start='node',
                        text_mid='n',
                        text_end='_0013_des.tdr')
                )
                if node in node_list[2]:
                    hdfpath_dict[node] = hdfpath

            except ValueError:
                pass

    print('\n', hdfpath_dict)

    for i in tqdm(range(len(node_list[0]))):
        if node_list[0][i] in hdfpath_dict.keys():
            with h5py.File(hdfpath_dict[node_list[0][i]], 'r') as f:
                f.visititems(GetListOnlyDataset)
                # print('\n', datasets_list)

                dataset_dict = GetDictFromList(datasets_list, f)
                row_limit = dataset_dict['geometry_0'][1]

                for colname in datasets[0]:
                    if colname in dataset_dict.keys():
                        data = list(f[dataset_dict[colname][0]][()])
                        if len(data) == row_limit:
                            if colname == 'geometry_0':
                                header[colname] += data
                                # geometry_0データはx, y に分割
                                x, y = map(list, zip(*data))
                                header['X'] += [i * 10000 for i in x]
                                header['Y'] += [i * 10000 for i in y]
                            else:
                                try:
                                    header[colname] += data
                                except KeyError:
                                    header[colname] += [np.nan] * row_limit
                        else:
                            header[colname] += [np.nan] * row_limit
                    else:
                        header[colname] += [np.nan] * row_limit

                header['Node_ID'] += [node_list[0][i]] * row_limit

            if node_list[1][i] in hdfpath_dict.keys():
                with h5py.File(hdfpath_dict[node_list[1][i]], 'r') as f:
                    datasets_list.clear()
                    f.visititems(GetListOnlyDataset)
                    # print('\n', datasets_list)

                    dataset_dict = GetDictFromList(datasets_list, f)

                    for colname in datasets[1]:
                        if colname[:-5] in dataset_dict.keys():
                            data = list(f[dataset_dict[colname[:-5]][0]][()])
                            if len(data) == row_limit:
                                try:
                                    header[colname] += data
                                except KeyError:
                                    header[colname] += [np.nan] * row_limit

                            elif colname == 'TotalCurrentDensity_@_Vf':
                                header['TotalCurrentDensity_@_Vf'] += \
                                    TransDataXY(data)

                            elif colname == 'ElectricField_@_Vf':
                                header['ElectricField_@_Vf'] += \
                                    TransDataXY(data)

                            else:
                                header[colname] += [np.nan] * row_limit
                        else:
                            header[colname] += [np.nan] * row_limit
            else:
                for colname in datasets[1]:
                    header[colname] += [np.nan] * row_limit

            if node_list[2][i] in hdfpath_dict.keys():
                with h5py.File(hdfpath_dict[node_list[2][i]], 'r') as f:
                    datasets_list.clear()
                    f.visititems(GetListOnlyDataset)
                    # print('\n', datasets_list)

                    dataset_dict = GetDictFromList(datasets_list, f)

                    for colname in datasets[2]:
                        if colname[:-5] in dataset_dict.keys():
                            data = list(f[dataset_dict[colname[:-5]][0]][()])
                            if len(data) == row_limit:
                                try:
                                    header[colname] += data
                                except KeyError:
                                    header[colname] += [np.nan] * row_limit

                            elif colname == 'TotalCurrentDensity_@_Vr':
                                header['TotalCurrentDensity_@_Vr'] += \
                                    TransDataXY(data)

                            elif colname == 'ElectricField_@_Vr':
                                header['ElectricField_@_Vr'] += \
                                    TransDataXY(data)

                            else:
                                header[colname] += [np.nan] * row_limit
                        else:
                            header[colname] += [np.nan] * row_limit
            else:
                for colname in datasets[2]:
                    header[colname] += [np.nan] * row_limit
        lens = map(len, header.values())
        if len(set(lens)) != 1:
            print('lengths are different at node ', np.str(node_list[0][i]))
            quit()

    # ディクショナリーをDataFrameに変換
    df = pd.DataFrame(header)
    df = df.drop('geometry_0', axis=1)
    df = df.sort_values(['Node_ID', 'X', 'Y'])
    df = df.set_index('Node_ID')

    df = df.round({
        'X': 4,
        'Y': 4,
        'AlActive': 0,
        'AlTotal': 0,
        'NActive': 0,
        'NTotal': 0,
        'PActive': 0,
        'PTotal': 0,
        'ElectrostaticPotential_@_Vf': 2,
        'ElectrostaticPotential_@_Vr': 2,
    })

    # saveオプションがTrueならHDFファイルとして保存
    if save:
        print('df_cross_section : ', df.shape)
        df.to_csv(output, encoding='utf_8_sig')
        print('df_cross_section.csv saved')

    return df


if __name__ == '__main__':
    df_proj = pd.read_csv('sim_file/df_Project.csv')
    datasets_l = [
        ['geometry_0', 'AlActive', 'AlTotal', 'NActive', 'NTotal', 'NetActive',
         'PActive', 'PTotal'],
        ['DopingConcentration_@_Vf', 'TotalCurrentDensity_@_Vf',
         'ElectricField_@_Vf', 'ElectrostaticPotential_@_Vf',
         'eDensity_@_Vf', 'hDensity_@_Vf'],
        ['DopingConcentration_@_Vr', 'TotalCurrentDensity_@_Vr',
         'ElectricField_@_Vr', 'ElectrostaticPotential_@_Vr',
         'eDensity_@_Vr', 'hDensity_@_Vr', 'ImpactIonization_@_Vr']
    ]
    col_l = ['Device_Mesh2_n', 'Vmax_n', 'BVmax_n']

    df_cross_section = MakeCrossSection(
        path=r'sim_file', df_project=df_proj, col_list=col_l,
        datasets=datasets_l, save=False, output=r'df_cross_section.csv')

pass
