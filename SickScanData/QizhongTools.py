import csv
import os
'''
起重机项目数据格式转换工具

扫描仪 一帧：360度，16根激光
=========数据集格式==========
帧号,X,Y,Z,角度,距离,时间戳,信号强度
'''
class QizhongTools:

    def doWork(self,inFilePath,outFilePath):

        #删除之前保存文件，重新写入
        if os.path.exists(outFilePath):
            os.remove(outFilePath)

        out = open(outFilePath, 'w', newline='')
        csv_write = csv.writer(out, dialect='excel')

        with open(inFilePath,'r') as File01:
            csv_Reader = csv.reader(File01, dialect='excel')
            # csv_Datas = list(csv_Reader)
            for row in csv_Reader:
                #排除包围盒之外的坐标点
                if float(row[1]) < -19.0 or float(row[1]) > -14.0:
                    continue
                if float(row[2]) < -25.0 or float(row[2]) > 0.0:
                    continue
                if float(row[3]) < -18.0 or float(row[3]) > -5.0:
                    continue
                csv_write.writerow(row)

        out.close()




if __name__ == '__main__':
    tools = QizhongTools()

    inFilePath = r'E:\qizhongji_result\181106\20181106133928_1.txt'
    outFilePath = r'E:\qizhongji_result\181106\20181106133928_1_AA.txt'

    tools.doWork(inFilePath, outFilePath)