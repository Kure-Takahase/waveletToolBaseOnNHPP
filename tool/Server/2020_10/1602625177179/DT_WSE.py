import math
import copy
import SRMtool
import time
import datetime
import random
import xlsxwriter
from scipy.optimize import minimize_scalar
import pytz
from multiprocessing import Process
import numpy as np
from scipy.optimize import minimize

def getGroupLength(dataLength):
    i = 1
    x = i
    while i <= dataLength:
        x = i
        i = i * 2
    return x

def getGroups(data, groupLength):
    i = 0
    dataLength = len(data)
    list = []
    while groupLength + i <= dataLength:
        list.append(data[i : groupLength + i])
        i = i + 1
    return list

def getHighestResolutionLevel(groupLength):
    return int(math.log(groupLength,2))

def FiszTransformFromGroups(scalingCoes,waveletCoes,var):
    groupsLength = len(scalingCoes)
    list = []
    i = 0
    while i < groupsLength:
        list.append(FiszTransformFromGroup(scalingCoes[i],waveletCoes[i],var))
        i = i + 1
    return list

def FiszTransformFromGroup(scalingCoe,waveletCoe,var):
    lists = []
    groupLength = len(scalingCoe)
    j = 0
    while j < groupLength:
        i = 0
        levelLength = len(scalingCoe[j])
        list = []
        while(i < levelLength):
            if scalingCoe[j][i] == 0:
                list.append( 0.0 )
            else:
                if(scalingCoe[j][i] < 0):
                    print("FiszTransformFromGroup");
                list.append( (var**0.5) * waveletCoe[j][i]/(scalingCoe[j][i]**0.5) )
            i = i + 1
        lists.append(list)
        j = j + 1
    return lists
    
def inverseFiszTransformFromGroups(scalingCoes,FiszCoes,var):
    groupsLength = len(scalingCoes)
    C_list = []
    D_list = []
    list = []
    i = 0
    while i < groupsLength:
        a = inverseFiszTransformFromGroup(scalingCoes[i],FiszCoes[i],var)
        C_list.append(a[0])
        D_list.append(a[1])
        i = i + 1
    list.append(C_list);
    list.append(D_list);
    return list
def Fisz_getD(c,f,var):
    f = f/(var ** 0.5);
    return f*(c**0.5);

def inverseFiszTransformFromGroup(scalingCoe,FiszCoe,var):
    scalingCoe = copy.deepcopy(scalingCoe);
    lists = []
    C_lists = []
    D_lists = []
    groupLength = len(scalingCoe)
    j = groupLength - 1
    while j >= 0:
        levelLength = len(scalingCoe[j])
        D_list = []
        i = 0
        #复原Dj
        while(i < levelLength):
            D_list.append(Fisz_getD(scalingCoe[j][i],FiszCoe[j][i],var));
            i = i + 1
        #复原Cj-1
        i = 0
        while(i < levelLength and j > 0):
            scalingCoe[j - 1][2 * i]     = scalingCoe[j][i] + D_list[i];
            scalingCoe[j - 1][2 * i + 1] = scalingCoe[j][i] - D_list[i];
            if(scalingCoe[j - 1][2 * i + 1] < 0):
                scalingCoe[j - 1][2 * i + 1] = 0
            if(scalingCoe[j - 1][2 * i ] < 0):
                scalingCoe[j - 1][2 * i] = 0
            i = i + 1;
        D_lists.append(D_list)
        j = j - 1
    #将D_lists内部顺序修改为和scalingCoe一样
    D_listx = []
    i = groupLength - 1;
    while i >= 0:
        D_listx.append(D_lists[i]);
        i = i - 1;
    lists.append(scalingCoe)
    lists.append(D_listx)
    return lists
    
def inverseAnscombeTransformFromGroups(AT_datas,var):
    AT_datas = copy.deepcopy(AT_datas)
    groupsLength = len(AT_datas)
    i = 0
    lists = []
    while(i < groupsLength):
        list = inverseAnscombeTransformFromGroup(AT_datas[i],var)
        lists.append(list)
        i = i + 1
    return lists
    
def inverseAnscombeTransformFromGroup(AT_data,var):
    length = len(AT_data)
    i = 0
    list = []
    while(i < length):
        a = AT_data[i]
        b = a * a
        d = (2 * (var**0.5)) ** -2
        c = d*b - 3/8
        list.append( c )
        i = i + 1
    return list

def AnscombeTransformFromGroups(groups,var):
    groupsLength = len(groups)
    list = []
    i = 0
    while i < groupsLength:
        list.append(AnscombeTransformFromGroup(groups[i],var))
        i = i + 1
    return list

def AnscombeTransformFromGroup(group,var):
    list = []
    groupLength = len(group)
    i = 0
    while i < groupLength:
        a = group[i] + 3/8
        if(a < 0):
            b = 0
        else:
            b = a**0.5
        
        c = b * 2 * (var**0.5)
        '''
        if(i == 0):
            print(3/8)
            print(float(3/8))
            print("a:"+str(a)+" = "+ str(group[i]) + " " + str(float(3/8)));
            print("b:"+str(b));
        '''
        list.append(c)
        i = i + 1
    #print(list)
    return list


def inverseBartlettTransformFromGroups(groups,var):
    groupsLength = len(groups)
    list = []
    i = 0
    while i < groupsLength:
        list.append(inverseBartlettTransformFromGroup(groups[i],var))
        i = i + 1
    return list
    '''
def inverseBartlettTransformFromGroups(AT_datas):
    AT_datas = copy.deepcopy(AT_datas)
    groupsLength = len(AT_datas)
    i = 0
    lists = []
    while(i < groupsLength):
        list = inverseBartlettTransformFromGroup(AT_datas[i])
        lists.append(list)
        i = i + 1
    return lists
    '''
def inverseBartlettTransformFromGroup(BT_data,var):
    length = len(BT_data)
    i = 0
    list = []
    while(i < length):
        a = BT_data[i] * BT_data[i]
        b = (2 * (var**0.5)) ** -2
        c = b*a - 0.5
        list.append( c )
        i = i + 1
    return list
'''
def inverseBartlettTransformFromGroup(BT_data):
    length = len(BT_data)
    i = 0
    list = []
    while(i < length):
        a = BT_data[i] * BT_data[i]
        c = a - 0.5
        list.append( c )
        i = i + 1
    return list
'''
def BartlettTransformFromGroups(groups,var):
    groupsLength = len(groups)
    list = []
    i = 0
    while i < groupsLength:
        list.append(BartlettTransformFromGroup(groups[i],var))
        i = i + 1
    return list

def BartlettTransformFromGroup(group,var):
    list = []
    groupLength = len(group)
    i = 0
    while i < groupLength:
        a = group[i] + 0.5
        b = a**0.5
        c = b * 2 * (var**0.5)
        list.append(c)
        i = i + 1
    return list



def getScalingCoefficientsFromGroup(group):
    lists = []
    J = getHighestResolutionLevel( len(group) )
    a = copy.deepcopy(group)
    lists.append(a) 
    j = 1
    while(j <= J):
        list = []
        k = 0
        while(k < 2**(J - j)):
            c = 0.5*( lists[j - 1][2 * k] + lists[j - 1][2 * k + 1])
            list.append(c)
            k = k + 1
        #print(list)
        lists.append(list)
        j = j + 1
    #print("-----------------------------------------------")
    return lists
     
def getScalingCoefficientsFromGroups(Groups):
    lists = []
    groupsLength = len(Groups)
    i = 0
    while(i < groupsLength):
        list = getScalingCoefficientsFromGroup(Groups[i])
        lists.append(list)
        i = i + 1
    return lists

