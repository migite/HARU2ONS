import glob
import sys
import os
import re
from tkinter import SE
import chardet

same_hierarchy = (os.path.dirname(sys.argv[0]))

scenario_dir = os.path.join(same_hierarchy,'scr','sc')


with open(os.path.join(same_hierarchy, 'default.txt')) as f:
	txt = f.read()

pathlist = glob.glob(os.path.join(scenario_dir, 'scr', '*.sc'))
pathlist.extend(glob.glob(os.path.join(scenario_dir, '*.sc')))

for snr_path in pathlist:
	
	with open(snr_path, 'rb') as f:
		char_code =chardet.detect(f.read())['encoding']

	with open(snr_path, encoding=char_code, errors='ignore') as f:
		txt += '\n;--------------- '+ os.path.splitext(os.path.basename(snr_path))[0] +' ---------------\nend\n\n'
		txt = txt.replace(';', ';;;')
        
        for line in f:
            #命令が特殊な形は先に分けておきます
            Split_line =  re.match('\.message',line)
            BGCG_line = re.match('\.stage',line)
            BGM_line = re.match('\.PlayBGM',line)
            SE_line = re.match('\.PlaySE',line)

            if Split_line:

                Separate_line = re.split(line)

                if re.search('[a-z]_[A]_[0-9]-[0-9]',line):
                    
                    line = 'dwave 0 Voice\\' + Separate_line[3] + '.ogg\n' + Separate_line[4] + '\n' + Separate_line[5] + '\n' 

                else:

                    line = Separate_line[3] + '\n' + Separate_line[4] + '\n'


            elif re.match('\.wait',line):
                line = re.sub('\.wait [0-9]','wait [0-9]')

            else:
                line = r';' + line
            
            txt += line

    
        

        

open(os.path.join(same_hierarchy,'0.txt'), 'w', errors='ignore').write(txt)

    

