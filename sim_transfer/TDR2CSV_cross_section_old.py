import h5py
import pandas as pd
import numpy as np
import glob
from tqdm import tqdm


def PrintOnlyDataset(name, obj):
    if isinstance(obj, h5py.Dataset):
        print(name)
        print('\t', obj)


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


def MakeCrossSection(
        path, df_project, col, datasets,
        save=True, output='df_cross_section.csv'):
    """
    測定条件をまとめたDataFrameを作成する。

    hdfpaths: HDFファイルへのパスのリスト
    datasets: HDFファイルから抽出したい情報パスのディクショナリー。
              keyはDataFrameのコラム名。
    """
    print('searching n*_fps.tdr files')
    hdfpaths = glob.glob(path + r'\**\n*_fps.tdr', recursive=True)
    print('No. of files:', len(hdfpaths))  # 確認用
    # print('files:', hdfpaths)
    nlist_Device_Mesh2 = df_project[col].values

    # このheaderというディクショナリーにdatasetsで指定した情報をHDFから読み取り追加
    header = {'Node_ID': []}

    for hdfpath in tqdm(hdfpaths):

        try:
            node = int(
                search_mid_end(
                    text=hdfpath,
                    text_start='node', text_mid='n', text_end='_fps.tdr')
            )
        except ValueError:
            node = 0.1

        if node in nlist_Device_Mesh2:
            # print(hdfpath)
            with h5py.File(hdfpath, 'r') as f:
                # f.visititems(PrintOnlyDataset)

                for colname, dataset in datasets.items():
                    # 最初のループ
                    if colname not in header:
                        # 最初のループの段階ではheaderには先に定義した'path'しかない
                        # 新しいkeyとリストにいれた文字列、数字、行列をvalueとして格納
                        if colname == 'Position':
                            header[colname] = list(f[dataset][()])
                            # Positionデータはx, y に分割
                            x, y = map(list, zip(*f[dataset][()]))
                            header['X'] = [i * 10000 for i in x]
                            header['Y'] = [i * 10000 for i in y]

                        else:
                            # 最初に文字列のデコードにトライ、ダメなら普通の数字としてトライ
                            # 値がなければnanを追加
                            # print(f[dataset][()])
                            try:
                                header[colname] = \
                                    [f[dataset][()].decode('utf-8')]
                            except AttributeError:
                                # ここはnumpy arrayをlistに変換
                                header[colname] = list(f[dataset][()])
                                print(header[colname])
                            except KeyError:
                                header[colname] = [np.nan] * len(x)

                    # 初回以降のループはディクショナリーの該当keyに入ったリストに値を追加していく
                    else:
                        if colname == 'Position':
                            header[colname] += list(f[dataset][()])
                            # Positionデータはx, y に分割
                            x, y = map(list, zip(*f[dataset][()]))
                            header['X'] += [i * 10000 for i in x]
                            header['Y'] += [i * 10000 for i in y]
                        else:
                            try:
                                header[colname] += \
                                    [f[dataset][()].decode('utf-8')]
                            except AttributeError:
                                header[colname] += list(f[dataset][()])
                            except KeyError:
                                header[colname] += [np.nan] * len(x)

                header['Node_ID'] += [node] * len(x)

            # print('done')

    # ディクショナリーをDataFrameに変換
    df = pd.DataFrame(header)
    df = df.drop('Position', axis=1)
    df = df.sort_values(['Node_ID', 'X', 'Y'])
    df = df.set_index('Node_ID')

    # saveオプションがTrueならHDFファイルとして保存
    if save:
        print('df_cross_section : ', df.shape)
        df.to_csv(output, encoding='utf_8_sig')
        print('df_cross_section.csv saved')

    return df


if __name__ == '__main__':
    df_proj = pd.read_csv('sim_file/df_Project.csv')
    datasets_list = \
        {'Position': 'collection/geometry_0/vertex',
         'AlActive': 'collection/geometry_0/state_0/dataset_7/values',
         'AlTotal': 'collection/geometry_0/state_0/dataset_3/values',
         'NActive': 'collection/geometry_0/state_0/dataset_6/values',
         'NTotal': 'collection/geometry_0/state_0/dataset_5/values',
         'NetActive': 'collection/geometry_0/state_0/dataset_0/values',
         'PActive': 'collection/geometry_0/state_0/dataset_4/values',
         'PTotal': 'collection/geometry_0/state_0/dataset_2/values',
         }

    df_cross_section = MakeCrossSection(
        path=r'sim_file', df_project=df_proj, col='Device_Mesh2_n',
        datasets=datasets_list, save=False, output=r'df_cross_section.csv')

pass
