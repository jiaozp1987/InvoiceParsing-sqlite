# InvoiceParsing-sqlite
解析增值税及普通电子发票，结果生成excel文档，可识别是否重复报销。

原始发票（pdf，png，jpg）放入input文件夹
png和jpg文件不支持中文名称，如果存在将被自动修改名称
在confDomain.py中设定好自己公司的名称和税号
执行main.py
output文件夹中获取excel结果文档
