# LLK Invest Research Implementation Improvement Plan

This plan is intended for handoff to a smaller model for implementation. Keep changes small, staged, and verified. The project is a small Django blog/site, so prioritize security, maintainability, deploy hygiene, and correctness before deeper feature work.

## Current Findings

- `python manage.py check --deploy` reports production security warnings.
- `python manage.py test` runs 0 tests.
- Django is pinned to `3.0.1`, which is unsupported.
- The production `SECRET_KEY` is committed in `llkinvestresearch/settings.py`.
- `db.sqlite3` is tracked.
- Generated `staticfiles/` output is tracked.
- Public blog views currently expose all posts, including drafts.
- The contact form is present visually but has no backend behavior.
- Several primary navigation links point to placeholders.

As of July 2026, Django's supported release lines include Django `5.2 LTS` and Django `6.0`. Prefer upgrading this project to Django `5.2.x` LTS unless there is a specific reason to use `6.0`.

Reference: https://www.djangoproject.com/download/

## Phase 1: Repository Hygiene

Files:

- `.gitignore`
- repository index

Tasks:

1. Update `.gitignore` to ignore runtime/generated files:

   ```gitignore
   db.sqlite3
   staticfiles/
   .env
   *.log
   ```

2. Remove generated/local files from git tracking without deleting local copies:

   ```bash
   git rm -r --cached staticfiles db.sqlite3
   ```

3. Review whether `content/The Case for Bitcoin.docx` belongs in source control. Leave it alone unless the owner confirms it should be removed.

4. Add a `README.md` with:
   - Python version.
   - Virtualenv setup.
   - Dependency installation.
   - Environment variables.
   - Migration commands.
   - Createsuperuser command.
   - Runserver command.
   - Test command.
   - Collectstatic/deployment notes.

Acceptance criteria:

- `staticfiles/` is no longer tracked.
- `db.sqlite3` is no longer tracked.
- New local database/static output does not appear in `git status`.
- A new contributor can run the project from the README.

## Phase 2: Settings, Secrets, And Production Config

Files:

- `llkinvestresearch/settings.py`
- `.env.example`
- `requirements.txt`, if adding env parsing dependency

Tasks:

1. Move these settings to environment variables:
   - `SECRET_KEY`
   - `DEBUG`
   - `ALLOWED_HOSTS`
   - database URL/config, if deployment uses a non-SQLite database

2. Use either standard `os.environ` parsing or a small dependency such as `django-environ`.

3. Add `.env.example`:

   ```env
   SECRET_KEY=change-me
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   DATABASE_URL=sqlite:///db.sqlite3
   ```

4. Rotate the production secret key in the hosting provider. The current key is committed and should be treated as compromised.

5. Remove the duplicate `STATICFILES_DIRS` assignment. Keep one clear tuple/list.

6. Add production security settings when `DEBUG=False`:
   - `SECURE_SSL_REDIRECT = True`
   - `SESSION_COOKIE_SECURE = True`
   - `CSRF_COOKIE_SECURE = True`
   - `SECURE_REFERRER_POLICY = "same-origin"` or another intentional policy
   - `SECURE_HSTS_SECONDS`, only after confirming HTTPS is stable
   - `SECURE_HSTS_INCLUDE_SUBDOMAINS`, only if all subdomains support HTTPS
   - `SECURE_HSTS_PRELOAD`, only if ready for browser preload consequences

Acceptance criteria:

- No secrets are committed.
- Local development works with `.env`.
- Production config passes `python manage.py check --deploy` for the intended deployment environment.

## Phase 3: Dependency Upgrade

Files:

- `requirements.txt`
- Django project files as needed for compatibility

Tasks:

1. Upgrade Django from `3.0.1` to latest `5.2.x` LTS.

2. Upgrade compatible packages:
   - `whitenoise`
   - `gunicorn`
   - `django-ckeditor`
   - `django-js-asset`
   - `asgiref`
   - `sqlparse`

3. Add or confirm a supported Python version. Django 5.2 supports modern Python 3 versions; use the deployed runtime's supported version.

4. Run:

   ```bash
   python manage.py check
   python manage.py makemigrations --check
   python manage.py test
   ```

5. Fix expected compatibility issues:
   - Add `DEFAULT_AUTO_FIELD` if needed.
   - Update static storage settings for current Django/WhiteNoise.
   - Replace deprecated settings if checks report them.

Acceptance criteria:

- App boots on Django 5.2.
- Migrations are stable.
- Tests pass.
- No compatibility warnings remain from basic checks.

