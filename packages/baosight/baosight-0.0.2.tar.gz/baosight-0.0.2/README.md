# 高通量计算流程

## 创建流程步骤

```python
from htscf.core.createStep import create

create(
    _id="xxxx",  # 步骤id
    program="python",  # 执行的程序名 
    script="...........",  # 执行的脚本内容
    settings={"a": "12"},  # 执行脚本相关设置
    dbName="htscf",  # 数据库名
    collectionName="xxx",  # 集合名
    host="192.1.1.100",  # 数据库Ip
    port=27017  # 数据库端口
)
```

## 脚本格式

```python
from sys import argv

rootPath, settingsId, prevLogId = argv[1:]

# 输出到下一步的数组使用print,即可传递到下一步的prevData
print(rootPath, settingsId)
```

## 流程化运行

```python
from htscf.core.flow import workflow

workflow(
    "./xxx",  # 流程执行根目录
    stepIds=["xx", "yy"],  # 按照该数组中排列一次执行每一步
    dbName="test",  # 数据库名
    stepsCollectionName="steps",  # 流程数组集合
    stepLogCollectionName="log",  # 
    host="00.00.00.00",
    port=27017
)

```

# 能带绘制工具

```
usage: htscf pyband [-h] [-f FILENAME] [--procar PROCAR] [-z EFERMI] [--adjust_gap ADJUST_GAP] [-o BANDIMAGE] [-k KPTS] [-s FIGSIZE FIGSIZE] [-y YLIM YLIM] [--hline HLINES] [--vline VLINES] [--save_gnuplot] [--lw LINEWIDTH]
                    [--lc LINECOLORS] [--dpi DPI] [--occ OCC] [--occL] [--occLC_cmap OCCLC_CMAP] [--occLC_lw OCCLC_LW] [--occLC_cbar_pos OCCLC_CBAR_POS] [--occLC_cbar_ticks OCCLC_CBAR_TICKS] [--occLC_cbar_vmin OCCLC_CBAR_VMIN]  
                    [--occLC_cbar_vmax OCCLC_CBAR_VMAX] [--occLC_cbar_ticklabels OCCLC_CBAR_TICKLABELS] [--occLC_cbar_size OCCLC_CBAR_SIZE] [--occLC_cbar_pad OCCLC_CBAR_PAD] [--occM OCCMARKER] [--occMs OCCMARKERSIZE]
                    [--occMc OCCMARKERCOLOR] [--spd SPDPROJECTIONS] [--spin {x,y,z}] [--lsorbit] [-q]

options:
  -h, --help            show this help message and exit
  -f FILENAME, --file FILENAME
                        location of OUTCAR
  --procar PROCAR       location of the PROCAR
  -z EFERMI, --zero EFERMI
                        energy reference of the band plot
  --adjust_gap ADJUST_GAP
                        基于当前gap进行调整
  -o BANDIMAGE, --output BANDIMAGE
                        output image name, "band.png" by default
  -k KPTS, --kpoints KPTS
                        kpoint path
  -s FIGSIZE FIGSIZE, --size FIGSIZE FIGSIZE
                        figure size of the output plot
  -y YLIM YLIM          energy range of the band plot
  --hline HLINES        Add horizontal lines to the figure.
  --vline VLINES        Add vertical lines to the figure.
  --save_gnuplot        save output band energies in gnuplot format
  --lw LINEWIDTH        linewidth of the band plot
  --lc LINECOLORS       line colors of the band plot
  --dpi DPI             resolution of the output image
  --occ OCC             orbital contribution of each KS state
  --occL                use Linecollection or Scatter to show the orbital contribution
  --occLC_cmap OCCLC_CMAP
                        colormap of the line collection
  --occLC_lw OCCLC_LW   linewidth of the line collection
  --occLC_cbar_pos OCCLC_CBAR_POS
                        position of the colorbar
  --occLC_cbar_ticks OCCLC_CBAR_TICKS
                        ticks for the colorbar
  --occLC_cbar_vmin OCCLC_CBAR_VMIN
                        minimum value for the color plot
  --occLC_cbar_vmax OCCLC_CBAR_VMAX
                        maximum value for the color plot
  --occLC_cbar_ticklabels OCCLC_CBAR_TICKLABELS
                        tick labels for the colorbar
  --occLC_cbar_size OCCLC_CBAR_SIZE
                        size of the colorbar, relative to the axis
  --occLC_cbar_pad OCCLC_CBAR_PAD
                        pad between colorbar and axis
  --occM OCCMARKER      the marker used in the plot
  --occMs OCCMARKERSIZE
                        the size of the marker
  --occMc OCCMARKERCOLOR
                        the color of the marker
  --spd SPDPROJECTIONS  Spd-projected wavefunction character of each KS orbital.
  --spin {x,y,z}        show the magnetization mx/y/z constributions to the states. Use this option along with --occ.
  --lsorbit             Spin orbit coupling on, special treament of PROCAR
```