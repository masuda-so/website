# Ether website

[日本語](README.md) | [English](README.en.md)

## Overview

Ether's corporate site and public product information for Grace, Still, Ukiyo,
Vault, and Weave. Django supplies the pages and local application; the static
export publishes the public site, including English and Japanese privacy,
terms, and support pages.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Features and limitations

The repository manages a Django application and a static public site. Product privacy, terms, and support pages are available in Japanese and English. Full Django production hosting and static publishing require different configuration.

## Getting started and usage

### Settings

See the [Cookiecutter Django settings guide](https://cookiecutter-django.readthedocs.io/en/latest/1-getting-started/settings.html).

### Basic Commands

#### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      uv run python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

#### Type checks

Running type checks with mypy:

    uv run mypy website

#### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    uv run coverage run -m pytest
    uv run coverage html
    uv run open htmlcov/index.html

##### Running tests with pytest

    uv run pytest

#### Linting and template formatting

Run the repository hooks before pushing:

    uv run pre-commit run --all-files

If a formatter modifies files, review the diff and run the command again before
committing. The hooks use versions pinned in `.pre-commit-config.yaml`, which
are independent of the development dependencies in `pyproject.toml` and `uv.lock`.
Check these configuration files for the current versions.
The Django profile and JavaScript formatting options
are configured in `[tool.djlint]` in `pyproject.toml`.

### Deployment

Real credentials and deployment configuration must not be committed to this repository. Copy the tracked examples when a local file is needed:

    cp .envs/.local/.django.example .envs/.local/.django
    cp .envs/.local/.postgres.example .envs/.local/.postgres

For a Django production deployment, provide the variables listed in `.envs/.production/*.example` through the hosting provider's encrypted environment-variable or secret-management interface. If a local production file is required, copy the examples and keep the resulting files ignored:

    cp .envs/.production/.django.example .envs/.production/.django
    cp .envs/.production/.postgres.example .envs/.production/.postgres

Do not reuse the placeholder values. Generate unique credentials for every environment. Values previously committed to Git history must be treated as compromised and revoked or rotated in every affected service. If a history rewrite is still required after the risk is mitigated, follow GitHub's [sensitive-data removal procedure](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).

The static corporate-site build does not require the production Django environment files:

    uv run python scripts/build_sites_static.py

The static build includes anonymous Privacy Policy, Terms of Use, and Support
pages for Weave, Vault, Ukiyo, Grace, and Still at
`/apps/<app>/privacy/`, `/apps/<app>/terms/`, and
`/apps/<app>/support/`. Japanese versions use the same paths below `/ja/`.

Production currently runs on Vercel, which builds the static site from `main`
and publishes `dist/client`. Pushes to other branches and pull requests create
Preview deployments. The Vercel build settings are in `vercel.json`.

A move to Cloudflare Workers (Static Assets) is in preparation. `wrangler.jsonc`
runs the same build through `build.command` and serves `dist/client` as static
assets; run `npx wrangler dev` to check it locally. `vercel.json` stays until
production has switched over. No Vercel or Cloudflare token or production
Django credentials belong in Git.

For the full Django application, set `DATABASE_URL` along with the variables in the production examples before starting the application.

## Support and documentation

### Repository structure

See [docs/structure.md](docs/structure.md) for source ownership, naming, generated
files, and verification. Django configuration remains in `config/`, application
code and templates in `website/`, and repository utilities in `scripts/`.

### Design references

The public site's product presentation, retained brand tokens, and asset
provenance are documented in [docs/DESIGN.md](docs/DESIGN.md).

## Development and contributions

Use the product support pages above for product questions. For repository changes,
consult the structure and design documents and describe the change and checks
in a pull request. PR descriptions and review comments use Japanese by default; an explicit request for another language takes precedence.

See [AGENTS.md](AGENTS.md) for shared repository instructions.
