import os

folderPath="D:\\"

sort_folder_number = [x for x in range(0, 56)]
for number in sort_folder_number:
    new_folder_path = os.path.join(folderPath, '%s' % number)  # 新文件夹形如 ‘folderPath\number'
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print("new a floder named " + str(number) + 'at the path of ' + new_folder_path)
print("完成目录创建！")