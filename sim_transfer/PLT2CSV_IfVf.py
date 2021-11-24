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


def MakeIfVf(path, df_project, col, save=True, output='df_IfVf.csv'):
    print('searching IfVf_n*_des.plt files')
    pltpaths = glob.glob(path + r'\**\IfVf_n*_des.plt', recursive=True)
    print('No. of files:', len(pltpaths))  # 確認用
    # print('PLT files:', pltpaths)
    nlist_Vmax = list(df_project[col].values)
    Project_ID_list = list(df_project.index.values)
    df_IfVf = ()
    for pltpath in tqdm(pltpaths):
        with open(pltpath) as f:
            pltfile = f.read()  # ファイル終端まで全て読んだデータを返す
            f.close()
            # print(type(pltfile))

        node = int(
            search_mid_end(
                text=pltpath, text_start='IfVf_', text_mid='n',
                text_end='_des.plt')
        )

        if node in nlist_Vmax:
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
            indx = nlist_Vmax.index(node)
            df['Project_ID'] = Project_ID_list[indx]

            if pltpath == pltpaths[0]:
                df_IfVf = df
            else:
                df_IfVf = concat([df_IfVf, df])

    df_IfVf = df_IfVf.astype({'time': float})
    df_IfVf = df_IfVf.sort_values(['Project_ID', 'time'])
    df_IfVf = df_IfVf.set_index('Project_ID')

    if save:
        print('df_BV : ', df_IfVf.shape)
        df_IfVf.to_csv(output, encoding='utf_8_sig')
        print('df_IfVf.csv saved')

    return df_IfVf


if __name__ == '__main__':
    df_proj = read_csv('../df_Project.csv')
    df_proj = df_proj.set_index('Project_ID')
    df_saved = MakeIfVf(
        path=r'sim_file', df_project=df_proj, col='Vmax_n',
        save=False, output='df_IfVf.csv')
pass
