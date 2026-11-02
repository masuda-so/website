# リポジトリガイドライン

## プロジェクト構成とモジュールの配置

Ether合同会社の企業サイトを管理する Django プロジェクト（cookiecutter-django 由来）。公開サイトは `scripts/build_sites_static.py` が静的ファイルに書き出し、Cloudflare Workers の Static Assets として配信する。

- `manage.py`（管理コマンドの入口）、`config/`（`settings/{base,local,test,production}.py`、`urls.py`、`api.py`、ASGI / WSGI）。
- `website/`（アプリケーション: `users/`、`contrib/`、`templates/`、静的ソース）。`website/*/migrations/` の番号と公開 URL は互換性の境界で、見栄えのために変えない。
- `scripts/`（静的サイトの生成、ローカル `.env` の作成）、`tests/`（リポジトリ統合テスト）、`locale/`（gettext カタログ）、`docs/`（開発文書とデザインの出どころ）。
- `.envs/` は `*.example` だけを追跡する。`dist/client/` は生成物で Git に含めない。`wrangler.jsonc` が配信設定、`vercel.json` は旧ホスティングの設定で連携解除まで残す。

## ビルド・テスト・開発コマンド

- `uv sync --locked` — 依存関係の導入（Python 3.14、`pyproject.toml` と `uv.lock` が正本）。
- `uv run pytest` — テスト。CI は PostgreSQL を起こし `DATABASE_URL=postgres://postgres:postgres@localhost:5432/postgres` を渡す。
- `uv run pre-commit run --all-files` — ruff、django-upgrade、pyproject-fmt、基本チェック。`uv run mypy website config scripts tests` — 型チェック。`uv run python manage.py check --settings=config.settings.test` — 設定検査。
- `uv run python scripts/build_sites_static.py` — 静的サイトの生成（本番の認証情報は不要。31 ページと `sitemap.xml`、`robots.txt`、`_headers` を `dist/client/` に書く）。`npx wrangler dev` — Workers の配信をローカルで確認。

## コーディングスタイルと命名規則

- ruff で lint と整形（`pyproject.toml` の `[tool.ruff]`。マイグレーションと `staticfiles/` は除外）。djLint は `profile = "django"`、インデント 2、1 行 119 桁。`.editorconfig` が文字コード・改行・インデントを揃える。
- モジュールと関数は `snake_case`、クラスは `CapWords`。`models.py`、`urls.py`、`migrations/`、`templates/`、`static/` という Django が認識する名前を保つ。
- 生成した公開物や第三者の依存をアプリケーションのソースに写さない。

## テストの指針

- pytest（`config.settings.test`、`--reuse-db`、`--import-mode=importlib`）。ファイル名は `tests.py` または `test_*.py`。
- `tests/` はリポジトリ統合テスト（アプリ文書ページ、圧縮、メール設定、`.env` 結合）、`website/users/tests/` はユーザーモジュール。メール設定のテストは全バックエンドを接続せずに検証する。
- マイグレーションを変えたら `manage.py check` と pytest を通す。

## コミットとプルリクエストの指針

- コミットは git 公式ガイドの形: 1 行目は 50 文字以内を目安にした要約、空行、本文（何を・なぜ、72 桁前後で折り返す）、空行、トレーラー。作者は `masudaso <258961222+masuda-so@users.noreply.github.com>`、SSH 署名付き（ルールセットで署名必須）。
- 初回コミットだけ author と committer の日時をその日の `00:00:00 +0900` に揃える。2 回目以降は実際の日時。
- AI が内容を書いたコミットには、関わったエージェントごとに GitHub 公式書式のトレーラーを 1 行ずつ付ける: `Co-authored-by: Codex <noreply@openai.com>`、`Co-authored-by: Claude Fable 5.1 <noreply@anthropic.com>`（モデル名は作業したもの）。大文字小文字は公式どおり `Co-authored-by:`。
- 公開済みの履歴は書き換えない。やむを得ない場合は本人が判断し `--force-with-lease` を使う。
- main への変更は PR 経由（直接 push 不可）。PR の題名・説明・レビューコメントは日本語を基本とし、利用者が別の言語を指定した場合はそれを優先する。説明には変更内容と検証結果を書く。CI の `build (3.14)` が必須チェック。
- `README.md`（日本語）と `README.en.md`（英語）は冒頭で相互リンクし、5 見出し（概要・主な機能と制約・導入と使い方・サポートと関連資料・開発と貢献）を揃え、仕様・手順・制約の変更は同じ PR で両方を更新する。未実装・未検証の内容を利用可能と書かない。

## セキュリティと設定の注意

- 実際の認証情報やデプロイ設定を Git に含めない。必要なら `.envs/**/*.example` をコピーして未追跡のまま使う。Vercel・Cloudflare のトークンと本番 Django の認証情報も同様。
- 過去の履歴に入った値は漏えいしたものとして失効・更新する。
- 静的サイトのビルドは本番用の環境設定ファイルを必要としない。

## エージェント向けの指示

- 作業報告、Issue や PR へのコメントは日本語を基本とする。コード識別子、ファイル名、コマンド、ログやエラーの引用は原文のまま残し、説明を日本語で添える。
- 言語の統一を理由に既存のコミット履歴や他者のコメントを書き換えない。投稿・コミット・push の許可は別途の作業指示に従う。
