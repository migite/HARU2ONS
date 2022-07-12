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

#初期値リストです
Screen_line = 0
Messege_line = 0
Messege_before = 0
Labelcount = 0

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
            Select3_line = re.match(r'\.select\s(\S*):(\S*)\s(\S*):(\S*)\s(\S*):(\S*)',line)
            Select2_line = re.match(r'\.select\s(\S+):(\S+)\s(\S+):(\S+)',line)
            movie_line = re.match(r'\.movie\s(\S*)\s(\S*).mpg',line)


            if TKT_line:
                Space_line = ''
                Messege_line = TKT_line[1]
                VoicePath = TKT_line[2]
                NoNameKigo = re.sub(r'@|#','',TKT_line[3])
                NorubyTXT = re.sub(r'\{\S*}|\\n|\\N','',TKT_line[4])


                #print(Screen_line)
                if  Screen_line == 0:

                    Enter_line = '\\\n'

                elif Screen_line == 1:

                    if Messege_line == Messege_before:
                        
                        Enter_line = '@\n'

                    else:
                        Enter_line = '\\\n'


                else:

                    Enter_line = '\\\n'

            
                linea = 'dwave 0, "voice\\' + VoicePath + '.ogg"\n'
                lineb = '[' + NoNameKigo +  ']' + NorubyTXT + Enter_line

                if VoicePath == '':
                    line = lineb

                else:
                    line = linea + lineb

                Messege_before = Messege_line

                #print(line)

                #if '#' in line:
                    #print(line)

            elif Stage1_line:
                #BGや立ち絵の調節をします。最長一致から並べていきます

                linea = 'cspchar \nlsph 39, ":a;bg\\' + Stage1_line[1] + '",' + Stage1_line[2] + ',' + Stage1_line[3] + '\n'
                lineb = 'lsph 32, ":a;st\\st' + Stage1_line[4] + '",160,80\n'
                linec = 'lsph 31, ":a;st\\st' + Stage1_line[6] + '",320,80 \n'
                lined = 'vsp 39,1\nvsp 32,1\nvsp 31,1\nprint 10,300\n'

                line = linea + '\n' + lineb + '\n' + linec + '\n' + lined +'\n'
                
                

            elif Stage2_line:

                linea = 'cspchar\nlsph 39, ":a;bg\\' + Stage2_line[1] + '",' + Stage2_line[2] + ',' + Stage2_line[3] + '\n'
                lineb = 'lsph 32, ":a;st\\st' + Stage2_line[4] + '",160,80\n'
                linec = 'lsph 31, ":a;st\\st' + Stage2_line[6] + '",320,80\n'
                lined = 'vsp 39,1\nvsp 32,1\nvsp 31,1\nprint 10,300\n'

                line = linea + '\n' + lineb + '\n' + linec + '\n' + lined + '\n'
                print(line)
                

            elif Stage3_line:

                linea = 'cspchar\nlsph 39, ":a;bg\\' + Stage3_line[1] + '",' + Stage3_line[2] + ',' + Stage3_line[3]  + '\n'
                lineb = 'lsph 31, ":a;st\\st' + Stage3_line[4] + '",240,80\n'
                linec = 'vsp 39,1\nvsp 31,1\nprint 10,300\n'

                line = linea + '\n' + lineb + '\n' + linec +'\n'
                

            elif Stage4_line:
                linea = 'cspchar\nlsph 39, ":a;bg\\' + Stage4_line[1] + '",' + Stage4_line[2] + ',' + Stage4_line[3] + '\nprint 10,300\n'
                lineb = 'vsp 39,1\nprint 10,300\n'

                line = linea + '\n' + lineb + '\n'
                
            elif Stage5_line:

                linea = 'cspchar\nlsph 39, ":a;bg\\' + Stage5_line[1] + '",' + Stage5_line[2] + ',' + Stage5_line[3] + '\n'
                lineb = 'lsph 38, ":a;bg\\' + Stage5_line[4] + '",0,0\n'
                linec = 'lsph 31, ":a;st\\st' + Stage5_line[5] + '",240,80 \n'
                lined = 'vsp 39,1\nvsp 38,1\nvsp 31,1\nprint 10,300\n'
                line = linea + '\n' + lineb + '\n' + linec + '\n' + lined + '\n'
                

            elif Stage6_line:

                linea = 'cspchar\nlsph 39, ":a;bg\\' + Stage6_line[4] + '",' + Stage6_line[5] + ',' + Stage6_line[6] +  '\n'
                lineb = 'lsph 38, ":a;bg\\' + Stage6_line[7] + '",0,0\n'
                linec = 'lsph 31, ":a;st\\st' + Stage6_line[1] + '",240,80 \n'
                lined = 'vsp 39,1\nvsp 38,1\nvsp 31,1\nprint 10,300\n'

                line = linea + '\n' + lineb + '\n' + linec + lined + '\n'
                

            elif Stage7_line:

                linea = 'cspchar\nlsph 39, ":a;bg\\' + Stage7_line[1] + '",240,80 \n'
                lineb = 'lsph 38, ":a;bg\\' + Stage7_line[2] + '",' + Stage7_line[3] + ',' + Stage7_line[4] +  '\n'
                lined = 'vsp 39,1\nvsp 32,1\nprint 10,300\n'

                line = linea + '\n' + lineb + '\n'
                

            elif Stage8_line:

                linea = 'cspchar\nlsph 39, ":a;bg\\' + Stage8_line[1] + '",' + Stage8_line[2] + ',' + Stage8_line[3] +  '\n'
                lineb = 'lsph 38, ":a;bg\\' + Stage8_line[4] + '",' + Stage8_line[5] + ',' + Stage8_line[6] +  '\n'
                linec = 'lsph 37, ":a;bg\\' + Stage8_line[7] + '",0,0\nprint 10,300\n'
                lined = 'vsp 39,1\nvsp 38,1\nvsp 37,1\nprint 10,300'

                line = linea + '\n' + lineb + '\n' + linec + '\n' + lined + '\n'
                
            #背景CG・立ち絵の処理ここまで

            elif BGM_line:

                BGMSTART =re.match(r'\.playBGM (\S*).ogg',line)
        
                if BGMSTART:

                    line = 'bgm "bgm\\' + BGMSTART[1] + '.ogg" \n' 

                else:
                    #BGM再生命令にファイルを指定していないときは一括でストップを掛けます
                    #本来は [playBGM *]のように[*]を使いますが、例外も含めストップさせておきます
                    line = 'bgmstop \n'

            elif SE_line:

                SESTART =re.match(r'\.playSE (\S*).ogg',line)

                if SESTART:
                
                    line = 'dwave 1,"se\\' + SESTART[1] + '.ogg" \n'

                else:

                    line = 'dwavestop 1\n'

            elif Window_line:
                #ウインドウモードの切替です。0で非表示、1で画像通り、2で全画面です 3は電話演出用
                #Screen_line変数は改行の仕方を変えるためにテストでおいています
                #0のときはメッセージごとに改行、1のときはメッセージ番号が前の番号から変わったら改行です
                

                if '0' in Window_line[1]:

                    line = 'setwin0\n'
                    #print(line)

                elif '1' in Window_line[1]:

                    line = 'setwin1\n'
                    Screen_line = 0
                    #print(line)

                elif '2' in Window_line[1]:

                    line = 'setwin2\n'
                    Screen_line = 1
                    #print(line)

                elif '3' in Window_line[1]:
                    line = 'setwin3\n'
                    Screen_line = 0

                else:
                    line = ';' + line
                    Screen_line == 9
                    #print(Window_line[1])


            elif Label_line:

                #テキスト内でのラベルジャンプを担当

                if re.match(r'\.label label[0-9]',line):

                    #なんかラベル名義重複回避のためにカウンタ作ってたら一つずれたので
                    Labelcount2 = Labelcount - 1

                    line = '*' + Label_line[1] + '_' + str(Labelcount2) + '\n'

                    #print(line)
                
                else:
                    line = '*' + Label_line[1] + '\n'
                    #print(line)
                    

            elif Include_line:
                line = '*' + Include_line[1] + '\n'

            elif Shake_line:
                #未作成・dafault.txtで処理する書き方にする予定
                line = 'quake ' + Shake_line[2] + ',' + Shake_line[3] + '\n'
                
            elif re.match(r'\.wait [0-9]',line):
                
                #line.replace('\.wait','wait')  + '\\\n'
                line = line[1:] + '\n'
                
            elif Chain_line:

                line = 'goto *' + Chain_line[1] + '\nend\n'
                #print(line)

            elif File_line:
                #シナリオファイル間の橋渡し用。コードとして危険ではある。
                line = '*' + File_line[1] + '\n'

            elif Select3_line:

                linea = '"' + Select3_line[1] + '",*' + Select3_line[2] + '_' + str(Labelcount) + ','
                lineb = '"' + Select3_line[3] + '",*' + Select3_line[4] + '_' + str(Labelcount) + ','
                linec = '"' + Select3_line[5] + '",*' + Select3_line[6] + '_' + str(Labelcount) + '\n'

                line = 'select ' + linea + lineb + linec
                Labelcount  = Labelcount + 1
                #print(Labelcount)
                
                #print(line)

            elif Select2_line:

                linea = '"' + Select2_line[1] + '",*' + Select2_line[2] + '_' + str(Labelcount) + ','
                lineb = '"' + Select2_line[3] + '",*' + Select2_line[4] + '_' + str(Labelcount) + '\n'

                line = 'select ' + linea + lineb
                Labelcount  = Labelcount + 1
                #print(Labelcount)
                #print(line)


            elif '.end' in line:

                line = ';end\n'

            elif movie_line:

                line = 'movie "mov\\' + movie_line[2] + '.mpg",click\nprint10,300\n'

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

    

