# Third-Party Notices

## Bootstrap

Source: https://github.com/twbs/bootstrap

The site loads Bootstrap 5.3.8 (`bootstrap.min.css` and
`bootstrap.bundle.min.js`, which includes Popper) unmodified from the official
jsDelivr build referenced in `website/templates/base.html`. The files are not
copied into this repository. `website/static/css/series-theme.css` sets
Bootstrap's documented CSS variables and contains no Bootstrap source.

The MIT License (MIT)

Copyright (c) 2011-2025 The Bootstrap Authors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


## Ether organization avatar (Paperclip)

Source: https://github.com/paperclipai/paperclip

Captured from the local Paperclip 2026.831.1 organization avatar on 2026-09-15.
The original 44 x 44 generated PNG background for the existing company name
is embedded unchanged in `website/static/images/favicons/ether.svg`.
The rounded clipping, white E, weight, proportions and shadow follow the
rendered sidebar avatar. SVG text uses the viewer's system font when Inter is
unavailable; this is a web adaptation of the organization avatar, not the
Paperclip product logo.

Paperclip license:

```text
MIT License

Copyright (c) 2025 Paperclip AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```

The PNG favicons (16/32), Apple touch icon (180), and ICO (16/32/48)
are rendered from the same SVG using sharp 0.35.4.
Reference: https://sharp.pixelplumbing.com/api-output/#png

## App screenshots and Apple tutorial sample photographs

`website/static/images/apps` contains screenshots captured from Ether's apps on
2026-09-16. The records and captions are fictional demonstration data. No
production customer data is included.

The photographs visible in Grace's and Ukiyo's screenshots are the `Samples` assets
from Apple's Grateful Moments tutorial, already distributed with Grace. Source:
https://developer.apple.com/tutorials/develop-in-swift/collect-model-and-store-data

The website's own text, layout, and CSS do not copy Apple's website source.
Reference links describe inspiration and do not imply endorsement.

The tutorial archive license is reproduced here:

```text
Copyright © 2021 Apple Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```


## AGENTS.md

The title and section outline of `AGENTS.md` follow the outline that OpenAI
Codex uses when it generates an `AGENTS.md` with its `/init` command
([openai/codex](https://github.com/openai/codex/blob/6478a751fde8884b2fdc76486fe23175a8e795d4/codex-rs/tui/assets/prompt_for_init_command.md),
`codex-rs/tui/assets/prompt_for_init_command.md`, commit `6478a751fde8`,
2026-08-29, Apache-2.0). The headings are translated into Japanese; the contents
are this repository's own.