def getWaveletCoefficientsFromGroup(WaveletCoefficients):
    WaveletCoefficients = copy.deepcopy(WaveletCoefficients)
    lists = []
    J = getHighestResolutionLevel( len(WaveletCoefficients[0]) )
    lists.append(WaveletCoefficients[0]) 
    j = 1
    while(j <= J):
        list = []
        k = 0
        while(k < 2**(J - j)):
            #print(str(WaveletCoefficients[j - 1][2 * k]) +" - "+str(WaveletCoefficients[j - 1][2 * k + 1]) )
            c = 0.5*( WaveletCoefficients[j - 1][2 * k] - WaveletCoefficients[j - 1][2 * k + 1] )
            list.append(c)
            k = k + 1
        lists.append(list)
        j = j + 1
    return lists

def getWaveletCoefficientsFromGroups(CS):
    lists = []
    groupsLength = len(CS)
    i = 0
    while(i < groupsLength):
        list = getWaveletCoefficientsFromGroup(CS[i])
        lists.append(list)
        i = i + 1
    return lists

def Threshold(coe,r,mode):
    if abs(coe) <= r :
        return 0
    if(mode == 'h'):
        return coe
    else:
        if(coe > 0):
            return coe - r
        else:
            return coe + r
        
def getUniversalThreshold(groupLength):
    #return 0;
    a = math.log(groupLength)
    #a=math.log(81)
    b = 2*a
    c = b**0.5
    return c
    
def universalThresholdForOneLevel(WaveletCoefficients,mode,t):
    WaveletCoefficients = copy.deepcopy(WaveletCoefficients)
    coefficientsLength = len(WaveletCoefficients)
    #print(str(coefficientsLength)+" "+str(t))
    #r = getUniversalThreshold(coefficientsLength)
    list = []
    i = 0
    while(i < coefficientsLength):
        #a = Threshold(WaveletCoefficients[i],r,mode)
        a = Threshold(WaveletCoefficients[i],t,mode)
        list.append(a)
        i = i + 1
    return list

def universalThresholdForGroup(GroupWaveletCoefficients,mode):
    groupLength = len(GroupWaveletCoefficients)
    lists = []
    i = 0
    ThresholdLength = len(GroupWaveletCoefficients[0]);
    t = getUniversalThreshold(ThresholdLength)
    #print(str(ThresholdLength)+" "+str(t))
    while(i < groupLength):
        #list = universalThresholdForOneLevel(GroupWaveletCoefficients[i],mode)
        list = universalThresholdForOneLevel(GroupWaveletCoefficients[i],mode,t)
        lists.append(list)
        i = i + 1
    return lists

def universalThresholdForGroups(Ds,mode):
    groupLength = len(Ds)
    lists = []
    i = 0
    while(i < groupLength):
        list = universalThresholdForGroup(Ds[i],mode)
        lists.append(list)
        i = i + 1
    return lists

def MyThresholdForOneLevel(WaveletCoefficients,mode,t):
    WaveletCoefficients = copy.deepcopy(WaveletCoefficients)
    coefficientsLength = len(WaveletCoefficients)
    #r = getMyThreshold(WaveletCoefficients)
    r = t
    list = []
    i = 0
    while(i < coefficientsLength):
        a = Threshold(WaveletCoefficients[i],r,mode)
        list.append(a)
        i = i + 1
    return list

def MyThresholdForGroup(GroupWaveletCoefficients,mode):
    groupLength = len(GroupWaveletCoefficients)
    lists = []
    i = 0
    t = getMyThreshold(GroupWaveletCoefficients[0])
    while(i < groupLength):
        list = MyThresholdForOneLevel(GroupWaveletCoefficients[i],mode,t)
        lists.append(list)
        i = i + 1
    return lists

def MyThresholdForGroups(Ds,mode):
    groupLength = len(Ds)
    lists = []
    i = 0
    while(i < groupLength):
        list = MyThresholdForGroup(Ds[i],mode)
        lists.append(list)
        i = i + 1
    return lists

def getMyThreshold(D,lht_last):
    groupLength = len(D)
    #bounds=(0, 2)
    #res = minimize_scalar(lostFunction,None,bounds,D, method='bounded')

    x0 = np.array([0])
    res = minimize(lostFunction, x0,(D,lht_last), method='nelder-mead',
                   options={'xatol': 1e-8, 'disp': False})
    #test start
    x1 = np.array([2])
    resu = minimize(lostFunction, x1,(D,lht_last), method='nelder-mead',
                   options={'xatol': 1e-8, 'disp': False})

    if( abs(float(res.x[0]) - float(resu.x[0])) > 0.001 ) and (float(res.fun) > float(resu.fun)):
        #print("no1")
        #print("%.3f %.3f" % (float(res.x[0]),float(res.fun)))
        #print("%.3f %.3f" % (float(resu.x[0]),float(resu.fun)))
        res.x[0] = resu.x[0]
        res.fun = resu.fun
    #test end

    if(res.x[0] < 0):
        bounds=(0, 1)
        resul = minimize_scalar(lostFunction,None,bounds,(D,lht_last), method='bounded')
        res.x[0] = resul.x


    a = math.log(2)/math.log(groupLength)
    b = 1 - a
    c = b ** -0.5
    #d = c * res.x
    d = c * res.x[0]
    #print(round(d,3))
    return d

#损失函数用阈值模块
def ThresholdForGroups_lost(Ds,mode,Threshold):
    #print("4")
    groupLength = len(Ds)
    lists = []
    i = 0
    while(i < groupLength):
        list = ThresholdForGroup_lost(Ds[i],mode,Threshold)
        lists.append(list)
        i = i + 1
    return lists
def ThresholdForGroup_lost(GroupWaveletCoefficients,mode,Threshold):
    groupLength = len(GroupWaveletCoefficients)
    lists = []
    i = 0
    ThresholdLength = len(GroupWaveletCoefficients[0]);
    #一般阈值
    t = Threshold
    while(i < groupLength):
        list = ThresholdForOneLevel(GroupWaveletCoefficients[i],mode,t)
        lists.append(list)
        i = i + 1
    return lists
def getLevelDependentThreshold(J,now_level,mean):
    log2j = math.log(2 ** now_level)
    a = 2 ** (-1 * 1/2 * J - now_level + 2);
    b = 2 * log2j
    c = 16 * (log2j ** 2 );
    d = 8 * mean * log2j * (2 ** J - now_level);
    t = a * (b + (c + d) ** 0.5);
    return t;

#通用阈值模块
def ThresholdForGroups(Ds,mode,ThresholdName):
    #print("4")
    groupLength = len(Ds)
    lists = []
    i = 0
    #print(Ds[0][0])
    #print(Ds[1][0])
    while(i < groupLength):
        if(i + 1 < groupLength):
            lht_last = Ds[i+1][0][len(Ds[i+1][0])-1]
        else:
            lht_last = Ds[0][0][len(Ds[0][0])-1]
        #暂时关闭lht_last
        lht_last = Ds[i][0][0]
        list = ThresholdForGroup(Ds[i],mode,ThresholdName,lht_last)
        lists.append(list)
        i = i + 1
    return lists

