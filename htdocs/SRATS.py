import SRMtool
# python c:\\xampp\\htdocs\\SRATS.py
#测试区
dataNum = '7' #修改数据集只需改这里
data_filename = 'C:\\xampp\\htdocs\\ftp_files\\work\\DS'+dataNum+'.txt'
para_filename1 = 'C:\\xampp\\htdocs\\sratsPara\\parameterList'+dataNum+'-1.txt'
para_filename2 = 'C:\\xampp\\htdocs\\sratsPara\\parameterList'+dataNum+'-2.txt'
para_filename3 = 'C:\\xampp\\htdocs\\sratsPara\\parameterList'+dataNum+'-3.txt'
para_filenames = [para_filename1,para_filename2,para_filename3]
predictionIntervals = [3/10,5/10,7/10];


SRMtool.SRATS_analysis(data_filename,para_filenames,predictionIntervals);
print("ok");