#!/usr/bin/env python3
from pathlib import Path
import concurrent.futures
import glob
import re


# ONScripter_Multi_Converter用タイトル情報管理関数
def title_info():

	#タイトル情報管理辞書作成
	info = {
		'brand': 'minori',
		'date': 20040723,
		'title': 'はるのあしおと',
		'cli_arg': 'minori_haruoto',
		'requiredsoft': [],
		'is_4:3': bool(not r'<ONS_RESOLUTION_CHECK_DISABLED>' in default_txt()),
		'program_name': ['はるのあしおと'],#一覧取得用
		'exe_name': ['haruoto'],

		'version': [
			'はるのあしおと パッケージ版(2004/07/23)',
		],

		'notes': [
			'本作の変換は主にRightHand氏が制作したものです',
			'詳細につきましては、github.com/migite/HARU2ONSを確認してください',
		]
	}

	#作った辞書をreturn
	return info


# ONScripter_Multi_Converter用アーカイブ自動展開関数
def extract_resource(values: dict, values_ex: dict, pre_converted_dir: Path):

	#GARbroを使って展開する関数をutils.pyから呼び出す
	from utils import extract_archive_garbro # type: ignore

	#並列で処理する最大数を引数の辞書から持ってきて変数に代入
	num_workers = values_ex['num_workers']
	
	#入力元のパスを引数の辞書から持ってきて変数に代入
	input_dir = values['input_dir']
	
	#並列処理を(さっき代入してきた最大数をセットして)開始
	with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:

		#並列処理管理用の配列を作成
		futures = []
		
		#展開予定のpazファイルの名前をfor文で回す
		for paz_name in ['bg', 'bgm', 'mov', 'scr', 'se', 'st', 'sys', 'voice']:

			#pazファイルのフルパスを代入
			p = Path(input_dir / Path(paz_name + '.paz'))

			#出力先のフルパスを代入
			e = Path(pre_converted_dir / paz_name)

			#pazファイルがなければ
			if not p.exists():

				#(ファイル名)が見つかりませんエラー
				raise FileNotFoundError('{}が見つかりません'.format(str(p.name)))
			
			#処理予定のタスクへ「"GARbroを使って展開する関数"へpazファイルと出力先を引数にして処理」を追加
			futures.append(executor.submit(extract_archive_garbro, p, e, 'png'))

		#並列処理タスクがすべて終わるまでここで待つ
		concurrent.futures.as_completed(futures)

	#bgフォルダ内の.aniファイルのパスをfor文で回す
	for filepath in Path(pre_converted_dir / 'bg').glob('*.ani'):

		#削除
		filepath.unlink()
	
	#stフォルダ内の.aniファイルのパスをfor文で回す
	for filepath in Path(pre_converted_dir / 'st').glob('*.ani'):

		#削除
		filepath.unlink()
	
	#scrフォルダ内のev~.scファイルのパスをfor文で回す
	for filepath in Path(pre_converted_dir / 'scr').glob('ev*.sc'):

		#削除
		filepath.unlink()

	#scrフォルダ内のtest.scファイルを削除
	Path(pre_converted_dir / 'scr' / 'test.sc').unlink()

	return


