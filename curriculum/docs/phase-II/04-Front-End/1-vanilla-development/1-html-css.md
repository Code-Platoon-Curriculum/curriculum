# HTML and CSS

## Introduction

Welcome to **HTML and CSS**, the foundation of front-end web development. In this lecture, we will explore how web pages are **structured** using HTML and how they are **styled and visually presented** using CSS.

Rather than treating HTML and CSS as separate technologies, this lecture emphasizes how they work **together** to create readable, accessible, and visually engaging web applications. Understanding this separation of concerns—**structure vs. presentation**—is critical before moving into JavaScript, front-end frameworks, or full stack application development.

---

## What Is HTML?

HTML (Hypertext Markup Language) is the language used to **structure content on the web**. It defines *what* content exists on a page—text, images, links, forms, and sections—and provides meaning and hierarchy to that content.

HTML is not a programming language; it is a **markup language**. Browsers read HTML documents and render them visually based on the tags and structure defined by the developer.

HTML answers the question:  
**“What is on this page?”**

---

## HTML Document Structure

Every HTML document follows a predictable structure that browsers rely on to properly render content.

### Essential HTML Tags

#### `<!DOCTYPE>`
- Declares the document as HTML5
- Ensures standards-compliant rendering across browsers

#### `<html>`
- Root element of the document
- Wraps all HTML content

#### `<head>`
- Contains metadata and configuration
- Not visible to users

Common elements inside `<head>`:

- `<title>` – Page title shown in browser tabs
- `<meta>` – Character encoding, viewport, SEO data
- `<link>` – External stylesheets and icons
- `<style>` – Internal CSS (discouraged for large projects)
- `<script>` – JavaScript files or inline scripts

#### `<body>`

- Contains all visible content rendered to the page
- Text, images, links, forms, components

---

## HTML Content Structure

HTML provides tags to organize content in a readable and accessible way.

### Common Content Tags

- Headings: `<h1>` → `<h6>`  
  Used to define content hierarchy and improve accessibility

- Paragraphs: `<p>`  
  Used for blocks of text

- Line breaks: `<br>`  
  Forces a new line without creating a new paragraph

---

## HTML Elements, Tags, and Attributes

### Elements and Tags

An HTML element consists of:

```html
<tag>content</tag>
```

Some elements are self-closing:

```html
<img />
<br />
```

### Common Structural Elements

* `<div>` – Generic block-level container
* `<span>` – Generic inline container
* `<strong>` – Strong importance (semantic)
* `<em>` – Emphasis (semantic)
* `<a>` – Hyperlinks

### Attributes

Attributes provide additional information about an element:

```html
<a href="https://example.com">Link</a>
```

Common attributes:

* `id`
* `class`
* `src`
* `href`
* `alt`

---

## HTML Forms and User Input

Forms allow users to **send data** to a server.

### Core Form Elements

* `<form>` – Wraps input elements
* `<input>` – Text, password, checkbox, radio, etc.
* `<textarea>` – Multi-line input
* `<select>` – Dropdown menu
* `<button>` – Submits or triggers actions

Key attributes:

* `action` – Where data is sent
* `method` – HTTP method (`GET`, `POST`)
* `name` – Used to identify submitted data

---

## HTML Lists, Images, and Tables

### Lists

* `<ul>` – Unordered list
* `<ol>` – Ordered list
* `<li>` – List item
* `<dl>`, `<dt>`, `<dd>` – Definition lists

### Images

```html
<img src="image.jpg" alt="Description" />
```

* `alt` is critical for accessibility

### Tables

* `<table>`, `<tr>`, `<th>`, `<td>`
* Used for tabular data, not layout

---

## HTML Semantics

Semantic HTML provides **meaning**, not just structure.

Common semantic elements:

* `<header>`
* `<nav>`
* `<main>`
* `<section>`
* `<article>`
* `<aside>`
* `<footer>`

Semantic HTML improves:

* Accessibility
* SEO
* Maintainability
* Team communication

---

## What Is CSS?

CSS (Cascading Style Sheets) controls the **presentation** of HTML content.

CSS answers the question:
**“What should this look like?”**

CSS defines:

* Colors
* Fonts
* Spacing
* Layout
* Responsiveness

HTML = structure
CSS = appearance

---

## Applying CSS to HTML

### Inline Styles (Discouraged)

```html
<p style="color: blue;">Text</p>
```

### Internal Styles

```html
<style>
  p {
    color: green;
  }
</style>
```

### External Stylesheets (Best Practice)

```html
<link rel="stylesheet" href="styles.css" />
```

External stylesheets:

* Improve maintainability
* Scale better for real projects
* Encourage separation of concerns

---

## CSS Selectors and Specificity

CSS uses **selectors** to target HTML elements.

### Selector Types

#### Element Selector

```css
p {
  font-size: 16px;
}
```

#### Class Selector

```css
.highlight {
  background-color: yellow;
}
```

#### ID Selector

```css
#header {
  font-size: 24px;
}
```

### Specificity Order

```
ID > Class > Element
```

More specific rules override less specific ones.

---

## Styling HTML Elements

Example:

```css
h1 {
  color: #ff5733;
  font-size: 24px;
}
```

Classes allow reusable styling:

```css
.card {
  padding: 16px;
}
```

---

## The CSS Box Model

Every HTML element is treated as a box:

* Content
* Padding
* Border
* Margin

Understanding the box model is essential for layout, spacing, and debugging UI issues.

---

## Responsive Design (Conceptual)

Responsive design ensures applications work across:

* Mobile
* Tablet
* Desktop

This is achieved using:

* Flexible layouts
* Relative units
* Media queries (covered later in depth)

---

## Best Practices and Standards

### HTML Best Practices

* Use semantic elements
* Validate HTML with W3C tools
* Write accessible markup

### CSS Best Practices

* Use external stylesheets
* Avoid inline styles
* Use meaningful class names
* Keep styles modular and readable

### Standards

* HTML and CSS are governed by the **W3C**
* MDN is the primary documentation reference

---

## Conclusion

HTML and CSS form the **visual and structural foundation** of the web. HTML defines *what exists*, while CSS defines *how it looks*. Together, they enable developers to create accessible, maintainable, and user-friendly interfaces.

A strong grasp of HTML and CSS is essential before introducing JavaScript, front-end frameworks, or full stack application architecture. Mastery here will significantly improve your ability to reason about UI behavior, layout issues, and component-driven design later in the curriculum.
