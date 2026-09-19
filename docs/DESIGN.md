# Ether website design

## Purpose

Help visitors understand Ether's five iOS apps, choose an app, reach its App Store
page, and find support. Preserve the existing Ether identity while making the
products themselves the main visual evidence.

## References inspected before implementation

- User-supplied method: [Masahiro Chaen's X post](https://x.com/masahirochaen/status/2099504707706454381)
  (checked 2026-09-16). The linked discussion describes turning a reference site's
  design information into reusable written guidance. It is a method reference,
  not an instruction to reproduce the post author's brand or a specific site.
- Primary product reference: [Apps by Apple](https://www.apple.com/apps/)
  (checked 2026-09-16). Its app catalog repeats an app name, concise purpose,
  product imagery, and a direct action. Ether adopts that information pattern;
  Apple assets, wording, claims, and brand typography are not copied.
- Secondary extraction: [Refero's Apple style](https://styles.refero.design/style/aecac5da-f397-4ddf-b71f-de1efc434cb8).
  The extracted hierarchy, consistent spacing, readable body text, and restrained
  decoration are useful comparison points. Refero is an independent description,
  not an Apple specification or a set of mandatory rules.
- Accessibility: [W3C WAI page headings](https://www.w3.org/WAI/tutorials/page-structure/headings/).
  Use one page heading, then section and app headings that describe the content.
  Keep the existing keyboard navigation, skip link, visible focus, and reduced
  motion behavior.

## Existing identity retained

| Role | Value | Use |
| --- | --- | --- |
| Paper | `#f3f0e8` | Main surface and app-card surface |
| Ink | `#17211b` | Text and company information |
| Lime | `#c7f34a` | Existing focus/menu/brand accents |
| Coral on light | `#b43a22` | Accented headings and categories |
| Body type | DM Sans / Noto Sans JP / sans-serif | Existing Latin/Japanese pairing |
| Company mark | `images/favicons/ether.svg` | Existing Ether organization avatar |

These are Ether's existing project values, not values prescribed by Apple.
The provenance and license of the company mark remain in `THIRD_PARTY_NOTICES.md`.

## Shared presentation

- Order: Grace, Vault, Ukiyo, Still, Weave, matching the store workstream.
- Each product has the same screenshot/category/name/tagline/description/store/support
  structure. The visible action wording is the same, with an app-specific
  accessible name.
- Main copy is 16–17 px with generous Japanese line spacing; longer headings use
  responsive sizes. Repeated gaps and padding use 4 px increments.
- Desktop sections use 96 px vertical padding; smaller screens preserve the
  existing responsive section behavior. App cards use 32 px padding (28 px on
  narrow screens), 24 px gaps and corners.
- Product images show actual app screens. Images keep their native aspect ratio;
  do not crop away controls, rebuild UI in CSS, or invent features.
- The hero places three real app screens beside the existing company statement.
  The decorative CSS circles and imitation business artwork are removed.
- Product links lead to the existing App Store URLs. Support links use the
  existing Japanese support routes. The Japanese home page remains `/`.
- Grace is the featured app (ETH-2, 2026-09-19). The home hero carries the
  official "Download on the App Store" badge once per page, linked to the
  Japanese storefront, plus a link to the product page at `/ja/apps/grace/`
  (English: `/apps/grace/`). The Grace card links to the same product page.
- Product-page copy mirrors the App Store listing draft (ETH-5) and the app's
  own Japanese UI terms (記録, 実績, 連続記録, 振り返り, デイリーパス/月額/年額).
  Claims must not exceed the shipped app; prices are left to the App Store.
  Japanese pages link to `apps.apple.com/jp`; English pages use the
  storefront-neutral `apps.apple.com/app/...` URL.
- Badge rules follow the App Store Marketing Guidelines
  (https://developer.apple.com/app-store/marketing/guidelines/): black badge,
  unmodified, 48 px tall (minimum 40 px), clear space of one-quarter its
  height, one badge per layout, and an Apple trademark credit line once per
  page in the footer.
- Current work is described separately from fields listed in the articles of
  incorporation. There are no invented clients, sales, growth rates, awards, or
  production AI-organization claims.

## Assets and publication boundaries

App screens are copied from the 2026-09-16 simulator capture workstream. They
contain fictional demonstration records and use 9:41, full battery, and consistent
signal status. The capture applications use isolated in-memory data, while the
production repositories are unchanged. The website copies retain the original
JPEG pixels; CSS scales them for display. The capture manifests in the task
workspace preserve the source commits and fixture changes.

Grace's and Ukiyo's sample photographs come from the app's Apple-derived sample
assets. Their notices are retained in `THIRD_PARTY_NOTICES.md` when those screens
are distributed on the site.

Build with `scripts/build_sites_static.py`; validate the generated home page and
all 30 existing app document routes. Preview at desktop and mobile widths before
publishing. Production publication is the separate Git/Vercel deployment step,
not implied by a successful local build.
