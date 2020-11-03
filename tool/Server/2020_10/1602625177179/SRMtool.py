import math
import xlsxwriter
import time
import random
import itertools
from sympy import *

def getData(filename):
    with open(filename, 'r') as f:
        data = f.readlines()
        list = []
        for line in data:
            odom = line.split()
            list.append(float(odom[1]))   
    return list

def getParameterList(filename):
    MethodNames = ['ExpSRM','GammaSRM','ParetoSRM','TruncNormalSRM','LogNormalSRM','TruncLogistSRM','LogLogistSRM','TruncEVMaxSRM','LogEVMaxSRM','TruncEVMinSRM','LogEVMinSRM']
    with open(filename, 'r') as f:
        data = f.readlines()
        ParameterList = []
        i = 0;
        j = 0;
        while (i < len(data)) and (j < len(MethodNames)):
            data[i]=data[i].strip('\n')
            if(data[i] != MethodNames[j]):
                i = i + 1;
                continue
            lists = []
            if(data[i] == 'ExpSRM'):
                lists.append(float(data[i + 1]))
                lists.append(float(data[i + 2]))
                lists.append(float(0))#仅形式上存在
            else:
                lists.append(float(data[i + 1]))
                lists.append(float(data[i + 2]))
                lists.append(float(data[i + 3]))
            ParameterList.append(lists);
            i = i + 1;
            j = j + 1;
    return ParameterList

#读取参数文件方法
def multi_ReadParaFunction(ParaFile):
    print("new multi_ReadParaFunction")
    # 读取参数
    MethodNames = ['weightMethods','costMethods','costDataMethods','thresholdMethods','thresholdRules','dataTransforms','predictionIntervals','vares','compares','ifUseEstimation','ifCompareNewData']
    with open(ParaFile,'r') as f:
        data = f.readlines()
        ParameterList = []
        i = 0
        j = 0
        while (i < len(data)) and (j < len(MethodNames)):
            data[i]=data[i].strip('\n')
            if(data[i] != MethodNames[j]):
                i = i + 1;
                continue
            lists = []
            readLine = int(data[i + 1])
            k = 0
            while k < readLine:
                if(MethodNames[j] == 'predictionIntervals' or MethodNames[j] == 'vares' or MethodNames[j] == 'compares'):
                    lists.append(float(data[i + k + 2].strip('\n')))
                else:
                    lists.append(data[i + k + 2].strip('\n'))
                k = k + 1
            ParameterList.append(lists);
            i = i + 1;
            j = j + 1;
            
    #获得所有参数的组合
    list1 = itertools.product( *ParameterList )
    paraTuple = tuple(x for x in list1)
    print("hello")
    return paraTuple


def MSE(originDatas,tranDatas):
    if(len(originDatas) != len(tranDatas)):
        return false;
    length = len(originDatas);
    #print("length:"+ length)
    total = 0;
    i = 0;
    for data in originDatas:
        x =  tranDatas[i] - data;
        total = total + x*x;
        i = i + 1;
    #print(i);
    #print(length);
    total = total ** 0.5;
    return total / length;

#累计数据
def MLL1(originDatas,tranDatas):
    length = len(originDatas);
    a = 0;
    b = tranDatas[length - 1]
    c = 0;
    i = 1;
    while i < length:
        x = (originDatas[i] - originDatas[i - 1]) * math.log(tranDatas[i] - tranDatas[i - 1]);
        a = a + x;
        i = i + 1;
    i = 1;
    while i < length:
        y = math.factorial( (originDatas[i] - originDatas[i - 1]) );
        x = math.log( y );
        c = c + x;
        i = i + 1;
    d = a - b - c;
    return d;

#单日数据
def MLL2(originDatas,tranDatas):
    length = len(originDatas);
    a = 0;
    b = 0;
    c = 0;
    i = 0;
    while i < length:
        #print(tranDatas[i])
        x = originDatas[i] * math.log(tranDatas[i]);
        a = a + x;
        i = i + 1;
    i = 0;
    while i < length:
        x = originDatas[i]
        b = b + x;
        i = i + 1;
    i = 0;
    while i < length:
        y = math.factorial(originDatas[i]);
        x = math.log( y );
        c = c + x;
        i = i + 1;
    d = a - b - c;
    return d;

