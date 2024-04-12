#!/usr/bin/python3
# cocos2d-js资源还原
# Date: 2024/2/14
import os
import json
import shutil
 
# static sheets
# src: cocos2d/core/utils/decode-uuid
i = [64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,62,64,64,64,63,52,53,54,55,56,57,58,59,60,61,64,64,64,64,64,64,64,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,64,64,64,64,64,64,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51]
a = ["", "", "", "", "", "", "", "", "-", "", "", "", "", "-", "", "", "", "", "-", "", "", "", "", "-", "", "", "", "", "", "", "", "", "", "", "", ""]
n = '0123456789abcdef'
s = [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 14, 15, 16, 17, 19, 20, 21, 22, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
 
def decode_uuid(t):
    if len(t) != 22:
        return t
    
    a[0] = t[0]
    a[1] = t[1]
    r = 2
    for e in range(2, 22, 2):
        o = i[ord(t[e])]
        l = i[ord(t[e + 1])]
        a[s[r]] = n[o >> 2]
        a[s[r + 1]] = n[(3 & o) << 2 | l >> 4]
        a[s[r + 2]] = n[15 & l]
        r += 3
        
    return ''.join(a)
 
def replace_uuids(json_str):
    data = json.loads(json_str)
    uuids = data.get('uuids', [])
    decoded_uuids = [decode_uuid(uuid) for uuid in uuids]
    data['uuids'] = decoded_uuids
    return json.dumps(data)
 
if not os.path.exists('config_patch.json'):
    json_str = open("config.json").read()
    json_str = replace_uuids(json_str)
    file = open("config_patch.json", "w")
    file.write(json_str)
    file.close() #Windows需要close
 
config = json.load(open('config_patch.json'))
# 遍历paths
for key, value in config["paths"].items():
    path = value[0]
    uuid_index = int(key)
    uuid = config["uuids"][uuid_index]
    output_dir = f"output/{path}"
    os.makedirs(output_dir, exist_ok=True)
 
    # 在import和native两个目录下判断{对应uuid前两位}/{对应uuid}.*
    for root, dirs, files in os.walk("import"):
        for file in files:
            if uuid[:2] in root and uuid in file:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(output_dir, file)
                # 如果output目录已存在同名文件，重命名
                if os.path.exists(dst_file):
                    index = 1
                    while True:
                        new_dst_file = os.path.join(output_dir, f"{file}.{index}")
                        if not os.path.exists(new_dst_file):
                            dst_file = new_dst_file
                            break
                        index += 1
                shutil.copy(src_file, dst_file)
 
    for root, dirs, files in os.walk("native"):
        for file in files:
            if uuid[:2] in root and uuid in file:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(output_dir, file)
                if os.path.exists(dst_file):
                    index = 1
                    while True:
                        new_dst_file = os.path.join(output_dir, f"{file}.{index}")
                        if not os.path.exists(new_dst_file):
                            dst_file = new_dst_file
                            break
                        index += 1
                shutil.copy(src_file, dst_file)
    #对单文件目录的处理
    files = os.listdir(output_dir)
    if len(files) == 1 and os.path.isfile(os.path.join(output_dir, files[0])):
        file_to_move = os.path.join(output_dir, files[0])
        new_path = os.path.join(os.path.dirname(output_dir), os.path.basename(output_dir) + os.path.splitext(files[0])[1])
        if os.path.exists(new_path):
            index = 1
            while True:
                new_paths = str(index) + "_" + new_path
                if not os.path.exists(new_paths):
                    new_path = new_paths
                    break
                index += 1
        try:
            os.rename(file_to_move, new_path)
        except:
            print(f"诶, {new_path} 无法访问")
        os.rmdir(output_dir)
 
print("文件复制完成")