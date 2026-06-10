<!-- DLE-Pifagor README Header -->
<p align="center">
  <a href="../README.md"><img src="../design/logos/main/pifagor-logo-primary.svg" alt="ЦОС Пифагор" width="104" /></a>
</p>

<p align="center">
  <strong>ЦОС "Пифагор"</strong><br />
  <sub>Документация проекта и материалы разработки</sub>
</p>

<p align="center">
  <a href="../README.md">README проекта</a> ·
  <a href="../docs/README.md">Документация</a> ·
  <a href="../README.en.md">English version</a>
</p>

---
<!-- /DLE-Pifagor README Header -->

# Дизайн-система

Папка `design/` хранит дизайн-материалы ЦОС «Пифагор»: логотипы, цветовые схемы, возрастные версии айдентики, макеты интерфейсов, презентационные шаблоны, UI-kit и брендбук.

Эта папка не является частью frontend-сборки напрямую. В неё складываются исходники и экспортированные дизайн-материалы, которые затем могут быть перенесены в `frontend/src/assets/` или `frontend/public/` только при необходимости.

---

## Структура

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

Раздел для брендбука и его исходников.

Сюда можно складывать:

- PDF-брендбук;
- исходники брендбука;
- правила использования логотипа;
- описание визуального языка;
- примеры фирменных носителей;
- экспортированные брендовые материалы.

Рекомендуемая будущая структура:

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

Раздел для логотипной системы Пифагора.

### `logos/main/`

Основные версии логотипа:

```text
main/
 ┣ pifagor-logo-dark.svg
 ┣ pifagor-logo-light.svg
 ┣ pifagor-logo-monochrome.svg
 ┗ pifagor-logo-primary.svg
```

Назначение:

- `pifagor-logo-primary.svg` — основная версия;
- `pifagor-logo-light.svg` — версия для тёмных фонов;
- `pifagor-logo-dark.svg` — строгая тёмная версия;
- `pifagor-logo-monochrome.svg` — монохромная версия для документов и печати.

### `logos/color-schemes/`

Цветовые схемы основного логотипа.

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

В каждой цветовой схеме могут храниться:

```text
Anastasia.svg
hero-logo.svg
icons.svg
logo.svg
```

Назначение файлов:

- `logo.svg` — основной логотип схемы;
- `hero-logo.svg` — версия для hero-блоков и крупных экранов;
- `icons.svg` — иконочная версия или набор знаков;
- `Anastasia.svg` — знак/иллюстрация ИИ-помощника, если предусмотрен в схеме.

### `logos/age-themes/`

Возрастные версии логотипа:

```text
age-themes/
 ┣ junior/
 ┣ middle/
 ┣ senior/
 ┣ college/
 ┗ university/
```

Назначение:

- `junior/` — младшие классы;
- `middle/` — средние классы;
- `senior/` — старшие классы;
- `college/` — СПО;
- `university/` — вуз.

Главное правило:

> Щит Пифагора остаётся ядром бренда. Меняются окружение, степень строгости и возрастная подача.

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

Раздел для макетов интерфейсов.

Назначение папок:

- `landing/` — публичные страницы и лендинг;
- `student-cabinet/` — кабинет учащегося;
- `parent-cabinet/` — кабинет родителя;
- `teacher-cabinet/` — кабинет преподавателя;
- `junior-interface/` — интерфейс младших классов;
- `middle-interface/` — интерфейс средних классов;
- `senior-interface/` — интерфейс старших классов.

Сюда можно складывать:

- PNG/JPG превью;
- Figma exports;
- прототипы;
- UI-скриншоты;
- варианты экранов.

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

Раздел для презентационного комплекта Пифагора.

Содержит:

- шаблон презентации;
- руководство по оформлению;
- экспортированные версии;
- используемые шрифты.

Важно:

> Не публиковать шрифты отдельно без проверки лицензии. Если шаблон будет распространяться пользователям, добавить `LICENSE.md` или отдельное пояснение по правам использования.

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

Раздел для элементов интерфейсной системы.

Сюда можно складывать:

- кнопки;
- карточки;
- формы;
- dashboard-блоки;
- иконки;
- состояния компонентов;
- экспортированные UI-элементы.

---

## Как использовать дизайн-материалы

### Для разработки frontend

В frontend переносить только те ассеты, которые реально используются приложением:

```text
frontend/src/assets/brand/
frontend/src/assets/icons/
frontend/src/assets/illustrations/
```

### Для публичного скачивания

Файлы, которые пользователь должен скачивать из приложения, можно хранить в:

```text
frontend/public/downloads/
```

Например:

```text
frontend/public/downloads/templates/pifagor-presentation-template.pptx
```

### Для документации

Правила использования дизайна описываются в:

```text
docs/03-design-system/
```

---

## Правила именования

Рекомендуется использовать английские системные имена файлов:

```text
pifagor-logo-primary.svg
pifagor-logo-junior.svg
pifagor-presentation-template.pptx
pifagor-presentation-guide.pdf
```

Избегать пробелов и нестабильных названий в путях.

---

## Главный принцип

> `design/` хранит дизайн-источники и визуальные материалы. В код приложения попадают только подготовленные и реально используемые ассеты.
---

<!-- DLE-Pifagor README Footer -->
---

<p align="center">
  <sub>ЦОС "Пифагор" · единая цифровая образовательная среда</sub>
</p>

<p align="center">
  <a href="../README.md">README проекта</a> ·
  <a href="../docs/README.md">Документация</a> ·
  <a href="../README.en.md">English version</a>
</p>
<!-- /DLE-Pifagor README Footer -->
