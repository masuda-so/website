from __future__ import annotations

from dataclasses import dataclass

from django.http import Http404
from django.urls import reverse
from django.utils import translation
from django.views.generic import TemplateView


@dataclass(frozen=True, slots=True)
class AppRecord:
    slug: str
    name: str
    summary: str
    summary_ja: str
    stored_content: str
    stored_content_ja: str
    sensitive_content: str
    sensitive_content_ja: str
    uses_photos: bool
    issue_url: str


APP_RECORDS = {
    "weave": AppRecord(
        slug="weave",
        name="Weave",
        summary=(
            "A private, local-first writing workspace for drafts and "
            "on-device assistance."
        ),
        summary_ja=(
            "下書きとデバイス上のアシスタントのための、プライベートで"
            "ローカルファーストな文章作成スペースです。"
        ),
        stored_content="draft titles, text, and dates",
        stored_content_ja="下書きのタイトル、本文、日付",
        sensitive_content=(
            "private drafts, messages, payment information, or other sensitive data"
        ),
        sensitive_content_ja=(
            "非公開の下書き、メッセージ、支払い情報、その他の機密情報"
        ),
        uses_photos=False,
        issue_url="https://github.com/masuda-so/weave/issues",
    ),
    "vault": AppRecord(
        slug="vault",
        name="Vault",
        summary=(
            "A private, local-first notebook with search and on-device assistance."
        ),
        summary_ja=(
            "検索とデバイス上のアシスタントを備えた、プライベートで"
            "ローカルファーストなノートです。"
        ),
        stored_content="note titles, text, and dates",
        stored_content_ja="ノートのタイトル、本文、日付",
        sensitive_content="private notes, payment information, or other sensitive data",
        sensitive_content_ja="非公開のノート、支払い情報、その他の機密情報",
        uses_photos=False,
        issue_url="https://github.com/masuda-so/vault/issues",
    ),
    "ukiyo": AppRecord(
        slug="ukiyo",
        name="Ukiyo",
        summary=(
            "A private, local-first visual journal for selected images and captions."
        ),
        summary_ja=(
            "選択した画像とキャプションのための、プライベートで"
            "ローカルファーストなビジュアルジャーナルです。"
        ),
        stored_content="captions, dates, and prepared copies of selected images",
        stored_content_ja="キャプション、日付、選択した画像から作成したコピー",
        sensitive_content=(
            "private photos, captions, payment information, or other sensitive data"
        ),
        sensitive_content_ja=(
            "非公開の写真、キャプション、支払い情報、その他の機密情報"
        ),
        uses_photos=True,
        issue_url="https://github.com/masuda-so/ukiyo/issues",
    ),
    "grace": AppRecord(
        slug="grace",
        name="Grace",
        summary=(
            "A private, local-first gratitude journal for meaningful notes and "
            "selected photos."
        ),
        summary_ja=(
            "大切な記録と選択した写真のための、プライベートで"
            "ローカルファーストな感謝ジャーナルです。"
        ),
        stored_content=(
            "moment titles, notes, dates, prepared images, badges, and relationships"
        ),
        stored_content_ja=(
            "瞬間のタイトル、メモ、日付、加工済み画像、バッジ、関連情報"
        ),
        sensitive_content=(
            "private journal content, photos, payment information, or other "
            "sensitive data"
        ),
        sensitive_content_ja=(
            "非公開のジャーナル内容、写真、支払い情報、その他の機密情報"
        ),
        uses_photos=True,
        issue_url="https://github.com/masuda-so/grace/issues",
    ),
    "still": AppRecord(
        slug="still",
        name="Still",
        summary=(
            "A private, local-first space for short pauses and on-device guidance."
        ),
        summary_ja=(
            "短い一時停止とデバイス上のガイドのための、プライベートで"
            "ローカルファーストなスペースです。"
        ),
        stored_content="completed pause start times, end times, and durations",
        stored_content_ja="完了した一時停止の開始日時、終了日時、継続時間",
        sensitive_content=(
            "private reflections, payment information, or other sensitive data"
        ),
        sensitive_content_ja="非公開の内省、支払い情報、その他の機密情報",
        uses_photos=False,
        issue_url="https://github.com/masuda-so/still/issues",
    ),
}