def default_txt():
	s = ''';$V2000G1000S800,600L10000
*define
caption "HARU2NS4ONSVer0.86"
nsa
globalon
rmenu "セーブ",save,"ロード",load,"リセット",reset,"スキップ",skip,"ログ",lookback
pretextgosub *pretext_sb
windowback
savenumber 18
humanz 30
selectvoice "","sys\\cursor.wav","sys\\click.wav"

mov %TEXT_size,1

;numalias領域
numalias st_x1,51
numalias st_y1,52
numalias st_x2,53
numalias st_y2,54
numalias st_x3,55
numalias st_y3,57
numalias st_x4,58
numalias st_y4,59
numalias st_x5,60
numalias st_y5,61
numalias x1_default,62
numalias x2_default,63
numalias x3_default,64
numalias x4_default,65
numalias x5_default,66
numalias winmode,100
numalias A_001,201
numalias clearChika,202
numalias clearNagomi,203
numalias clearYuduki,204
numalias clearYuu,205
numalias favNagomi,206
numalias favYuduki,207
numalias favYuu,208
numalias B_004,209
numalias B_008,210
numalias B_011,211
numalias B_015,212
numalias C_007,213
numalias C_012,214
numalias C_015,215
numalias C_017,216
numalias D_004,217
numalias D_006,218
numalias D_007,219
numalias D_009,220
numalias D_013,221
numalias D_015,222
numalias E_007,223
numalias E_008,224
numalias route,225
numalias Vol_bgm,250
numalias Vol_voice,251
numalias Vol_Se,252
numalias TEXT_size,260
numalias eroskip,261

;defsub領域
defsub setwin0
defsub setwin1
defsub setwin2
defsub cspchar
defsub csptitle
defsub cspmemory
defsub stposition
defsub bg			;erasetextwindow用bg命令乗っ取り

;effect領域
effect 2,10,300		;エフェクト番号2に効果番号10(クロスフェード)の300ミリ秒を割り当て

game
;スプライト番号一覧
;10,11　名前表示
;30~34　立ち絵
;37,38　演出背景(現在廃止中)
;39　標準背景
;41~45　タイトル画面ボタン
;49　タイトル背景

;------------------定義域ここまで-------------------

*start

goto *title

*bg
erasetextwindow 1
getparam $0,%0
_bg $0,%0
return

*pretext_sb
saveoff

erasetextwindow 0

gettag $0

if %winmode == 0 csp 11

if %winmode == 1 lsp 10,":s/30,30,0;#ffffff$0",55,430
if %winmode == 1 lsp 11,"sys\\namePanel.png",0,417,128

print 1

saveon
return


*setwin0
textoff
csp 10:csp 11
mov %winmode,0
return

*setwin1
textoff
if %TEXT_size == 0 setwindow3 50,480,30,3,24,24,1,2,10,1,1,":a;sys/msgPanel.png",0,417
if %TEXT_size == 1 setwindow3 50,480,26,4,26,26,1,2,10,1,1,":a;sys/msgPanel.png",0,417
if %TEXT_size == 2 setwindow3 50,480,22,4,30,30,1,2,10,1,1,":a;sys/msgPanel.png",0,417
mov %winmode,1
return

*setwin2
textoff
if %TEXT_size == 0 setwindow3 100,50,20,10,24,24,1,2,10,1,1,":a;sys/fullPanel.png",0,0
if %TEXT_size == 1 setwindow3 100,50,18,10,26,26,1,2,10,1,1,":a;sys/fullPanel.png",0,0
if %TEXT_size == 2 setwindow3 100,50,16,10,28,28,1,2,10,1,1,":a;sys/fullPanel.png",0,0
mov %winmode,2
return

*cspchar
csp 37
csp 38
csp 30
csp 31
csp 32
csp 33
csp 34
print 1
return

*csptitle
csp 41
csp 42
csp 43
csp 44
csp 45
csp 49
print 10,300
return

*cspmemory
csp 51
csp 52
csp 53
csp 54
csp 55
csp 56
csp 57
csp 58
return

*stposition
getspsize 34,%st_x1,%st_y1
getspsize 33,%st_x2,%st_y2
getspsize 32,%st_x3,%st_y3
getspsize 31,%st_x4,%st_y4
getspsize 30,%st_x5,%st_y5

div %st_x1,2
add %st_x1,%x1_default
sub %st_x1,800
sub %st_y1,600
mov %st_x1,-%st_x1
mov %st_y1,-%st_y1

amsp 34,%st_x1,%st_y1
vsp 34,1

if %st_x2 == 0 print 1
if %st_x2 == 0 return

div %st_x2,2
add %st_x2,%x2_default
sub %st_x2,800
sub %st_y2,600
mov %st_x2,-%st_x2
mov %st_y2,-%st_y2

amsp 33,%st_x2,%st_y2
vsp 33,1

if %st_x3 == 0 print 1
if %st_x3 == 0 return 

div,%st_x3,2
add %st_x3,%x3_default
sub %st_x3,800
sub %st_y3,600
mov %st_x3,-%st_x3
mov %st_y3,-%st_y3

amsp 32,%st_x3,%st_y3
vsp 32,1

if %st_x4 == 0 print 1
if %st_x4 == 0 return

div %st_x4,2
add %st_x4,%x4_default
sub %st_x4,800
sub %st_y4,600
mov %st_x4,-%st_x4
mov %st_y4,-%st_y4

amsp 31,%st_x4,%st_y4
vsp 31,1

if %st_x5 == 0 print 1
if %st_x5 == 0 return

div %st_x5,2
add %st_x5,%x5_default
sub %st_x5,800
sub %st_y5,600
mov %st_x5,-%st_x5
mov %st_y5,-%st_y5

amsp 30,%st_x5,%st_y5
vsp 30,1

return

;----------追加命令ここまで-------------

*title
csp -1
rmode 0
bgm "bgm\\bgm_22.ogg"
lsph 41,":a;sys/mainmenuNewGame.png",570,45
lsph 42,":a;sys/mainmenuLoadGame.png",570,90
lsph 43,":a;sys/mainmenuSystem.png",570,135
lsph 44,":a;sys/mainmenuMemories.png",570,180
lsph 45,":a;sys/mainmenuExit.png",570,225
lsph 49,":a;sys/topmenu.png",0,0

vsp 49,1

exbtn 41,41, "P41"
exbtn 42,42, "P42"
exbtn 43,43, "P43"
exbtn 44,44, "P44"
exbtn 45,45, "P45"

exbtn_d "C41C42C43C44C45"

*title_loop

btnwait %0
if %0 == 0 goto *title_loop
if %0 == -1 goto *title_loop

if %0 == 41 goto *startmode
if %0 == 42 goto *loadmode
if %0 == 43 goto *settingmode
if %0 == 44 goto *memory
if %0 == 45 goto *endmode

goto *title_loop
end

*startmode
csptitle
rmode 1
bgmstop
saveon
setwin0
erasetextwindow 0
goto *A_001
end

*loadmode
csptitle
saveon
lsph 49,":a;sys/saveloadBase.png",0,0:vsp 49,1
print 1
systemcall load
bgmstop
goto *title
end

*settingmode
csptitle
lsph 49,":a;sys/configBase.png",0,0:vsp 49,1
print 1
bgmstop

*settingmenu
setwin2
select "音量設定",*volconfig_select,"文字サイズ変更",*mojisize,"Ｈシーンスキップ",*skipero,"おわる",*title


*volconfig_select
select "かんたん設定",*volconfig,"詳細設定",*volmenu_GUI


*volconfig
setwin1
selnum %Vol_bgm,"音量設定　ＢＧＭ１００","音量設定　ＢＧＭ５０","音量設定　ＢＧＭ０"

if %Vol_bgm == 0 mov %Vol_bgm,100
if %Vol_bgm == 1 mov %Vol_bgm,50
if %Vol_bgm == 2 mov %Vol_bgm,0

bgmvol %Vol_bgm

selnum %Vol_voice,"音量設定　ＶＯＩＣＥ１００","音量設定　ＶＯＩＣＥ５０","音量設定　ＶＯＩＣＥ０"

if %Vol_voice == 0 mov %Vol_voice,100
if %Vol_voice == 1 mov %Vol_voice,50
if %Vol_voice == 2 mov %Vol_voice,0

voicevol %Vol_voice

selnum %Vol_Se,"音量設定　ＳＥ１００","音量設定　ＳＥ５０","音量設定　ＳＥ０"

if %Vol_Se == 0 mov %Vol_Se,100
if %Vol_Se == 1 mov %Vol_Se,50
if %Vol_Se == 2 mov %Vol_Se,0

sevol %Vol_Se

設定が完了しました\\
setwin0
goto *settingmenu

*mojisize
setwin1
selnum %TEXT_size,"文字サイズ小","文字サイズ中","文字サイズ大"


設定が完了しました\\
setwin0
goto *settingmenu

*skipero
setwin1
selnum %eroskip,"オフ","オン"
設定が完了しました\\
goto *settingmenu

*memory

lsph 69,"sys\\exmPrologue.png",0,0:vsp 49,1
print 1
wait 2000
cspmemory
goto *title
end

*endmode
csptitle
;_bg black,10,300		;ここ多分記述ミスなので修正しますた
_bg black,2				;こっちではエフェクト番号だけ指定、定義節で効果番号とエフェクト番号の紐づけ(?)を行うのが正解
end


;------ 以下Prince-of-seaが勝手に移植したガバガバGUI音量設定 --------------
*volmenu_GUI
	;https://gist.github.com/Prince-of-sea/325b8ae6912ecf23316a71c3d008480c
	;文字/数字/スプライト/ボタン
	;全部130~149までを使ってます - 競合に注意
	
	;はるのあしおと専用
	vsp 49,0
	_bg black,2
	
	;バー文字列定義
	mov $130,":s;#FFFFFF#666666○――――――――――"
	mov $131,":s;#FFFFFF#666666―○―――――――――"
	mov $132,":s;#FFFFFF#666666――○――――――――"
	mov $133,":s;#FFFFFF#666666―――○―――――――"
	mov $134,":s;#FFFFFF#666666――――○――――――"
	mov $135,":s;#FFFFFF#666666―――――○―――――"
	mov $136,":s;#FFFFFF#666666――――――○――――"
	mov $137,":s;#FFFFFF#666666―――――――○―――"
	mov $138,":s;#FFFFFF#666666――――――――○――"
	mov $139,":s;#FFFFFF#666666―――――――――○―"
	mov $140,":s;#FFFFFF#666666――――――――――○"
	
*volmenu_loop
	;取得
	getbgmvol   %130
	getsevol    %131
	getvoicevol %132
	
	;文字列変換
	itoa2 $141,%130
	itoa2 $142,%131
	itoa2 $143,%132
	
	;バー代入
	if %130==  0 mov $146,$130
	if %130== 10 mov $146,$131
	if %130== 20 mov $146,$132
	if %130== 30 mov $146,$133
	if %130== 40 mov $146,$134
	if %130== 50 mov $146,$135
	if %130== 60 mov $146,$136
	if %130== 70 mov $146,$137
	if %130== 80 mov $146,$138
	if %130== 90 mov $146,$139
	if %130==100 mov $146,$140
	if %131==  0 mov $147,$130
	if %131== 10 mov $147,$131
	if %131== 20 mov $147,$132
	if %131== 30 mov $147,$133
	if %131== 40 mov $147,$134
	if %131== 50 mov $147,$135
	if %131== 60 mov $147,$136
	if %131== 70 mov $147,$137
	if %131== 80 mov $147,$138
	if %131== 90 mov $147,$139
	if %131==100 mov $147,$140
	if %132==  0 mov $148,$130
	if %132== 10 mov $148,$131
	if %132== 20 mov $148,$132
	if %132== 30 mov $148,$133
	if %132== 40 mov $148,$134
	if %132== 50 mov $148,$135
	if %132== 60 mov $148,$136
	if %132== 70 mov $148,$137
	if %132== 80 mov $148,$138
	if %132== 90 mov $148,$139
	if %132==100 mov $148,$140
	
	;画面作成
	lsp 130,":s;#FFFFFF［Ｃｏｎｆｉｇ］", 50, 50
	lsp 131,":s;#FFFFFF#666666リセット", 400,450
	lsp 132,":s;#FFFFFF#666666戻る",     550,450
	
	lsp 135,":s;#FFFFFFＢＧＭ",           50,150
	lsp 136,":s;#FFFFFF#666666＜",       200,150
	lsp 137,$146,                        250,150
	lsp 138,":s;#FFFFFF#666666＞",       550,150
	lsp 139,":s;#FFFFFF#666666"+$141,    600,150
	
	lsp 140,":s;#FFFFFFＳＥ",             50,250
	lsp 141,":s;#FFFFFF#666666＜",       200,250
	lsp 142,$147,                        250,250
	lsp 143,":s;#FFFFFF#666666＞",       550,250
	lsp 144,":s;#FFFFFF#666666"+$142,    600,250
	
	lsp 145,":s;#FFFFFFＶＯＩＣＥ",       50,350
	lsp 146,":s;#FFFFFF#666666＜",       200,350
	lsp 147,$148,                        250,350
	lsp 148,":s;#FFFFFF#666666＞",       550,350
	lsp 149,":s;#FFFFFF#666666"+$143,    600,350
	
	print 1
	
	;ボタン定義
	bclear
	spbtn 131,131
	spbtn 132,132
	spbtn 136,136
	spbtn 138,138
	spbtn 141,141
	spbtn 143,143
	spbtn 146,146
	spbtn 148,148
	
	;入力待ち
	btnwait %140
	
	if %140==131 bgmvol 100:sevol 100:voicevol 100
	if %140==132 csp -1:reset
	if %140==136 if %130!=  0 sub %130,10:bgmvol %130
	if %140==138 if %130!=100 add %130,10:bgmvol %130
	if %140==141 if %131!=  0 sub %131,10:sevol %131
	if %140==143 if %131!=100 add %131,10:sevol %131
	if %140==146 if %132!=  0 sub %132,10:voicevol %132
	if %140==148 if %132!=100 add %132,10:voicevol %132
	
goto *volmenu_loop
;音量調整ここまで


;-------------------シナリオここから------------------

'''

	return s