def ThresholdForGroup(GroupWaveletCoefficients,mode,ThresholdName,lht_last):
    dataLength = len(GroupWaveletCoefficients[0]);
    #一般阈值
    t = 1000
    #print("5")
    if(ThresholdName == 'ut'):
        t = getUniversalThreshold(dataLength)
    if(ThresholdName == 'lht'):
        t = getMyThreshold(GroupWaveletCoefficients[0],lht_last)
        #print(str(round(t,3))+" "+str(round(getUniversalThreshold(dataLength),3)))
    lists = []
    lists.append(GroupWaveletCoefficients[0])
    i = 1
    groupLength = len(GroupWaveletCoefficients)
    while(i < groupLength):
        if(ThresholdName == 'ldt'):
            J = getHighestResolutionLevel(dataLength);
            #mean = sum(GroupWaveletCoefficients[0]) / (2 ** (J - i));
            mean = sum(GroupWaveletCoefficients[0]) / dataLength;
            t = getLevelDependentThreshold(J,i,mean);
        list = ThresholdForOneLevel(GroupWaveletCoefficients[i],mode,t)
        lists.append(list)
        i = i + 1
    return lists

def ThresholdForOneLevel(WaveletCoefficients,mode,t):
    WaveletCoefficients = copy.deepcopy(WaveletCoefficients)
    coefficientsLength = len(WaveletCoefficients)
    list = []
    i = 0
    while(i < coefficientsLength):
        a = Threshold(WaveletCoefficients[i],t,mode)
        list.append(a)
        i = i + 1
    return list

def inverseHaarWaveletTransformForGroup(scalingCoe,waveletCoe):
    scalingCoe = copy.deepcopy(scalingCoe)
    waveletCoe = copy.deepcopy(waveletCoe)
    groupLength = len(scalingCoe)
    if groupLength != len(waveletCoe):
        return false
    J = groupLength - 1
    k = 0
    '''
    list = []
    #print("2**(J-1):", 2**(J-1) )
    while(k < 2**(J - 1)):
        list.append( scalingCoe[1][k] + waveletCoe[1][k] )
        list.append( scalingCoe[1][k] - waveletCoe[1][k] )
        k = k + 1
    return list
    '''
    j = groupLength - 1

    while(j > 0):

        k = 0
        while(k < 2**(J - j)):

            scalingCoe[j - 1][2 * k]     = scalingCoe[j][k] + waveletCoe[j][k]
            scalingCoe[j - 1][2 * k + 1] = scalingCoe[j][k] - waveletCoe[j][k]
           
            k = k + 1
        j = j - 1
    return scalingCoe[0]
    
    

def inverseHaarWaveletTransformForGroups(scalingCoes,waveletCoes):
    scalingCoes = copy.deepcopy(scalingCoes)
    waveletCoes = copy.deepcopy(waveletCoes)
    #print("-----------inverseHaarWaveletTransformForGroups----------------------")
    #print(scalingCoes)
    #print(waveletCoes)
    groupsLength = len(scalingCoes)
    #print(groupsLength);
    #print(len(waveletCoes));
    if groupsLength != len(waveletCoes):
        return false
    i = 0
    lists = []
    while(i < groupsLength):
        list = inverseHaarWaveletTransformForGroup(scalingCoes[i],waveletCoes[i])
        
        lists.append(list)
        i = i + 1
    return lists

def movingAverage(iGroups,dataLength):
    iGroups = copy.deepcopy(iGroups)
    dataSum = [0]*dataLength
    counter = [0]*dataLength
    result  = [0]*dataLength
    groupsSum = len(iGroups)
    groupLength = len(iGroups[0])
    i = 0
    #print("groupsSum:"+str(groupsSum));
    #print("groupLength:"+str(groupLength));
    while(i < groupsSum):
        j = 0
        while(j < groupLength):
            dataSum[i + j] = dataSum[i + j] + iGroups[i][j]
            counter[i + j] = counter[i + j] + 1
            j = j + 1
        i = i + 1
    k = 0
    #print(iGroups[0])
    while(k < dataLength):
        #print(counter[k]);
        result[k] = dataSum[k] / counter[k];
        #print(str(result[k])+" = "+str(dataSum[k])+" / "+str(counter[k]));
        if(result[k] < 0 ):
            result[k] = 0;
        #result[k] = round(result[k], 5)
        k = k + 1
    return result

def getTimeShiftGroups(group):
    list = [];
    length = len(group);
    i = 0
    while i < length:
        Tgroup = [];
        j = 0
        while j < length:
            if(i + j < length):
                Tgroup.append(group[i + j])
            else:
                Tgroup.append(group[i + j - length])
            j = j + 1
        list.append(Tgroup);
        i = i + 1
    return list

def inverseTimeShiftGroups(iGroups):
    list = [];
    length = len(iGroups[0])
    i = 0
    while i < len(iGroups):
        j = 0
        group = [];
        while j < length:
            if(j - i < 0):
                group.append(iGroups[i][j - i + length])
            else:
                group.append(iGroups[i][j - i])
            j = j + 1;
        list.append(group)
        i = i + 1;
    return list;

def averTimeShiftGroups(igroups):
    list = [];
    length = len(igroups[0])
    groupsLength = len(igroups)
    i = 0;
    while i < length:
        j = 0;
        total = 0;
        counter = 0;
        while j < groupsLength:
            total = total + igroups[j][i];
            counter = counter + 1;
            j = j + 1
        list.append(total/counter)
        i = i + 1;
    return list;

#新
#thresholdMode: 's'、'h'
#thresholdName: 'ut'、'lht'
def HTI(filename,thresholdMode,thresholdName):
    data = SRMtool.getData(filename)
    dataLength  = len(data)
    groupLength = getGroupLength(dataLength)
    groups = getGroups(data,groupLength)
    #对每一个分组获取完全位移后分组，并进行去噪处理，再还原
    list = [];
    for group in groups:
        #获取完全位移后的分组群
        TIgroups = getTimeShiftGroups(group); 
        #获取每个经位移后的分组的小波系数、尺度系数
        Cs  = getScalingCoefficientsFromGroups(TIgroups);
        Ds  = getWaveletCoefficientsFromGroups(Cs);
        #去噪
        Denoise_Ds = ThresholdForGroups(Ds,thresholdMode,thresholdName);
        #Denoise_Ds = Ds
        #还原去噪数据
        iTI_groups = inverseHaarWaveletTransformForGroups(Cs,Denoise_Ds);
        #还原位移
        igroups = inverseTimeShiftGroups(iTI_groups);
        #取平均值后完成一组group的处理
        aver_igroup = averTimeShiftGroups(igroups);
        list.append(aver_igroup)
    #移动平均获得最终估计
    idata= movingAverage(list,dataLength);
    return idata;

def HFT(filename,thresholdMode,thresholdName,var):
    data = SRMtool.getData(filename)
    dataLength  = len(data)
    groupLength = getGroupLength(dataLength)
    groups = getGroups(data,groupLength)
    Cs1  = getScalingCoefficientsFromGroups(groups)
    Ds1  = getWaveletCoefficientsFromGroups(Cs1)
    Fs1  = FiszTransformFromGroups(Cs1,Ds1,var)
    C01s = inverseHaarWaveletTransformForGroups(Cs1,Fs1)
    #去噪开始
    Cs2  = getScalingCoefficientsFromGroups(C01s)
    Ds2  = getWaveletCoefficientsFromGroups(Cs2)
    Denoise_Ds2 = ThresholdForGroups(Ds2,thresholdMode,thresholdName)
    #Denoise_Ds2 = Ds2
    C02s = inverseHaarWaveletTransformForGroups(Cs2,Denoise_Ds2)
    #去噪结束
    Cs3  = getScalingCoefficientsFromGroups(C02s)
    Fs2  = getWaveletCoefficientsFromGroups(Cs3)
    CDs  = inverseFiszTransformFromGroups(Cs3,Fs2,var)
    Ds3 = CDs[1];
    Cs4 = CDs[0];
    C03s = inverseHaarWaveletTransformForGroups(Cs4,Ds3)
    idata= movingAverage(C03s,dataLength)
    return idata
