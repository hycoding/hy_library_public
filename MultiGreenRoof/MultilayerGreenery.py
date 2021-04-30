# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 20:27:47 2021
本程序用于计算多节点绿化的热湿耦合传递过程
@author: 何旸
"""
import xlrd
import numpy as np
#%%输入数据
FileName='InputDataX.xlsx'
def ReadExcel(A,sheet):
    """A表示文件名称，sheet为表单名称"""
    book=xlrd.open_workbook(A)
    table=book.sheet_by_name(sheet)
    nrows=table.nrows #行数
    ncols=table.ncols #列数
    B=np.zeros(((nrows-1),(ncols-1)),dtype=float)
    B=[[table.cell_value(i,j) for j in range(1,ncols)] for i in range(1,nrows)]
    return B 
def ReadStringData(File,sheet,x1,y1):
    """File表示文件名称，sheet为表单名称，x1和y1表示首列和最后一列的列数"""
    book=xlrd.open_workbook(File)
    table=book.sheet_by_name(sheet)
    nrows=table.nrows
    C2=[]    
    for k in range(0,(y1-x1)):
        C2.append([])
    for i in range(1,nrows):
        for j in range(x1,y1):
            C2[j-x1].append(table.cell(i,j))
    #----------------------------
    for i in range(0,(y1-x1)):
        listx=[]
        for j in range(0,nrows-1):
            listz=[]
            str1=C2[i][j].value
            if type(str1)==str:
                listy=str1.split(",")
                for k in listy:
                    listz.append(float(k))
            else:
                listz.append(str1)
            listz=np.array(listz)
            listx.append(listz)
    return listx
def Detail_Meteo_data(HY,A):
    DD=[0,31,28,31,30,31,30,31,31,30,31,30,31]#DD表示每个月固定天数
    DD[int(HY[4][1])]=int(HY[4][2])
    Time=[0,0,0,0,0]#年，月，日，时，分
    Tstep=int(HY[2])#单位是秒
    Mstep=int(HY[9]) #单位是秒,表示气象条件采集的时间步长，比如说5分钟采集一次或者1小时采集一次
    TotalNode=0
    Ax=[]#详细的气象数据
    Timex=[]#详细的时间序列
    Time[0]=int(HY[3][0])
    hnode=int(3600/Tstep)
    Startmonth=int(HY[3][1])
    Endmonth=int(HY[4][1]+1)
    startday=int(HY[3][2])
#------Warming up
    Days=1
    WarmupDays=[startday,startday,startday,startday,startday]
    Time[1]=Startmonth
    for Day in WarmupDays:
        Time[2]=Day
        for Hour in range(0,24):
            Time[3]=Hour
            for k in range(0,hnode):
                # nodex=int(k/(Mstep/60))
                Time[4]=int(Tstep/60*k)
                Timex.append([Time[0],Time[1],Time[2],Time[3],Time[4]])
                TotalNode+=1
                st_node=int((Hour+(Days-1)*24)*(3600/Mstep)+int(k*Tstep/(Mstep)))
                Axs=A[st_node,:]+(A[st_node+1,:]-A[st_node,:])/(Mstep/(Tstep))*(k-(Mstep/(Tstep)*int(k/(Mstep/(Tstep)))))
                Ax.append(Axs) 
    return Ax
"""读取气象文件"""
A=np.array(ReadExcel(FileName,'We'))#读取气象条件
HY=ReadStringData(FileName,'Ba',1,2)#读取有关信息
Ax=Detail_Meteo_data(HY,A)
Ax=np.array(Ax)
print(Ax[0])
print(Ax[2])