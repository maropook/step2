# Cache documentation
## Cache
hashmapを使用する, page_url, webページ, next(next_url), prev(older_url)をvalueに持たせる
globalにnewest_url, oldest_urlをもたせる

### access_page(url, contents)
url == newestの場合は何も更新せず終了
urlがすでにcacheにある場合は一旦削除, ない場合でsizeがlimitと等しい場合はoldestを削除
url情報からPageを作成しhash_tableに追加
元newestのnextをurlに更新
newest_urlをurlに更新

### get_pages -> List<str>
newest_urlをクエリとしてpageを取得
page.nextをさらにクエリとしてpageを取得をoldest_urlに一致するまで回すことで新しい順にPage情報を取得

### remove_oldest
oldest_urlをoldest pageのnextに更新

### remove_target_if_exist -> bool
urlがすでにcacheにないばあいはFalse
ある場合かつoldestの場合はremove_oldestを呼び出す
それ以外の場合は、target情報を取り出し、Pageに持たせた前後関係を解決する
target.prevのnextをtarget.nextに更新
target.nextのprevをtarget.prevに更新
targetをhash_tableから削除しTrueを返す

