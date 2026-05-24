# Task2
木構造を使えば O(log N)、ハッシュテーブルを使えばほぼ O(1) で検索・追加・削除を実現することができて、これだけ見ればハッシュテーブルのほうが優れているように見える。ところが現実の大規模なデータベースでは、ハッシュテーブルではなく木構造が使われることが多い。その理由を考えよ。
いくつか重要な理由があるので思いつくだけ書いてください！

hashテーブルでは要素数以上のメモリを使用する
要素が入ってないhashテーブルの部分が無駄になるため、無駄が多い
再hashするタイミングでレイテンシが高くなる
検索を行う際に木構造であれば近くのものを持ってくるだけでよい
バランス木に調整するほうが再hash化より負荷が小さい
hash関数の設計が難しい(現実のサービスではhash値の衝突が起こりやすい)

### 挑戦クイズ
つねに O(1) で検索・追加・削除できるデータ構造はあるか？🤔
「ない」という答えでも OK です
調べるより考えて！
わかった人は haraken まで Slack で DM ください

そらさんが言っていたように制限があるか質問中

## Task3
hashtableに入れるItemにolder, newerのkeyを入れておく
globalにoldest, newestを持っておく
targetのolderはあるがnewerは無いので

tableにないばあい
buckets内のnewestのolderをtargetにする, target.olderをnewestにしてnewest=target
buckets内のoldestのnewerをoldestにする, oldestを削除

tableにある場合
newestの場合, 何も変更無し

oldestの場合, tableにない場合と同じ挙動
その他の場合 targetをnewestにする+前後を修正する必要がある。removeしてnewerに入れればいいだけ
target.newer.older = target.older
target.older.newer = target.newer
newest.newerをtargetにする
target.older = newest
newestのnewerとnewestをtargetにする

新しいものを入れた時size()がX以下の場合はoldest削除しなくてもいい

====

消す
targetを消す
oldestを消す

要素数がすでにXの場合 or targetがすでにある場合削除
newestを消す場合は無い
oldestを消す→ oldestを削除 oldest = oldest.newer
targetを消す→ target.newer.older = target.older, target.older.newer = target.newer
(target消した時の前後関係を管理したり、oldestを記憶するためにolderもnewerも必要)

入れる(size >= xならば削除したらいい)
oldestの更新は必要ない
newest.newer = target, target.older = newest,  newest = target

動きをよく見ていたら、oldestを削除する、またはtargetを削除する+新しいものを追加する


それ以外
課題3 大きさXのhashmapを使用する。valueにはItemsを持ち、next, newer, olderを持つように
globalとしてoldest, newestを持つようにする