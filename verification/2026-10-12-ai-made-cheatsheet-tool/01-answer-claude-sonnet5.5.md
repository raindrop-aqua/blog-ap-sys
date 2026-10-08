DB保守のご担当、お疲れさまです。psqlは基本さえ押さえれば日々の作業がぐっと楽になります。

## 接続方法

```bash
# 基本形
psql -h ホスト名 -p 5432 -U ユーザー名 -d データベース名

# 例
psql -h db.example.com -p 5432 -U postgres -d mydb

# 接続文字列(URI)で指定
psql "postgresql://ユーザー名@ホスト名:5432/データベース名"
```

- パスワードは接続時に聞かれます。毎回の入力を避けたい場合は、`~/.pgpass`(権限は `chmod 600`)に `ホスト:ポート:DB:ユーザー:パスワード` の形式で書いておけます。
- 環境変数(`PGHOST`、`PGUSER`、`PGDATABASE` など)でも指定できます。
- 本番環境では、うっかり操作を防ぐため、接続先を必ず確認してから作業するのがおすすめです。

## よく使うメタコマンド(`\` で始まるもの)

| コマンド | 内容 |
|---|---|
| `\?` | メタコマンドの一覧 |
| `\h CREATE TABLE` | SQL文のヘルプ |
| `\l` | データベース一覧 |
| `\c DB名` | 別のDBに接続し直す |
| `\dt` | テーブル一覧 |
| `\d テーブル名` | テーブル定義(列・インデックス・制約) |
| `\d+ テーブル名` | 上記の詳細版(サイズ等も) |
| `\di` | インデックス一覧 |
| `\dv` | ビュー一覧 |
| `\dn` | スキーマ一覧 |
| `\du` | ロール(ユーザー)一覧 |
| `\dx` | 拡張機能の一覧 |
| `\conninfo` | 現在の接続情報 |
| `\x` | 縦表示の切り替え(列が多い結果が見やすい) |
| `\timing` | クエリの実行時間を表示 |
| `\e` | エディタでSQLを編集 |
| `\i ファイル名` | SQLファイルを実行 |
| `\o ファイル名` | 結果をファイルに出力 |
| `\q` | 終了 |

## 保守でよく使うSQL

```sql
-- DBのサイズ
SELECT pg_size_pretty(pg_database_size('mydb'));

-- テーブルごとのサイズ(上位10件)
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC LIMIT 10;

-- 接続中のセッションと実行中のクエリ
SELECT pid, usename, state, query_start, query
FROM pg_stat_activity;

-- VACUUM / ANALYZE
VACUUM (VERBOSE, ANALYZE) テーブル名;
```

## 便利なオプション

```bash
psql -c "SELECT now();"        # 1コマンドだけ実行
psql -f script.sql             # ファイルを実行
psql -X                        # 設定ファイル(~/.psqlrc)を読まない
```

## 補足

- 実行中のクエリを止める場合は `pg_cancel_backend(pid)`(穏やか)や `pg_terminate_backend(pid)`(強制)を使いますが、本番では影響範囲を確認してからにしてください。
- バックアップ(`pg_dump` / `pg_basebackup`)や監視、レプリケーションは、また別の重要テーマです。

保守担当として、次に何を深めたいでしょうか。バックアップ・VACUUMの運用・スロークエリの調査など、状況に合わせて一緒に整理していけます。