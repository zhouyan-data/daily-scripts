import pandas as pd
import os

def csv_to_excel(csv_path, excel_path=None):
    if excel_path is None:
        excel_path = csv_path.replace('.csv', '.xlsx')
    
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
        df.to_excel(excel_path, index=False)
        print(f"转换完成: {excel_path}")
    except Exception as e:
        print(f"转换失败: {e}")

def batch_convert(folder_path):
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    for f in files:
        csv_to_excel(os.path.join(folder_path, f))

if __name__ == '__main__':
    path = input("输入csv文件路径或文件夹路径: ")
    if os.path.isfile(path):
        csv_to_excel(path)
    elif os.path.isdir(path):
        batch_convert(path)
    else:
        print("路径不存在")
