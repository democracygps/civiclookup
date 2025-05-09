# Contributing to civiclookup

Thank you for your interest in contributing to **civiclookup** — an open-source project to help people around the world identify their elected representatives by address. We welcome contributions from developers, civic tech advocates, designers, translators, researchers, and more.

This project is designed to start with the U.S. and scale globally through community input. Whether you're fixing a typo, adding a new country’s data, or improving the API, your help is valued.

---

## 🚀 How to Contribute

### 1. Clone the repository

```bash
git clone https://github.com/democracygps/civiclookup.git
cd civiclookup
```

### 2. Set up your development environment

**For Python:**
- Use Python 3.10+
- Install dependencies:

```bash
pip install -r requirements.txt
```

**For JavaScript:**
- Use Node.js 18+
- Install dependencies:

```bash
npm install
```

---

### 🧹 Code Style & Linting

To keep the codebase clean and consistent, please follow these formatting and linting guidelines:

**Python**
- Use [`black`](https://black.readthedocs.io/en/stable/) for auto-formatting
- Run [`flake8`](https://flake8.pycqa.org/) to catch style issues
- Use [`mypy`](http://mypy-lang.org/) for static type checking
- Sort imports using [`isort`](https://pycqa.github.io/isort/)
- Most tools are preconfigured via `pyproject.toml` or `.flake8`

**JavaScript / TypeScript**
- Use [`prettier`](https://prettier.io/) for formatting
- Use [`eslint`](https://eslint.org/) for linting
- Config files: `.prettierrc`, `.eslintrc.json`, etc.

Before submitting a pull request, please run the appropriate formatters and linters to ensure consistency.

---

### 3. Open an issue (optional but encouraged)

Before submitting a pull request (PR), please open a GitHub Issue to:
- Report a bug
- Propose a new feature
- Ask a question or request guidance

This helps prevent duplication and fosters discussion.

### 4. Make your changes

Please:
- Keep your commits focused and descriptive
- Follow existing formatting and style conventions
- Add or update tests if applicable

### 5. Submit a pull request

Once your changes are ready, open a pull request (PR) against the `main` branch. Please:
- Explain your changes clearly
- Link to any related issues
- Be ready to discuss or revise

We’ll review your submission as soon as possible.

---

## 🌐 Unicode and Multilingual Support

This project is intended to be **international and multilingual**. When adding support for names, regions, addresses, or districts outside the English-speaking world, please:

- Use **UTF-8 encoding** and **Unicode-aware text processing** at all times
- Preserve original names, accents, and characters (e.g., “Çáceres”, “São Paulo”, “Ελλάδα”)
- Avoid unnecessary ASCII transliteration
- Favor open datasets in their **native language(s)** when available

If you're unsure how to handle specific characters or formats, just ask — we’re here to help.

---

## 📄 Code of Conduct

By participating in this project, you agree to follow our [Code of Conduct](CODE_OF_CONDUCT.md). We are committed to fostering a welcoming and respectful space for all contributors.

---

## 🙌 Need Help?

If you're not sure where to start:
- Browse [open issues](https://github.com/democracygps/civiclookup/issues)
- Reach out by opening a "question" issue
- Or email the maintainers listed in the repo

We’re glad you’re here. Let’s build something meaningful together.