#var 设定数据转换成高斯后的方差
def HAT(filename,thresholdMode,thresholdName,var):
    #print("2")
    data = SRMtool.getData(filename)
    dataLength = len(data)
    groupLength = getGroupLength(dataLength)
    groups = getGroups(data,groupLength)
    AT_groups = AnscombeTransformFromGroups(groups,var)

    Cs = getScalingCoefficientsFromGroups(AT_groups)
    Ds = getWaveletCoefficientsFromGroups(Cs)
    #print("3")

    Denoise_Ds = ThresholdForGroups(Ds,thresholdMode,thresholdName)
    #Denoise_Ds = Ds
    iAT_groups = inverseHaarWaveletTransformForGroups(Cs,Denoise_Ds)

    #iGroups = inverseAnscombeTransformFromGroups(iAT_groups)
    #idata = movingAverage(iGroups,dataLength)
    idata = movingAverage(iAT_groups,dataLength)
    idata = inverseAnscombeTransformFromGroup(idata,var);

    return idata
#var 设定数据转换成高斯后的方差
def HBT(filename,thresholdMode,thresholdName,var):
    #print("2")
    data = SRMtool.getData(filename)
    dataLength = len(data)
    groupLength = getGroupLength(dataLength)
    groups = getGroups(data,groupLength)
    BT_groups = BartlettTransformFromGroups(groups,var)

    Cs = getScalingCoefficientsFromGroups(BT_groups)
    Ds = getWaveletCoefficientsFromGroups(Cs)
    #print("3")
    Denoise_Ds = ThresholdForGroups(Ds,thresholdMode,thresholdName)
    #Denoise_Ds = Ds
    iBT_groups = inverseHaarWaveletTransformForGroups(Cs,Denoise_Ds)

    #iGroups = inverseAnscombeTransformFromGroups(iBT_groups)
    #idata = movingAverage(iGroups,dataLength)
    idata = movingAverage(iBT_groups,dataLength)

    idata = inverseBartlettTransformFromGroup(idata,var);
    return idata



#给定阈值t和数据C0，将C0展开成哈尔小波系数，用给定阈值t对小波系数进行去噪，随后通过逆哈尔小波转换得到去噪后的C0，返回C0。
def HWT_threshold(C0,t):
    Cs = getScalingCoefficientsFromGroup(C0)

    Ds = getWaveletCoefficientsFromGroup(Cs)
    Denoise_Ds =ThresholdForGroup_lost(Ds,'s',t)

    i_C0 = inverseHaarWaveletTransformForGroup(Cs,Denoise_Ds)
    return i_C0
#新算法
def lostFunction(t,group,lht_last):
    group = copy.deepcopy(group);
    i = 0;
    groupO = []
    groupE = []
    originGroup = []
    length = len(group) / 2

    #分奇偶
    while i < length:
        groupO.append( group[2 * i] )
        groupE.append( group[2 * i +1] )
        originGroup.append(group[2 * i])
        originGroup.append(group[2 * i +1])
        i = i + 1
    originGroup.append(group[0])
    originGroup.append(lht_last)

    

    O_igroup = HWT_threshold(groupO,t)
    E_igroup = HWT_threshold(groupE,t)

    #混合
    t_group_O_ = []
    t_group_E_ = []
    i = 0
    while(i < len(O_igroup)):
        if i + 1 < len(O_igroup):
            a = 0.5 * (O_igroup[i] + O_igroup[i + 1])
        else:
            #print("last")
            a = 0.5 * (O_igroup[i] + O_igroup[0])
        t_group_O_.append( a )
        if i + 1 < len(E_igroup):
            b = 0.5 * (E_igroup[i] + E_igroup[i + 1])
        else:
            #print("last")
            b = 0.5 * (E_igroup[i] + E_igroup[0])
        t_group_E_.append( b )
        i = i + 1

    #print(len(t_group_O_))
    #print(len(t_group_E_))
    #算损失
    i = 0
    m = 0
    #print(groupO)
    #print(groupE)
    #print(len(group))
    while i < len(group)/2:
        #print(i)
        e = t_group_E_[i] - originGroup[2*(i+1)]
        e = e*e
        o = t_group_O_[i] - originGroup[2*(i+1)-1]
        o = o*o
        #print("%d %.1f" % (2*(i+1)-1,originGroup[2*(i+1)-1]))
        #print("%d %.1f" % (2*(i+1),originGroup[2*(i+1)]))
        '''
        e = t_group_E_[i] - t_groupO[i+1]
        e = e*e
        o = t_group_O_[i] - t_groupE[i]
        o = o*o
        #print(e+o)
        '''
        m = m + e + o
        i = i + 1
    #print(e+o)
    m = m + e + o
    return m
#旧
def lostFunction_1(t,group):
    i = 0
    t_group_O = []
    t_group_E = []
    t_groupO = []
    t_groupE = []
    originGroup = []
    length = len(group) / 2

    Cs = getScalingCoefficientsFromGroup(group)
    Ds = getWaveletCoefficientsFromGroup(Cs)
    Denoise_Ds = ThresholdForGroup_lost(Ds,'s',t)
    #print(Cs)
    #print(Denoise_Ds)

    igroup = inverseHaarWaveletTransformForGroup(Cs,Denoise_Ds)
    while i < length:
        t_groupO.append( group[2 * i] )
        t_groupE.append( group[2 * i +1] )
        originGroup.append(group[2 * i])
        originGroup.append(group[2 * i +1])
        #a = Threshold(igroup[2 * i],0,'s')
        #b = Threshold(igroup[2 * i + 1],0,'s')
        #a = Threshold(group[2 * i],t,'s')
        #b = Threshold(group[2 * i + 1],t,'s')
        a = igroup[2 * i]
        b = igroup[2 * i + 1]
        t_group_O.append( a )
        t_group_E.append( b )
        i = i + 1
    originGroup.append(group[0])
    #print(t_group_O)
    #print(t_group_E)
    #print(originGroup)
    t_group_O_ = []
    t_group_E_ = []
    i = 0
    while(i < len(t_group_O)):
        if i + 1 < len(t_group_O):
            a = 0.5 * (t_group_O[i] + t_group_O[i + 1])
        else:
            a = 0.5 * (t_group_O[i] + t_group_O[0])
        t_group_O_.append( a )
        if i + 1 < len(t_group_E):
            b = 0.5 * (t_group_E[i] + t_group_E[i + 1])
        else:
            b = 0.5 * (t_group_E[i] + t_group_E[0])
        t_group_E_.append( b )
        i = i + 1
    #print("2")
    #print(t_group_O_)
    #print(t_group_E_)
    i = 0
    m = 0
    while i < len(group)/2:
        e = t_group_E_[i] - originGroup[2 * i + 2]
        e = e*e
        o = t_group_O_[i] - originGroup[2 * i + 1]
        o = o*o
        '''
        e = t_group_E_[i] - t_groupO[i+1]
        e = e*e
        o = t_group_O_[i] - t_groupE[i]
        o = o*o
        #print(e+o)
        '''
        m = m + e + o
        i = i + 1
    '''
    e = t_group_E_[len(t_group_E_)-1] - t_groupO[0]
    e = e*e
    o = t_group_O_[len(t_group_E_)-1] - t_groupE[len(t_group_E_)-1]
    o = o*o
    #print(e+o)
    m = m + e + o
    '''
    return m;

