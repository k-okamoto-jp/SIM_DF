import glob
from pandas import read_csv, DataFrame, concat
from tqdm import tqdm


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


def MakeBV(path, df_project, col='BVmax_n', save=True, output='df_BV.csv'):
    print('searching BV_n*_des.plt files')
    pltpaths = glob.glob(path + r'\**\BV_n*_des.plt', recursive=True)
    print('No. of files:', len(pltpaths))  # 確認用
    # print('PLT files:', pltpaths)
    nlist_BVmax = list(df_project[col].values)
    Project_ID_list = list(df_project.index.values)
    df_BV = ()
    for pltpath in tqdm(pltpaths):
        with open(pltpath) as f:
            pltfile = f.read()  # ファイル終端まで全て読んだデータを返す
            f.close()
            # print(type(pltfile))

        node = int(
            search_mid_end(
                text=pltpath, text_start='BV_',
                text_mid='n', text_end='_des.plt')
        )

        if node in nlist_BVmax:
            dataset = search_mid_end(
                text=pltfile, text_start='dataset', text_mid='[', text_end=']')
            dataset_list = dataset \
                .replace('\n', '').replace(' ', '').replace('"', '\t').split()
            # print(dataset_list)

            data = search_mid_end(
                text=pltfile, text_start='Data', text_mid='{', text_end='}')
            data_list = data.split()
            # print(data_list)

            data_multi_list = \
                [[data_list[i * len(dataset_list) + j]
                  for j in range(0, len(dataset_list))]
                 for i in range(0,
                                int(len(data_list) / len(dataset_list)))]
            df = DataFrame(data=data_multi_list, columns=dataset_list)
            indx = nlist_BVmax.index(node)
            df['Project_ID'] = Project_ID_list[indx]

            if pltpath == pltpaths[0]:
                df_BV = df
            else:
                df_BV = concat([df_BV, df])

    df_BV = df_BV.astype({'time': float})
    df_BV = df_BV.sort_values(['Project_ID', 'time'])
    df_BV = df_BV.set_index('Project_ID')

    if save:
        print('df_BV : ', df_BV.shape)
        df_BV.to_csv(output, encoding='utf_8_sig')
        print('df_BV.csv saved')

    return df_BV


if __name__ == '__main__':
    df_proj = read_csv('../df_Project.csv')
    df_proj = df_proj.set_index('Project_ID')
    df_saved = MakeBV(
        path=r'sim_file', df_project=df_proj, col='BVmax_n',
        save=False, output='df_BV.csv')
pass
