# AGENTS.md — VOILA FRAGRANCES

## Purpose

- This file governs coding-agent work in this repository.
- Build a polished, maintainable, static-first fragrance storefront.
- Follow the user's current task before considering future features.
- Prefer small, verifiable changes over broad rewrites.
- Treat design references as guidance, not as source code.

## Project Identity

- Brand: **VOILA FRAGRANCES** (never "VIOLA").
- Primary site language: Turkish.
- Audience: customers shopping for fragrances and related products.
- Current phase: static website design and implementation.
- Payment processing and order handling are future phases.
- Product catalog, prices, photographs, and claims may be provisional.
- Do not present provisional material as confirmed business information.

## Source of Truth

- `assets/reference/build-reference.png`: approved homepage visual reference.
- `assets/reference/Concept_02_Modern_Boutique.png`: secondary style reference.
- `assets/logos/logo.png`: official logo asset for the website.
- Existing working code is the implementation baseline.
- Explicit user instructions override earlier aesthetic suggestions.
- Where references conflict, prefer the approved build reference.
- Where requirements remain unclear, choose a conservative solution.
- State significant assumptions in the handoff summary.

## Visual Direction

- Modern boutique: refined, warm, elegant, and shopping-focused.
- Keep generous but intentional whitespace; avoid awkward empty bands.
- Favor ivory and light beige surfaces with dark, readable text.
- Use the logo's vivid pink sparingly for important accents.
- Use refined serif display typography and clear sans-serif UI text.
- Maintain a consistent spacing scale and typography hierarchy.
- Product photography should lead; decorative UI should not compete.
- Keep the layout orderly without turning it into a generic template.
- Avoid unnecessary badges, carousels, banners, or promotional clutter.
- Match proportions and alignment before polishing tiny details.

## Logo and Header

- Use the provided logo file; do not redraw it without being asked.
- Preserve the logo's original colors and aspect ratio.
- Display one circular logo at the left of the desktop navigation.
- Do not place a second wordmark beside the circular logo.
- Keep the logo fully within the header's height.
- Keep the navigation bar's bottom edge flat and continuous.
- Do not introduce protrusions, cutouts, or decorative header bumps.
- Size the logo modestly, in proportion to the other header elements.
- Ensure the header remains balanced at mobile and tablet widths.

## Stack

- Use semantic HTML5, modern CSS, and minimal vanilla JavaScript.
- No React, Vue, Next.js, Tailwind, Bootstrap, or UI frameworks.
- Do not introduce a build system unless the user requests one.
- Avoid unnecessary npm packages and third-party dependencies.
- Prefer native browser features over custom abstractions.
- Use JavaScript only when behavior requires it.
- Keep the site runnable from a basic local HTTP server.
- Preserve static hosting compatibility.

## Repository Organization

- Inspect the existing tree before creating or moving files.
- Do not reorganize working files without a concrete benefit.
- Keep the homepage at `index.html` unless directed otherwise.
- Keep shared styles in `css/styles.css` when that file exists.
- Keep shared behavior in `js/main.js` when that file exists.
- Keep images under `assets/` in appropriate subdirectories.
- Use stable, descriptive, lowercase, hyphenated asset filenames.
- Keep sample catalog data separate from markup where practical.
- Add directories only when a real feature needs them.
- Do not create empty placeholder modules to anticipate future work.

## Scope and Change Discipline

- Read the current prompt and relevant files before editing.
- Implement only what the requested iteration covers.
- Make the smallest coherent change that solves the problem.
- Reuse established patterns instead of inventing parallel ones.
- Do not replace working code just to enforce personal preferences.
- Avoid unrelated refactors, renames, and formatting churn.
- Never overwrite supplied source images or reference files.
- Never remove user work without explicit authorization.
- Do not create Git commits unless specifically requested.
- Do not run destructive Git commands.
- Do not add license files, badges, or tooling without a reason.
- If blocked, document the specific blocker and safe next action.

## HTML Guidelines

- Use semantic landmarks: `header`, `nav`, `main`, `section`, `footer`.
- Maintain a logical heading hierarchy, starting with one `h1`.
- Use anchors for navigation and buttons for actions.
- Provide descriptive labels for interactive controls.
- Supply meaningful `alt` text for informative images.
- Use empty `alt` text for purely decorative images.
- Associate form labels with their inputs.
- Do not nest interactive elements inside one another.
- Avoid unnecessary wrapper elements.
- Keep metadata, document language, and page title accurate.
- Write clean, readable HTML rather than compressed markup.

## CSS Guidelines

- Define common colors, fonts, spacing, and radii as CSS variables.
- Prefer normal flow, flexbox, and grid over absolute positioning.
- Use fluid widths and reasonable `max-width` constraints.
- Start with robust small-screen behavior; enhance for larger screens.
- Keep selectors shallow and component-focused.
- Use classes for styling; avoid IDs as styling hooks.
- Avoid `!important` except for a documented necessity.
- Avoid unexplained magic numbers and positional hacks.
- Keep transitions subtle and respect reduced-motion preferences.
- Do not force fixed heights on text-heavy sections.
- Make image cropping intentional with `object-fit` where appropriate.
- Verify there is no horizontal scrolling at mobile widths.

