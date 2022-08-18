@echo off

cd %~dp0
chcp 65001

md bg
md bgm
md mov
md scr
md se
md st
md sys
md voice

echo 作られたフォルダに従って展開してください

echo bg.paz内の画像データ--- bgフォルダ
echo bgm.paz内の音楽データ-- bgmフォルダ
echo mov.paz内のムービー---- movフォルダ
echo scr.paz内のシナリオ---- scrフォルダ
echo se.paz内の効果音データ- seフォルダ
echo st.paz内の立ち絵データ- stフォルダ
echo sys.paz内の画像データ-- sysフォルダ
echo voice.paz内のボイス---- voiceフォルダ
echo 画像はすべて.png、音源はすべて.oggに設定

pause