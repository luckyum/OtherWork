import csv
import os

'''
==========扫描煤堆扫描数据========
扫描仪，1帧 2400个点，每个点度数 0.512 ,时间戳间隔 200ms

=========数据集格式==========
帧号,X,Y,Z,角度,距离,时间戳，X轴偏角，Y轴偏角,小车位置

'''
class MeikuangTools:
    '''
    pcap文件 10秒分割一个文件，然后转换为点云数据，这个函数是把
    分割转换的点云文件合并成一个文件，方便工具查看
    '''
    def doWork1(self, outFilePath, inFilePaths):

        #删除之前保存文件，重新写入
        if os.path.exists(outFilePath):
            os.remove(outFilePath)

        out = open(outFilePath, 'a', newline='')
        csv_write = csv.writer(out, dialect='excel')

        for filePath in inFilePaths:
            with open(filePath,'r') as fileCSV:
                csv_data = csv.reader(fileCSV)
                for rows in csv_data:
                    csv_write.writerow(rows)


'''
程序处理
'''
if __name__ == "__main__":
    tools = MeikuangTools()

    print('煤矿扫描数据集处理')

    outFilePath = r'D:/SCanData/point/1/20/00000.txt'
    inFilePaths = []

    for i in range(1,9):
        # print("D:/SCanData/point/82/%d" % i )
        inFilePaths.append("D:/SCanData/pcap/1/20/{0}.txt".format(i) )

    tools.doWork1(outFilePath = outFilePath, inFilePaths = inFilePaths)

