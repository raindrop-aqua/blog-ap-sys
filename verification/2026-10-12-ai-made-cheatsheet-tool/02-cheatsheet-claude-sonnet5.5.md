# PostgreSQL 保守用チートシート(psql)

## 1. 接続方法

```bash
# 基本形
psql -h ホスト名 -p 5432 -U ユーザー名 -d データベース名

# 例
psql -h db.example.com -p 5432 -U postgres -d mydb

# 接続文字列(URI)で指定
psql "postgresql://ユーザー名@ホスト名:5432/データベース名"
```

### パスワードの扱い

- 接続時にプロンプトで入力する。
- 毎回の入力を避ける場合は `~/.pgpass` に記述する(権限は `chmod 600`)。
  - 書式: `ホスト:ポート:DB:ユーザー:パスワード`
- 環境変数でも指定できる: `PGHOST` / `PGPORT` / `PGUSER` / `PGDATABASE` / `PGPASSWORD`

### 注意

- 本番環境では、作業前に接続先(ホスト・DB名)を必ず確認する。
- 接続後は `\conninfo` で現在の接続先を確認できる。

---

## 2. よく使うメタコマンド(`\` で始まる)

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

---

## 3. 保守でよく使うSQL

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

### 実行中のクエリを止める

```sql
SELECT pg_cancel_backend(pid);     -- クエリのみ中断(穏やか)
SELECT pg_terminate_backend(pid);  -- 接続ごと強制終了
```

- 本番では、対象の `pid` と影響範囲を確認してから実行する。

---

## 4. 便利なコマンドラインオプション

```bash
psql -c "SELECT now();"   # 1コマンドだけ実行して終了
psql -f script.sql        # SQLファイルを実行
psql -X                   # ~/.psqlrc を読み込まない
```

---

## 5. 今後深めたいテーマ(メモ欄)

- [ ] バックアップ(`pg_dump` / `pg_basebackup`)
- [ ] VACUUM / autovacuum の運用
- [ ] スロークエリの調査
- [ ] 監視
- [ ] レプリケーション
