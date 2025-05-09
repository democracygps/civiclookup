# civiclookup

🌍 Fast, open-source tools to identify your elected representatives by address — starting with the U.S., built for global expansion.

**civiclookup** is an open-source project that helps developers, nonprofits, journalists, and civic technologists find out *who represents a given address* — starting with the United States, and designed to scale globally.

🔍 **What it does (coming soon)**
- Look up U.S. federal legislators (House & Senate) by address
- Built to support international contributions and datasets
- Replaces the retired Google Civic Info Representatives API
- Available in both Python (`pip install civiclookup`) and JavaScript (`npm install civiclookup`)

### 🔄 Replaces the Retired Google Civic Info Representatives API

The original [Google Civic Information API](https://developers.google.com/civic-information) provided a `/representatives` endpoint that let developers look up elected officials by address. That endpoint was **shut down in April 2025**, breaking many civic applications.

**civiclookup** fills that gap by:
- Using the still-operational [`/divisionsByAddress`](https://developers.google.com/civic-information/docs/v2/divisions/divisionsByAddress) endpoint to identify political districts based on a user-provided address.
- Matching those districts to **open-source legislator data** (e.g., [congress-legislators](https://github.com/unitedstates/congress-legislators)) to determine who represents that area.

⚠️ **Note:**
- This tool **requires each user to provide their own Google Civic API key**.
- It depends on the continued availability of Google’s `/divisionsByAddress` endpoint. If that endpoint is discontinued, a replacement data source will be needed.

🌐 **Why this matters**
When citizens don't know who represents them, accountability breaks down. This project aims to make that information universally accessible, free of corporate silos or shutdowns.

📦 **Project Structure**
- `js/` – Lightweight NPM module
- `python/` – PyPI-compatible library
- `docs/` – API documentation and contribution guidelines

🚀 **Planned Features**
- U.S. state and local expansion
- Country modules for Canada, the EU, Australia, and Latin America
- Browser-first widget
- Optional integration with Firestore, SQLite, and other civic data stores

🤝 **How to Contribute**
Want to add your country's representatives or build a new plugin? See [`CONTRIBUTING.md`](CONTRIBUTING.md) (coming soon).

---

### 📘 Acknowledgments

Some portions of this project’s documentation and source code were drafted with the assistance of [ChatGPT](https://openai.com/chatgpt), [Claude](https://claude.ai/), and [Claude Code](https://github.com/anthropics/claude-code) to accelerate development, editing, and clarity. All content has been reviewed and approved by human maintainers before inclusion.

---

### License

[MIT License](LICENSE)

This project is released under the MIT License — you can use it freely in open or commercial software. Contributions welcome.
