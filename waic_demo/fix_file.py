# 读取文件
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到第 619 行（索引 618），保留到这一行为止
# 第 617-618 行是 "if __name__ == "__main__":" 和 "    pass"
# 从第 619 行开始删除

# 保留前 619 行（索引 0-618）
clean_lines = lines[:619]

# 写回文件
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(clean_lines)

print("文件已清理，保留前 619 行")