_STAGE_BACKGROUND = r'(\S+)\s(\d*)\s(\d*)'
_STAGE_CHARACTER = r'\sst(\S+)\s(\d*)'
# 既存のマッチ範囲を保ち、人数が多い形式を先に試す。
_STAGE_CAST_PATTERNS = (
	re.compile(r'(\S+)\s(\d+)\s(\d+)' + r'\sst(\S+)\s(\d+)' * 4 + _STAGE_CHARACTER),
	re.compile(_STAGE_BACKGROUND + _STAGE_CHARACTER * 3 + r'\sst(\S)\s(\d+)'),
	re.compile(_STAGE_BACKGROUND + _STAGE_CHARACTER * 3),
	re.compile(_STAGE_BACKGROUND + _STAGE_CHARACTER * 2),
	re.compile(_STAGE_BACKGROUND + _STAGE_CHARACTER),
)


def _background_command(name, x, y):
	return f'lsph 39,":a;bg\\{name}",-{x},-{y}:vsp 39,1\n'


def _stage_with_characters(match):
	background, x, y, *cast = match.groups()
	commands = ['cspchar\n', _background_command(background, x, y)]
	positions = []
	for index, (name, position) in enumerate(zip(cast[::2], cast[1::2]), start=1):
		commands.append(f'lsph {35 - index},":a;st\\st{name}",0,0\n')
		positions.append(f'mov %x{index}_default,{800 - int(position)}\n')
	commands.extend(positions)
	commands.append('stposition\n\n')
	if len(positions) == 1:
		commands.append('print 1\n')
	return ''.join(commands)