@dataclass(frozen=True, slots=True)
class ProductCopy:
    """Localized product-page text. Every claim must match the shipped app."""

    store_name: str
    subtitle: str
    lead: str
    features: tuple[str, ...]
    pro_heading: str
    pro_paragraphs: tuple[str, ...]
    privacy_heading: str
    privacy_paragraphs: tuple[str, ...]
    availability: str
    meta_description: str


@dataclass(frozen=True, slots=True)
class ProductRecord:
    """A dedicated product page for one app. Only flagship apps have one."""

    slug: str
    # Japanese pages link to the Japanese storefront; English pages use the
    # storefront-neutral URL, which the App Store resolves to the visitor's own
    # storefront.
    app_store_url_ja: str
    app_store_url: str
    screenshot: str
    screenshot_alt: str
    screenshot_alt_ja: str
    copy: ProductCopy
    copy_ja: ProductCopy


# Copy mirrors the App Store listing draft for Grace (ETH-5) and the shipped
# app's own UI terms: 記録 (Moments), 実績 (Achievements), 連続記録 (Streak),
# 振り返り (Reflection), デイリーパス / 月額 / 年額, 購入を復元. Prices are left to
# the App Store so the page never contradicts the storefront.
GRACE_APP_STORE_URL_JA = (
    "https://apps.apple.com/jp/app/grace-gratitude-journal/id6807439542"
)
GRACE_APP_STORE_URL = "https://apps.apple.com/app/grace-gratitude-journal/id6807439542"

PRODUCT_RECORDS = {
    "grace": ProductRecord(
        slug="grace",
        app_store_url_ja=GRACE_APP_STORE_URL_JA,
        app_store_url=GRACE_APP_STORE_URL,
        screenshot="images/apps/grace.jpg",
        screenshot_alt="Grace timeline showing gratitude moments with photos",
        screenshot_alt_ja="写真つきの感謝の記録が並ぶGraceのタイムライン画面",
        copy=ProductCopy(
            store_name="Grace: Gratitude Journal",
            subtitle="Private gratitude journal",
            lead=(
                "Grace is a private, local-first gratitude journal for meaningful "
                "notes and selected photos. Your journal stays on your device."
            ),
            features=(
                "Capture moments with a title, note, date, and optional photo",
                "Revisit entries in a visual hexagon timeline",
                "Earn badges and keep gentle daily streaks",
                "Delete any saved moment when you choose",
                "No account, ads, analytics, or automatic uploads",
            ),
            pro_heading="Grace Pro (optional)",
            pro_paragraphs=(
                "The free journal is fully usable without a purchase. Grace Pro adds "
                "an on-device assistant powered by Apple’s Foundation Models. Ask it "
                "for help and it prepares an editable title, note, and date for a "
                "new moment; nothing is saved until you review it and choose "
                "Save Moment.",
                "Pro is offered as a 24-hour Daily Pass (one-time, does not renew) "
                "or as a Monthly or Yearly auto-renewing subscription. Pro plans can "
                "be purchased only when the on-device assistant is available: iOS 26 "
                "or later, a device that supports Apple Intelligence with Apple "
                "Intelligence turned on, and a supported language. Current prices "
                "are shown on the App Store.",
            ),
            privacy_heading="Privacy",
            privacy_paragraphs=(
                "Moments and photos are stored on your device. Photos are selected "
                "through Apple’s system picker; Grace never requests full "
                "photo-library access.",
                "Grace is not medical, mental-health, emergency, or professional "
                "advice.",
            ),
            availability=(
                "Free with in-app purchases. Requires iOS 18 or iPadOS 18 or later on "
                "iPhone or iPad. Available in English and Japanese."
            ),
            meta_description=(
                "Grace is a private, local-first gratitude journal for meaningful "
                "notes and selected photos. Free on the App Store; Grace Pro adds an "
                "on-device assistant on Apple Intelligence devices."
            ),
        ),
        copy_ja=ProductCopy(
            store_name="Grace: 感謝日記",
            subtitle="端末だけで書く、写真つき感謝日記",
            lead=(
                "Graceは、心に残った出来事をメモと写真で残す、プライベートな感謝日記です。"
                "データは端末内にだけ保存されます。"
            ),
            features=(
                "タイトル・メモ・日付・写真（任意）で「記録」を残す",
                "六角形のタイムラインで記録を見返す",
                "バッジの獲得と連続記録（ストリーク）で習慣づけ",
                "記録はいつでも削除できます",
                "アカウント登録、広告、分析、自動アップロードなし",
            ),
            pro_heading="Grace Pro（任意）",
            pro_paragraphs=(
                "日記の機能は購入しなくてもすべて使えます。Grace Proでは、"
                "AppleのFoundation Modelsによる端末内アシスタントが使えます。"
                "頼むと、新しい記録のタイトル・メモ・日付の候補を用意します。"
                "内容を確認して「記録を保存」を選ぶまで、日記には何も保存されません。",
                "Proは、24時間だけ使えるデイリーパス（買い切り、自動更新なし）、"
                "または月額・年額の自動更新サブスクリプションから選べます。"
                "Proプランは端末内アシスタントが利用できる場合にのみ購入できます"
                "（iOS 26以降、Apple Intelligence対応端末でApple Intelligenceがオン、"
                "対応言語であること）。価格はApp Storeに表示されます。",
            ),
            privacy_heading="プライバシー",
            privacy_paragraphs=(
                "記録と写真は端末内に保存されます。写真はAppleの標準ピッカーで選択し、"
                "写真ライブラリ全体へのアクセスは求めません。",
                "Graceは医療・メンタルヘルス・緊急時・専門家の助言に代わるものではありません。",
            ),
            availability=(
                "無料（アプリ内課金あり）。iPhone・iPad（iOS・iPadOS 18以降）に対応。"
                "日本語と英語に対応しています。"
            ),
            meta_description=(
                "Graceは、心に残った出来事をメモと写真で残す、プライベートな感謝日記です。"
                "App Storeで無料。Grace Proは、Apple Intelligence対応端末で"
                "端末内アシスタントを追加します。"
            ),
        ),
    ),
}

