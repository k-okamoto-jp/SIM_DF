import os
import sim_transfer.Project
import sim_transfer.TDR2CSV_cross_section
import sim_transfer.PLT2CSV_BV
import sim_transfer.PLT2CSV_IfVf


filePath = input("プロジェクトcsvファイルのパスを指定して下さい")
head_tail = os.path.split(filePath)

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

df_project = sim_transfer.Project.MakeProject(path=filePath, save=True)
df_cross_section = sim_transfer.TDR2CSV_cross_section.MakeCrossSection(
    path=head_tail[0], df_project=df_project, col_list=col_l,
    datasets=datasets_l, save=True, output='df_cross_section.csv'
)
df_BV = sim_transfer.PLT2CSV_BV.MakeBV(
    path=head_tail[0], df_project=df_project, col='BVmax_n', save=True,
    output='df_BV.csv'
)
df_IfVf = sim_transfer.PLT2CSV_IfVf.MakeIfVf(
    path=head_tail[0], df_project=df_project, col='Vmax_n', save=True,
    output='df_IfVf.csv'
)

pass
