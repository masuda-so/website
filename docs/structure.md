# Repository structure

This is a Django project with a static export for its public site. Retain Django's
module, template, translation, and migration conventions rather than adopting
an iOS or plugin directory layout.

| Location | Responsibility |
| --- | --- |
| `manage.py` | Django management entry point |
| `config/` | Settings, root URL configuration, ASGI, and WSGI |
| `website/` | Application modules, templates, and static source assets |
| `website/*/migrations/` | Versioned Django database migrations |
| `website/*/tests/`, `tests/` | Application tests and repository integration tests |
| `scripts/` | Static export and local environment-file utility |
| `docs/` | Development documentation and design provenance |
| `locale/` | Gettext catalogs with Django's prescribed locale layout |
| `.envs/` | Tracked examples; actual local credentials stay ignored |
| `dist/client/` | Generated public export, excluded from source control |
| `.github/workflows/` | Continuous integration and Claude Code automation |

## Naming and generated content

Use Python's `snake_case` for modules and functions and `CapWords` for classes.
Keep Django-recognized names such as `models.py`, `urls.py`, `migrations/`,
`templates/`, and `static/`. `config/` and `scripts/` are project choices, not
mandatory Django directory names. Existing migration numbers and resource URLs
are compatibility boundaries; do not rename them for cosmetic consistency.

`.editorconfig` controls encoding, newlines, and indentation. `pyproject.toml`
configures Ruff and djLint; `.pre-commit-config.yaml` pins the local development hooks.
The dependency contract is Python 3.14, `pyproject.toml`, and `uv.lock`.
Do not copy generated exports or third-party dependencies into application source.

## Verification

Run `uv sync --locked`, then the local development checks below. CI runs the
test suite only, as described in the Continuous integration section:

```sh
uv run pre-commit run --all-files
uv run pytest
uv run mypy website config scripts tests
uv run python manage.py check --settings=config.settings.test
uv run python scripts/build_sites_static.py
```

The full tests require PostgreSQL. Settings read the database from
`DATABASE_URL`, or from the `POSTGRES_*` variables when it is unset, as the
Cookiecutter Django template does; pytest and mypy need one of them. The static
export uses its own build settings and does not require production credentials.
Moving `scripts/merge_production_dotenvs.py` preserves its repository-relative
input and output locations; run it only when intentionally creating a local
`.env` from local production files. Its tests use temporary fixtures.

## Email configuration

The Django 6.1 `MAILERS` mapping selects SMTP in base settings, console output
locally, the in-memory backend in tests, and Amazon SES in production.
`DJANGO_EMAIL_BACKEND` remains the environment override for base/local settings;
it is not a deprecated Django setting. SMTP retains `localhost` and a five-second
timeout. Other backends receive their own options rather than SMTP-only values.

Administrator error notifications use `config.logging.ResilientAdminEmailHandler`
to report delivery failures to the console without obscuring the original error.
This replaces the old handler's implicit `fail_silently` behavior, which changes
when `MAILERS` is enabled. Ordinary account email still propagates delivery errors.
The mail settings tests instantiate every backend without connecting and verify
allauth messages with the in-memory outbox. Actual SES delivery remains a separate
deployment check.

