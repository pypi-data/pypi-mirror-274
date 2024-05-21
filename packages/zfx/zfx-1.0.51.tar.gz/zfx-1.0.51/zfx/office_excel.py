import openpyxl
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment


def excel_打开Excel文件(文件路径):
    """
    参数:
    - 文件路径: 要打开的 Excel 文件的路径

    返回值:
    - 如果成功打开文件，则返回 表格对象；如果文件打开失败，则返回 None

    使用提示：
    - 在文件被占用时，此函数无法获得操作权限，则会打开失败，返回None
    """
    try:
        return load_workbook(filename=文件路径)
    except Exception:
        return None


def excel_读取单元格(表格对象, 工作表名, 单元格):
    """
    参数:
    - 表格对象: 要读取单元格的表格对象
    - 工作表名: 要读取单元格的工作表名称
    - 单元格: 要读取的单元格的坐标，例如 'A1'

    返回值:
    - 如果成功读取单元格内容，则返回 单元格内容 ；如果读取失败，则返回 None
    """
    try:
        工作表 = 表格对象[工作表名]
        return 工作表[单元格].value
    except Exception:
        return None


def excel_修改单元格(表格对象, 工作表名, 单元格, 新值):
    """
    参数:
    - 表格对象: 要修改单元格的表格对象
    - 工作表名: 要修改单元格的工作表名称
    - 单元格: 要修改的单元格的坐标，例如 'A1'
    - 新值: 要设置的新值

    返回值:
    - 如果成功修改单元格内容，则返回 True ；如果修改失败，则返回 False
    """
    try:
        工作表 = 表格对象[工作表名]
        工作表[单元格] = 新值
        return True
    except Exception:
        return False


def excel_插入行(表格对象, 工作表名, 行号):
    """
    参数:
    - 表格对象: 要操作的表格对象
    - 工作表名: 要插入行的工作表名称
    - 行号: 要插入行的行号

    返回值:
    - 如果成功插入行，则返回 True；如果插入失败，则返回 False
    """
    try:
        工作表 = 表格对象[工作表名]
        工作表.insert_rows(行号)
        return True
    except Exception:
        return False


def excel_删除行(表格对象, 工作表名, 行号):
    """
    参数:
    - 表格对象: 要操作的表格对象
    - 工作表名: 要删除行的工作表名称
    - 行号: 要删除的行号

    返回值:
    - 如果成功删除行，则返回 True；如果删除失败，则返回 False
    """
    try:
        工作表 = 表格对象[工作表名]
        工作表.delete_rows(行号)
        return True
    except Exception:
        return False


def excel_设置单元格格式(表格对象, 工作表名, 单元格, 对齐=None):
    """
    参数:
    - 表格对象: 要操作的表格对象
    - 工作表名: 要设置单元格格式的工作表名称
    - 单元格: 要设置格式的单元格坐标，例如 'A1'
    - 对齐: 对齐方式，可选值为 "左对齐"、"右对齐"、"居中对齐"

    返回值:
    - 如果成功设置单元格格式，则返回 True；如果设置失败，则返回 False
    """
    try:
        工作表 = 表格对象[工作表名]
        单元格对象 = 工作表[单元格]
        if 对齐:
            if 对齐 == "左对齐":
                单元格对象.alignment = Alignment(horizontal='left')
            elif 对齐 == "右对齐":
                单元格对象.alignment = Alignment(horizontal='right')
            elif 对齐 == "居中对齐":
                单元格对象.alignment = Alignment(horizontal='center')
        return True
    except Exception:
        return False


def excel_保存Excel文件(表格对象, 文件路径):
    """
    参数:
    - 表格对象: 要保存的 Excel 文件的表格对象
    - 文件路径: 要保存的文件路径

    返回值:
    - 如果成功保存文件，则返回 True ；如果保存失败，则返回 False
    """
    try:
        表格对象.save(filename=文件路径)
        return True
    except Exception:
        return False


def excel_关闭Excel文件(表格对象):
    """
    参数:
    - 表格对象: 要关闭的 Excel 文件的表格对象

    返回值:
    - 如果成功关闭文件，则返回 True ；如果关闭失败，则返回 False

    使用提示：
    - 注意，如果修改内容之后直接调用此命令关闭表格，修改的内容不会进行保存。
    """
    try:
        表格对象.close()
        return True
    except Exception:
        return False