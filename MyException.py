# 查重的文本没有汉字
class noChinese_error(Exception):
    def __init__(self):
        print("该查重文本没有汉字，错误！")
#读取的文件为空
class emptyText_error(Exception):
    def __init__(self):
        print("文本为空,请检查!")
