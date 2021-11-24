import h5py
import pandas as pd
import numpy as np

hdfpaths = [r'sim_file/node/2704/n2704_0013_des.tdr']
datasets = {'test_column_1': 'collection/geometry_0/vertex'
            }
print('No. of HDF files:', len(hdfpaths))  # 確認用


def PrintOnlyDataset(name, obj):
    # if isinstance(obj, h5py.Dataset):
        print(name)
        # print('\t', obj)


def MakeMeasurementList(hdfpaths, datasets, save=False, output='df.h5'):
    """
    測定条件をまとめたDataFrameを作成する。

    hdfpaths: HDFファイルへのパスのリスト
    datasets: HDFファイルから抽出したい情報パスのディクショナリー。
              keyはDataFrameのコラム名。
    """

    # このheaderというディクショナリーにdatasetsで指定した情報をHDFから読み取り追加
    header = {}

    for hdfpath in hdfpaths:
        print(hdfpath)
        with h5py.File(hdfpath, 'r') as f:
            f.visititems(PrintOnlyDataset)
            for colname, dataset in datasets.items():
                # 最初のループ
                if not colname in header:
                    # 最初のループの段階ではheaderには先に定義した'path'しかない
                    # 新しいkeyとリストにいれた文字列、数字、行列をvalueとして格納
                    if colname == 'total counts':
                        header[colname] = [f[dataset][()].sum()]
                    elif colname == 'counts':
                        header[colname] = [f[dataset][()]]
                    else:
                        # 最初に文字列のデコードにトライ、ダメなら普通の数字としてトライ
                        # 値がなければnanを追加
                        print(f[dataset][()])
                        # a, b = zip(*f[dataset][()])
                        # print(a, b)
                        try:
                            header[colname] = [f[dataset][()].decode('utf-8')]
                        except AttributeError:
                            # ここはnumpy arrayをlistに変換
                            header[colname] = list(f[dataset][()])
                        except KeyError:
                            header[colname] = [np.nan]

                # 初回以降のループはディクショナリーの該当keyに入ったリストに値を追加していく
                else:
                    if colname == 'total counts':
                        header[colname].append(f[dataset][()].sum())
                    elif colname == 'counts':
                        header[colname].append(f[dataset][()])
                    else:
                        try:
                            header[colname].append(
                                f[dataset][()][0].decode('utf-8'))
                        except AttributeError:
                            header[colname].append(f[dataset][()][0])
                        except KeyError:
                            header[colname].append(np.nan)
    # ディクショナリーをDataFrameに変換
    df = pd.DataFrame(header)

    # saveオプションがTrueならHDFファイルとして保存
    if save:
        df.to_hdf(output, 'df')

    return df


sim_df = MakeMeasurementList(hdfpaths, datasets, save=False, output='df.h5')



pass
