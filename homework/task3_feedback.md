

__doc__ shinx build in document shinx
## Document Feedback
ドキュメント書くなら説明チックでもいい 何がしたい 背景
プロジェクトの説明
Code見るだけだとどの関数がUserに使ってほしいかわからない 
他の人がどの関数をどう呼び出したらいいかわかる 公式ドキュメント Repository Pythonのライブラリ
どういうライブラリなのか、こういう機能持ってる、こういうのもあるけどココだとこういうのができないからこれはできる
なぜこれがあるか、何が目的なのか
入力数式のような文字列一つ、入力想定、tokenizeに文字列を渡す　tokenizeの出力 evaluate→答えが出ます
roundは対応してる これは対応してない
O(N)とかあると嬉しい

## Code Feedback
documentの参考：https://docs.python.org/ja/3/library/functions.html#eval
0で割ったらまずい問題、数膨大案件→pythonバカでかい数input not a number 例外を投げる
やってみないとわからない系のerror case, ぐちゃぐちゃ諦めは必要
記号連続はだめ連続したらだめなものabsの後にかっこがない
()とかに当てはまるやつ最初に簡易チェックする？残りの深いケース
helper function みたいなのをつかってそれを中で呼ぶのはいいかも どんなerrorを投げるか？stack traceも表示する
10文字目でplusが連続してる　どこで、なんで起きてる?
Errorが正しく起きるかもテストする TestError作ってエラーのTry catch catchの文面が一緒か

### TestCase
見落としがちな値 0
空文字, 負の値どれぐらい
0をどこで使ったらまずいか,
優先順位が正しく処理されているか
test_caseの名前も見えるようにするのもあり
基礎
コーナーケース
いろんなアルゴリズム調べる 再帰降下型parser 式をどういう形で書きたいのか？

コードに対して
0で割ったらまずい問題、数膨大案件→pythonバカでかい数input not a number 例外を投げる
関数の定義順はOK
tokenizeの順番 今回のケース
やってみないとわからない系のerror case, ぐちゃぐちゃ諦めは必要
記号連続はだめ連続したらだめなものabsの後にかっこがない
()とかに当てはまるやつ最初に簡易チェックする？残りの深いケース
helper function みたいなのをつかってそれを中で呼ぶのはいいかも どんなerrorを投げるか？stack traceも表示する
10文字目でplusが連続してる　どこで、なんで起きてる?
Errorが正しく起きるかもテストする TestError作ってエラーのTry catch catchの文面が一緒か
