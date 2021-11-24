import os
from typing import Tuple

import sim_transfer.Project
import sim_transfer.TDR2CSV_cross_section
import sim_transfer.PLT2CSV_BV
import sim_transfer.PLT2CSV_IfVf
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

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


# ファイル指定の関数
def filedialog_clicked():
    fTyp = [("", "*")]
    iFile = os.path.abspath(os.path.dirname(__file__))
    iFilePath = filedialog.askopenfilename(filetype=fTyp, initialdir=iFile)
    entry2.set(iFilePath)


# 実行ボタン押下時の実行関数
def conductMain():
    filePath = entry2.get()
    if filePath:
        messagebox.showinfo("info",
                            '以下のファイルのあるディレクトリからSIMデータ形成します\n'
                            + filePath
                            + '\n\nVf 1.15V, Vr 650V'
                            + '\nノード指定：' + str(col_l)
                            + '\nデータ列：' + str(datasets_l)
                            )
        head_tail: Tuple[str, str] = os.path.split(filePath)

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
        print('Everything completed successfully')

    else:
        messagebox.showerror("error", "パスの指定がありません。")


if __name__ == "__main__":
    # rootの作成
    root = Tk()
    root.title("SIM transfer")

    # Frame2の作成
    frame2 = ttk.Frame(root, padding=10)
    frame2.grid(row=2, column=1, sticky=E)

    # 「ファイル参照」ラベルの作成
    IFileLabel = ttk.Label(frame2, text="Projectファイル指定＞＞", padding=(5, 2))
    IFileLabel.pack(side=LEFT)

    # 「ファイル参照」エントリーの作成
    entry2 = StringVar()
    IFileEntry = ttk.Entry(frame2, textvariable=entry2, width=30)
    IFileEntry.pack(side=LEFT)

    # 「ファイル参照」ボタンの作成
    IFileButton = ttk.Button(frame2, text="参照", command=filedialog_clicked)
    IFileButton.pack(side=LEFT)

    # Frame3の作成
    frame3 = ttk.Frame(root, padding=10)
    frame3.grid(row=5, column=1, sticky=W)

    # 実行ボタンの設置
    button1 = ttk.Button(frame3, text="実行", command=conductMain)
    button1.pack(fill="x", padx=30, side="left")

    # キャンセルボタンの設置
    button2 = ttk.Button(frame3, text="閉じる", command=root.destroy)
    button2.pack(fill="x", padx=30, side="left")

    root.mainloop()
