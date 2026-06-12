import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sec.bin import sheet_url



os.chdir(os.path.dirname(os.path.abspath(__file__)))


#a = [
#    [1,4],
#    [2,5],
#    [2,6]
#]


def insert_matrix(sheet_name:str, start_cell:str, data_list:list, credential_path= 'sec\\sw-ocp-29764e9584b5.json', spreadsheet_url=sheet_url):
    """
    在指定sheet，從指定格開始插入一定範圍資料。

    :param spreadsheet_url: sheet網址
    :param sheet_name: 工作表名稱
    :param start_cell: 起始cell
    :param data_list: 插入資料, row_list in list matrix格式
    :param credential_path: google api 密鑰路徑
    """

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credential_path, scope)
    client = gspread.authorize(creds)

    spreadsheet = client.open_by_url(spreadsheet_url)
    worksheet = spreadsheet.worksheet(sheet_name)

    # start cell error catch

    import re
    match = re.match(r"([A-Za-z]+)(\d+)", start_cell)
    if not match:
        raise ValueError("起始儲存格格式錯誤。")
    
    start_col_letter, start_row = match.groups()
    start_row = int(start_row)
    start_col_index = col_letter_to_index(start_col_letter)

    #轉數字算長寬再轉回
    num_rows = len(data_list)
    num_cols = len(data_list[0]) if num_rows > 0 else 0
    end_col_index = start_col_index + num_cols - 1
    end_col_letter = col_index_to_letter(end_col_index)
    end_row = start_row + num_rows - 1
    end_cell = f"{end_col_letter}{end_row}"

    cell_range = f"{start_cell}:{end_cell}"
    worksheet.update(cell_range, data_list)

    

def col_letter_to_index(col_letter):
    """將 Excel 欄位字母轉換為 0-indexed 數字（A=0, B=1, ..., Z=25, AA=26, AB=27, ...）"""
    col_letter = col_letter.upper()
    result = 0
    for c in col_letter:
        result = result * 26 + (ord(c) - ord('A') + 1)
    return result - 1  # 改為 0-indexed


def col_index_to_letter(index):
    """將 0-indexed 欄位數字轉換為 Excel 字母"""
    index += 1  # 改為 1-indexed
    letters = ""
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


if __name__ == '__main__':
    print('working')