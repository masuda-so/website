# Ether website

[日本語](README.md) | [English](README.en.md)

## 概要

Etherの企業サイトと、Grace・Still・Ukiyo・Vault・Weaveの製品情報を管理します。Djangoがページとローカルアプリケーションを提供し、静的書き出しによって、日英のプライバシーポリシー・利用規約・サポートページを含む公開サイトを生成します。

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

ライセンス：MIT

## 主な機能と制約

Djangoによるアプリケーションと静的な公開サイトを管理します。製品別のプライバシー・利用規約・サポートページは日英に対応しています。Django本番運用と静的公開では必要な設定が異なります。

## 導入と使い方

### 設定

[Cookiecutter Djangoの設定ガイド](https://cookiecutter-django.readthedocs.io/en/latest/1-getting-started/settings.html)を参照してください。

データベースは`DATABASE_URL`、または`POSTGRES_DB`・`POSTGRES_USER`・`POSTGRES_PASSWORD`(必要に応じて`POSTGRES_HOST`・`POSTGRES_PORT`)で指定します。pytestとmypyの実行にも必要です。

### 基本的なコマンド

#### ユーザーの作成

- **通常のアカウント**は、Sign Upのフォームから作成します。送信後の「Verify Your E-mail Address」画面では、コンソールに出力される確認メールのリンクをブラウザで開き、メールアドレスを確認します。
- **管理者アカウント**は次のコマンドで作成します。

      uv run python manage.py createsuperuser

通常ユーザーをChrome、管理者をFirefoxなど別のブラウザでログインさせると、両方の動作を比較できます。

#### 型チェック

mypyによる型チェック：

    uv run mypy website

#### テストカバレッジ

テストを実行し、カバレッジとHTMLレポートを確認します。

    uv run coverage run -m pytest
    uv run coverage html
    uv run open htmlcov/index.html

##### pytestによるテスト

    uv run pytest

#### Lintとテンプレート整形

push前にリポジトリのフックを実行します。

    uv run pre-commit run --all-files

整形でファイルが変わった場合は差分を確認し、コミット前に再実行してください。フックのバージョンは`.pre-commit-config.yaml`で固定され、`pyproject.toml`と`uv.lock`の開発依存関係とは別に管理されています。現在のバージョンは各設定ファイルで確認してください。DjangoプロファイルとJavaScript整形の設定は`pyproject.toml`の`[tool.djlint]`にあります。

`website/templates/base.html`のSpeed Insights初期化処理は、Vercelの[HTML向け手順](https://vercel.com/docs/speed-insights/quickstart)に沿い、遅延読み込みのスクリプトが動く前に`window.si` / `window.siq`へ呼び出しを蓄積します。インラインJavaScriptの整形はdjLintに任せてください。空白の変更ではキューの動作は変わりません。`/_vercel/speed-insights/script.js`はVercelが提供するパスで、ローカルのDjango開発サーバーが提供するものではありません。

### デプロイ

実際の認証情報やデプロイ設定をGitに含めないでください。ローカルファイルが必要な場合は、追跡済みのサンプルをコピーします。

    cp .envs/.local/.django.example .envs/.local/.django
    cp .envs/.local/.postgres.example .envs/.local/.postgres

Djangoを本番運用する場合は、`.envs/.production/*.example`の変数をホスティング先の暗号化された環境変数・シークレット管理から設定します。ローカルに本番設定ファイルが必要な場合もサンプルをコピーし、生成したファイルはGitの追跡対象外に保ちます。

    cp .envs/.production/.django.example .envs/.production/.django
    cp .envs/.production/.postgres.example .envs/.production/.postgres

サンプルの仮の値を流用せず、環境ごとに固有の認証情報を作成してください。過去のGit履歴に含まれた値は漏えいしたものとして、該当サービスで失効または更新してください。対処後も履歴からの削除が必要な場合は、GitHubの[機密データ削除手順](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)に従います。

静的な企業サイトのビルドには、本番Djangoの環境設定ファイルは不要です。

    uv run python scripts/build_sites_static.py

静的サイトには、Weave・Vault・Ukiyo・Grace・Stillの未ログインで閲覧できるページを含みます。パスは`/apps/<app>/privacy/`、`/apps/<app>/terms/`、`/apps/<app>/support/`です。日本語版は`/ja/`の下に同じパスを配置します。

Vercelは`main`から静的サイトをビルドし、`dist/client`を本番公開します。他のブランチへのpushやPRではPreviewデプロイを作成します。ビルド設定は`vercel.json`で管理し、Vercelのトークンや本番Djangoの認証情報はGitに含めません。

Djangoアプリケーション全体を起動する場合は、本番用サンプルの変数に加え、`DATABASE_URL`を設定してください。

## サポートと関連資料

### リポジトリ構成

ソースの管理範囲、命名、生成ファイル、検証については[docs/structure.md](docs/structure.md)を参照してください。Djangoの設定は`config/`、アプリのコードとテンプレートは`website/`、補助ツールは`scripts/`にあります。

### デザインの参照元

公開サイトの製品紹介、維持しているブランド設定、素材の出典は[docs/DESIGN.md](docs/DESIGN.md)に記載しています。

## 開発と貢献

製品の問い合わせには上記のサポートページを使用してください。リポジトリを変更する場合は構成・デザインの資料を確認し、変更内容と検証結果をPRに記載してください。PRの説明とレビューコメントは日本語を基本とします。利用者が別の言語を指定した場合は、その指定を優先します。

作業時の共通方針は[AGENTS.md](AGENTS.md)を参照してください。
