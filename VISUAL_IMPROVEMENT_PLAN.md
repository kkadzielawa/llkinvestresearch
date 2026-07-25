# LLK Invest Research Visual Improvement Plan

This plan is intended for implementation by a smaller model. Keep changes scoped to visual polish, responsive behavior, and frontend user experience. Do not refactor unrelated Django internals unless needed to support the visual work.

## Current Visual Problems

- The header/navigation feels dated and crowded, with many placeholder links and a hamburger icon that appears as a loose Font Awesome icon.
- The home splash video takes over the first screen but lacks modern overlay treatment, readable text composition, fallback handling, and a refined call to action.
- Typography is basic and understructured. The site uses one imported font without a clear scale for nav, hero, blog titles, body text, and metadata.
- The blog list and post detail pages are plain text blocks, not designed reading experiences.
- The contact page looks unfinished and form styling is minimal.
- Mobile layout needs polish: menu layering, touch targets, spacing, and text sizing are fragile.
- The visual system relies heavily on dark gray, navy, and red without enough hierarchy or contrast refinement.

## Design Direction

Aim for a restrained investment research publication feel:

- Quiet, credible, analytical, and modern.
- More like a premium research desk or financial intelligence publication than a generic personal site.
- Keep the palette dark but make it more intentional with neutral charcoal, off-white text, muted blue-gray, and one restrained accent color.
- Use generous spacing, clean typographic hierarchy, and crisp interactive states.
- Avoid flashy finance cliches, heavy gradients, and oversized decorative effects.

Recommended palette:

```css
:root {
  --color-bg: #101418;
  --color-surface: #171d23;
  --color-surface-soft: #202832;
  --color-text: #f4f1ea;
  --color-muted: #a9b0b8;
  --color-border: rgba(244, 241, 234, 0.14);
  --color-accent: #b88a44;
  --color-accent-strong: #d2a45c;
}
```

Use a readable serif or editorial display font for major headings if desired, but keep body and interface text clean and compact. Do not use viewport-width font scaling.

## Phase 1: Header And Navigation

Files:

- `templates/base.html`
- `static/css/main.css`
- `static/js/main.js`

Tasks:

1. Replace the loose `.menu-btn` div with a real `<button>`:
   - Add `type="button"`.
   - Add `aria-label="Open navigation"`.
   - Add `aria-expanded="false"`.
   - Add `aria-controls="primary-navigation"`.

2. Give the nav list an id:

   ```html
   <ul id="primary-navigation" class="main-menu">
   ```

3. Make the logo link route to home instead of `#`.

4. Remove or hide placeholder nav links until real pages exist:
   - About
   - MicroView Blog
   - Technical Analysis
   - TheStockAnalyzer

   If the owner wants to keep them visible, style them as disabled only if there is explicit copy explaining availability. Prefer removing them from primary navigation for now.

5. Restyle the header:
   - Use a sticky or fixed top header only if it does not fight the hero video.
   - Header height should be content-driven, not `15vh`.
   - Logo should have stable dimensions, for example `48px`.
   - Nav items need consistent spacing and a subtle active/hover underline.

6. Mobile menu:
   - Use a slide-in panel or dropdown anchored below the header.
   - Add a backdrop or clear background so links remain legible.
   - Set correct z-index.
   - Prevent layout jumping.
   - Toggle `aria-expanded` in JS.
   - Close menu when a nav link is clicked.

Acceptance criteria:

- Header looks balanced at desktop, tablet, and mobile widths.
- Hamburger is a proper button and toggles cleanly.
- No placeholder `href="# "` links remain in primary nav.
- JS does not create global variables or crash if elements are missing.

## Phase 2: Home Splash Video

Files:

- `templates/home.html`
- `static/css/main.css`
- `static/img/splash_video.mp4`

Tasks:

1. Keep the splash video, but make it feel intentional:
   - Add a dark overlay using `::before` or a sibling overlay element.
   - Keep text readable over the video.
   - Use `min-height` with responsive constraints instead of fixed `75vh`.
   - Ensure the next section is slightly visible on common desktop and mobile heights.

2. Recompose hero content:
   - Use one strong headline.
   - Add one short supporting sentence.
   - Use a refined CTA button.

Suggested copy:

```html
<h1>LLK Investment Research</h1>
<p>Independent market notes across macro, digital assets, commodities, and trading strategy.</p>
<a href="{% url 'blog' %}" class="btn btn-primary">Read MacroView</a>
```

3. Add a fallback poster image if available. If no poster exists, add a CSS fallback background color and ensure the page still looks polished if video fails.

4. Respect reduced motion:

```css
@media (prefers-reduced-motion: reduce) {
  .showcase .video {
    display: none;
  }
}
```