#移动平均法获取之后N天的预测值
#def averPrediction(data,times,dataTransform,thresholdRule,thresholdMethod):


#误差法获取之后N天的预测值
#costDataMethod:可选'quota'或'grow'。选择quota，则每次以n天为单位进行预测。若选择grow，则选择预测值+过去的所有数据来进行预测
#costMethod:可选'origin'或'denoise'。denoise，损失函数与去噪后数据比较，origin，损失函数与原数据进行比较
#weightMethod:可选'none','boxcar','Gaussian','Epanechnikov','tricube'。none，损失函数中不对数据进行加权处理。其他则分别为对应的核函数进行加权
#time:往后预测多少天。例如 times = 30，则往后预测30天
def costPrediction(data,costMethod,costDataMethod,weightMethod,h,times,dataTransform,thresholdRule,thresholdMethod,var,compare,ifUseEstimation,ifCompareNewData):
    #print("costPrediction6")
    originData = copy.deepcopy(data);
    i = 0;
    length = len(data);
    while i < times:
        #获取数据
        if(costDataMethod == 'quota'):
            lists = originData[i:length + i - 1];
        elif(costDataMethod == 'grow'):
            lists = originData[0:length + i - 1];
        else:
            return false;
        # 跳过非法参数
        if(costMethod == 'denoise' and ifCompareNewData == 1) or (dataTransform == 'TranslationInvariant' and thresholdMethod == 'ut') or (dataTransform != 'TranslationInvariant' and thresholdMethod == 'ldt'):
            res = 0;
        else:
            #进行预测
            if(costMethod == 'origin'):
                res = getNextDayNum1(lists,dataTransform,thresholdRule,thresholdMethod,weightMethod,h,var,compare,ifCompareNewData);
            elif(costMethod == 'denoise'):
                res = getNextDayNum2(lists,dataTransform,thresholdRule,thresholdMethod,weightMethod,h,var,compare);
            else:
                print('costMethod:'+costMethod)
                return false;
                
            if(ifUseEstimation == 1):
                # ~q1 版
                #start 新的数据值应为原本q1的估计值,故此处求加入res以后,对全体进行估计后，取res的估计值
                #print("q1")
                lists.append(res)
                if(dataTransform == 'Anscombe'):
                    result1 = p_HAT(lists,thresholdRule,thresholdMethod,var)
                elif(dataTransform == 'Fisz'):
                    result1 = p_HFT(lists,thresholdRule,thresholdMethod,var)
                elif(dataTransform == 'Bartlett'):
                    result1 = p_HBT(lists,thresholdRule,thresholdMethod,var)
                elif(dataTransform == 'TranslationInvariant'):
                    result1 = p_HTI(lists,thresholdRule,thresholdMethod)
                else :
                    sys.exit(1);
                res = result1[ len(result1) - 1 ]
                #end
            
        originData.append(res);
        i = i + 1;
    return originData;


#获取之后N天的预测值,方法1
def getPrediction1(data,times,dataTransform,thresholdRule,thresholdMethod,weightMethod,h,compare,ifCompareNewData):
    originData = copy.deepcopy(data);
    i = 0;
    length = len(data);
    while i < times:
        #获取最近的length个数据
        lists = originData[i:length + i - 1];
        res = getNextDayNum1(lists,dataTransform,thresholdRule,thresholdMethod,weightMethod,h,compare,ifCompareNewData);
        originData.append(res);
        i = i + 1;
    return originData;


#获取下一天的预测值,方法1
def getNextDayNum1(data,dataTransform,thresholdRule,thresholdMethod,weightMethod,h,var,compare,ifCompareNewData):
    data = copy.deepcopy(data);
    max_data = max(data) * 5;
    if(max_data > 10000):
        max_data = 10000
    #print(max_data)
    bounds=(0, max_data);
    arg = (data,dataTransform,thresholdRule,thresholdMethod,weightMethod,h,var,compare,ifCompareNewData)
    #print(prediction_cost2(0.1,data,'Fisz','s','ut'))
    res = minimize_scalar(prediction_cost1,None,bounds,arg, method='bounded')
    #print(res)
    return res.x

#获取之后N天的预测值,方法2
def getPrediction2(data,times,dataTransform,thresholdRule,thresholdMethod,weightMethod,h,compare):
    originData = copy.deepcopy(data);
    i = 0;
    length = len(data);
    while i < times:
        #获取最近的length个数据
        lists = originData[i:length + i - 1];
        res = getNextDayNum2(lists,dataTransform,thresholdRule,thresholdMethod,weightMethod,h,compare);
        originData.append(res);
        i = i + 1;
    return originData;


#获取下一天的预测值,方法2
def getNextDayNum2(data,dataTransform,thresholdRule,thresholdMethod,weightMethod,h,var,compare):
    data = copy.deepcopy(data);
    max_data = max(data) * 5;
    if(max_data > 10000):
        max_data = 10000
    #print(max_data)
    bounds=(0, max_data);
    arg = (data,dataTransform,thresholdRule,thresholdMethod,weightMethod,h,var,compare)
    #print(prediction_cost2(0.1,data,'Fisz','s','ut'))
    res = minimize_scalar(prediction_cost2,None,bounds,arg, method='bounded')
    #print(res)
    return res.x




#预测用损失函数-大师姐版（与原数据做对比）
#可选是否用核函数
def prediction_cost1(new_day,originDatas,dataTransform,thresholdRule,thresholdMethod,weightMethod,h,var,compare,ifCompareNewData):
    originDatas = copy.deepcopy(originDatas);
#def prediction_cost1(new_day,args):
    #print(args)
    '''
    originDatas     = args[0];
    dataTransform  = args[1];
    thresholdRule   = args[2];
    thresholdMethod = args[3];
    '''
    #加入预测值
    originDatas.append(new_day);
    #降噪
    if(dataTransform == 'Anscombe'):
        result1 = p_HAT(originDatas,thresholdRule,thresholdMethod,var)
    elif(dataTransform == 'Fisz'):
        result1 = p_HFT(originDatas,thresholdRule,thresholdMethod,var)
    elif(dataTransform == 'Bartlett'):
        result1 = p_HBT(originDatas,thresholdRule,thresholdMethod,var)
    elif(dataTransform == 'TranslationInvariant'):
        result1 = p_HTI(originDatas,thresholdRule,thresholdMethod)
    else :
        sys.exit(1);
    #添加权值
    length = len(originDatas);
    if(weightMethod != 'none'):
        weight = SRMtool.KernelWeight(length + 1,1,length,h,weightMethod);
        i = 0
        while i < length:
            result1[i] = result1[i] * weight[i]
            i = i + 1;
    #计算误差 第一个到预测日
    i = 0;
    total = 0;

    # 可选减少计算误差的比较对象,不比较前 compare% 的数据.为0时为比较所有对象
    #compare = 0
    i = math.floor(length * compare)

    #不计算与预测日的误差 N
    if(ifCompareNewData == 1):
        length = length - 1
    #计算与预测日的误差 N+1
    while i < length:
        x = result1[i] - originDatas[i];
        total = total + x**2;
        i = i + 1;
    total = total ** 0.5;
    return total;