def _convert_stage(line):
	line = re.sub(
		r'\.stage\s\* |\.stage\s|:\[\S+,\S+,\S+\]ol_\S+.png|:ol_\S+.png|:\[\S+,\S+,\S+\]',
		'', line,
	)
	for pattern in _STAGE_CAST_PATTERNS:
		match = pattern.match(line)
		if match:
			return _stage_with_characters(match)

	# st で始まる背景・拡大表示は、画面効果付きの背景より優先する。
	match = re.match(r'st(\S+)\s(\S{4,})\s(\d*)\s(\d*)', line)
	if match:
		return ('cspchar\n' + _background_command(match[2], match[3], match[4])
			+ f'lsph 34,":a;bg\\st{match[1]}",0,0:vsp 34,1\n\nprint 1\n')
	match = re.match(r'st(\S+)\s(\d*)\s(\d*)', line)
	if match:
		return f'cspchar\nlsph 34,":a;st\\st{match[1]}",0,0:vsp 34,1\n\nprint 1\n'

	match = re.match(r'\S+\s(\S+)\s(\d+)\s(\d+)\sst(\S+)\s(\d)', line)
	if match:
		x = 800 - int(match[5])
		return (_background_command(match[1], match[2], match[3])
			+ f'lsph 34,":a;st\\st{match[4]}",{x},0\nmov %x1_default,{x}\nstposition\n\n')

	match = re.match(r'\S+\s(\S{4,})\s(\d+)\s(\d+)', line) or re.match(_STAGE_BACKGROUND, line)
	if match:
		return 'cspchar\n' + _background_command(*match.groups()) + '\nprint 1\n'
	return line