5. Avoid absolute positioning for all hero text. Use a content wrapper positioned over the video with CSS grid or flex.

Acceptance criteria:

- Hero looks modern and readable with the video.
- Text and CTA do not overlap on mobile.
- Home page still looks good if video is unavailable or reduced motion is enabled.

## Phase 3: Global Typography And Layout System

Files:

- `templates/base.html`
- `static/css/main.css`

Tasks:

1. Define a simple type scale:
   - Hero h1: large but capped with `clamp()`.
   - Page h1/h2: moderate editorial sizing.
   - Body text: 16 to 18px with comfortable line height.
   - Nav text: compact and legible.

2. Add reusable layout classes:
   - `.page-shell`
   - `.section`
   - `.content-narrow`
   - `.content-wide`

3. Update body background and text colors using CSS variables.

4. Add consistent link, button, focus, and hover states.

5. Add `:focus-visible` styles for keyboard navigation.

Acceptance criteria:

- Pages share one visual language.
- Text hierarchy is clear.
- Buttons and links have polished hover and keyboard focus states.

## Phase 4: Blog List Visual Redesign

Files:

- `templates/blog.html`
- `static/css/main.css`

Tasks:

1. Replace the plain stacked headings with a research-index layout:
   - Page header: `MacroView`
   - Short subtitle.
   - Post list as clean article rows or compact cards.

2. Each post preview should include:
   - Title
   - Created date
   - Short excerpt
   - Read more link

3. Do not use nested cards. Prefer full-width article rows with a border-bottom, or individual cards only if the layout remains simple.

4. Add empty state text for no published posts.

5. Ensure excerpts do not break HTML mid-tag. If the current implementation slices rich HTML, replace it with `striptags|truncatewords`.

Suggested template pattern:

```django
{% for post in object_list %}
  <article class="post-preview">
    <p class="post-meta">{{ post.created_on|date:"M j, Y" }}</p>
    <h2><a href="{% url 'post_detail' post.slug %}">{{ post.title }}</a></h2>
    <p>{{ post.content|striptags|truncatewords:36 }}</p>
    <a class="text-link" href="{% url 'post_detail' post.slug %}">Read analysis</a>
  </article>
{% empty %}
  <p class="empty-state">No research notes have been published yet.</p>
{% endfor %}
```

Acceptance criteria:

- Blog index feels like a publication archive.
- Post previews are scannable.
- Rich text is not visibly broken in excerpts.

## Phase 5: Post Detail Reading Experience

Files:

- `templates/post_detail.html`
- `static/css/main.css`

Tasks:

1. Create a focused article layout:
   - Back link above article.
   - Title.
   - Metadata row with date and author if available.
   - Narrow readable content column.

2. Style rich text content:
   - Paragraph spacing.
   - Headings.
   - Lists.
   - Blockquotes.
   - Links.
   - Images, if any are embedded.

3. Keep line length readable with max width around `68ch` to `76ch`.

Acceptance criteria:

- Post detail feels like a polished research article.
- Long-form text is comfortable to read.

## Phase 6: Contact Page Visual Completion

Files:

- `templates/contact.html`
- `static/css/main.css`

Tasks:

1. If the form is not functional yet, visually replace it with a clean contact section:
   - Name/title.
   - Email link or LinkedIn link.
   - Short contact copy.

2. If keeping the form, style it properly:
   - Labels.
   - Inputs.
   - Textarea.
   - Submit button.
   - Focus states.
   - Error/success states if backend is added later.

3. Use a two-column layout on desktop and a single-column layout on mobile.

Acceptance criteria:

- Contact page no longer looks unfinished.
- Form controls or contact links are visually consistent with the rest of the site.

## Phase 7: Responsive QA

Test these widths:

- 375px
- 768px
- 1024px
- 1440px

Checks:

- Header does not overlap content.
- Hamburger menu opens and closes.
- Hero text fits and remains readable.
- CTA button is easy to tap.
- Blog list is scannable.
- Post detail content width is comfortable.
- Footer does not crowd content.
- No horizontal scrolling.

Run:

```bash
python manage.py check
python manage.py runserver
```

Then manually inspect the site in browser dev tools.

## Suggested Commit Order

1. Header and hamburger modernization.
2. Home hero video redesign.
3. Global CSS variables, typography, buttons, and layout helpers.
4. Blog list redesign.
5. Post detail redesign.
6. Contact page polish.
7. Responsive cleanup and final QA.

## Do Not Do In This Visual Pass

- Do not upgrade Django as part of this visual-only handoff.
- Do not alter database schema unless needed for visible metadata.
- Do not remove the splash video unless the owner explicitly asks.
- Do not introduce a frontend framework.
- Do not commit generated `staticfiles/` changes.

