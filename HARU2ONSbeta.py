import glob
import sys
import os
import re
import chardet
#from PIL import Image

same_hierarchy = (os.path.dirname(sys.argv[0]))

scenario_dir = os.path.join(same_hierarchy,'scr')

PSP = bool(os.path.isfile(os.path.join(same_hierarchy,'ONS.INI')) )

bgcg_dir =os.path.join(same_hierarchy,'bg')
stand_dir =os.path.join(same_hierarchy,'st')
sys_dir =os.path.join(same_hierarchy,'sys')

with open(os.path.join(same_hierarchy, 'default.txt')) as f:
	txt = f.read()

pathlist = glob.glob(os.path.join(scenario_dir, '*.sc'))


for snr_path in pathlist:

    with open(snr_path, 'rb') as f:
        char_code =chardet.detect(f.read())['encoding']

    with open(snr_path, encoding=char_code, errors='ignore') as f:
        txt += '\n;--------------- '+ os.path.splitext(os.path.basename(snr_path))[0] +' ---------------\nend\n\n'
        txt = txt.replace('//', ';;;')

        #print(txt)

        for line in f:
            #命令が特殊な形は先に分けておきます
            TKT_line =  re.match(r'\.message\s([0-9]+)\t(.*?)\t(.*?)\t(.+)',line)
            Stage1_line = re.match(r'\.stage\s\* (\S*) (\S*) (\S*) st(\S*) (\S*) st(\S*)\:(\S*)',line)
            Stage2_line = re.match(r'\.stage\s\* (\S*) (\S*) (\S*) st(\S*) (\S*) st(\S*) (\S*)',line)
            Stage3_line = re.match(r'\.stage\s\* (\S*) (\S*) (\S*) st(\S*) (\S*)',line)
            Stage4_line = re.match(r'\.stage\s\* (\S*) (\S*) (\S*)',line)
            Stage5_line = re.match(r'\.stage\s(\S*) (\S*) (\S*) (\S*) st(\S*) (\S*)',line)
            Stage6_line = re.match(r'\.stage\sst(\S*) (\S*) (\S*) (\S*) (\S*) (\S*) (\S*) (\S*)',line)
            Stage7_line = re.match(r'\.stage\s(\S*) (\S*) (\S*) (\S*)',line)
            Stage8_line = re.match(r'\.stage\s(\S*) (\d{1}) (\d{1}) (\S*) (\d{1}) (\d{1}) (\S*) (\d{1})',line)
            BGM_line = re.match(r'\.playBGM',line)
            SE_line = re.match(r'\.playSE (\S*)',line)
            Window_line = re.match(r'\.panel\s([0-9]+)([\s]*)([0-9]*)',line)
            Label_line = re.match(r'\.label (\S*)',line)
            Chain_line = re.match(r'\.chain (\S*).sc',line)
            Include_line = re.match(r'\.include (\S*).sc',line)
            Shake_line = re.match(r'\.shakeScreen\t([A-Z]+)\t([0-9]+)\t([0-9]+)',line)
            File_line = re.match(r'\; ファイル: (\S*).txt',line)


            if TKT_line:

                VoicePath = TKT_line[2]
                NoNameKigo = re.sub(r'@|#','',TKT_line[3])
                NorubyTXT = re.sub(r'\{\S*}|\\n|\\N','',TKT_line[4])
            
                line = '[' + NoNameKigo + '|' + VoicePath + ']' + NorubyTXT + '\n'

                if '#' in line:
                    print(line)

            elif Stage1_line:
                #BGや立ち絵の調節をします。最長一致から並べていきます

                linea = 'cspchar \nlspsy 37, "bg\\' + Stage1_line[1] + ',384,288 \n'
                lineb = 'lspsy 36, "st\\st' + Stage1_line[4] + ',384,288\n'
                linec = 'lspsy 35, "st\\st' + Stage1_line[6] + ',384,288 \nprint 10,300\n'

                line = linea + '\n' + lineb + '\n' + linec + '\n'
                
                

            elif Stage2_line:

                linea = 'cspchar\nlspsy 37, "bg\\' + Stage2_line[1] + ',384,288 \n'
                lineb = 'lspsy 36, "st\\st' + Stage2_line[4] + ',384,288\n'
                linec = 'lspsy 35, "st\\st' + Stage2_line[6] + ',384,288 \nprint 10,300\n'

                line = linea + '\n' + lineb + '\n' + linec + '\n'
                

            elif Stage3_line:

                linea = 'cspchar\nlspsy 37, "bg\\' + Stage3_line[1] + ',384,288 \n'
                lineb = 'lspsy 36, "st\\st' + Stage3_line[4] + ',384,288\n'

                line = linea + '\n' + lineb + '\n'
                

            elif Stage4_line:
                line = 'cspchar\nlspsy 37, "bg\\' + Stage4_line[1] + ',384,288 \n'
                
                

            elif Stage5_line:

                linea = 'cspchar\nlspsy 37, "bg\\' + Stage5_line[1] + ',384,288 \n'
                lineb = 'lspsy 36, "bg\\' + Stage5_line[4] + ',384,288\n'
                linec = 'lspsy 35, "st\\st' + Stage5_line[5] + ',384,288 \nprint 10,300\n'

                line = linea + '\n' + lineb + '\n' + linec + '\n'
                

            elif Stage6_line:

                linea = 'cspchar\nlspsy 37, "bg\\' + Stage6_line[4] + ',384,288 \n'
                lineb = 'lspsy 36, "bg\\' + Stage6_line[7] + ',384,288\n'
                linec = 'lspsy 35, "st\\st' + Stage6_line[1] + ',384,288 \nprint 10,300\n'

                line = linea + '\n' + lineb + '\n' + linec + '\n'
                

            elif Stage7_line:

                linea = 'cspchar\nlspsy 37, "bg\\' + Stage7_line[1] + ',384,288 \n'
                lineb = 'lspsy 36, "bg\\' + Stage7_line[2] + ',384,288\n'

                line = linea + '\n' + lineb + '\n'
                

            elif Stage8_line:

                linea = 'cspchar\nlspsy 37, "bg\\' + Stage8_line[1] + ',384,288 \n'
                lineb = 'lspsy 36, "bg\\' + Stage8_line[4] + ',384,288\n'
                linec = 'lspsy 35, "bg\\' + Stage8_line[7] + ',384,288 \nprint 10,300\n'

                line = linea + '\n' + lineb + '\n' + linec + '\n'
                
            #背景CG・立ち絵の処理ここまで

            elif BGM_line:

                BGMSTART =re.match(r'\.playBGM (\S*).ogg',line)
        
                if BGMSTART:

                    line = 'bgm `bgm\\' + BGMSTART[1] + '.ogg` \n' 

                else:
                    #BGM再生命令にファイルを指定していないときは一括でストップを掛けます
                    #本来は [playBGM *]のように[*]を使いますが、例外も含めストップさせておきます
                    line = 'bgmstop \n'

            elif SE_line:

                SESTART =re.match(r'\.playSE (\S*).ogg',line)

                if SESTART:
                
                    line = 'dwave 1,`se\\' + SE_line[1] + '.ogg` \n'

                else:

                    line = 'dwavestop\n'

            elif Window_line:
                #ウインドウモードの切替です。0で非表示、1で画像通り、2で全画面です 3は電話演出用

                

                if '0' in Window_line[1]:

                    line = 'setwin0\n'
                    #print(line)

                elif '1' in Window_line[1]:

                    line = 'setwin1\n'
                    #print(line)

                elif '2' in Window_line[1]:

                    line = 'setwin2\n'
                    #print(line)

                else:
                    line = ';' + line
                    print(Window_line[1])


            elif Label_line:

                #テキスト内でのラベルジャンプを担当
                
                line = '*' + Label_line[1] + '\n'
                    

            elif Include_line:
                line = '*' + Include_line[1] + '\n'

            elif Shake_line:
                #未作成・dafault.txtで処理する書き方にする予定
                line = line
                


            elif re.match(r'\.wait [0-9]',line):
                
                #line.replace('\.wait','wait')  + '\\\n'
                line = line[1:] + '\n'
                
            elif Chain_line:

                line = 'goto *' + Chain_line[1] + '\n'
                #print(line)

            elif File_line:
                #シナリオファイル間の橋渡し用。コードとして危険ではある。
                line = '*' + File_line[1] + '\n'

            elif '.end' in line:

                line = 'end\n'

            else:
                #if '.stage' in line:
                    #print(line)
                
                line = ';' + line + '\n'
                
        

            
            txt += line

#if PSP:
    #pathlist2 = glob.glob(os.path.join(stand_dir, '*.png'))
    #pathlist2.extend(glob.glob(os.path.join(bgcg_dir, '*.png')))
    #pathlist2.extend(glob.glob(os.path.join(sys_dir, '*.png')))

    

print('猫猫柔軟')

open(os.path.join(same_hierarchy,'0.txt'), 'w', errors='ignore').write(txt)

    

