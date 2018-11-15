import csv
import os

'''
==========扫描华能电厂煤堆扫描数据========
煤堆长度大约 260米
大车移动速度 20米/分钟
扫描仪，1帧 2400个点，每个点度数 0.512 ,时间戳间隔 200ms

=========数据集格式==========
帧号,X,Y,Z,角度,距离,时间戳

'''
class HuaNengTools:
    '''
    由于Pacp扫描文件太大，所以把帧数据分成4份导出
    1、将导出的4个点云数据集合并成1个数据集
    2、通过大车移动速度计算X坐标
    3、X 轴进行翻转
    '''
    def doWork1(self, outFilePath, inFilePaths):
        #计算参数
        CarSpeed = 0.06333
        FrameNum = 2400
        MaxX = 253.38333

        #删除之前保存文件，重新写入
        if os.path.exists(outFilePath):
            os.remove(outFilePath)

        out = open(outFilePath, 'a', newline='')
        csv_write = csv.writer(out, dialect='excel')

        index = 0
        for filePath in inFilePaths:
            with open(filePath,'r') as fileCSV:
                csv_data = csv.reader(fileCSV)
                for rows in csv_data:
                    timeStep = int(index / FrameNum)
                    X = timeStep * CarSpeed
                    rows[0] = timeStep
                    rows[1] = MaxX - X
                    csv_write.writerow(rows)
                    index += 1

    '''
    Sick扫描后的数据通过 CloudCompare工具裁剪，格式 X Y Z
    1、把格式改成 X,Y,Z
    2、智能补全，网格化处理程序调用，需要改变数据格式
    原始格式    X:煤堆长度(大车运动方向)  Y:煤堆高度  Z:煤堆横截面
    修改后格式   X:煤堆长度(大车运动方向)  Y:煤堆横截面 Z:煤堆高度
    3、做10选1处理
    4、煤堆高度数据反向
    '''
    def doWork2(self, inFilePath, outFilePath ):
        #参数设置
        MaxHeight = 13
        FillerNum = 10

        #删除之前保存文件，重新写入
        if os.path.exists(outFilePath):
            os.remove(outFilePath)

        out = open(outFilePath, 'w', newline='')
        csv_write = csv.writer(out, dialect='excel')

        index = 0  # 十选一计数
        with open(inFilePath, 'r') as oFile:
            csv_file01 =  csv.reader(oFile, delimiter = ' ',  quotechar = ' ')
            for str in csv_file01:
                newStr = []
                str = list(str)
                newStr.append(abs(float(str[0])))
                newStr.append(abs(float(str[2])))
                newStr.append(MaxHeight - abs(float(str[1])))
                if index % FillerNum == 0:
                    csv_write.writerow(newStr)
                index +=1

        out.close()

'''
程序处理
'''
if __name__ == "__main__":
    tools = HuaNengTools()

    print('华能电厂扫描数据集处理')

    outFilePath = r'20181024093450.txt'
    inFilePaths = [
        '20181024093450_1.txt',
        '20181024093450_2.txt',
        '20181024093450_3.txt',
        '20181024093450_1.txt'
    ]

    tools.doWork1(outFilePath = outFilePath, inFilePaths = inFilePaths)

    #生成智能补全程序数据集格式
    # outFilePath = r'E:\meidui_result\20181024093450_right_AA.txt'
    # inFilePath = r'E:\meidui_result\20181024093450_right_A.txt'
    # tools.doWork2(inFilePath = inFilePath, outFilePath = outFilePath)