class _ScenarioConverter:
	"""全シナリオで共有する改ページ状態と選択肢の通し番号を管理する。"""

	def __init__(self, show_progress):
		self.show_progress = show_progress
		self.group_messages = False
		self.previous_message = None
		self.choice_number = 0

	def _message(self, match):
		number, voice, speaker, text = match.groups()
		speaker = re.sub(r'[@#]', '', speaker)
		text = re.sub(r'\{\S*}|\\[nNaw]', '', text)
		end = '@\n' if self.group_messages and number == self.previous_message else '\\\n'
		self.previous_message = number
		audio = f'dwave 0,"voice\\{voice}.ogg"\n' if voice else ''
		return f'{audio}[{speaker}]{text}{end}'

	def _panel(self, mode, line):
		for digit, window in (('0', 0), ('1', 1), ('2', 2), ('3', 1)):
			if digit in mode:
				self.group_messages = window == 2
				return f'setwin{window}\n'
		return ';' + line

	def _select(self, match):
		groups = match.groups()
		options = [f'"{text}",*{label}_{self.choice_number}'
			for text, label in zip(groups[::2], groups[1::2])]
		self.choice_number += 1
		return 'select ' + ','.join(options) + '\n'

	def convert_line(self, line):
		match = re.match(r'\.message\s([0-9]+)\t(.*?)\t(.*?)\t(.+)', line)
		if match:
			return self._message(match)
		if line.startswith('.stage'):
			return _convert_stage(line)
		if line.startswith('.playBGM'):
			match = re.match(r'\.playBGM (\S*).ogg', line)
			return f'bgm "bgm\\{match[1]}.ogg" \n' if match else 'bgmstop\n'
		if line.startswith('.playSE '):
			match = re.match(r'\.playSE (\S*).ogg', line)
			return f'dwave 1,"se\\{match[1]}.ogg" \n' if match else 'dwavestop 1\n'

		match = re.match(r'\.panel\s([0-9]+)', line)
		if match:
			return self._panel(match[1], line)
		match = re.match(r'\.label (\S*)', line)
		if match:
			suffix = f'_{self.choice_number - 1}' if re.match(r'label[0-9]', match[1]) else ''
			return f'*{match[1]}{suffix}\n'
		match = re.match(r'\.include\s(\S*).sc', line)
		if match:
			return f'*{match[1]}\n'
		match = re.match(r'\.shakeScreen\t[A-Z]+\t([0-9]+)\t([0-9]+)', line)
		if match:
			return f'quake {match[1]},{match[2]}\n'
		match = re.match(r'\.wait (\d+)', line)
		if match:
			return f'delay {match[1]}\n'
		match = re.match(r'\.chain (\S*).sc', line)
		if match:
			return f'goto *{match[1]}\nend\n'
		match = (re.match(r'\.select\s(\S*):(\S*)\s(\S*):(\S*)\s(\S*):(\S*)', line)
			or re.match(r'\.select\s(\S+):(\S+)\s(\S+):(\S+)', line))
		if match:
			return self._select(match)

		if '.end' in line:
			return ';end\n'
		match = re.match(r'\.movie\s\S*\s(\S*).mpg', line)
		if match:
			return f'csp -1:print 1\nmovie "mov\\{match[1]}.mpg",click\nprint 1\n'
		match = re.match(r'\.if (\S*) (\S*) (\d*) (\S*)', line)
		if match:
			return f'if %{match[1]} {match[2]} {match[3]}:goto *{match[4]}\n'
		match = re.match(r'\.goto\s(\S*)', line)
		if match:
			return f'goto *{match[1]}\n'
		match = re.match(r'\.set (\S*) = \S* \+ (\d*)', line)
		if match:
			return f'add %{match[1]},{match[2]}\n'
		match = re.match(r'\.set (\S*) = (\d*)', line) or re.match(r'\.setGlobal\s(\S*) = (\S*)', line)
		if match:
			return f'mov %{match[1]},{match[2]}\n'
		match = re.match(r'\.transition \d* \S* (\d*)', line)
		if match:
			duration = int(match[1])
			zeros = '00' if duration <= 10 else '0' if duration <= 100 else ''
			return f'delay {match[1]}{zeros}\n'
		match = re.match(r'#include\s(\S*).sc', line)
		if match:
			return f'if %eroskip == 0 gosub *{match[1]}\n'
		if line.startswith(';■エロシーンここまで'):
			if self.show_progress:
				print('Convert now…')
			return 'return\nend\n'
		match = re.match(r'\.[vh]scroll\s(\d+)\s\d+', line)
		if match:
			return f'delay {match[1]}\n'
		return ';' + line + '\n'


