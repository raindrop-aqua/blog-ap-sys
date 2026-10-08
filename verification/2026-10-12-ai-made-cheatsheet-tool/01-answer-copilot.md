PostgreSQL の保守担当になったら、まずは psql で接続できること と 基本的な確認コマンドを覚えること が重要です。

1. psql で PostgreSQL に接続する
ローカル接続
psql -U postgres

-U : ユーザー名指定
postgres : PostgreSQL の管理ユーザー
データベースを指定して接続
psql -U postgres -d mydb

-d : データベース名
リモートサーバーへ接続
psql -h 192.168.1.100 -p 5432 -U postgres -d mydb

-h : 接続先ホスト
-p : ポート番号
-U : ユーザー名
-d : データベース名
接続文字列形式
psql "host=192.168.1.100 port=5432 dbname=mydb user=postgres"

パスワードを聞かれずに接続

環境変数を利用

export PGPASSWORD='password'
psql -h localhost -U postgres -d mydb


本番環境では .pgpass の利用が一般的です。

2. 接続後によく使う psql メタコマンド

SQLではなく、psql専用コマンドです。

現在の接続情報
\conninfo


例

You are connected to database "mydb"
as user "postgres"

データベース一覧
\l


または

\list

データベース切り替え
\c mydb

テーブル一覧
\dt

ビュー一覧
\dv

スキーマ一覧
\dn

ユーザー一覧
\du

テーブル定義確認
\d table_name


例

\d users

テーブル詳細表示
\d+ users


表示内容

カラム
インデックス
サイズ
コメント

など

3. SQLでよく使う確認コマンド
PostgreSQL バージョン
SELECT version();

現在のDB名
SELECT current_database();

現在のユーザー
SELECT current_user;

現在時刻
SELECT now();

接続セッション確認
SELECT * FROM pg_stat_activity;


保守作業では非常によく使います。

4. テーブルサイズ確認
テーブルサイズ
SELECT
    pg_size_pretty(pg_relation_size('users'));

大きいテーブルを調べる
SELECT
    relname,
    pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

5. インデックス確認
\d users


または

SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename = 'users';

6. ロック確認

障害対応で頻出です。

SELECT *
FROM pg_locks;


実際によく使うのは

SELECT
    pid,
    usename,
    state,
    query
FROM pg_stat_activity;


です。

7. 実行計画確認

SQLチューニングの基本です。

EXPLAIN
SELECT * FROM users;


実際に実行して確認

EXPLAIN ANALYZE
SELECT * FROM users;

8. VACUUM と ANALYZE

保守担当なら必須知識です。

統計情報更新
ANALYZE users;

不要領域回収
VACUUM users;

両方実施
VACUUM ANALYZE users;

9. psql終了
\q

保守担当になったら最初に覚えたい「鉄板コマンド」
\conninfo
\l
\dt
\d テーブル名

SELECT version();
SELECT current_database();
SELECT current_user();

SELECT * FROM pg_stat_activity;

EXPLAIN ANALYZE ...
VACUUM ANALYZE テーブル名;


このあたりを使いこなせれば、日常的な PostgreSQL の運用・保守業務の 7〜8割は対応できるようになります。特に \dt、\d テーブル名、pg_stat_activity、EXPLAIN ANALYZE は現場で頻繁に使われます。