DOCUMENT_LABELS = {
    "privacy": "Privacy Policy",
    "terms": "Terms of Use",
    "support": "Support",
}

DOCUMENT_LABELS_JA = {
    "privacy": "プライバシーポリシー",
    "terms": "利用規約",
    "support": "サポート",
}


class AppDocumentView(TemplateView):
    template_name = "pages/app_document.html"

    def get_context_data(self, **kwargs: str):
        context = super().get_context_data(**kwargs)
        app_slug = kwargs["app_slug"]
        document = kwargs["document"]
        try:
            app = APP_RECORDS[app_slug]
            is_japanese = (translation.get_language() or "en").startswith("ja")
            document_label = (DOCUMENT_LABELS_JA if is_japanese else DOCUMENT_LABELS)[
                document
            ]
        except KeyError as exc:
            message = "App document not found"
            raise Http404(message) from exc

        language_code = "ja" if is_japanese else "en"
        app_summary = app.summary_ja if is_japanese else app.summary
        stored_content = app.stored_content_ja if is_japanese else app.stored_content
        sensitive_content = (
            app.sensitive_content_ja if is_japanese else app.sensitive_content
        )

        url_kwargs = {"app_slug": app.slug, "document": document}
        with translation.override("en"):
            english_path = reverse("app-document", kwargs=url_kwargs)
        with translation.override("ja"):
            japanese_path = reverse("app-document", kwargs=url_kwargs)

        canonical_path = japanese_path if is_japanese else english_path
        punctuation = "。" if is_japanese else "."
        context.update(
            app=app,
            app_summary=app_summary,
            stored_content=stored_content,
            sensitive_content=sensitive_content,
            document=document,
            document_label=document_label,
            language_code=language_code,
            is_japanese=is_japanese,
            english_url=english_path,
            japanese_url=japanese_path,
            alternate_language_url=(english_path if is_japanese else japanese_path),
            alternate_language_label=("English" if is_japanese else "日本語"),
            canonical_url=self.request.build_absolute_uri(canonical_path),
            english_absolute_url=self.request.build_absolute_uri(english_path),
            japanese_absolute_url=self.request.build_absolute_uri(japanese_path),
            page_title=f"{app.name} {document_label} | Ether LLC",
            meta_description=f"{app_summary} {document_label}{punctuation}",
            og_locale="ja_JP" if is_japanese else "en_US",
            documents_aria_label=(
                f"{app.name}の文書" if is_japanese else f"{app.name} documents"
            ),
            og_image_alt=(
                "アイデアを、価値へ。— Ether LLC / Tokyo"
                if is_japanese
                else "Turn ideas into value — Ether LLC / Tokyo"
            ),
        )
        return context


