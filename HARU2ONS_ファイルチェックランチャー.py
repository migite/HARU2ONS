import os
import sys
import glob
import re
import difflib

gnd_pass = (os.path.dirname(sys.argv[0]))

resource_dir = os.path.join(gnd_pass,'resource')

background_dir = os.path.join(gnd_pass,'bg')
bgm_dir = os.path.join(gnd_pass,'bgm')
stand_dir = os.path.join(gnd_pass,'st')
scenario_dir = os.path.join(gnd_pass,'scr')
movie_dir = os.path.join(gnd_pass,'mov')
system_dir = os.path.join(gnd_pass,'sys')
voice_dir = os.path.join(gnd_pass,'voice')
se_dir = os.path.join(gnd_pass,'se')


print('はるのあしおと for ONS PSP 起動ランチャー\n')

print('このコンバータはVer x.xxです。\n')

print('変換前に、ファイルの整合性チェックを行います。\n')

print('データの展開が正しく行われていない場合、正常に変換できない場合があります。\n')

bguser_file = os.path.join(resource_dir, 'bguser.txt')
bgpath = glob.glob(os.path.join(background_dir, '*'))

#ユーザのbgフォルダの中身をフルパスで取得します
with open(bguser_file,'w') as f:

    for file in bgpath:
        
        f.writelines(file)

#フルパスではなくbg//*の形にします
bgwrite = ''
with open(bguser_file, 'r',) as f:
    for line in bgpath:
        
        match_obj = re.match(r'(\S+)bg\\(\S+)', line)
        if match_obj:
            linecfg = 'bg\\' + match_obj[2] + '\n'
            bgwrite += linecfg
            #print(bgwrite)

#チェック用のテキストファイルを作ります
with open(bguser_file, 'w') as f:
    f.writelines(bgwrite)

f.close()

bg_file1 = os.path.join(resource_dir,'collectbg.txt')
bg_file2 = os.path.join(resource_dir,'bguser.txt')

bg_file1_opend = open(bg_file1)
bg_file2_opend = open(bg_file2)

diff = difflib.Differ()

#これ以降実装うまく行ってないです
#なんか16進数で出てくるんですけど見る限り普通の文字列とバイナリ値参照して比較してない？
#あとおそらく最後の行しか書き込めてない
output_diff = diff.compare(bg_file1_opend.readlines(), bg_file2_opend.readlines())