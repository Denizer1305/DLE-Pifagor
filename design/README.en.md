<!-- DLE-Pifagor README Header -->
<p align="center">
  <a href="../README.en.md"><img src="../design/logos/main/pifagor-logo-primary.svg" alt="DLE Pifagor" width="104" /></a>
</p>

<p align="center">
  <strong>DLE "Pifagor"</strong><br />
  <sub>Project documentation and development materials</sub>
</p>

<p align="center">
  <a href="../README.en.md">Project README</a> ·
  <a href="../docs/README.en.md">Documentation</a> ·
  <a href="../README.md">Русская версия</a>
</p>

---
<!-- /DLE-Pifagor README Header -->

# Design

The `design/` folder stores design materials for DLE “Pifagor”: logos, color schemes, age-based identity versions, interface mockups, presentation templates, UI kit assets, and brandbook sources.

This folder is not intended to be bundled directly into the frontend. It stores source and exported design assets that can later be moved to `frontend/src/assets/` or `frontend/public/` only when needed.

---

## Structure

```text
design/
 ┣ brandbook/
 ┣ logos/
 ┣ mockups/
 ┣ presentations/
 ┣ ui-kit/
 ┣ README.en.md
 ┗ README.md
```

---

## `brandbook/`

```text
brandbook/
 ┗ sources/
```

Brandbook and source materials.

This folder may contain:

- PDF brandbook;
- brandbook source files;
- logo usage rules;
- visual language descriptions;
- branded media examples;
- exported brand assets.

Recommended future structure:

```text
brandbook/
 ┣ pifagor-brandbook.pdf
 ┗ sources/
```

---

## `logos/`

```text
logos/
 ┣ age-themes/
 ┣ color-schemes/
 ┗ main/
```

Logo system for Pifagor.

### `logos/main/`

Main logo versions:

```text
main/
 ┣ pifagor-logo-dark.svg
 ┣ pifagor-logo-light.svg
 ┣ pifagor-logo-monochrome.svg
 ┗ pifagor-logo-primary.svg
```

Purpose:

- `pifagor-logo-primary.svg` — main version;
- `pifagor-logo-light.svg` — version for dark backgrounds;
- `pifagor-logo-dark.svg` — strict dark version;
- `pifagor-logo-monochrome.svg` — monochrome version for documents and print.

### `logos/color-schemes/`

Color schemes of the main logo.

```text
color-schemes/
 ┣ blue/
 ┣ dark/
 ┣ green/
 ┣ light/
 ┣ light-blue/
 ┣ orange/
 ┣ pink/
 ┣ red/
 ┣ violet/
 ┗ yellow/
```

Each scheme may contain:

```text
Anastasia.svg
hero-logo.svg
icons.svg
logo.svg
```

File purpose:

- `logo.svg` — main logo for the scheme;
- `hero-logo.svg` — large version for hero sections;
- `icons.svg` — icon version or symbol set;
- `Anastasia.svg` — AI assistant sign/illustration if provided.

### `logos/age-themes/`

Age-based logo versions:

```text
age-themes/
 ┣ junior/
 ┣ middle/
 ┣ senior/
 ┣ college/
 ┗ university/
```

Purpose:

- `junior/` — primary school;
- `middle/` — middle school;
- `senior/` — senior school;
- `college/` — vocational/college level;
- `university/` — university level.

Main rule:

> The Pifagor shield remains the core of the brand. Surrounding elements, maturity, and age tone may change.

---

## `mockups/`

```text
mockups/
 ┣ junior-interface/
 ┣ landing/
 ┣ middle-interface/
 ┣ parent-cabinet/
 ┣ senior-interface/
 ┣ student-cabinet/
 ┗ teacher-cabinet/
```

Interface mockups.

Folder purpose:

- `landing/` — public pages and landing;
- `student-cabinet/` — student cabinet;
- `parent-cabinet/` — parent cabinet;
- `teacher-cabinet/` — teacher cabinet;
- `junior-interface/` — primary school interface;
- `middle-interface/` — middle school interface;
- `senior-interface/` — senior school interface.

This folder may contain PNG/JPG previews, Figma exports, prototypes, UI screenshots, and screen variations.

---

## `presentations/`

```text
presentations/
 ┣ exports/
 ┣ fonts/
 ┣ guides/
 ┣ templates/
 ┗ README.md
```

Presentation kit for Pifagor.

Contains:

- presentation template;
- presentation guide;
- exported versions;
- fonts used by templates.

Important:

> Do not publish font files separately without checking the license. If the template is distributed to users, add `LICENSE.md` or a clear usage rights note.

---

## `ui-kit/`

```text
ui-kit/
 ┣ buttons/
 ┣ cards/
 ┣ dashboards/
 ┣ forms/
 ┗ icons/
```

Interface system assets.

This folder may contain buttons, cards, forms, dashboard blocks, icons, component states, and exported UI elements.

---

## How to Use Design Assets

### For frontend development

Move only assets that are actually used by the application:

```text
frontend/src/assets/brand/
frontend/src/assets/icons/
frontend/src/assets/illustrations/
```

### For public downloads

Files users should download from the platform may be placed in:

```text
frontend/public/downloads/
```

Example:

```text
frontend/public/downloads/templates/pifagor-presentation-template.pptx
```

### For documentation

Design usage rules are described in:

```text
docs/03-design-system/
```

---

## Naming Rules

Use stable English file names:

```text
pifagor-logo-primary.svg
pifagor-logo-junior.svg
pifagor-presentation-template.pptx
pifagor-presentation-guide.pdf
```

Avoid spaces and unstable names in paths.

---

## Main Principle

> `design/` stores design sources and visual materials. Only prepared and actually used assets should be added to the application code.
---

<!-- DLE-Pifagor README Footer -->
---

<p align="center">
  <sub>DLE "Pifagor" · unified digital learning environment</sub>
</p>

<p align="center">
  <a href="../README.en.md">Project README</a> ·
  <a href="../docs/README.en.md">Documentation</a> ·
  <a href="../README.md">Русская версия</a>
</p>
<!-- /DLE-Pifagor README Footer -->
