#!/bin/sh
set -e

# コンテナ起動時に持っているSQLiteのデータベースファイルは、
# 後続処理でリストアに成功したら削除したいので、リネームしておく
if [ -f /backend/db.sqlite3 ]; then
  mv /backend/db.sqlite3 /backend/db.sqlite3.bk
fi

# Cloud Storage からリストア
litestream restore -if-replica-exists -config /etc/litestream.yml /backend/db.sqlite3

if [ -f /backend/db.sqlite3 ]; then
  # リストアに成功したら、リネームしていたファイルを削除
  echo "---- Restored from Cloud Storage ----"
  rm /backend/db.sqlite3.bk
else
  # 初回起動時にはレプリカが未作成であり、リストアに失敗するので、
  # その場合には、冒頭でリネームしたdbファイルを元の名前に戻す
  echo "---- Failed to restore from Cloud Storage ----"
  mv /backend/db.sqlite3.bk /backend/db.sqlite3
fi

# マイグレーションを実行
python manage.py migrate

# レプリケーションしながらDjangoを起動
exec litestream replicate -exec "python manage.py runserver 0.0.0.0:8080" -config /etc/litestream.yml