import chardet, os, sys


# 显示当前工作目录
# print(os.getcwd())

def get_encoding(file):
    with open(file, "rb") as f:
        data = f.read()
        return chardet.detect(data)['encoding']

def change_encoding(file):
    # 正确解码-->二进制；
    with open(file, "r", encoding=code_type) as f:
        content = f.read()
    # 二进制-->正确编码；
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("编码已经转为：utf-8。")

code_type = ''

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("缺少目标文件！")
        exit(0)
    # argv[0]脚本自身路径名，参数从argv[1]开始；argv[1]是文件名；
    if len(sys.argv) >= 2: 
        code_type = get_encoding(sys.argv[1])
        print("本文件编码为：" + code_type)
    
    if len(sys.argv) == 3:
        if sys.argv[2] == '--change': # 默认修改为utf-8；
            change_encoding(sys.argv[1])
        else:
            print("参数错误！")
