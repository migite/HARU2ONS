# HARU2ONS
2004年にminoriより発売された「はるのあしおと」をONScripter向けに移植するコンバータです<br>
 パッケージ版のみの対応となります。ダウンロード版は現在ファイルの展開方法が確立されていないので動作不可です。<br>

<お知らせ>Prince of Sea氏が制作した[ONScripter_Multi_Converter](https://github.com/Prince-of-sea/ONScripter_Multi_Converter)に
当コンバータを提供しております。<br>
そちらもご利用ください。<br>
追記:HARU2ONS.exeはpyinstallerでコンパイルしているためWindows Defenderで弾かれる可能性があります。<br>
除外設定などを用いてご利用ください。


## ツールの使い方
 必要なファイルを指示通りに展開し、同一ディレクトリにHARU2ONS.exeを実行するだけです<br>
 詳しい説明は[こちら](https://ameblo.jp/righthand0920/entry-12754247374.html)

### シナリオ変換
パッケージ版「はるのあしおと」をインストールして、各アーカイブ(.paz)を展開する<br>
アーカイブ名と同じ名前のフォルダに展開をします。展開したあとのフォルダ構成は以下の通りです。
```
├─bg    ←bg.paz (bg1.pazは使用しません)
├─bgm   ←bgm.paz
├─mov   ←mov.paz
├─scr   ←scr.paz (scr1.paz,scr2.pazは使用しません)
├─se    ←se.paz
├─st    ←st.paz (st1.pazは使用しません)
├─sys   ←sys.paz (sys1.pazは使用しません)
├─voice ←voice.paz
├─HARU2ONS.exe
├─default.txt
└─first.bat
```
bgフォルダ、stフォルダに有るであろう*.aniのファイルは使用しません。各自消去して構いません<br>
scrフォルダ内のev~.sc,test.scはすべて消去してください。特にtest.scは消去しないと変換エラーが起こります<br>
<br>
各自展開したら、HARU2ONS.exeを実行してください

### PSP,Vita用変換作業
Prince of Sea氏が制作した[ONScripter_Multi_Converter](https://github.com/Prince-of-sea/ONScripter_Multi_Converter)をご利用ください<br>
こちらのコンバータを使う際は以下のファイル構成です。
```
├─bg    ←bg.paz (bg1.pazは使用しません)
├─bgm   ←bgm.paz
├─mov   ←mov.paz
├─scr   ←scr.paz (scr1.paz,scr2.pazは使用しません)
├─se    ←se.paz
├─st    ←st.paz (st1.pazは使用しません)
├─sys   ←sys.paz (sys1.pazは使用しません)
├─voice ←voice.paz
```

### 注意点
 - 元のゲームデータは勿論、展開したゲームデータもすべて、minori様の著作物です。個人の利用の範囲でお楽しみください。

 - 本コンバータはminori様の公式の許諾を受けたものではありません。minori様に問い合わせるような行為はご迷惑となりますのでおやめください。

#### 制作:RightHand Twitter:[@RightHand0920](https://twitter.com/RightHand0920)

---------------------------------------------------------------------------------------------------------------
2022/07/20 バグ報告:ver0.71~0.74において、うまくセーブが出来ないバグが発生しております

2022/07/21 追記 Ver0.75にて修正

---------------------------------------------------------------------------------------------------------------
## 更新履歴
 - 2023/02/07 Ver0.84 公開<br>
 コンフィグの音量調整機能を拡張<br>
 ついでにREADME.mdを多少整理しました<br>

 - 2022/08/18 Ver0.83 公開<br>
 コンバータ本体の変更点は特になし・GARbro側のオブジェクトエラー対策＆支援用にファイル作成、データ展開誘導のfirst.bat同梱

 - 2022/08/08 Ver0.82 公開<br>
 Hシーンスキップ(笑)機能実装です<br>
 外で遊ぶときにどうぞ<br>
 その他演出強化<br>

 - 2022/08/02 Ver0.81 公開<br>
 回想リセットの頻度を増やし、PSPでのRAM不足によるフリーズがほぼ起こらなくなりました<br>
 最終ルート終了時に強制終了される不具合を解消しました<br>

 - 2022/07/27 Ver0.80 公開<br>
 回想スタックのリセットポイントを設定しました。PSPでのRAM超過が改善されると思います<br>
 設定から音量の個別設定が出来るようになりました。文字サイズの設定が追加されました。<br>

 - 2022/07/21 Ver0.75 公開<br>
 セーブに関するバグを修正完了<br>
 文字サイズを調整<br>

 - 2022/07/20 Ver0.74 公開<br>
 文字サイズを大きくしました<br>

 - 2022/07/20 Ver0.73 公開<br>
 セーブ数を9→15に拡大<br>
 右クリックメニューで「ウィンドウを消す」を選択できるように<br>

 - 2022/07/19 Ver0.72 公開<br>
 PSPでの動作が重いため、必ず表示する背景画像のスプライトの消去処理を省くようににしました(立ち絵は据え置きです)<br>

 - 2022/07/18 Ver0.71 公開<br>
 ディレイ時間を増やし処理の安定性を上げました<br>

 - 2022/07/18 Ver0.7 公開<br>
 原作にあった細かい処理は省いていますが、最後まで動作します<br>
 オプションや回想モードは未実装です<br>

 - 2022/07/16 Ver0.334公開<br>
 智夏ルート以外のルートがエンディングまで完走できるようになりました(智夏ルートはフラグ管理が未完成なため出現しません)<br>
 画像の表示がおかしいところは追々修正しようと思います<br>

 - 2022/07/15 Ver0.2933公開<br>
 タイトル画面がまともになりました<br>
 wait命令でなくdelay命令を使うことにしました。<br>

 - 2022/07/14 Ver0.28公開<br>
 立ち絵・背景の変換命令をほぼイチから書き直しました。<br>
 画像のサイズ依存の見切れ以外はほとんど不具合なく立ち絵表示ができるようになりました<br>

 - 2022/07/14 Ver0.2133公開<br>
 立ち絵が問題なく表示できるようになり、見た目上マシになりました。大きさの関係で見切れてるけど。<br>
 Hシーン手前くらいで落ちるんだよなぁ…<br>

 - 2022/07/11 Ver0.19公開<br>
 (なんか立ち絵出)ないです。なんでやろなぁ(すっとぼけ)<br>
 背景がおそらく逆にずれてるけどもしかしてこのエンジンxy逆な気がする<br>