## JavaScript Guidelines

- Keep scripts small, modular, and understandable.
- Prefer plain functions and straightforward event handlers.
- Avoid unnecessary classes, state libraries, and clever patterns.
- Query elements defensively when code runs on multiple pages.
- Do not inject untrusted content through `innerHTML`.
- Use `textContent` for text and safe APIs for DOM construction.
- Add keyboard support for custom interactions when unavoidable.
- Avoid global variables unless there is a clear reason.
- Do not log sensitive or customer information.
- Handle absent data and empty states gracefully.
- Avoid blocking page rendering with unnecessary script work.

## Content and Assets

- Write customer-facing interface text in natural Turkish.
- Use the exact brand spelling everywhere: VOILA FRAGRANCES.
- Do not invent product benefits, ingredients, or safety claims.
- Do not invent certifications, customer reviews, or testimonials.
- Do not imply mock products are available for purchase.
- Treat prices and shipping thresholds as placeholders until verified.
- Keep placeholder records easy to replace with real catalog data.
- Do not use competitor branding or proprietary imagery.
- Do not use the entire design reference screenshot as a page image.
- Crop reference art only if it is suitable and contains no baked-in UI.
- Do not stretch, recolor, or distort the official logo.
- Optimize production images without destroying useful detail.
- Use descriptive asset filenames and correct image dimensions.

## Responsive Design

- Design for phone, tablet, laptop, and desktop viewports.
- Ensure primary navigation works on touch devices.
- Make tap targets comfortably usable.
- Keep headings legible without excessive line breaks.
- Let product grids reduce columns as space narrows.
- Keep pricing, titles, and purchase-related actions easy to scan.
- Avoid hover-only interactions.
- Prevent overlays, menus, and modals from trapping content.
- Check that the circular logo never overlaps navigation elements.
- Prefer graceful stacking to shrinking everything to fit.

## Accessibility

- Maintain readable contrast, including on pink buttons.
- Show visible keyboard focus on interactive elements.
- Ensure menus and dialogs can be operated by keyboard.
- Give icon-only buttons accessible names.
- Use real text for important content, not text embedded in images.
- Avoid autoplay motion and flashing decorative effects.
- Respect `prefers-reduced-motion` where animation exists.
- Keep form errors understandable and connected to fields.
- Test at zoomed text sizes when possible.
- Accessibility is part of completion, not a later enhancement.

## Commerce Boundaries

- Static product display is allowed in the current phase.
- Do not integrate payment providers until explicitly requested.
- Do not invent checkout endpoints or order-confirmation behavior.
- Do not label a nonfunctional checkout as operational.
- Disable, omit, or clearly label unavailable purchase actions.
- If a local cart is requested, make its limitations explicit.
- Do not collect personal or payment data in a demo flow.
- Leave provider-specific integration behind a clear boundary.
- Never expose secrets or credentials in client-side files.
- Do not claim legal or tax compliance without verification.

## Security and Privacy

- Treat customer input as untrusted.
- Avoid unsafe string interpolation into HTML.
- Do not embed private addresses, tokens, passwords, or API keys.
- Avoid third-party scripts unless their purpose is justified.
- Use HTTPS URLs for external resources when applicable.
- Avoid unnecessary analytics or tracking.
- Do not invent a privacy policy or terms for the business.
- Flag privacy-sensitive features before implementing them.

## Formatting Guide

- Use UTF-8, LF line endings, and a final newline.
- Indent HTML, CSS, and JavaScript with **2 spaces**; no tabs.
- Aim for lines under 100 characters; wrap when it improves clarity.
- Use double quotes for HTML attribute values.
- Use single quotes for JavaScript strings where practical.
- Use semicolons in JavaScript.
- Use trailing commas in multiline JavaScript objects and arrays.
- Put CSS opening braces on the selector line.
- Put each CSS declaration on its own line, with a semicolon.
- Group related declarations and separate rules with blank lines.
- Use `kebab-case` for CSS classes, filenames, and custom properties.
- Use `camelCase` for JavaScript variables and functions.
- Use `UPPER_SNAKE_CASE` only for genuine constants.
- Prefer descriptive names over abbreviations.
- Keep comments short and focused on *why*, not obvious *what*.
- Match the established style if a file already differs.
- Avoid formatting unrelated files.

## Validation

- Run the simplest available local preview or test command.
- Check for missing assets, broken links, and console errors.
- Verify the homepage against `build-reference.png` at desktop size.
- Inspect at least one narrow mobile width.
- Check keyboard navigation and visible focus states.
- Test menus, buttons, and links that were changed.
- Confirm there is no unintended horizontal overflow.
- Verify Turkish characters display correctly.
- Verify the logo is undistorted and header edge is flat.
- Do not claim tests were performed unless they actually were.
- If visual/browser tooling is unavailable, say so explicitly.

## Handoff Format

- Briefly summarize the implemented change.
- List files created, modified, or deleted.
- State the checks performed and their results.
- Mention remaining design mismatches or limitations.
- Call out any unverified placeholders or assumptions.
- Suggest the next smallest useful iteration if appropriate.
- Keep the summary factual and concise.
- Do not imply that deferred checkout or backend features work.
