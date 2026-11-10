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

## Component system (Web series)

The site is built from stock [Bootstrap 5.3](https://getbootstrap.com/docs/5.3/)
components and utilities (checked 2026-11-10, version 5.3.8). This is the shared
rule for Ether's Web / Django repositories: structure and components are common,
and a product differs only in its tokens.

- `website/templates/base.html` loads Bootstrap's unmodified CSS and its JS
  bundle from the official jsDelivr build, pinned by version and SRI hash. The
  static build's Content-Security-Policy allows that one host for scripts and
  styles.
- `website/static/css/series-theme.css` is the shared theme. It maps the
  `--series-*` tokens onto Bootstrap's documented CSS variables (body, links,
  buttons, cards, navigation, list groups, forms, dark sections). Keep it
  identical across the series; change it in every repository together.
- `website/static/css/project.css` defines Ether's `--series-*` tokens (the
  identity values in the table above) and the few rules Bootstrap has no
  component for: the header that turns opaque on scroll, the headline tracking,
  the three-screen hero, the app screenshot frame, and the scroll reveal.
- Templates use Bootstrap's own parts: `navbar` + `collapse` for the header,
  the grid (`row` / `col-*`) for layout, `card` for apps and business areas,
  `btn` (pill) for actions and the filter, `nav-pills` for document tabs,
  `list-group` for support links, `alert` for warnings, `badge` for numbering,
  and `visually-hidden-focusable` for the skip link.
- Primary actions use `btn-dark`; the lime accent is `btn-primary` and is kept
  for the skip link and accents on dark sections. Do not add new component CSS
  when a Bootstrap component or utility already does the job.

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
