import glob
import sys
import os
import re

import chardet
#from PIL import Image

same_hierarchy = (os.path.dirname(sys.argv[0]))

scenario_dir = os.path.join(same_hierarchy,'scr')

with open(os.path.join(same_hierarchy, 'default.txt')) as f:
	txt = f.read()

pathlist = glob.glob(os.path.join(scenario_dir, '*.sc'))

#初期値リストです
Screen_line = 0
Messege_line = 0
Messege_before = 0
Labelcount = 0

print('コンバートを開始します…')

for snr_path in pathlist:

    with open(snr_path, 'rb') as f:
        char_code =chardet.detect(f.read())['encoding']

    with open(snr_path, encoding=char_code, errors='ignore') as f:
        
        txt += 'cspchar\ngoto *title\n;--------------- '+ os.path.splitext(os.path.basename(snr_path))[0] +' ---------------\nend\n*' + os.path.splitext(os.path.basename(snr_path))[0] + '\nlookbackflush\n'
        txt = txt.replace('//', ';;;')

        #print(txt)
        
        for line in f:
            #命令が特殊な形は先に分けておきます
            TKT_line =  re.match(r'\.message\s([0-9]+)\t(.*?)\t(.*?)\t(.+)',line)
            Stage_st_line =re.match(r'\.stage\s(\S*)\s(\d*)\s(\S*)\s(\d*)',line)
            Stage_line = re.match(r'\.stage',line)
            BGM_line = re.match(r'\.playBGM',line)
            SE_line = re.match(r'\.playSE (\S*)',line)
            Window_line = re.match(r'\.panel\s([0-9]+)([\s]*)([0-9]*)',line)
            Label_line = re.match(r'\.label (\S*)',line)
            Chain_line = re.match(r'\.chain (\S*).sc',line)
            Include_line = re.match(r'\.include\s(\S*).sc',line)
            Shake_line = re.match(r'\.shakeScreen\t([A-Z]+)\t([0-9]+)\t([0-9]+)',line)
            Wait_line = re.match(r'\.wait (\d+)',line)
            Select3_line = re.match(r'\.select\s(\S*):(\S*)\s(\S*):(\S*)\s(\S*):(\S*)',line)
            Select2_line = re.match(r'\.select\s(\S+):(\S+)\s(\S+):(\S+)',line)
            movie_line = re.match(r'\.movie\s(\S*)\s(\S*).mpg',line)
            if_line = re.match(r'\.if (\S*) (\S*) (\d*) (\S*)',line)
            Jump_line = re.match(r'\.goto\s(\S*)',line)
            mov_line = re.match(r'\.setGlobal\s(\S*) = (\S*)',line)
            add_line = re.match(r'\.set (\S*) =',line)
            trancelate_line = re.match(r'\.transition (\d*) (\S*) (\d*)',line)
            erojump_line = re.match(r'#include\s(\S*).sc',line)
            eroreturn_line = re.match(r';■エロシーンここまで',line)
            vscroll_line = re.match(r'\.vscroll\s(\d+)\s(\d+)',line)
            hscroll_line = re.match(r'\.hscroll\s(\d+)\s(\d+)',line)



            if TKT_line:
                Space_line = ''
                Messege_line = TKT_line[1]
                VoicePath = TKT_line[2]
                NoNameKigo = re.sub(r'@|#','',TKT_line[3])
                NorubyTXT = re.sub(r'\{\S*}|\\n|\\N|\\a|\\w','',TKT_line[4])

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

                linea = 'dwave 0,"voice\\' + VoicePath + '.ogg"\n'
                lineb = '[' + NoNameKigo + ']' + NorubyTXT + Enter_line

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

                line = re.sub(r'\.stage\s\* |\.stage\s|\:\[(\S+)\,(\S+)\,(\S+)\]ol_(\S+).png|\:ol_(\S+).png|\:\[(\S+)\,(\S+)\,(\S+)\]','',line)
                #print(line)
                #背景 + 立ち絵最大5人で分類していきます。?
                Stage1_line = re.match(r'(\S+)\s(\d+)\s(\d+)\sst(\S+)\s(\d+)\sst(\S+)\s(\d+)\sst(\S+)\s(\d+)\sst(\S+)\s(\d+)\sst(\S+)\s(\d*)',line)
                Stage2_line = re.match(r'(\S+)\s(\d*)\s(\d*)\sst(\S+)\s(\d*)\sst(\S+)\s(\d*)\sst(\S+)\s(\d*)\sst(\S)\s(\d+)',line)
                Stage3_line = re.match(r'(\S+)\s(\d*)\s(\d*)\sst(\S+)\s(\d*)\sst(\S+)\s(\d*)\sst(\S+)\s(\d*)',line)
                Stage4_line = re.match(r'(\S+)\s(\d*)\s(\d*)\sst(\S+)\s(\d*)\sst(\S+)\s(\d*)',line)
                Stage5_line = re.match(r'(\S+)\s(\d*)\s(\d*)\sst(\S+)\s(\d*)',line)
                #ここから画面効果を含んだパターンです。画面効果は現在省いています
                Stage6_line = re.match(r'(\S+)\s(\S+)\s(\d+)\s(\d+)\sst(\S+)\s(\d)',line)
                Stage7_line = re.match(r'(\S+)\s(\S{4,})\s(\d+)\s(\d+)',line)
                #ここからはst命令という名の背景だったり拡大などです
                Stage11_line = re.match(r'st(\S+)\s(\S{4,})\s(\d*)\s(\d*)',line)
                Stage12_line = re.match(r'st(\S+)\s(\d*)\s(\d*)',line)
                #最後に背景表示のみです
                Stage99_line = re.match(r'(\S+)\s(\d*)\s(\d*)',line)

                

                if Stage1_line:
                    #print(line)
                    #最長一致。背景画像+立ち絵5人
                    line0 = 'cspchar\n'
                    st1_x = 800 - int(Stage1_line[5])
                    st2_x = 800 - int(Stage1_line[7])
                    st3_x = 800 - int(Stage1_line[9])
                    st4_x = 800 - int(Stage1_line[11])
                    st5_x = 800 - int(Stage1_line[13])

                    line1 = 'lsph 39,":a;bg\\' + Stage1_line[1] + '",-' + Stage1_line[2] + ',-' + Stage1_line[3] + ':vsp 39,1\n'
                    line2 = 'lsph 34,":a;st\\st' + Stage1_line[4] + '",0,0\n'
                    line3 = 'lsph 33,":a;st\\st' + Stage1_line[6] + '",0,0\n'
                    line4 = 'lsph 32,":a;st\\st' + Stage1_line[8] + '",0,0\n'
                    line5 = 'lsph 31,":a;st\\st' + Stage1_line[10] + '",0,0\n'
                    line6 = 'lsph 30,":a;st\\st' + Stage1_line[12] + '",0,0\n'

                    line7 = 'mov %x1_default,' + str(st1_x) + '\n'
                    line8 = 'mov %x2_default,' + str(st2_x) + '\n'
                    line9 = 'mov %x3_default,' + str(st3_x) + '\n'
                    line10 = 'mov %x4_default,' + str(st4_x) + '\n'
                    line11 = 'mov %x5_default,' + str(st5_x) + '\n'
                    line12 = 'stposition\n'

                    line = line0 + line1 + line2 + line3 + line4 +line5 + line6 + line7 + line8 + line9 + line10 + line11 + line12 +'\n'
                    #print(line)

                elif Stage2_line:

                    line0 = 'cspchar\n'
                    st1_x = 800 - int(Stage2_line[5])
                    st2_x = 800 - int(Stage2_line[7])
                    st3_x = 800 - int(Stage2_line[9])
                    st4_x = 800 - int(Stage2_line[11])

                    line1 = 'lsph 39,":a;bg\\' + Stage2_line[1] + '",-' + Stage2_line[2] + ',-' + Stage2_line[3] + ':vsp 39,1\n'
                    line2 = 'lsph 34,":a;st\\st' + Stage2_line[4] + '",0,0\n'
                    line3 = 'lsph 33,":a;st\\st' + Stage2_line[6] + '",0,0\n'
                    line4 = 'lsph 32,":a;st\\st' + Stage2_line[8] + '",0,0\n'
                    line5 = 'lsph 31,":a;st\\st' + Stage2_line[10] + '",0,0\n'

                    line6 = 'mov %x1_default,' + str(st1_x) + '\n'
                    line7 = 'mov %x2_default,' + str(st2_x) + '\n'
                    line8 = 'mov %x3_default,' + str(st3_x) + '\n'
                    line9 = 'mov %x4_default,' + str(st4_x) + '\n'
                    line10 = 'stposition\n'

                    line = line0 + line1 + line2 + line3 + line4 +line5 + line6 + line7 + line8 + line9 + line10 +'\n'
                    #print(line)

                elif Stage3_line:
                    #print(line)
                    line0 = 'cspchar\n'
                    st1_x = 800 - int(Stage3_line[5])
                    st2_x = 800 - int(Stage3_line[7])
                    st3_x = 800 - int(Stage3_line[9])

                    line1 = 'lsph 39,":a;bg\\' + Stage3_line[1] + '",-' + Stage3_line[2] + ',-' + Stage3_line[3] + ':vsp 39,1\n'
                    line2 = 'lsph 34,":a;st\\st' + Stage3_line[4] + '",0,0\n'
                    line3 = 'lsph 33,":a;st\\st' + Stage3_line[6] + '",0,0\n'
                    line4 = 'lsph 32,":a;st\\st' + Stage3_line[8] + '",0,0\n'

                    line5 = 'mov %x1_default,' + str(st1_x) + '\n'
                    line6 = 'mov %x2_default,' + str(st2_x) + '\n'
                    line7 = 'mov %x3_default,' + str(st3_x) + '\n'
                    line8 = 'stposition\n'

                    line = line0 + line1 + line2 + line3 + line4 +line5 + line6 + line7 + line8 +'\n'

                    #print(line)
                elif Stage4_line:
                    
                    #print(line)
                    line0 = 'cspchar\n'
                    st1_x = 800 - int(Stage4_line[5])
                    st2_x = 800 - int(Stage4_line[7])

                    line1 = 'lsph 39,":a;bg\\' + Stage4_line[1] + '",-' + Stage4_line[2] + ',-' + Stage4_line[3] + ':vsp 39,1\n'
                    line2 = 'lsph 34,":a;st\\st' + Stage4_line[4] + '",0,0\n'
                    line3 = 'lsph 33,":a;st\\st' + Stage4_line[6] + '",0,0\n'

                    line4 = 'mov %x1_default,' + str(st1_x) + '\n'
                    line5 = 'mov %x2_default,' + str(st2_x) + '\n'
                    line6 = 'stposition\n'

                    line = line0 + line1 + line2 + line3 + line4 +line5 + line6 +'\n'

                elif Stage5_line:
                    line0 = 'cspchar\n'
                    st1_x = 800 - int(Stage5_line[5])

                    line1 = 'lsph 39,":a;bg\\' + Stage5_line[1] + '",-' + Stage5_line[2] + ',-' + Stage5_line[3] + ':vsp 39,1\n'
                    line2 = 'lsph 34,":a;st\\st' + Stage5_line[4] + '",0,0\n'

                    line3 = 'mov %x1_default,' + str(st1_x) + '\n'
                    line4 = 'stposition\n'
                    line = line0 + line1 + line2 + line3 + line4 +'\nprint 1\n'

                elif Stage11_line:
                    #print(line)
                    line0 = 'cspchar\n'

                    line1 = 'lsph 39,":a;bg\\' + Stage11_line[2] + '",-' + Stage11_line[3] + ',-' + Stage11_line[4] + ':vsp 39,1\n'
                    line2 = 'lsph 34,":a;bg\\st' + Stage11_line[1] + '",0,0:vsp 34,1\n'

                    line = line0 + line1 + line2 + '\nprint 1\n'

                elif Stage12_line:
                    #print(line)
                    line0 = 'cspchar\n'

                    line1 = 'lsph 34,":a;st\\st' + Stage12_line[1] + '",0,0:vsp 34,1\n'

                    line = line0 + line1 + '\nprint 1\n'

                elif Stage6_line:
                    line0 = 'cspchar\n'
                    st1_x = 800 - int(Stage6_line[6])

                    line1 = 'lsph 39,":a;bg\\' + Stage6_line[2] + '",-' + Stage6_line[3] + ',-' + Stage6_line[4] + ':vsp 39,1\n'
                    line2 = 'lsph 34,":a;st\\st' + Stage6_line[5] + '",' + str(st1_x) + ',0\n'

                    line3 = 'mov %x1_default,' + str(st1_x) + '\n'
                    line4 = 'stposition\n'

                    line = line1 + line2 + line3 + line4 +'\n'

                elif Stage7_line:
                    line0 = 'cspchar\n'

                    line1 = 'lsph 39,":a;bg\\' + Stage7_line[2] + '",-' + Stage7_line[3] + ',-' + Stage7_line[4] + ':vsp 39,1\n'

                    line =line0 + line1 + '\nprint 1\n'
                    #print(line)


                elif Stage99_line:
                    #print(line)
                    line0 = 'cspchar\n'

                    line1 = 'lsph 39,":a;bg\\' + Stage99_line[1] + '",-' + Stage99_line[2] + ',-' + Stage99_line[3] + ':vsp 39,1\n'
                    line = line0 + line1 + '\nprint 1\n'
                    #print(line)

                else:
                    line = line
                    #print(line)

   
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
                
                #print(line)
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
                    #print(line)
                    line = 'setwin1\n'
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
                #print(line)
                line = '*' + Include_line[1] + '\n'

            elif Shake_line:
                #未作成・dafault.txtで処理する書き方にする予定
                #7/12訂正　このままで大丈夫そう
                line = 'quake ' + Shake_line[2] + ',' + Shake_line[3] + '\n'
                
            elif Wait_line:
                
                #line.replace('\.wait','wait')  + '\\\n'
                line = 'delay ' + Wait_line[1] + '\n'
                #print(line)
                
            elif Chain_line:

                line = 'goto *' + Chain_line[1] + '\nend\n'
                #print(line)

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

                line = 'csp -1:print 1\nmovie "mov\\' + movie_line[2] + '.mpg",click\nprint 1\n'

            elif if_line:

                line = 'if %' + if_line[1] + ' ' + if_line[2] + ' ' + if_line[3] + ':goto *' + if_line[4] + '\n'

            elif Jump_line:

                line = 'goto *' + Jump_line[1] + '\n'

            elif add_line:

                
                ADDVAR = re.match(r'\.set (\S*) = (\S*) \+ (\d*)',line)
                ADD2VAR = re.match(r'\.set (\S*) = (\S*) \+ (\d*)',line)
                SETVAR = re.match(r'\.set (\S*) = (\d*)',line)

                if ADDVAR:
                    line = 'add %' +ADDVAR[1] + ',' + ADDVAR[3] + '\n'
                    #print(line)

                elif SETVAR:

                    line = 'mov %' + SETVAR[1] + ',' + SETVAR[2] + '\n' 

                    #print(line)

                else:

                    line = ';' + line + '\n'



            elif mov_line:

                line = 'mov %' + mov_line[1] + ',' + mov_line[2] + '\n' 

            elif trancelate_line:
                
                line = 'delay ' + trancelate_line[3] + '\n'

            elif erojump_line:
                #print(line)

                line = 'gosub *'  + erojump_line[1] + '\n'

            elif eroreturn_line:
                print('Convert now…')
                line = 'return\nend\n'

            elif vscroll_line:

                line = 'delay ' + vscroll_line[1] + '\n'

            elif hscroll_line:

                line = 'delay ' + hscroll_line[1] + '\n'



            else:
                #if 'include' in line:
                    #print(line)
                
                line = ';' + line + '\n'
            line = line.replace('[]　\\','click\nlookbackflush\n')
            line = line.replace('if %clearNagomi < 1:goto *label2','if %clearNagomi < 1:goto *label2_2')
            line = line.replace('if %clearYuduki < 1:goto *label2','if %clearYuduki < 1:goto *label2_2')
            line = line.replace('if %clearYuduki < 1:goto *label2','if %clearYuduki < 1:goto *label2_2')
            line = line.replace('\\v\\','\\')
            line = line.replace('mov %clearChika,1','mov %clearChika,1\ncsp -1:print 1:setwin0:goto *title')
            line = line.replace('mov %clearNagomi,1','mov %clearNagomi,1\ncsp -1:print 1:setwin0:goto *title')
            line = line.replace('mov %clearYuduki,1','mov %clearYuduki,1\ncsp -1:print 1:setwin0:goto *title')
            line = line.replace('mov %clearYuu,1','mov %clearYuu,1\ncsp -1:print 1:setwin0:goto *title')
                
        

            
            txt += line

    

print("処理が完了しました")

open(os.path.join(same_hierarchy,'0.txt'), 'w', errors='ignore').write(txt)

    

