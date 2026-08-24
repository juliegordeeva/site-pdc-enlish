# Psy Development Center (English)

Static English website for **Psy Development Center** — Evidence-Based Therapy Centre.

- **Domain:** [https://psydc.world](https://psydc.world)
- **Russian site:** [https://psydc.org](https://psydc.org)
- **Contact:** Telegram [@psydevcenter](https://t.me/psydevcenter) · `s.romanchenko@psydc.org` · +7 (925) 459-88-89

## Pages

| Page | File |
|------|------|
| Home | `index.html` |
| Services | `services.html` |
| Assessments | `diagnostics.html` |
| Programmes | `programs.html` |
| Articles | `articles.html` |
| Team | `team.html` |
| Contact Us | `contacts.html` |
| Privacy Policy | `privacy.html` |
| Consent | `consent.html` |
| Consultation Rules | `consultation-rules.html` |

Routes live at the site root (not under `/en/`).

## Local preview

Open any HTML file in a browser, or serve the folder:

```bash
python3 -m http.server 8080
```

Then visit `http://localhost:8080`.

## Deploy

GitHub Pages (or similar) with custom domain `psydc.world`. The `CNAME` file and `robots.txt` / `sitemap.xml` already use this domain.
