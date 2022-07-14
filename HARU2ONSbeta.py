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
            Stage_line = re.match(r'\.stage',line)
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
            if_line1 = re.match(r'\.if (\S*) (\S*) < (\S*)',line)
            if_line2 = re.match(r'\.if (\S*) (\S*) > (\S*)',line)
            Jump_line = re.match(r'\.goto\s(\S*)',line)
            mov_line = re.match(r'\.setGlobal (\S*) = (\S*)',line)


            if TKT_line:
                Space_line = ''
                Messege_line = TKT_line[1]
                VoicePath = TKT_line[2]
                NoNameKigo = re.sub(r'@|#','',TKT_line[3])
                NorubyTXT = re.sub(r'\{\S*}|\\n|\\N','',TKT_line[4])

                if TKT_line[1] == '0':
                    line = '\n'

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

            elif Stage_line:
                #BGや立ち絵の調節をします。最長一致から並べていきます

                line = re.sub(r'\.stage\s\* |\.stage\s|\:\[(\S*)\,(\S*)\,(\S*)\]ol_(\S*).png|\:ol_(\S*).png|\:\[(\S*)\,(\S*)\,(\S*)\]','',line)
                #print(line)
                #背景 + 立ち絵最大5人で分類していきます。もしかして4人出るパターン存在しない?
                Stage1_line = re.match(r'(\S*) (\d*) (\d*) st(\S*) (\d*) st(\S*) (\d*) st(\S*) (\d*) st(\S*) (\d*) st(\S*) (\d*)',line)
                Stage2_line = re.match(r'(\S*) (\d*) (\d*) st(\S*) (\d*) st(\S*) (\d*) st(\S*) (\d*) st(\S*) (\d*)',line)
                Stage3_line = re.match(r'(\S*) (\d*) (\d*) st(\S*) (\d*) st(\S*) (\d*) st(\S*) (\d*)',line)
                Stage4_line = re.match(r'(\S*) (\d*) (\d*) st(\S*) (\d*) st(\S*) (\d*)',line)
                Stage5_line = re.match(r'(\S*) (\d*) (\d*) st(\S*)\s(\d*)',line)
                #ここから画面効果を含んだパターンです。画面効果は現在省いています
                Stage6_line = re.match(r'(\S*) (\S*) (\d*) (\d*) st(\S*) (\d)',line)
                Stage7_line = re.match(r'(\S*) (\S*) (\d*) (\d*)',line)
                Stage99_line = re.match(r'(\S*) (\d*) (\d*)',line)

                if Stage1_line:
                    #print(line)
                    #最長一致。背景画像+立ち絵5人
                    line0 = 'cspchar\n'
                    st1_x = 800 - int(Stage1_line[5])
                    st2_x = 800 - int(Stage1_line[7])
                    st3_x = 800 - int(Stage1_line[9])
                    st4_x = 800 - int(Stage1_line[11])
                    st5_x = 800 - int(Stage1_line[13])

                    line1 = 'lsph 39,":a;bg\\' + Stage1_line[1] + '",-' + Stage1_line[2] + ',-' + Stage1_line[3] + '\nvsp 39,1\n'
                    line2 = 'lsph 34,":a;st\\st' + Stage1_line[4] + '",' + str(st1_x) + ',80\nvsp 34,1\n'
                    line3 = 'lsph 33,":a;st\\st' + Stage1_line[6] + '",' + str(st2_x) + ',80\nvsp 33,1\n'
                    line4 = 'lsph 32,":a;st\\st' + Stage1_line[8] + '",' + str(st3_x) + ',80\nvsp 32,1\n'
                    line5 = 'lsph 31,":a;st\\st' + Stage1_line[10] + '",' + str(st4_x) + ',80\nvsp 31,1\n'
                    line6 = 'lsph 30,":a;st\\st' + Stage1_line[12] + '",' + str(st5_x) + ',80\nvsp 30,1\n'

                    line = line0 + line1 + line2 + line3 + line4 +line5 + line6 + '\nprint 10,300\n'
                    #print(line)

                elif Select2_line:
                    #print(line)
                    #print('あ')
                    line0 = 'cspchar\n'
                    st1_x = 800 - int(Stage2_line[5])
                    st2_x = 800 - int(Stage2_line[7])
                    st3_x = 800 - int(Stage2_line[9])
                    st4_x = 800 - int(Stage2_line[11])

                    line1 = 'lsph 39,":a;bg\\' + Stage2_line[1] + '",-' + Stage2_line[2] + ',-' + Stage2_line[3] + '\nvsp 39,1\n'
                    line2 = 'lsph 34,":a;st\\st' + Stage2_line[4] + '",' + str(st1_x) + ',80\nvsp 34,1\n'
                    line3 = 'lsph 33,":a;st\\st' + Stage2_line[6] + '",' + str(st2_x) + ',80\nvsp 33,1\n'
                    line4 = 'lsph 32,":a;st\\st' + Stage2_line[8] + '",' + str(st3_x) + ',80\nvsp 32,1\n'
                    line5 = 'lsph 31,":a;st\\st' + Stage2_line[10] + '",' + str(st4_x) + ',80\nvsp 31,1\n'

                    line = line0 + line1 + line2 + line3 + line4 +line5 + '\nprint 10,300\n'
                    print(line)

                elif Stage3_line:
                    #print(line)
                    line0 = 'cspchar\n'
                    st1_x = 800 - int(Stage3_line[5])
                    st2_x = 800 - int(Stage3_line[7])
                    st3_x = 800 - int(Stage3_line[9])

                    line1 = 'lsph 39,":a;bg\\' + Stage3_line[1] + '",-' + Stage3_line[2] + ',-' + Stage3_line[3] + '\nvsp 39,1\n'
                    line2 = 'lsph 34,":a;st\\st' + Stage3_line[4] + '",' + str(st1_x) + ',80\nvsp 34,1\n'
                    line3 = 'lsph 33,":a;st\\st' + Stage3_line[6] + '",' + str(st2_x) + ',80\nvsp 33,1\n'
                    line4 = 'lsph 32,":a;st\\st' + Stage3_line[8] + '",' + str(st3_x) + ',80\nvsp 32,1\n'

                    line = line0 + line1 + line2 + line3 + line4 + '\nprint 10,300\n'

                    #print(line)
                elif Stage4_line:

                    line0 = 'cspchar\n'
                    st1_x = 800 - int(Stage4_line[5])
                    st2_x = 800 - int(Stage4_line[7])

                    line1 = 'lsph 39,":a;bg\\' + Stage4_line[1] + '",-' + Stage4_line[2] + ',-' + Stage4_line[3] + '\nvsp 39,1\n'
                    line2 = 'lsph 34,":a;st\\st' + Stage4_line[4] + '",' + str(st1_x) + ',80\nvsp 34,1\n'
                    line3 = 'lsph 33,":a;st\\st' + Stage4_line[6] + '",' + str(st2_x) + ',80\nvsp 33,1\n'

                    line = line0 + line1 + line2 + line3 + '\nprint 10,300\n'
                    #print(line)

                elif Stage5_line:
                    line0 = 'cspchar\n'

                    st1_x = 800 - int(Stage5_line[5])

                    line1 = 'lsph 39,":a;bg\\' + Stage5_line[1] + '",-' + Stage5_line[2] + ',-' + Stage5_line[3] + '\nvsp 39,1\n'
                    line2 = 'lsph 34,":a;st\\st' + Stage5_line[4] + '",' + str(st1_x) + ',80\nvsp 34,1\n'

                    line = line0 + line1 + line2 + '\nprint 10,300\n'

                elif Stage6_line:
                    line0 = 'cspchar\n'

                    st1_x = 800 - int(Stage6_line[6])

                    line1 = 'lsph 39,":a;bg\\' + Stage6_line[2] + '",-' + Stage6_line[3] + ',-' + Stage6_line[4] + '\nvsp 39,1\n'
                    line2 = 'lsph 34,":a;st\\st' + Stage6_line[5] + '",' + str(st1_x) + ',80\nvsp 34,1\n'

                    line = line1 + '\nprint 10,300\n'

                elif Stage7_line:
                    line0 = 'cspchar\n'

                    line1 = 'lsph 39,":a;bg\\' + Stage7_line[2] + '",-' + Stage7_line[3] + ',-' + Stage7_line[4] + '\nvsp 39,1\n'

                    line =line0 + line1 + '\nprint 10,300\n'

                elif Stage99_line:

                    line0 = 'cspchar\n'

                    line1 = 'lsph 39,":a;bg\\' + Stage99_line[1] + '",-' + Stage99_line[2] + ',-' + Stage99_line[3] + '\nvsp 39,1\n'
                    line = line0 + line1 + '\nprint 10,300\n'

                else:
                    line = line
                    print(line)

   
            #背景CG・立ち絵の処理ここまで

            elif BGM_line:

                BGMSTART =re.match(r'\.playBGM (\S*).ogg',line)
        
                if BGMSTART:

                    line = 'bgm "bgm\\' + BGMSTART[1] + '.ogg" \n' 

                else:
                    #BGM再生命令にファイルを指定していないときは一括でストップを掛けます
                    #本来は [playBGM *]のように[*]を使いますが、例外も含めストップさせておきます
                    line = 'bgmstop\n'

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
                    Screen_line = 5
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
                #7/12訂正　このままで大丈夫そう
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

                line = 'movie "mov\\' + movie_line[2] + '.mpg",click\nprint 10,300\n'

            elif if_line1:
                

                linea = 'notif $' + if_line1[1] + ' > ' + if_line1[2] + '\n'
                lineb = 'goto *' + if_line1[3] + '\n'

                line = linea + lineb + '\n'
                print(line)

            elif if_line2:

                linea = 'if $' +if_line2[1] + ' < ' + if_line2[2] + '\n'
                lineb = 'goto *' + if_line1[3] + '\n'

                line = linea + lineb + '\n'

            elif Jump_line:

                line = 'goto *' + Jump_line[1] + '\n'

            elif mov_line:

                line = 'mov $' + mov_line[1] + ',' + mov_line[2] + '\n' 

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

    

