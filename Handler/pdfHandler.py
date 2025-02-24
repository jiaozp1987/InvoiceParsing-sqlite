import os
import time

import fitz
from pyzbar.pyzbar import decode
from PIL import Image

from confDomain import confDomain
from invoiceDomain import invoiceDomain
from Handler.dbHandler import SQLops


class PDFInvoice:

    def __init__(self):
        self.base_path = "./input"
        self.file_paths = ""
        self.invoiceList = list()

    def get_filepath(self):
        '''获取当前路径下所有的电子发票pdf文件路径'''
        file_paths = []
        file_names = os.listdir(self.base_path)
        for file_name in file_names:
            if file_name.endswith('.pdf'):
                file_paths.append(os.path.join(self.base_path, file_name))
        self.file_paths = file_paths

    def get_invoiceList(self):

        '''逐一对所有电子发票文件左上角的二维码识别并重命名文件'''
        for file_path in self.file_paths:
            invoice = self.get_qrcode(file_path)
            self.invoiceList.append(invoice)

    # def record_invoice(self):
    #
    #     excelOps().add(self.invoiceList)

    def get_qrcode(self, file_path):
        invoice = invoiceDomain()
        '''提取pdf文件中左上角的二维码并识别'''
        pdfDoc = fitz.open(file_path)
        invoice.fileName = file_path.replace("./input\\", "")
        # 初始化一个空字符串来收集文本
        full_text = ""

        # 遍历每一页
        for page in pdfDoc:
            # 提取当前页面的文本并追加到full_text字符串
            full_text += page.get_text()

        full_text_list = full_text.split("\n")
        invoice.typeName = full_text_list[0]
        conf = confDomain()
        ini_index = 0
        for item in full_text_list:
            if item.find(conf.active) >= 0:
                ini_index = full_text_list.index(item)

        invoice.id = full_text_list[ini_index - 2]
        invoice.invoiceDate = full_text_list[ini_index - 1]
        invoice.toName = full_text_list[ini_index]
        invoice.toID = full_text_list[ini_index + 1]
        invoice.formName = full_text_list[ini_index + 2]
        invoice.formID = full_text_list[ini_index + 3]
        info = SQLops().find_by_id(invoice)
        if info is None:
            invoice.repeat = "否"
        else:
            invoice.createDate = info[10]
            invoice.repeat = "是"

        # page = pdfDoc[0]    #只对第一页的二维码进行识别

        rotate = int(0)
        zoom_x = 3.0
        zoom_y = 3.0
        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
        rect = page.rect
        mp = rect.tl + (rect.br - rect.tl) * 1 / 5
        clip = fitz.Rect(rect.tl, mp)
        pix = page.get_pixmap(matrix=mat, alpha=False, clip=clip)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        barcodes = decode(img)

        # 关闭文档
        pdfDoc.close()
        for barcode in barcodes:
            QRresult = barcode.data.decode("utf-8")
        QRresultList = QRresult.split(",")
        invoice.sumPrice = QRresultList[4]
        invoice.typeID = QRresultList[1]
        return invoice

    def main(self):
        self.get_filepath()
        self.get_invoiceList()
        # self.record_invoice()


if __name__ == '__main__':
    PDFInvoice().main()