#预测用损失函数-独创版（与处理过的数据做对比）
#可选是否用核函数
def prediction_cost2(new_day,originDatas,dataTransform,thresholdRule,thresholdMethod,weightMethod,h,var,compare):
    originDatas = copy.deepcopy(originDatas);
    #降噪
    if(dataTransform == 'Anscombe'):
        result1 = p_HAT(originDatas,thresholdRule,thresholdMethod,var)
    elif(dataTransform == 'Fisz'):
        result1 = p_HFT(originDatas,thresholdRule,thresholdMethod,var)
    elif(dataTransform == 'Bartlett'):
        result1 = p_HBT(originDatas,thresholdRule,thresholdMethod,var)
    elif(dataTransform == 'TranslationInvariant'):
        result1 = p_HTI(originDatas,thresholdRule,thresholdMethod)
    else :
        sys.exit(1);
    
    length = len(originDatas);
    # 添加两次权值，不等于没有添加权值吗... 故而删除作为比较对象的权值
    '''
    #添加权值
    if(weightMethod != 'none'):
        weight = SRMtool.KernelWeight(length + 1,1,length,h,weightMethod);
        i = 0
        while i < length:
            result1[i] = result1[i] * weight[i]
            i = i + 1;
    '''
    #加入预测值
    originDatas.append(new_day);
    #降噪
    if(dataTransform == 'Anscombe'):
        result2 = p_HAT(originDatas,thresholdRule,thresholdMethod,var)
    elif(dataTransform == 'Fisz'):
        result2 = p_HFT(originDatas,thresholdRule,thresholdMethod,var)
    elif(dataTransform == 'Bartlett'):
        result2 = p_HBT(originDatas,thresholdRule,thresholdMethod,var)
    elif(dataTransform == 'TranslationInvariant'):
        result2 = p_HTI(originDatas,thresholdRule,thresholdMethod)
    else :
        sys.exit(1);
    #添加权值
    if(weightMethod != 'none'):
        i = 0
        while i < length:
            result2[i] = result2[i] * weight[i]
            i = i + 1;
    #计算误差 第一个到预测日前一日
    i = 0;
    total = 0;
    # 可选减少计算误差的比较对象,不比较前 compare% 的数据.为0时为比较所有对象
    #compare = 0
    i = math.floor(length * compare)
    while i < length:
        x = result1[i] - result2[i];
        total = total + x**2;
        i = i + 1;
    total = total ** 0.5;
    return total;




#预测用降噪函数
def p_HTI(originDatas,thresholdMode,thresholdName):
    data = copy.deepcopy(originDatas);
    dataLength  = len(data)
    groupLength = getGroupLength(dataLength)
    groups = getGroups(data,groupLength)
    #对每一个分组获取完全位移后分组，并进行去噪处理，再还原
    list = [];
    for group in groups:
        #获取完全位移后的分组群
        TIgroups = getTimeShiftGroups(group); 
        #获取每个经位移后的分组的小波系数、尺度系数
        Cs  = getScalingCoefficientsFromGroups(TIgroups);
        Ds  = getWaveletCoefficientsFromGroups(Cs);
        #去噪
        Denoise_Ds = ThresholdForGroups(Ds,thresholdMode,thresholdName);
        #Denoise_Ds = Ds
        #还原去噪数据
        iTI_groups = inverseHaarWaveletTransformForGroups(Cs,Denoise_Ds);
        #还原位移
        igroups = inverseTimeShiftGroups(iTI_groups);
        #取平均值后完成一组group的处理
        aver_igroup = averTimeShiftGroups(igroups);
        list.append(aver_igroup)
    #移动平均获得最终估计
    idata= movingAverage(list,dataLength);
    return idata;

def p_HFT(originDatas,thresholdMode,thresholdName,var):
    data = copy.deepcopy(originDatas);
    dataLength  = len(data)
    groupLength = getGroupLength(dataLength)
    groups = getGroups(data,groupLength)
    Cs1  = getScalingCoefficientsFromGroups(groups)
    Ds1  = getWaveletCoefficientsFromGroups(Cs1)
    Fs1  = FiszTransformFromGroups(Cs1,Ds1,var)
    C01s = inverseHaarWaveletTransformForGroups(Cs1,Fs1)
    #去噪开始
    Cs2  = getScalingCoefficientsFromGroups(C01s)
    Ds2  = getWaveletCoefficientsFromGroups(Cs2)
    Denoise_Ds2 = ThresholdForGroups(Ds2,thresholdMode,thresholdName)
    #Denoise_Ds2 = Ds2
    C02s = inverseHaarWaveletTransformForGroups(Cs2,Denoise_Ds2)
    #去噪结束
    Cs3  = getScalingCoefficientsFromGroups(C02s)
    Fs2  = getWaveletCoefficientsFromGroups(Cs3)
    CDs  = inverseFiszTransformFromGroups(Cs3,Fs2,var)
    Ds3 = CDs[1];
    Cs4 = CDs[0];
    C03s = inverseHaarWaveletTransformForGroups(Cs4,Ds3)
    idata= movingAverage(C03s,dataLength)
    return idata

def p_HAT(originDatas,thresholdMode,thresholdName,var):
    #print("2")
    data = copy.deepcopy(originDatas);
    dataLength = len(data)
    groupLength = getGroupLength(dataLength)
    groups = getGroups(data,groupLength)
    AT_groups = AnscombeTransformFromGroups(groups,var)

    Cs = getScalingCoefficientsFromGroups(AT_groups)
    Ds = getWaveletCoefficientsFromGroups(Cs)
    #print("3")

    Denoise_Ds = ThresholdForGroups(Ds,thresholdMode,thresholdName)
    #Denoise_Ds = Ds
    iAT_groups = inverseHaarWaveletTransformForGroups(Cs,Denoise_Ds)

    #iGroups = inverseAnscombeTransformFromGroups(iAT_groups)
    #idata = movingAverage(iGroups,dataLength)
    idata = movingAverage(iAT_groups,dataLength)
    idata = inverseAnscombeTransformFromGroup(idata,var);

    return idata

def p_HBT(originDatas,thresholdMode,thresholdName,var):
    #print("2")
    data = copy.deepcopy(originDatas);
    dataLength = len(data)
    groupLength = getGroupLength(dataLength)
    groups = getGroups(data,groupLength)
    BT_groups = BartlettTransformFromGroups(groups,var)

    Cs = getScalingCoefficientsFromGroups(BT_groups)
    Ds = getWaveletCoefficientsFromGroups(Cs)
    #print("3")
    Denoise_Ds = ThresholdForGroups(Ds,thresholdMode,thresholdName)
    #Denoise_Ds = Ds
    iBT_groups = inverseHaarWaveletTransformForGroups(Cs,Denoise_Ds)

    #iGroups = inverseAnscombeTransformFromGroups(iBT_groups)
    #idata = movingAverage(iGroups,dataLength)
    idata = movingAverage(iBT_groups,dataLength)

    idata = inverseBartlettTransformFromGroup(idata,var);
    return idata

