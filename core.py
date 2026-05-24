import os, re, random, shutil
os.chdir(os.path.dirname(__file__).replace(r'\StardewValleySaveDuplicater',''))
def main(folder = None, farm_name = None):
    os.chdir(f'C:/Users/{os.environ.get('USERNAME')}/AppData/Roaming/StardewValley/Saves')
    try:
        if folder.isnumeric() and len(folder) != 9: print('ID須為9位數字')
    except:
        pass
    # 輸入全文
    if '_' in folder and len(folder[folder.rfind('_')+1:]) == 9 :
        path = f'./{folder}'
    elif folder.isnumeric():
        # 輸入ID``
        end = str(os.listdir('./')).find(folder) + 8
        start = str(os.listdir('./'))[:end].rfind('\'') + 1
        num = f'./{(str(os.listdir('./'))[:end])}'
        path = (str(os.listdir('./'))[start:end+1])
    else:
        head = str(os.listdir('./')).find(folder)
        # 輸入存檔名稱
        path = f'./{(str(os.listdir('./'))[head:head+len(folder)+10])}'
        
    # 輸入牧場名
    try:
        farm_name = farm_name
        if farm_name == None: raise
    except:
        print('牧場名不能為空')
    uniqueIDForThisGame = str(random.randint(0,999999999)).zfill(9)
    new_path = f'./{farm_name}_{uniqueIDForThisGame}'

    shutil.copytree(path, new_path,)
    os.rename(new_path+'/'+path.replace('.',''), new_path+new_path.replace('.',''))
    os.rename(f'{new_path}/{path.replace('.','')}_old', f'{new_path}{new_path.replace('.','')}_old')

    file_info = new_path + '/SaveGameInfo'
    file_info_old = new_path + '/SaveGameInfo_old'
    file_main = new_path + new_path.replace('.','')
    file_old = new_path + new_path.replace('.','') + '_old'

    for i in [file_info, file_info_old, file_main, file_old]:
        with open(i, 'r') as f:
            new_file_content = re.sub(r'(?<=<farmName>).*?(?=</farmName>)',farm_name ,f.read())
            new_file_content = re.sub(r'(?<=<uniqueIDForThisGame>)\d{9}(?=</uniqueIDForThisGame>)',uniqueIDForThisGame , new_file_content)
        
        with open(i, 'w') as f:
            f.write(new_file_content)

def find_saves():
    output = []
    for i in os.listdir():
        if re.match('.*?\\d{9}', i):
            output.append(i)
    return output
    