def toCulData(data):
    c_odata = [0]*len(data)
    i = 0;
    for x in data:
        if(i == 0):
            c_odata[i] = x;
        else :
            c_odata[i] = c_odata[i - 1] + x;
        i = i + 1;
    return c_odata;

#利用核函数计算数据的权值 now_day是天数，例如65，则返回1~64天，每天的数据相对于第65天的权值.h为带宽
#kernelMethod 为选择核方法，可选值为 boxcar,Gaussian,Epanechnikov,tricube
def KernelWeight(now_day,startDay,endDay,h,kernelMethod):
    if(startDay > endDay):
        return false;
    weights = [];
    denominator = 0;
    i = startDay;
    while i <= endDay:
        a = (i - now_day) / h;
        weight = Kernel(a, kernelMethod);
        denominator = denominator + weight;
        weights.append(weight);
        i = i + 1;
    i = 0;
    while i < endDay - startDay + 1:
        weights[i] = weights[i]/denominator;
        i = i + 1;
    return weights;

#核函数计算
def Kernel(x,kernelMethod):
    if(kernelMethod == 'boxcar'):
        return boxcarKernel(x);
    elif(kernelMethod == 'Gaussian'):
        return GaussianKernel(x);
    elif(kernelMethod == 'Epanechnikov'):
        return EpanechnikovKernel(x);
    elif(kernelMethod == 'tricube'):
        return tricubeKernel(x);
    else:
        return false;

#核函数具体实现
def boxcarKernel(x):
    a = 0.5 * I(x);
    return a;

def GaussianKernel(x):
    a = -0.5 * x * x;
    b = math.exp(a);
    c = (math.pi * 2) ** -0.5
    d = c * b;
    return d;

def EpanechnikovKernel(x):
    a = 0.75 * (1 - x*x) * I(x);
    return a;

def tricubeKernel(x):
    a = 70/81;
    b = (1 - abs(x)**3)**3;
    c = a * b * I(x);
    return c;

def I(x):
    x = abs(x);
    if(x <= 1):
        return 1;
    return 0;