app_document_view = AppDocumentView.as_view()


class AppProductView(TemplateView):
    template_name = "pages/app_product.html"

    def get_context_data(self, **kwargs: str):
        context = super().get_context_data(**kwargs)
        app_slug = kwargs["app_slug"]
        try:
            app = APP_RECORDS[app_slug]
            product = PRODUCT_RECORDS[app_slug]
        except KeyError as exc:
            message = "App page not found"
            raise Http404(message) from exc

        is_japanese = (translation.get_language() or "en").startswith("ja")
        copy = product.copy_ja if is_japanese else product.copy

        url_kwargs = {"app_slug": app.slug}
        with translation.override("en"):
            english_path = reverse("app-page", kwargs=url_kwargs)
        with translation.override("ja"):
            japanese_path = reverse("app-page", kwargs=url_kwargs)
        canonical_path = japanese_path if is_japanese else english_path

        context.update(
            app=app,
            product=product,
            copy=copy,
            app_store_url=(
                product.app_store_url_ja if is_japanese else product.app_store_url
            ),
            is_japanese=is_japanese,
            screenshot_alt=(
                product.screenshot_alt_ja if is_japanese else product.screenshot_alt
            ),
            # Official Apple badge artwork, localized modifier, "App Store" in
            # English. See App Store Marketing Guidelines.
            badge_image=(
                "images/badges/app-store-badge-ja.svg"
                if is_japanese
                else "images/badges/app-store-badge-en.svg"
            ),
            badge_alt=(
                "App Storeでダウンロード"
                if is_japanese
                else "Download on the App Store"
            ),
            # Apple requires one credit line per page that uses its trademarks
            # (App Store Marketing Guidelines, Legal requirements).
            trademark_credit=(
                "Apple、Appleのロゴ、App Store、iPhone、iPad、Apple Intelligenceは、"
                "米国およびその他の国や地域で登録されたApple Inc.の商標です。"
                "IOSは、Ciscoの米国およびその他の国における商標または登録商標であり、"
                "ライセンスに基づき使用されています。"
                if is_japanese
                else "Apple, the Apple logo, App Store, iPhone, iPad, and Apple "
                "Intelligence are trademarks of Apple Inc., registered in the U.S. "
                "and other countries. IOS is a trademark or registered trademark of "
                "Cisco in the U.S. and other countries and is used under license."
            ),
            alternate_language_url=(english_path if is_japanese else japanese_path),
            alternate_language_label=("English" if is_japanese else "日本語"),
            canonical_url=self.request.build_absolute_uri(canonical_path),
            english_absolute_url=self.request.build_absolute_uri(english_path),
            japanese_absolute_url=self.request.build_absolute_uri(japanese_path),
            page_title=(
                f"{copy.store_name} | Ether合同会社"
                if is_japanese
                else f"{copy.store_name} | Ether LLC"
            ),
            meta_description=copy.meta_description,
            og_locale="ja_JP" if is_japanese else "en_US",
            og_image_alt=(
                "アイデアを、価値へ。— Ether LLC / Tokyo"
                if is_japanese
                else "Turn ideas into value — Ether LLC / Tokyo"
            ),
        )
        return context


app_product_view = AppProductView.as_view()