- [Django mailer migration](https://docs.djangoproject.com/en/dev/howto/mailers-migration/)
- [Django MAILERS setting](https://docs.djangoproject.com/en/6.1/ref/settings/#mailers)

## Partial user updates

The user API uses `ModelSchema.Meta.fields_optional` and
`model_dump(exclude_unset=True)` for PATCH requests. Omitted values stay unchanged;
explicit nulls are rejected because these database fields are not nullable.
Model-derived length limits and the explicit field allowlist remain in effect.
Both routes normalize usernames and call Django's model validation before saving
only the supplied fields. Invalid or duplicate usernames return field-level 422
errors. A database transaction handles a username claimed between validation and
save without persisting the rest of the rejected update. Tests cover both routes,
Unicode names, concurrent changes, account isolation, and real CSRF checks.

- [Django Ninja partial updates](https://django-ninja.dev/guide/model-schema/#making-fields-optional)
- [Django model validation](https://docs.djangoproject.com/en/6.1/ref/models/instances/#validating-objects)
- [Django transactions](https://docs.djangoproject.com/en/6.1/topics/db/transactions/)

## Dependency security

The Amazon SES backend is used for outgoing mail. Install `django-anymail` and
`boto3` directly, following Anymail's documented installation alternative.
There is no inbound mail webhook or encrypted S3 receipt action in this project.
The `amazon-ses` extra in Anymail 15.2 also installs an unneeded inbound encryption
client whose `cryptography<49` constraint prevents security updates. Omitting
that unused extra retains SES sending and allows the patched cryptography
release without overriding any package's compatibility constraints.

The 2026-10-12 follow-up updated cryptography, sqlparse, urllib3, virtualenv, and
Werkzeug to their advisory-fixed releases in `uv.lock`; python-discovery also
changed to satisfy virtualenv's dependency requirements. SES request preparation
is tested against a stubbed boto3 client with network access prohibited.
No live email is sent by these tests. Re-run a dependency audit after lockfile
changes; a clean scan covers known advisories, not all possible vulnerabilities.

- [Anymail Amazon SES installation](https://anymail.dev/en/stable/esps/amazon_ses/#installation)
- [PyPA pip-audit](https://github.com/pypa/pip-audit)

## Compression compatibility

As of 2026-10-12, the latest release, django-compressor 4.6.0, still calls
`codecs.open()` to read CSS and JavaScript. Python 3.14 deprecates that function
and recommends `open()` and text I/O instead.

`config.compressors` overrides only the source reader through the `COMPRESSORS`
class mapping used by upstream's template tag. `Path.open()` uses the recommended
text I/O, with explicit encoding and `newline=""` to preserve existing line
endings. UTF-8 BOM removal, decoding failures, CSS/JS processing, storage selection,
and JavaScript `defer` handling are preserved. This is a project compatibility
adapter using an upstream configuration point, not an upstream-released fix or
a migration specifically prescribed by Compressor's documentation. It neither
suppresses warnings nor modifies the installed package.

`tests/test_compressors.py` treats deprecations as errors and covers source
encodings, BOMs, newlines, invalid/missing files, actual minified output, and
CSS/JS generation from the 404 and 500 pages. Output and Compressor's cached
backend are isolated per test so earlier requests cannot reuse stale URLs;
tests do not access Amazon S3. The public static export still deliberately
disables compression and copies the source assets.

The upstream changelog lists Django 6.1 support as unreleased. Successful project
tests do not establish upstream support for every Django 6.1 feature. When a
compatible release replaces `codecs.open()`, upgrade the lockfile, remove this
adapter and the `COMPRESSORS` override, then rerun the compression regression
tests and normal CI checks.

- [Django Compressor changelog](https://django-compressor.readthedocs.io/en/latest/changelog.html)
- [Python codecs.open deprecation](https://docs.python.org/3.14/library/codecs.html#codecs.open)
- [Upstream compressor class selection](https://github.com/django-compressor/django-compressor/blob/develop/compressor/templatetags/compress.py)

## Sources and attribution

See [DESIGN.md](DESIGN.md) for public-site design references and
[THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) for source attribution.
Cookiecutter Django is the project's template, not an official requirement that
unrelated templates or unused tooling remain in the product README.

- [Django project and application layout](https://docs.djangoproject.com/en/6.1/intro/tutorial01/)
- [Django application modules](https://docs.djangoproject.com/en/6.1/ref/applications/)
- [Python naming conventions](https://peps.python.org/pep-0008/#naming-conventions)
- [Ruff formatter and trailing-comma rule](https://docs.astral.sh/ruff/rules/missing-trailing-comma/)
- [Cookiecutter Django](https://github.com/cookiecutter/cookiecutter-django)

## Git workflow

Follow the [Git commit guidelines](https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project):
keep each commit focused on one logical change, including its necessary tests,
configuration, and documentation. Separate unrelated fixes, formatting, and
localization metadata. Use a concise imperative subject (aim for about 50
characters), a blank line, and a body explaining the problem and resulting
behavior, wrapped at about 72 characters. Run `git diff --check` and the relevant
checks before publishing; report any validation limits accurately.

Use the configured signing identity and verify signatures locally and on GitHub.
Preserve truthful authorship and timestamps. Add attribution, review, or sign-off
trailers only when their meaning is justified; they are not substitutes for a
cryptographic signature. Git's own submission-specific requirements do not
become mandatory rules for these repositories.

Before publishing substantial changes, preserve the previous branch tip and a
verified Git bundle; also save uncommitted files when applicable. Prefer
fast-forward updates and signed revert commits for rollback. Rewrite published
history only when explicitly authorized. Verify the remote commit IDs, content,
metadata, signatures, and available CI results after pushing.

- [Git bundle backups](https://git-scm.com/docs/git-bundle)
- [GitHub signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification)

## Continuous integration

`.github/workflows/ci.yml` uses GitHub's official
[django starter workflow](https://github.com/actions/starter-workflows/blob/e3c451d60f119b71caebf13c98ac45da6e15b4b7/ci/django.yml).
The recorded upstream revision is `e3c451d60f119b71caebf13c98ac45da6e15b4b7`.
Workflow templates are meant to be adapted ("Optionally, make additional
changes"), so the template's shape, names, and steps are kept and only what
this project needs is changed. Besides the two `$default-branch` placeholders,
which are replaced with `main`:

- The Python matrix is `"3.14"`, the version `pyproject.toml` requires
  (`requires-python = "==3.14.*"`). The template's 3.7 to 3.9 cannot install
  the project, and 3.7 is no longer offered on the runner. The version is
  quoted so YAML does not read it as a number.
- Dependencies come from `pyproject.toml` and `uv.lock` through
  `astral-sh/setup-uv` and `uv sync --locked`, as uv's GitHub Actions guide
  shows. The template's `requirements.txt` does not exist here.
- A `postgres:18` service container with GitHub's documented health check
  provides the test database through `DATABASE_URL`.
- Tests run with `uv run pytest`, which applies the pytest configuration
  (`--ds=config.settings.test`). `python manage.py test` discovers none of
  the existing pytest tests ("Ran 0 tests").
- A top-level `permissions: contents: read` block limits the workflow token to
  read access, as CodeQL's `actions/missing-workflow-permissions` query asks.

Pre-commit, mypy, migration checks, and the static export remain local checks
listed under Verification.

- [Using workflow templates](https://docs.github.com/en/actions/how-tos/write-workflows/use-workflow-templates)
- [Using uv in GitHub Actions](https://docs.astral.sh/uv/guides/integration/github/)
- [Creating PostgreSQL service containers](https://docs.github.com/en/actions/tutorials/use-containerized-services/create-postgresql-service-containers)

<details>
<summary>GitHub starter workflow license</summary>

```text
MIT License

Copyright (c) 2020 GitHub

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
SOFTWARE. THIS LICENSE DOES NOT GRANT YOU RIGHTS TO USE ANY CONTRIBUTORS'
NAME, LOGO, OR TRADEMARKS.
```

</details>

## Dependency updates

Dependabot alerts and security-update PRs are enabled through GitHub's repository
API. `.github/dependabot.yml` also schedules version-update PRs for Monday at
09:00 Asia/Tokyo, including the workflow references to GitHub Actions. Updates
require review and successful checks; automatic merging is not enabled. Preserve
imported reference snapshots; scheduled updates cover product manifests and CI
actions, not a rewrite of reference material.

- [Dependabot configuration](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference)
- [Repository security API](https://docs.github.com/en/rest/repos/repos#enable-vulnerability-alerts)

Dependabot checks the root uv manifest, including indirect dependencies.
Minor and patch Python version updates are grouped for review.