def predictionMultiThreadingTest(filename,weightMethods,costMethods,costDataMethods,thresholdMethods,thresholdRules,dataTransforms,predictionIntervals,vares):
    #资源准备
    o_data = SRMtool.getData(filename)
    #excel文件准备
    res_filename = "MultPrediction_" + str(int(time.time())) + str(random.randint(0,9999)) + ".xlsx";
    desktop_path = '/var/www/html/wavelet/'+res_filename;
    desktop_path = "C:\\xampp\\htdocs\\" + res_filename;
    #desktop_path = res_filename;
    workbook = xlsxwriter.Workbook(desktop_path)
    #创建、写入文件信息页
    MessageWorksheet = workbook.add_worksheet('Information');
    InformationNames = ['filename','message']
    Informations = [filename,'多线程测试']
    SRMtool.excel_WriteRaw(InformationNames,0,0,MessageWorksheet)
    SRMtool.excel_WriteRaw(Informations,1,0,MessageWorksheet)
    #创建、写入结果汇总页
    TotalWorksheet = workbook.add_worksheet('TotalStudyResult');
    TotalStudyRawNames = ['weightMethod','costMethod','costDataMethod','dataTransform','thresholdMethod','thresholdRule','bandwidth','var'];
    SRMtool.excel_WriteRaw(TotalStudyRawNames,0,2*len(predictionIntervals),TotalWorksheet)
    TotalWorksheet.set_column(0,len(TotalStudyRawNames) + 2 * len(predictionIntervals) - 1,15);
    #创建多线程
    ThreadList = []
    i = 0;
    for predictionInterval in predictionIntervals:
        # 创建thread对象，target传入线程执行的函数，args传参数
        predictionIntervalMult = []
        predictionIntervalMult.append(predictionInterval);
        t = Process(target=predictionRun, args=(o_data,workbook,TotalWorksheet,i,len(predictionIntervals),weightMethods,costMethods,costDataMethods,thresholdMethods,thresholdRules,dataTransforms,predictionIntervalMult,vares,))
        ThreadList.append(t)
        i = i + 1
    #开始执行多线程
    for t in ThreadList:
        t.start()
    # 使用join()来完成线程同步
    for t in ThreadList:
        t.join()
    workbook.close();
    print(res_filename);

#功能类似predictionTest，只不过为了多线程调用而设计。供predictionMultiThreadingTest调用使用
#去除了读取数据，改为直接通过参数传入。去除了创建excel文件，改为传入excel文件句柄
def predictionRun(o_data,workbook,TotalWorksheet,totalCol,len_predictionIntervals,weightMethods,costMethods,costDataMethods,thresholdMethods,thresholdRules,dataTransforms,predictionIntervals,vares):
    predictionInterval = predictionIntervals[0]
    print(str(predictionInterval)+"_start!");
    #计算前准备
    tz = pytz.timezone('Asia/Tokyo');
    groupLength = len(o_data);
    logtotal_a  = len(weightMethods)*len(costMethods)*len(costDataMethods)*len(thresholdMethods)*len(thresholdRules)*len(predictionIntervals)
    logtotal    = logtotal_a*len(vares)*(len(dataTransforms)-1) + logtotal_a
    lognum = 1
    start_time = time.time();
    #初始化excel
    col_result = 0;
    raw_study = 1;
    #写入excel,原始数据
    StudyRawNames = ['predInterval','MSE1','MSE2','weightMethod','costMethod','costDataMethod','dataTransform','thresholdMethod','thresholdRule','bandwidth','var'];
    PredictionWorksheet = workbook.add_worksheet('PredictionResult_'+str(predictionInterval));
    StudyWorksheet = workbook.add_worksheet('PredictionStudy_'+str(predictionInterval));
    PredictionWorksheet.set_column(0, 0, 12);
    StudyWorksheet.set_column(0,len(StudyRawNames) - 1,15);
    SRMtool.excel_WriteRaw(StudyRawNames,0,0,StudyWorksheet)
    PredictionWorksheet.write(0, 0, 'OriginData');
    SRMtool.excel_WriteCol(o_data,1,col_result,PredictionWorksheet);
    TotalStudyNames = ['MSE1_'+str(predictionInterval),'MSE2_'+str(predictionInterval)];
    SRMtool.excel_WriteRaw(TotalStudyNames,0,2*totalCol,TotalWorksheet)
    col_result = col_result + 1;
    #分割数据
    predictionPoint = math.floor(groupLength * predictionInterval);
    ahead_data = o_data[0: predictionPoint];
    after_data = o_data[predictionPoint: groupLength];
    #写入excel,分割后数据(应与原始数据相同)
    PredictionWorksheet.write(0, 1, 'CutData');
    SRMtool.excel_WriteCol(ahead_data,1,col_result,PredictionWorksheet);
    SRMtool.excel_WriteCol(after_data,len(ahead_data) + 1,col_result,PredictionWorksheet);
    col_result = col_result + 1;
    #开始计算
    for weightMethod in weightMethods:
        for costMethod in costMethods:
            for costDataMethod in costDataMethods:
                for dataTransform in dataTransforms:
                    for thresholdMethod in thresholdMethods:
                        for thresholdRule in thresholdRules:
                            for var in vares:
                                h = 1.1;
                                if(weightMethod == 'none'):
                                    h = -1;
                                if(dataTransform == 'TranslationInvariant'):
                                    var = -1;
                                result = costPrediction(ahead_data,costMethod,costDataMethod,weightMethod,h,groupLength - predictionPoint,dataTransform,thresholdRule,thresholdMethod,var);
                                ahead  = result[0 : predictionPoint];
                                result = result[predictionPoint: groupLength];
                                parameterCombination = "PredictionInterval:"+str(predictionInterval)+" "+costMethod+"_"+costDataMethod+"_"+dataTransform+"_"+weightMethod+"_"+thresholdRule+"_"+thresholdMethod+"_var="+str(var)+"_h="+str(h)
                                #记录预测值到excel
                                PredictionWorksheet.write(0, col_result, parameterCombination);
                                SRMtool.excel_WriteCol(ahead,1,col_result,PredictionWorksheet);
                                SRMtool.excel_WriteCol(result,len(ahead) + 1,col_result,PredictionWorksheet);
                                col_result = col_result + 1;
                                #分析结果
                                mse1 = SRMtool.MSE(after_data,result);
                                mse2 = SRMtool.MSE(SRMtool.toCulData(after_data),SRMtool.toCulData(result));
                                #记录分析结果到excel
                                StudyResults = [predictionInterval,mse1,mse2,weightMethod,costMethod,costDataMethod,dataTransform,thresholdMethod,thresholdRule,h,var];
                                SRMtool.excel_WriteRaw(StudyResults,raw_study,0,StudyWorksheet)
                                TotalStudyResults = [weightMethod,costMethod,costDataMethod,dataTransform,thresholdMethod,thresholdRule,h,var];
                                SRMtool.excel_WriteRaw(TotalStudyResults,raw_study,2*len_predictionIntervals,TotalWorksheet)
                                TotalStudyMSEs = [mse1,mse2];
                                SRMtool.excel_WriteRaw(TotalStudyMSEs,raw_study,2*totalCol,TotalWorksheet)
                                raw_study = raw_study + 1;
                                #直接输出结果
                                i = datetime.datetime.now(tz)
                                now_time = "%s/%s %s:%s" % (i.month, i.day, i.hour, i.minute)
                                print("已完成:"+str(round((lognum/logtotal)*100,1))+"% 预计剩余时间:"+SRMtool.leftTime(start_time,lognum/logtotal)+" 当前时间:"+now_time+" "+str(round(mse1,3))+" "+str(round(mse2,3))+" "+parameterCombination);
                                lognum = lognum + 1
                                if(dataTransform == 'TranslationInvariant'):
                                    break;



