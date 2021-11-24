from pandas import read_csv


def MakeProject(path, save=True):
    print('reading Project.csv')
    df_project = read_csv(path)

    # print(project_df.columns.values)
    column_duplicate_list = [
        col[0:-2] for col in df_project.columns.values if col[-2:] == '.1']
    column_rename_list = [
        col + '_n' if col in column_duplicate_list
        else col[0:-2] if col[-2:] == '.1' else col
        for col in df_project.columns.values]

    df_project = df_project.set_axis(column_rename_list, axis=1)
    df_project.index.name = 'Project_ID'
    df_project.index = df_project.index + 1

    if save:
        print('shape of df_Project : ', df_project.shape)
        df_project.to_csv(r'df_Project.csv', encoding='utf_8_sig')
        print('df_Project.csv saved')
    return df_project


if __name__ == '__main__':
    Dir = r'sim_file\Project.csv'
    df = MakeProject(path=Dir, save=True)
    pass
