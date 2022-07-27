# HARU2ONS
2004年にminoriより発売された「はるのあしおと」をONScripter向けに移植するコンバータです
ダウンロード版はファイルの暗号化が掛けられており、現状では展開ツールの存在も確認できていないので、動作の対象外です

追記:HARU2ONS.exeがpyinstallerでコンパイルしているためWindows Defenderで弾かれる可能性があります。除外設定などを用いてご利用ください

・ツールの使い方
 必要なファイルを指示通りに展開し、同一ディレクトリにHARU2ONS.exeを実行するだけです

・シナリオ変換
パッケージ版「はるのあしおと」をインストールして、各アーカイブ(.paz)を展開する

アーカイブ名と同じ名前のフォルダに展開をします。「st1.paz」のようなアーカイブは展開しなくて結構です

bgフォルダ、stフォルダに有るであろう*.aniのファイルは使用しません。各自消去して構いません

scrフォルダ内のev~.sc,test.scはすべて消去してください。特にtest.scは消去しないと変換エラーが起こります


各自展開したら、HARU2ONS.exeを実行してください

・PSP用変換作業
Prince of Sea氏が制作した
 https://github.com/Prince-of-sea/ONScripter_Multi_Converter
 をご利用ください
 
・元のゲームデータは勿論、展開したゲームデータもすべて、minori様の著作物です。個人の範囲でお楽しみください。

・本コンバータはminori様の公式の許諾を受けたものではありません。minori様に問い合わせるような行為はご迷惑となりますのでおやめください。

制作:RightHand Twitter:@RightHand0920
---------------------------------------------------------------------------------------------------------------
2022/07/20 バグ報告:ver0.71~0.74において、うまくセーブが出来ないバグが発生しております
2022/07/21　追記　Ver0.75にて修正
---------------------------------------------------------------------------------------------------------------
更新履歴
2022/07/27 Ver0.80 公開
回想スタックのリセットポイントを設定しました。PSPでのRAM超過が改善されると思います
設定から音量の個別設定が出来るようになりました。文字サイズの設定が追加されました。

2022/07/21 Ver0.75 公開
セーブに関するバグを修正完了
文字サイズを調整

2022/07/20 Ver0.74 公開
文字サイズを大きくしました

2022/07/20 Ver0.73 公開
セーブ数を9→15に拡大
右クリックメニューで「ウィンドウを消す」を選択できるように

2022/07/19 Ver0.72 公開
PSPでの動作が重いため、必ず表示する背景画像のスプライトの消去処理を省くようににしました(立ち絵は据え置きです)

2022/07/18 Ver0.71 公開
ディレイ時間を増やし処理の安定性を上げました

2022/07/18 Ver0.7 公開
原作にあった細かい処理は省いていますが、最後まで動作します
オプションや回想モードは未実装です

2022/07/16 Ver0.334公開
智夏ルート以外のルートがエンディングまで完走できるようになりました(智夏ルートはフラグ管理が未完成なため出現しません)
画像の表示がおかしいところは追々修正しようと思います

2022/07/15 Ver0.2933公開
タイトル画面がまともになりました
wait命令でなくdelay命令を使うことにしました。

2022/07/14 Ver0.28公開
立ち絵・背景の変換命令をほぼイチから書き直しました。
画像のサイズ依存の見切れ以外はほとんど不具合なく立ち絵表示ができるようになりました

2022/07/14 Ver0.2133公開
立ち絵が問題なく表示できるようになり、見た目上マシになりました。大きさの関係で見切れてるけど。
Hシーン手前くらいで落ちるんだよなぁ…

2022/07/11 Ver0.19公開
(なんか立ち絵出)ないです。なんでやろなぁ(すっとぼけ)
背景がおそらく逆にずれてるけどもしかしてこのエンジンxy逆な気がする