#python c:\\xampp\\htdocs\\test.py C:\\xampp\\htdocs\\DS1.txt
def predictionTest(filename,weightMethods,costMethods,costDataMethods,thresholdMethods,thresholdRules,dataTransforms,predictionIntervals,vares):
    print(filename);
    o_data = SRMtool.getData(filename)
    tz = pytz.timezone('Asia/Tokyo');
    #结果写入excel
    res_filename = "Prediction_" + str(int(time.time())) + str(random.randint(0,9999)) + ".xlsx";
    desktop_path = '/var/www/html/wavelet/'+res_filename;
    desktop_path = "C:\\xampp\\htdocs\\" + res_filename;
    desktop_path = res_filename;
    workbook = xlsxwriter.Workbook(desktop_path)
    MessageWorksheet = workbook.add_worksheet('Information');
    InformationNames = ['filename']
    Informations = [filename]
    SRMtool.excel_WriteRaw(InformationNames,0,0,MessageWorksheet)
    SRMtool.excel_WriteRaw(Informations,1,0,MessageWorksheet)
    TotalWorksheet = workbook.add_worksheet('TotalStudyResult');
    TotalStudyRawNames = ['weightMethod','costMethod','costDataMethod','dataTransform','thresholdMethod','thresholdRule','bandwidth','var'];
    SRMtool.excel_WriteRaw(TotalStudyRawNames,0,2*len(predictionIntervals),TotalWorksheet)
    TotalWorksheet.set_column(0,len(TotalStudyRawNames) + 2 * len(predictionIntervals) - 1,15);
    totalCol = 0;
    h = 0;
    groupLength = len(o_data);
    logtotal_a  = len(weightMethods)*len(costMethods)*len(costDataMethods)*len(thresholdMethods)*len(thresholdRules)*len(predictionIntervals)
    logtotal    = logtotal_a*len(vares)*(len(dataTransforms)-1) + logtotal_a
    lognum = 1
    start_time = time.time();
    print("start!")
    for predictionInterval in predictionIntervals:
        col_result = 0;
        raw_study = 1;
        #写入excel,原始数据
        StudyRawNames = ['predInterval','MSE1','MSE2','weightMethod','costMethod','costDataMethod','dataTransform','thresholdMethod','thresholdRule','bandwidth','var'];
        PredictionWorksheet = workbook.add_worksheet('PredictionResult_'+str(predictionInterval));
        StudyWorksheet = workbook.add_worksheet('PredictionStudy_'+str(predictionInterval));
        PredictionWorksheet.set_column(0, 0, 12);
        StudyWorksheet.set_column(0,len(StudyRawNames) - 1,15);
        SRMtool.excel_WriteRaw(StudyRawNames,0,0,StudyWorksheet)
        PredictionWorksheet.write(0, 0, 'OriginData');
        SRMtool.excel_WriteCol(o_data,1,col_result,PredictionWorksheet);
        TotalStudyNames = ['MSE1_'+str(predictionInterval),'MSE2_'+str(predictionInterval)];
        SRMtool.excel_WriteRaw(TotalStudyNames,0,2*totalCol,TotalWorksheet)
        col_result = col_result + 1;
        #开始计算
        predictionPoint = math.floor(groupLength * predictionInterval);
        ahead_data = o_data[0: predictionPoint];
        after_data = o_data[predictionPoint: groupLength];
        #写入excel,分割后数据(应与原始数据相同)
        PredictionWorksheet.write(0, 1, 'CutData');
        SRMtool.excel_WriteCol(ahead_data,1,col_result,PredictionWorksheet);
        SRMtool.excel_WriteCol(after_data,len(ahead_data) + 1,col_result,PredictionWorksheet);
        col_result = col_result + 1;
        #开始计算
        for weightMethod in weightMethods:
            for costMethod in costMethods:
                for costDataMethod in costDataMethods:
                    for dataTransform in dataTransforms:
                        for thresholdMethod in thresholdMethods:
                            for thresholdRule in thresholdRules:
                                for var in vares:
                                    h = 1.1;
                                    if(weightMethod == 'none'):
                                        h = -1;
                                    if(dataTransform == 'TranslationInvariant'):
                                        var = -1;
                                    result = costPrediction(ahead_data,costMethod,costDataMethod,weightMethod,h,groupLength - predictionPoint,dataTransform,thresholdRule,thresholdMethod,var);
                                    ahead  = result[0 : predictionPoint];
                                    result = result[predictionPoint: groupLength];
                                    parameterCombination = "PredictionInterval:"+str(predictionInterval)+" "+costMethod+"_"+costDataMethod+"_"+dataTransform+"_"+weightMethod+"_"+thresholdRule+"_"+thresholdMethod+"_var="+str(var)+"_h="+str(h)
                                    #记录预测值到excel
                                    PredictionWorksheet.write(0, col_result, parameterCombination);
                                    SRMtool.excel_WriteCol(ahead,1,col_result,PredictionWorksheet);
                                    SRMtool.excel_WriteCol(result,len(ahead) + 1,col_result,PredictionWorksheet);
                                    col_result = col_result + 1;
                                    #分析结果
                                    mse1 = SRMtool.MSE(after_data,result);
                                    mse2 = SRMtool.MSE(SRMtool.toCulData(after_data),SRMtool.toCulData(result));
                                    #记录分析结果到excel
                                    StudyResults = [predictionInterval,mse1,mse2,weightMethod,costMethod,costDataMethod,dataTransform,thresholdMethod,thresholdRule,h,var];
                                    SRMtool.excel_WriteRaw(StudyResults,raw_study,0,StudyWorksheet)
                                    TotalStudyResults = [weightMethod,costMethod,costDataMethod,dataTransform,thresholdMethod,thresholdRule,h,var];
                                    SRMtool.excel_WriteRaw(TotalStudyResults,raw_study,2*len(predictionIntervals),TotalWorksheet)
                                    TotalStudyMSEs = [mse1,mse2];
                                    SRMtool.excel_WriteRaw(TotalStudyMSEs,raw_study,2*totalCol,TotalWorksheet)
                                    raw_study = raw_study + 1;
                                    #直接输出结果
                                    i = datetime.datetime.now(tz)
                                    now_time = "%s/%s %s:%s" % (i.month, i.day, i.hour, i.minute)
                                    print("已完成:"+str(round((lognum/logtotal)*100,1))+"% 预计剩余时间:"+SRMtool.leftTime(start_time,lognum/logtotal)+" 当前时间:"+now_time+" "+str(round(mse1,3))+" "+str(round(mse2,3))+" "+parameterCombination);
                                    lognum = lognum + 1
                                    if(dataTransform == 'TranslationInvariant'):
                                        break;
        totalCol = totalCol + 1;
    workbook.close();
    print(res_filename);










#预测用损失函数-多元版
#可选是否用核函数
def prediction_cost3(new_days,originDatas,dataTransform,thresholdRule,thresholdMethod,weightMethod,h,var):
    originDatas = copy.deepcopy(originDatas);
    new_days = copy.deepcopy(new_days);
#def prediction_cost1(new_day,args):
    #print(args)
    '''
    originDatas     = args[0];
    dataTransform  = args[1];
    thresholdRule   = args[2];
    thresholdMethod = args[3];
    '''
    #加入预测值
    length_test = len(originDatas);
    for x in new_days:
        originDatas.append(x)
    #降噪
    if(dataTransform == 'Anscombe'):
        result1 = p_HAT(originDatas,thresholdRule,thresholdMethod,var)
    elif(dataTransform == 'Fisz'):
        result1 = p_HFT(originDatas,thresholdRule,thresholdMethod,var)
    elif(dataTransform == 'Bartlett'):
        result1 = p_HBT(originDatas,thresholdRule,thresholdMethod,var)
    elif(dataTransform == 'TranslationInvariant'):
        result1 = p_HTI(originDatas,thresholdRule,thresholdMethod)
    else :
        sys.exit(1);
    #添加权值
    length = len(originDatas);
    if(weightMethod != 'none'):
        weight = SRMtool.KernelWeight(length + 1,1,length,h,weightMethod);
        i = 0
        while i < length:
            result1[i] = result1[i] * weight[i]
            i = i + 1;
    #计算误差 第一个到预测日
    i = 0;
    total = 0;
    while i < length:
        x = result1[i] - originDatas[i];
        total = total + x**2;
        i = i + 1;
    total = total ** 0.5;
    return total;