def _apply_game_fixes(line):
	line = line.replace('[]　\\', 'click\nlookbackflush\n')
	line = line.replace('if %clearNagomi < 1:goto *label2', 'if %clearNagomi < 1:goto *label2_2')
	# 旧変換では Yuduki の置換が2回適用される。
	line = line.replace('if %clearYuduki < 1:goto *label2', 'if %clearYuduki < 1:goto *label2_2_2')
	line = line.replace('\\v\\', '\\')
	for name in ('Chika', 'Nagomi', 'Yuduki', 'Yuu'):
		flag = f'mov %clear{name},1'
		line = line.replace(flag, flag + '\ncsp -1:print 1:setwin0:goto *title')
	return line


# メイン関数
def main(values: dict = {}, values_ex: dict = {}, pre_converted_dir: Path = Path.cwd()):
	if values:
		extract_resource(values, values_ex, pre_converted_dir)
	else:
		print('コンバートを開始します…')

	root = Path(pre_converted_dir)
	converter = _ScenarioConverter(show_progress=not values)
	txt = default_txt()
	for filename in glob.glob(str(root / 'scr' / '*.sc')):
		path = Path(filename)
		txt += f'cspchar\ngoto *title\n;--------------- {path.stem} ---------------\nend\n*{path.stem}\nlookbackflush\n'
		# 元の変換と同じく、次のシナリオの開始時にそれまでの // を置換する。
		txt = txt.replace('//', ';;;')
		with path.open(encoding='shift_jis', errors='ignore') as scenario:
			for line in scenario:
				txt += _apply_game_fixes(converter.convert_line(line))

	(root / '0.txt').write_text(txt, encoding='cp932', errors='ignore')
	if not values:
		print('処理が完了しました')


#事前に展開済みなら一応単体でも動作するようにしておく
if __name__ == "__main__":
	main()