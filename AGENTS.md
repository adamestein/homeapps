# AGENTS.md

Django 5.2 personal home apps. Django apps live under `apps/` (`finances`, `utilities`; `library` is shared infra: middleware, admin autodiscover, testing helpers). App URLs are namespaced (`finances:`, `utilities:`).

## Environment

- No `pyproject.toml`/`uv.lock` — NOT uv-managed. `uv run ...` runs in the ambient venv `~/.virtualenvs/homeapps` (Python 3.13). Use `uv run` for all python/manage.py/pytest calls.
- Dev DB: MySQL `homeapps`/`homeapps@localhost`. Prod: PythonAnywhere MySQL. Bump `VERSION` in `homeapps/settings/base.py` on user-visible changes (commit convention).

## Settings

- Settings is a package. `DJANGO_SETTINGS_MODULE=homeapps.settings` (`__init__.py`) is the real entry: it picks dev/prod via presence of `https_proxy`, and if `test` is in `sys.argv` swaps in SQLite `/tmp/default.db` and appends `django_behave`.
- `homeapps/settings/testing.py` is an add-on merged by `__init__.py`, NOT standalone — it has no `INSTALLED_APPS`/`DATABASES`. Setting `DJANGO_SETTINGS_MODULE=homeapps.settings.testing` yields empty settings and `ContentType ... app_label` errors. Never use it directly.
- `homeapps/settings/pytest.py` is the standalone pytest settings module (wired via `pytest.ini`): `from .dev import *` then SQLite `/tmp/homeapps_test.sqlite3`, migrations disabled, fast password hasher. It exists because the dev MySQL user can't create the `test_*` DB pytest-django needs, and because `__init__.py`'s `test`-in-argv branch (which references the removed `django_behave`) is never hit under pytest.
- Gotcha: any manage.py command with `test` in argv now dies with `No module named 'django_behave'` (dep removed, `__init__.py` still references it).

## Tests (migrating: behave/splinter/selenium → pytest + pytest-playwright)

- `./run_tests` is the new runner: `uv run pytest -m <marker>` with `-u`=unit, `-b`=behavior, `-a`=all, `-d`=headed. The old `bdd_tests` script and `./manage.py test` are dead (deps uninstalled).
- `pytest.ini` sets `DJANGO_SETTINGS_MODULE=homeapps.settings.pytest`, so plain `uv run pytest` just works (SQLite, no MySQL test DB needed). Markers `unit`/`behavior` are registered there.
- Unit tests live in `<app>/tests/unit/test_*.py` and carry `@pytest.mark.unit` (`pytestmark = pytest.mark.unit` at module level) so `./run_tests -u` collects them. Use pytest style (fixtures, plain asserts) — no Django `TestCase` classes.
- Playwright behavior tests don't exist yet. Existing BDD lives in `apps/finances/features` + `apps/library/features` (Behave) and can't run without the removed deps.
- `tests/finances/**` and `tests/library/web-site/**` are PNG/PDF golden-image baselines from the old screenshot-diff BDD harness (`apps/library/testing/`; compares via Wand, pins clock to 2020-01-08 with forbiddenfruit). `packages/chrome_extensions/` is the Chrome "clear downloads" extension that harness loaded.

## Dependencies / layout

- `requirements.txt` installs `tekextensions` (an INSTALLED_APP) from a GitHub zip URL — keep it. `packages/` holds vendored JS.
- Project templates are in repo-root `templates/`; static in `apps/static/`. Legacy committed `.pyc` files and `__pycache__/` sit alongside sources — ignore them.
