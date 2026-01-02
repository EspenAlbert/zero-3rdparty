# path-sync copy -n python-template

# === OK_EDIT ===
# Custom variables and setup


# === DO_NOT_EDIT: path-sync standard ===
pre-push: lint fmt-check test
  @echo "All checks passed"

pre-commit: fmt fix lint
  @echo "Pre-commit checks passed"

lint:
  uv run ruff check .

fmt:
  uv run ruff format .

fmt-check:
  uv run ruff format --check .

fix:
  uv run ruff check --fix .

test:
  uv run pytest

build:
  uv build
# === OK_EDIT ===

# === DO_NOT_EDIT: path-sync path-sync ===
path-sync-validate:
  uv run path-sync validate-no-changes -n python-template
# === OK_EDIT ===

# === DO_NOT_EDIT: path-sync coverage ===
cov:
  uv run pytest --cov --cov-report=html

cov-full:
  uv run pytest --cov --cov-report=html --cov-report=xml

open-cov: cov
  open htmlcov/index.html
# === OK_EDIT ===

# === DO_NOT_EDIT: path-sync typing ===
type-check:
  uv run pyright
# === OK_EDIT ===

# === DO_NOT_EDIT: path-sync pkg-ext ===
pkg-pre-push:
  uv run pkg-ext pre-push

pkg-pre-merge:
  uv run pkg-ext --is-bot pre-merge

pkg-post-merge:
  uv run pkg-ext --is-bot post-merge --push

pkg-release-notes tag:
  uv run pkg-ext release-notes --tag {{tag}}
# === OK_EDIT ===

# Custom recipes below