#python c:\\xampp\\htdocs\\SRMtool.py
#originDatas为单日产生bug数,并非累积.前predictionInterval的数据不参与mse的计算
def SRATS_analysis(data_filename,para_filenames,predictionIntervals):
    if(len(para_filenames) != len(predictionIntervals)):
        return false;
    #获取数据和参数
    originDatas = getData(data_filename);
    parameterLists = []
    for file in para_filenames:
        parameterList = getParameterList(file);
        parameterLists.append(parameterList);
    #创建平均数函数数组
    meanFunctions = [ExpSRM,GammaSRM,ParetoSRM,TruncNormalSRM,LogNormalSRM,TruncLogistSRM,LogLogistSRM,TruncEVMaxSRM,LogEVMaxSRM,TruncEVMinSRM,LogEVMinSRM];
    #结果写入excel
    res_filename = "SRATS_analysis_"+str(time.time()) + str(random.randint(0,9999)) + ".xlsx";
    desktop_path = '/var/www/html/wavelet/'+res_filename;
    desktop_path = "C:\\xampp\\htdocs\\" + res_filename;
    desktop_path = res_filename;
    ResultColNames = ['OriginData','ExpSRM','GammaSRM','ParetoSRM','TruncNormalSRM','LogNormalSRM','TruncLogistSRM','LogLogistSRM','TruncEVMaxSRM','LogEVMaxSRM','TruncEVMinSRM','LogEVMinSRM']
    StudyColNames = ['MethodName','MSE1','MSE2']
    MethodNames = ['ExpSRM','GammaSRM','ParetoSRM','TruncNormalSRM','LogNormalSRM','TruncLogistSRM','LogLogistSRM','TruncEVMaxSRM','LogEVMaxSRM','TruncEVMinSRM','LogEVMinSRM']

    '''
    #测试用数组
    meanFunctions = [ExpSRM,GammaSRM];
    ResultColNames = ['OriginData','ExpSRM','GammaSRM']
    MethodNames = ['ExpSRM','GammaSRM']
    '''
    #计算预计剩余时间用
    logtotal = len(parameterLists)*len(meanFunctions)
    lognum = 1
    start_time = time.time();
    
    workbook = xlsxwriter.Workbook(desktop_path)
    TotalWorksheet = workbook.add_worksheet('TotalStudyResult');
    totalCol = 0;
    fileNum = 0;
    for parameterList in parameterLists:
        predictionInterval = predictionIntervals[fileNum];
        fileNum = fileNum + 1;
        ResultWorksheet = workbook.add_worksheet('Result'+str(predictionInterval));
        StudyWorksheet = workbook.add_worksheet('Study'+str(predictionInterval));
        excel_WriteRaw(ResultColNames,0,0,ResultWorksheet);
        excel_WriteCol(originDatas,1,0,ResultWorksheet);
        excel_WriteRaw(StudyColNames,0,0,StudyWorksheet);
        excel_WriteCol(MethodNames,1,0,StudyWorksheet);
        excel_WriteRaw(StudyColNames,0,totalCol,TotalWorksheet);
        excel_WriteCol(MethodNames,1,totalCol,TotalWorksheet);
        TotalWorksheet.write(0,totalCol,'MethodName'+str(predictionInterval));
        TotalWorksheet.set_column(totalCol, totalCol, 16);
        StudyWorksheet.set_column(0, 0, 16);
        ResultWorksheet.set_column(0, 0, 16);
        #开始利用STATS推断出的参数进行计算
        groupLength = len(originDatas);
        predictionPoint = math.floor(groupLength * predictionInterval);
        after_data = originDatas[predictionPoint: groupLength];
        Results = []
        MSEResults = []
        i = 0;
        for meanFunction in meanFunctions:
            times = 1;
            lists = [];
            Results.append(lists);
            mseLists = [];
            MSEResults.append(mseLists);
            while times <= groupLength:

                #计算单日增量
                if(times != 1):
                    Results[i].append(meanFunction(times,parameterList[i][0],parameterList[i][1],parameterList[i][2]) - meanFunction(times - 1,parameterList[i][0],parameterList[i][1],parameterList[i][2]));
                else:
                    Results[i].append(meanFunction(times,parameterList[i][0],parameterList[i][1],parameterList[i][2]));
                '''
                #计算累积bug数
                Results[i].append(meanFunction(times,parameterList[i][0],parameterList[i][1],parameterList[i][2]));
                '''
                times = times + 1
            print("已完成:"+str(round((lognum/logtotal)*100,1))+"% 预计剩余时间:"+leftTime(start_time,lognum/logtotal)+" "+str(parameterList[i][0])+" "+str(parameterList[i][1])+" "+str(parameterList[i][2])+" ");
            lognum = lognum + 1
            after_result_data = Results[i][predictionPoint: groupLength];
            mse1 = MSE(after_data,after_result_data);
            mse2 = MSE(toCulData(after_data),toCulData(after_result_data));
            MSEResults[i].append(mse1);
            MSEResults[i].append(mse2);
            i = i + 1;
        #记录结果至excel
        i = 1;
        for Result in Results:
            excel_WriteCol(Result,1,i,ResultWorksheet);
            StudyWorksheet.write(i,1,MSEResults[i-1][0]);
            StudyWorksheet.write(i,2,MSEResults[i-1][1]);
            TotalWorksheet.write(i,totalCol+1,MSEResults[i-1][0]);
            TotalWorksheet.write(i,totalCol+2,MSEResults[i-1][1]);
            i = i + 1;
        totalCol = totalCol + 3
    workbook.close();

#将datas内的数据写入一列。从(raw,col)开始往下写入.(0,0)为第一行第一列
def excel_WriteCol(datas,raw,col,worksheet):
    i = 0;
    for data in datas:
        worksheet.write(raw + i,col,data);
        i = i + 1;

#将datas内的数据写入一行。从(raw,col)开始往右写入.(0,0)为第一行第一列
def excel_WriteRaw(datas,raw,col,worksheet):
    i = 0;
    for data in datas:
        worksheet.write(raw,col + i,data);
        i = i + 1;

#SRM平均值计算
#ExpSRM的参数c仅为了与其他函数保持参数列表形式上的一致而设立，并未使用
def ExpSRM(t,a,b,c):
    def F(times,p2):
        x = math.exp(-1 * p2 * times);
        return 1 - x;
    return a * F(t,b);
    