## Phase 4: Blog Correctness And Safety

Files:

- `blog/models.py`
- `blog/views.py`
- `templates/blog.html`
- `templates/post_detail.html`
- `blog/tests.py`

Tasks:

1. Update `PostList` to show only published posts:

   ```python
   queryset = Post.objects.filter(status=1).order_by("-created_on")
   ```

2. Update `PostDetail` to return 404 for draft posts. Use `get_queryset()`:

   ```python
   def get_queryset(self):
       return Post.objects.filter(status=1)
   ```

3. Add pagination to `PostList`, for example:

   ```python
   paginate_by = 10
   ```

4. Add `get_absolute_url()` to `Post`.

5. Improve the status choices:
   - Prefer `models.IntegerChoices` or named constants over raw `0` and `1`.

6. Decide the rich-text trust policy:
   - If only trusted admins can edit posts, document that.
   - If non-admins can create/edit content, sanitize rich text before rendering. Consider `bleach`.

7. Add tests:
   - Published post appears in blog list.
   - Draft post does not appear in blog list.
   - Published post detail returns 200.
   - Draft post detail returns 404.
   - Post ordering is newest first.

Acceptance criteria:

- Draft content is not public.
- Blog behavior is covered by tests.

## Phase 5: Contact Page

Files:

- `templates/contact.html`
- `llkinvestresearch/urls.py`
- possible new `forms.py` or view file
- tests

Tasks:

1. Decide between two valid approaches:
   - Remove the form and provide real contact links.
   - Implement a real Django contact form.

2. If implementing a form:
   - Create a `forms.Form` with name, email, optional phone, and message.
   - Add CSRF token.
   - Use `method="post"`.
   - Validate input.
   - Send email through Django's email backend.
   - Configure email settings from environment variables.
   - Show success/failure messages.

3. Add tests for:
   - GET renders form.
   - Invalid POST re-renders errors.
   - Valid POST sends mail or calls configured mail backend.

Acceptance criteria:

- The contact page does not contain a dead form.
- POST behavior is covered if a form remains.

## Phase 6: Navigation And Frontend Cleanup

Files:

- `templates/base.html`
- `static/js/main.js`
- `static/css/main.css`

Tasks:

1. Replace placeholder navigation links with real routes, remove them, or mark them intentionally unavailable.

2. Make the logo link route to home.

3. Fix JavaScript globals:

   ```javascript
   const menuBtn = document.querySelector(".menu-btn");
   const mainMenu = document.querySelector(".main-menu");

   if (menuBtn && mainMenu) {
     menuBtn.addEventListener("click", () => {
       mainMenu.classList.toggle("show");
     });
   }
   ```

4. If keeping the mobile menu, make it accessible:
   - Use a `<button>`.
   - Toggle `aria-expanded`.
   - Add an accessible label.
   - Close menu after link click.

5. Add accessible labels to icon-only social links.

6. Update footer copyright year.

Acceptance criteria:

- No dead primary navigation links remain.
- Mobile menu works without console errors.
- Basic accessibility issues in the header/footer are addressed.

## Phase 7: Deployment Polish

Files:

- deployment config files as applicable
- `requirements.txt`
- `settings.py`
- README

Tasks:

1. Confirm deployment target. Existing config suggests Heroku, but verify before changing deployment-specific files.

2. If Heroku is still used, add or update:
   - `Procfile`
   - Python runtime/version declaration
   - static file collection notes
   - required config vars in README

3. Configure WhiteNoise static files for production:
   - Use compressed manifest storage or current Django/WhiteNoise equivalent.

4. Run:

   ```bash
   python manage.py collectstatic --noinput
   gunicorn llkinvestresearch.wsgi
   ```

Acceptance criteria:

- Deployment steps are documented.
- Static files collect successfully.
- Gunicorn starts the app locally.

## Suggested Commit Order

1. Repository hygiene and README.
2. Settings, env vars, and security configuration.
3. Dependency upgrade to Django 5.2 LTS.
4. Blog queryset fixes and tests.
5. Contact page behavior.
6. Navigation and small frontend accessibility cleanup.
7. Deployment verification.

## Do Not Do Without Explicit Approval

- Do not delete user content.
- Do not remove `content/The Case for Bitcoin.docx` unless approved.
- Do not rewrite the visual design in this implementation pass; use `VISUAL_IMPROVEMENT_PLAN.md` for that.
- Do not commit generated `staticfiles/`.
- Do not commit local databases or secrets.

