# website

Behold My Awesome Project!

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Settings

Moved to [settings](https://cookiecutter-django.readthedocs.io/en/latest/1-getting-started/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      uv run python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    uv run mypy website

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    uv run coverage run -m pytest
    uv run coverage html
    uv run open htmlcov/index.html

#### Running tests with pytest

    uv run pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/2-local-development/developing-locally.html#using-webpack-or-gulp).

## Deployment

Real credentials and deployment configuration must not be committed to this repository. Copy the tracked examples when a local file is needed:

    cp .envs/.local/.django.example .envs/.local/.django
    cp .envs/.local/.postgres.example .envs/.local/.postgres

For a Django production deployment, provide the variables listed in `.envs/.production/*.example` through the hosting provider's encrypted environment-variable or secret-management interface. If a local production file is required, copy the examples and keep the resulting files ignored:

    cp .envs/.production/.django.example .envs/.production/.django
    cp .envs/.production/.postgres.example .envs/.production/.postgres

Do not reuse the placeholder values. Generate unique credentials for every environment. Values previously committed to Git history must be treated as compromised and revoked or rotated in every affected service. If a history rewrite is still required after the risk is mitigated, follow GitHub's [sensitive-data removal procedure](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).

The static corporate-site build does not require the production Django environment files:

    .venv/bin/python scripts/build_sites_static.py

The static build includes anonymous Privacy Policy, Terms of Use, and Support
pages for Weave, Vault, Ukiyo, Grace, and Still at
`/apps/<app>/privacy/`, `/apps/<app>/terms/`, and
`/apps/<app>/support/`. Japanese versions use the same paths below `/ja/`.

Vercel builds the static site from `main` and publishes `dist/client` to
production. Pushes to other branches and pull requests create Preview
deployments. The versioned build contract is in `vercel.json`; no Vercel token
or production Django credentials belong in Git.

For the full Django application, set `DATABASE_URL` along with the variables in the production examples before starting the application.
