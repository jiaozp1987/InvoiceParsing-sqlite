from Handler.excelHandler import excelOps
from Handler.ocrHandler import OCR
from Handler.pdfHandler import PDFInvoice


class invoiceRecord:

    def main(self):
        pdf = PDFInvoice()
        ocr = OCR()
        pdf.main()
        ocr.main()
        allInvoiceList = list()
        allInvoiceList.extend(pdf.invoiceList)
        allInvoiceList.extend(ocr.invoiceList)
        excelOps().add(allInvoiceList)


if __name__ == '__main__':
    invoiceRecord().main()