def GammaSRM(t,a,b,c):
    def F(times,p2,p3):
        s = symbols('s');
        return integrate(((p3**p2)*(s**(p2-1))*exp(-1*p3*s))/GammaFunction(p2),(s,0,times)).evalf()
    return a * F(t,b,c)
    
def ParetoSRM(t,a,b,c):
    def F(times,p2,p3):
        x = (p3 / (times + p3)) ** p2;
        return 1 - x;
    return a * F(t,b,c);

def TruncNormalSRM(t,a,b,c):
    F0 = NormalFunction(0,b,c);
    return a * (NormalFunction(t,b,c) - F0) / (1 - F0);
    
def LogNormalSRM(t,a,b,c):
    return a * NormalFunction(math.log(t),b,c);

def TruncLogistSRM(t,a,b,c):
    F0 = LogistFunction(0,b,c);
    return a * (LogistFunction(t,b,c) - F0) / (1 - F0);
    
def LogLogistSRM(t,a,b,c):
    return a * LogistFunction(math.log(t),b,c);

def TruncEVMaxSRM(t,a,b,c):
    F0 = EVFunction(0,b,c);
    return a * (EVFunction(t,b,c) - F0) / (1 - F0);
    
def LogEVMaxSRM(t,a,b,c):
    return a * EVFunction(math.log(t),b,c);

def TruncEVMinSRM(t,a,b,c):
    F0 = EVFunction(0,b,c);
    return a * (F0 - EVFunction(-1*t,b,c)) / F0;

def LogEVMinSRM(t,a,b,c):
    return a * (1 - EVFunction(-1 * math.log(t),b,c));

#SRM函数
def NormalFunction(t,b,c):
    x = 1/(math.sqrt(2 * math.pi)*b);
    s = symbols('s');
    #此处存疑。到底是 2*(b**2) 还是 (2*b)**2.暂时按前者计算
    #更新：已验证，前者正确。
    y = integrate(exp(-1*(((s-c)**2))/(2*b*b)),(s,-oo,t)).evalf();
    return x * y;

def LogistFunction(t,b,c):
    x = math.exp(-1 * (t - c)/b);
    return 1 / (1 + x);

def EVFunction(t,b,c):
    x = -1 * (t - c)/b;
    y = -1 * math.exp(x)
    return math.exp(y);

#伽玛函数
def GammaFunction(x):
    if(x <= 0):
        return false;
    t = symbols('t');
    return integrate((t ** (x-1))*exp(-1*t), (t, 0, +oo)).evalf();

#progress为一个0到1之间的数，表示已经完成了百分之多少的进度
#计算从start_time开始，到运行此函数时，已经完成了progress的进度的情况下，剩余进度需要多久完成。返回字符串
def leftTime(start_time,progress):
    now_time = time.time();
    time_left = now_time - start_time;
    expect_total_time = time_left / progress
    expect_left_time = expect_total_time - time_left;
    if(expect_left_time < 0):
        expect_left_time = 0
    m, s = divmod(int(expect_left_time), 60)
    h, m = divmod(m, 60)
    return "%d小时%02d分钟%02d秒"%(h, m, s)

#python c:\\xampp\\htdocs\\SRMtool.py
#测试区
'''
data_filename = 'C:\\xampp\\htdocs\\DS2.txt'
para_filename = 'C:\\xampp\\htdocs\\parameterList2-3.txt'
predictionInterval = 7/10;

originDatas = getData(data_filename);
parameterList = getParameterList(para_filename);
SRATS_analysis(originDatas,parameterList,predictionInterval);
print("ok");
'''
'''
a = parameterList[1][0];
b = parameterList[1][1];
c = parameterList[1][2];

print(str(a)+" "+str(b)+" "+str(c))

#ExpSRM
#ParetoSRM
#TruncNormalSRM
#LogNormalSRM
#TruncLogistSRM
#LogLogistSRM
#TruncEVMaxSRM
#LogEVMaxSRM
#TruncEVMinSRM
#LogEVMinSRM
i = 1;
while i < 10:
    print(GammaSRM(i,a,b,c))
    i = i + 1;
'''



