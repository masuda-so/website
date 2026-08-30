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
