import os
import json
import shutil
import sys
 
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
 
def parse_json_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                json_file = os.path.join(root, file)
                with open(json_file, 'r') as f:
                    json_data = json.load(f)
                try:
                 if json_data[3][0][0] != 'sp.SkeletonData':
                     continue
                except:
                 # Wrong format, skip
                 continue
                
                spine_data = json_data[5][0]
                spine_name = os.path.basename(os.path.dirname(json_file))
                
                if isinstance(spine_data[4], dict):
                    with open(os.path.join(root, f'{spine_name}.skel.json'), 'w') as f:
                        json.dump(spine_data[4], f)
                    with open(os.path.join(root, f'{spine_name}.atlas'), 'w') as f:
                        f.write(spine_data[2])
                    png_files = [f for f in os.listdir(root) if f.endswith('.png')]
                    if len(png_files) > 1:
                        print(f'error: 出现多个.png，目录: {root}')
                    elif len(png_files) == 1:
                        shutil.copyfile(os.path.join(root, png_files[0]), os.path.join(root, f'{spine_name}.png'))
                else:
                    with open(os.path.join(root, f'{spine_name}.atlas'), 'w') as f:
                        f.write(spine_data[3])
                    bin_files = [f for f in os.listdir(root) if f.endswith('.bin')]
                    if len(bin_files) > 1:
                        print(f'error: 出现多个.bin，目录: {root}')
                    elif len(bin_files) == 1:
                        shutil.copyfile(os.path.join(root, bin_files[0]), os.path.join(root, f'{spine_name}.skel.json'))
                    png_files = [f for f in os.listdir(root) if f.endswith('.png')]
                    if len(png_files) > 1:
                        print(f'error: 出现多个.png，目录: {root}')
                    elif len(png_files) == 1:
                        shutil.copyfile(os.path.join(root, png_files[0]), os.path.join(root, f'{spine_name}.png'))
 
parse_json_files('.')