import os
import time

from confDomain import confDomain
from invoiceDomain import invoiceDomain
from Handler.dbHandler import SQLops

from paddleocr import PaddleOCR


class OCR:
    def __init__(self):
        self.base_path = "./input"
        self.file_paths = ""
        self.invoiceList = list()

    def rename4pic(self):
        """
        重命名函数fun2
        输入：文件夹路径
        功能：对某一个文件夹中的某一类文件进行统一命名，命名格式为：基础名+数字序号
        """
        i = 1
        for file in os.listdir(self.base_path):
            if file.endswith('.png') or file.endswith('.jpg'):
                if file.endswith('.png'):
                    suffix = '.png'
                else:
                    suffix = '.jpg'
                if os.path.isfile(os.path.join(self.base_path, file)):
                    new_name = file.replace(file, str(round(time.time()))+str(i) + suffix)  # 根据需要设置基本文件名
                    os.rename(os.path.join(self.base_path, file), os.path.join(self.base_path, new_name))
                    i += 1
        print("rename4pic over")

    def get_filepath(self):
        self.rename4pic()
        '''获取当前路径下所有的电子发票pdf文件路径'''
        file_paths = []
        file_names = os.listdir(self.base_path)
        for file_name in file_names:
            if file_name.endswith('.png'):
                file_paths.append(os.path.join(self.base_path, file_name))
            if file_name.endswith('.jpg'):
                file_paths.append(os.path.join(self.base_path, file_name))
        self.file_paths = file_paths

    def get_invoiceList(self):
        for item in self.file_paths:
            self.invoiceList.append(self.get_content(item))



    def get_content(self, img_path):
        invoice = invoiceDomain()
        invoice.fileName = img_path.replace("./input\\", "")
        ocr = PaddleOCR(use_angle_cls=True, lang="ch")
        result = ocr.ocr(img_path, cls=True)
        txts = list()
        for line in result[0]:
            txts.append(line[1][0])
        conf = confDomain()
        for i in range(len(txts)):
            if txts[i].find("发票号码") >= 0:
                ltxt = txts[i].split("：")
                invoice.id = ltxt[1]
            if txts[i].find("开票日期") >= 0:
                ltxt = txts[i].split("：")
                invoice.invoiceDate = ltxt[1]
            if txts[i] == '增值税专用发票' or txts[i] == '增值税电子普通发票':
                invoice.typeName = txts[i]
            if txts[i].find(conf.active) >= 0:
                ltxt = txts[i].split("：")
                invoice.toName = ltxt[1]
            if txts[i].find(conf.company[conf.active]) >= 0:
                ltxt = txts[i].split("：")
                invoice.toID = ltxt[1]
            if txts[i].find('名称') == 0:
                ltxt = txts[i].split("：")
                invoice.formName = ltxt[1]
            if txts[i].find('纳税人识别号') == 0:
                ltxt = txts[i].split("：")
                invoice.formID = ltxt[1]
            # 原格式文本输出
            # print(txts[i])
        qr_result = self.get_qr(img_path)
        qr_result = qr_result[0].split(",")
        invoice.typeID = qr_result[1]
        invoice.id = qr_result[3]
        invoice.sumPrice = qr_result[4]
        info = SQLops().find_by_id(invoice)
        if info is None:
            invoice.repeat = "否"
        else:
            invoice.createDate = info[10]
            invoice.repeat = "是"
        # print(txts)
        return invoice

    def get_qr(self, img_path):
        import cv2

        # 使用微信的识别模型
        qrstr = cv2.wechat_qrcode_WeChatQRCode()

        # 读取图片
        image = cv2.imread(img_path)

        # 获取值
        result, pos = qrstr.detectAndDecode(image)

        return result

    def main(self):
        self.get_filepath()
        self.get_invoiceList()
        # self.record_invoice()


if __name__ == '__main__':
    # OCR().main()
    print(round(time.time()))
    # import cv2
    #
    # # 使用微信的识别模型
    # qrstr = cv2.wechat_qrcode_WeChatQRCode()
    #
    # # 读取图片
    # image = cv2.imread('./20250102222223.png')
    #
    # # 获取值
    # result, pos = qrstr.detectAndDecode(image)
    #
    # print('结果:', result)
    # print('坐标定位:', pos)
