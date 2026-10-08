#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build /ru/ locale on psydc.world and retarget EN language switchers."""
from __future__ import annotations

from pathlib import Path
import re

EN = Path("/Users/prof_jouls/Documents/site PDC EN")
ORG = Path("/Users/prof_jouls/Documents/site PDC")
RU = EN / "ru"
(RU / "articles").mkdir(parents=True, exist_ok=True)


def asset_prefix(depth: int) -> str:
    return "../" * depth


def en_switch_href(en_path: str) -> str:
    if en_path in ("index.html", ""):
        return "/index.html"
    return f"/{en_path}"


def hreflang_block(en_path: str, ru_path: str) -> str:
    en_url = "https://psydc.world/" if en_path in ("index.html", "") else f"https://psydc.world/{en_path}"
    ru_url = "https://psydc.world/ru/" if ru_path == "index.html" else f"https://psydc.world/ru/{ru_path}"
    return (
        f'  <link rel="alternate" hreflang="en" href="{en_url}">\n'
        f'  <link rel="alternate" hreflang="ru" href="{ru_url}">\n'
        f'  <link rel="alternate" hreflang="x-default" href="{en_url}">'
    )


def canonical_ru(ru_path: str) -> str:
    return "https://psydc.world/ru/" if ru_path == "index.html" else f"https://psydc.world/ru/{ru_path}"


NAV_ITEMS = [
    ("index.html", "Главная"),
    ("services.html", "Услуги"),
    ("diagnostics.html", "Диагностика"),
    ("programs.html", "Программы"),
    ("team.html", "Команда"),
    ("articles.html", "Статьи"),
    ("contacts.html", "Контакты"),
]


def ru_header(current: str, depth: int, en_path: str) -> str:
    def nav_href(page: str) -> str:
        return f"../{page}" if depth == 2 else page

    items = []
    for page, label in NAV_ITEMS:
        cur = ' aria-current="page"' if page == current else ""
        items.append(f'          <li><a href="{nav_href(page)}"{cur}>{label}</a></li>')
    return f'''  <a class="skip-link" href="#content">Перейти к содержанию</a>

  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="{nav_href("index.html")}">
        <span class="brand-name">Psy Development Center</span>
        <span class="brand-tag">Центр доказательной терапии</span>
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Открыть меню">
        <span class="nav-toggle-bars" aria-hidden="true"></span>
      </button>
      <nav class="site-nav" id="site-nav" aria-label="Основная навигация">
        <ul class="nav-list">
{chr(10).join(items)}
        </ul>
        <a class="btn btn-primary" href="https://t.me/psydevcenter" rel="noopener noreferrer" target="_blank" aria-label="Записаться в Telegram">Записаться</a>
        <a class="nav-lang" href="{en_switch_href(en_path)}" hreflang="en" lang="en">English</a>
      </nav>
    </div>
  </header>'''


def ru_footer(depth: int) -> str:
    def href(page: str) -> str:
        return f"../{page}" if depth == 2 else page

    p = asset_prefix(depth)
    return f'''  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <div class="footer-brand">Psy Development Center</div>
          <p>Доказательная психологическая помощь</p>
          <p>Очно · Онлайн</p>
          <p class="footer-note">Условия работы и договор согласовываются индивидуально после знакомства.</p>
        </div>
        <div>
          <h2 class="footer-title">Разделы</h2>
          <ul class="footer-list">
            <li><a href="{href("services.html")}">Услуги</a></li>
            <li><a href="{href("diagnostics.html")}">Диагностика</a></li>
            <li><a href="{href("programs.html")}">Программы</a></li>
            <li><a href="{href("team.html")}">Команда</a></li>
            <li><a href="{href("articles.html")}">Статьи</a></li>
            <li><a href="{href("contacts.html")}">Контакты</a></li>
          </ul>
        </div>
        <div>
          <h2 class="footer-title">Связь</h2>
          <ul class="footer-list">
            <li><a href="https://t.me/psydevcenter" rel="noopener noreferrer" target="_blank">Telegram @psydevcenter</a></li>
            <li><a href="mailto:s.romanchenko@psydc.world">s.romanchenko@psydc.world</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>© <span data-year>2026</span> Psy Development Center</p>
        <p>
          <a href="{href("privacy.html")}">Политика обработки персональных данных</a>
          ·
          <a href="{href("consultation-rules.html")}">Правила консультаций</a>
          ·
          <a href="{href("consent.html")}">Согласие на обработку персональных данных</a>
        </p>
      </div>
    </div>
  </footer>

  <script src="{p}assets/js/main.js" defer></script>
</body>
</html>'''


def head_shell(
    title: str,
    description: str,
    ru_path: str,
    en_path: str,
    depth: int,
    extra_head: str = "",
    robots: str | None = None,
    css_query: str = "",
) -> str:
    p = asset_prefix(depth)
    robots_line = f'  <meta name="robots" content="{robots}">\n' if robots else ""
    canon = canonical_ru(ru_path)
    css = f"{p}assets/css/styles.css{css_query}"
    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
{robots_line}  <link rel="canonical" href="{canon}">
{hreflang_block(en_path, ru_path)}
  <meta property="og:type" content="website">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canon}">
  <meta property="og:image" content="https://psydc.world/assets/images/og-cover.svg">
  <meta name="theme-color" content="#7A3F1F">
  <link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
  <link rel="manifest" href="{p}site.webmanifest">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{css}">
{extra_head}</head>
<body>
'''


def extract_main(html: str) -> str:
    m = re.search(r"<main\b[^>]*>.*?</main>", html, re.S | re.I)
    if not m:
        raise ValueError("no main")
    return m.group(0)


def scrub_body(main: str, depth: int) -> str:
    p = asset_prefix(depth)
    main = re.sub(r'(src|href)="assets/', rf'\1="{p}assets/', main)
    main = main.replace("s.romanchenko@psydc.org", "s.romanchenko@psydc.world")
    main = main.replace("https://psydc.org", "https://psydc.world")
    main = main.replace("psydc.org", "psydc.world")
    main = main.replace("«Психология и развитие»", "Psy Development Center")
    main = main.replace("психологического центра «Психология и развитие»", "Psy Development Center")
    main = main.replace("Психология и развитие", "Psy Development Center")
    main = main.replace("центра психологии и развития", "Psy Development Center")
    main = main.replace("Центра психологии и развития", "Psy Development Center")
    main = re.sub(r'<a[^>]*href="tel:[^"]*"[^>]*>.*?</a>', "", main, flags=re.S)
    main = re.sub(r'<p>\s*<a[^>]*href="https://wa\.me/[^"]*"[^>]*>.*?</a>\s*</p>\s*', "", main, flags=re.S)
    main = re.sub(r'<a[^>]*href="https://wa\.me/[^"]*"[^>]*>.*?</a>\s*', "", main, flags=re.S)
    main = main.replace("Обсудить запрос", "Записаться")
    main = main.replace("Очно в Москве", "Очно")
    main = main.replace("Онлайн по всему миру", "Онлайн")
    main = re.sub(
        r"mailto:s\.romanchenko@psydc\.world\?subject=[^\"]+",
        "mailto:s.romanchenko@psydc.world?subject=%D0%97%D0%B0%D1%8F%D0%B2%D0%BA%D0%B0%20%D1%81%20%D1%81%D0%B0%D0%B9%D1%82%D0%B0%20Psy%20Development%20Center",
        main,
    )
    main = main.replace("pravila.html", "consultation-rules.html")
    # Remove Moscow address / map blocks commonly found in org contacts-style content
    main = re.sub(
        r'<p><a href="https://yandex\.ru/maps/[^\"]*"[^>]*>.*?</a></p>\s*',
        "",
        main,
        flags=re.S,
    )
    return main


def write_page(
    out: Path,
    title: str,
    description: str,
    ru_path: str,
    en_path: str,
    current_nav: str,
    depth: int,
    main_html: str,
    extra_head: str = "",
    robots: str | None = None,
    css_query: str = "",
) -> None:
    doc = (
        head_shell(title, description, ru_path, en_path, depth, extra_head, robots, css_query)
        + ru_header(current_nav, depth, en_path)
        + "\n\n"
        + main_html
        + "\n\n"
        + ru_footer(depth)
    )
    out.write_text(doc, encoding="utf-8")
    print(f"wrote {out.relative_to(EN)}")


# ---------- INDEX (org body + EN-style CTA/team) ----------
org_index = (ORG / "index.html").read_text(encoding="utf-8")
index_main = extract_main(org_index)
index_main = scrub_body(index_main, 1)

# Hero CTAs: match EN pattern (Telegram + Contacts), primary Записаться
index_main = re.sub(
    r'<div class="btn-group">\s*<a class="btn btn-primary"[^>]*>.*?</a>\s*<a class="btn btn-secondary"[^>]*>.*?</a>\s*</div>',
    '''<div class="btn-group">
            <a class="btn btn-primary" href="https://t.me/psydevcenter" rel="noopener noreferrer" target="_blank" aria-label="Записаться в Telegram">Записаться</a>
            <a class="btn btn-secondary" href="contacts.html">Контакты</a>
          </div>''',
    index_main,
    count=1,
    flags=re.S,
)

# Hero meta already scrubbed Очно/Онлайн
# Replace team preview cards with EN-style links only
index_main = re.sub(
    r'(<section class="section section-tint-cream" aria-labelledby="team-preview-title">.*?<div class="section-intro">.*?</div>)\s*<div class="grid grid-2">.*?</div>\s*<p style="margin-top: 1\.5rem;">.*?</p>',
    r'''\1
        <p><a class="btn btn-ghost" href="team.html">Познакомиться с командой</a> <a class="btn btn-ghost" href="team.html#history">История</a></p>''',
    index_main,
    count=1,
    flags=re.S,
)

# Final CTA: match EN (Контакты + Записаться), no phone/email buttons
index_main = re.sub(
    r'<div class="btn-group" style="justify-content: center;">.*?</div>\s*</div>\s*</section>\s*</main>',
    '''<div class="btn-group" style="justify-content: center;">
          <a class="btn btn-on-dark" href="contacts.html">Контакты</a>
          <a class="btn btn-on-dark-outline" href="https://t.me/psydevcenter" rel="noopener noreferrer" target="_blank" aria-label="Записаться в Telegram" data-consent-action="telegram">Записаться</a>
        </div>
      </div>
    </section>
  </main>''',
    index_main,
    count=1,
    flags=re.S,
)

# Process step: remove phone mention
index_main = index_main.replace(
    "Вы описываете запрос в Telegram, по телефону или электронной почте.",
    "Вы описываете запрос в Telegram или по электронной почте.",
)

# Online/in person card text if still Moscow-specific
index_main = index_main.replace(
    "Работаем очно в Москве и онлайн с клиентами из разных стран.",
    "Проводим очные встречи и онлайн-сессии.",
)
index_main = index_main.replace(
    "Очно в Москве и онлайн",
    "Очно и онлайн",
)

ld_index = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    "name": "Psy Development Center",
    "alternateName": "Центр доказательной терапии",
    "url": "https://psydc.world/ru/",
    "description": "Психологический центр, который оказывает помощь детям, подросткам и взрослым на основе современных научных данных и клинических рекомендаций.",
    "email": "s.romanchenko@psydc.world",
    "areaServed": ["Очно", "Онлайн"],
    "sameAs": ["https://t.me/psydevcenter"]
  }
  </script>
'''

write_page(
    RU / "index.html",
    "Psy Development Center | Центр доказательной терапии",
    "Доказательная психологическая помощь детям, подросткам, взрослым и семьям. Очно и онлайн.",
    "index.html",
    "index.html",
    "index.html",
    1,
    index_main,
    extra_head=ld_index,
)


# ---------- Generic org-adapted pages ----------
GENERIC = {
    "services.html": (
        "Услуги Psy Development Center",
        "Индивидуальная и семейная психотерапия, поддержка детей и подростков, карьерная диагностика.",
    ),
    "diagnostics.html": (
        "Диагностика — Psy Development Center",
        "Психологическая диагностика развития, эмоционального состояния, поведения и обучения. ADOS-2.",
    ),
    "programs.html": (
        "Программы — Psy Development Center",
        "Антитревожный тренинг, перинатальная поддержка, осознанное родительство и другие программы.",
    ),
    "articles.html": (
        "Статьи — Psy Development Center",
        "Статьи психологов центра для родителей и взрослых.",
    ),
    "404.html": (
        "Страница не найдена — Psy Development Center",
        "Запрашиваемая страница не найдена.",
    ),
}

for fname, (title, desc) in GENERIC.items():
    src = ORG / fname
    main = scrub_body(extract_main(src.read_text(encoding="utf-8")), 1)
    # articles list links stay relative
    current = fname if fname != "404.html" else ""
    write_page(RU / fname, title, desc, fname, fname, current if current in dict(NAV_ITEMS) else "index.html", 1, main)


# Fix 404 nav current (no aria-current)
# Re-write 404 without current on Главная incorrectly — use empty current
main_404 = scrub_body(extract_main((ORG / "404.html").read_text(encoding="utf-8")), 1)
write_page(
    RU / "404.html",
    "Страница не найдена — Psy Development Center",
    "Запрашиваемая страница не найдена.",
    "404.html",
    "404.html",
    "",
    1,
    main_404,
)


# ---------- Articles ----------
for art in ("ados-2-chto-eto.html", "kak-nachat-rabotu-so-sluzhboy.html"):
    src = ORG / "articles" / art
    html = src.read_text(encoding="utf-8")
    title_m = re.search(r"<title>(.*?)</title>", html, re.S)
    desc_m = re.search(r'<meta name="description" content="([^"]*)"', html)
    title = title_m.group(1).strip() if title_m else art
    title = title.replace("Психология и развитие", "Psy Development Center")
    title = title.replace("«Психология и развитие»", "Psy Development Center")
    desc = desc_m.group(1) if desc_m else ""
    desc = desc.replace("Психология и развитие", "Psy Development Center")
    main = scrub_body(extract_main(html), 2)
    # Fix relative links from articles/ to parent ru pages
    main = re.sub(r'href="(?!https?:|mailto:|#|../)([^"]+\.html[^"]*)"', r'href="../\1"', main)
    main = main.replace('href="../articles/', 'href="')
    # article sibling links already basename
    write_page(
        RU / "articles" / art,
        title,
        desc,
        f"articles/{art}",
        f"articles/{art}",
        "articles.html",
        2,
        main,
    )


# ---------- CONTACTS (EN structure, RU copy) ----------
contacts_main = '''  <main id="content">
    <section class="page-hero section-tint-olive">
      <div class="container">
        <div class="split split-photo">
          <div>
            <p class="eyebrow">Контакты</p>
            <h1>Контакты</h1>
            <p class="lead">Как начать работу с центром. Короткое знакомство, где мы ответим на вопросы, уточним запрос и обсудим подходящий формат.</p>
            <p class="contact-routing">Заявки в Telegram принимает координатор психологического центра — Александра Коккинаки. Мы поможем сориентироваться и подскажем следующий шаг.</p>
          </div>
          <figure class="section-photo person-photo-round">
            <img src="../assets/images/team/alexandra-kokkinaki.webp" width="800" height="800" alt="Александра Коккинаки, координатор центра" loading="eager" decoding="async">
          </figure>
        </div>
      </div>
    </section>

    <section class="section section-alt" id="write">
      <div class="container" data-consent-gate>
        <div class="consent-panel">
          <p class="consent-lead">Отправляя сообщение, вы автоматически соглашаетесь с <a href="privacy.html">Политикой обработки персональных данных</a> и <a href="consent.html">Согласием на обработку персональных данных</a>.</p>
          <div class="consent-checks">
            <label class="consent-check consent-check-required">
              <input type="checkbox" name="consent-pd" data-consent-required required>
              <span>Ознакомлен(а) с политикой и согласен(а) на обработку персональных данных <abbr title="обязательно">*</abbr></span>
            </label>
            <label class="consent-check">
              <input type="checkbox" name="consent-marketing" data-consent-marketing>
              <span>Согласен(а) на рассылку информационных материалов</span>
            </label>
          </div>
          <p class="consent-hint" data-consent-hint hidden>Отметьте обязательный пункт, чтобы продолжить</p>
        </div>

        <div class="grid grid-2">
          <a class="card contact-card card-link card-tone-lilac" href="https://t.me/psydevcenter" rel="noopener noreferrer" target="_blank" data-consent-action="telegram">
            <div class="contact-label">Telegram</div>
            <div class="contact-value">@psydevcenter</div>
            <p>Основной способ быстро обсудить запрос. Обычно отвечаем в течение 24 часов.</p>
          </a>
          <a class="card contact-card card-link card-tone-rose" href="mailto:s.romanchenko@psydc.world?subject=%D0%97%D0%B0%D1%8F%D0%B2%D0%BA%D0%B0%20%D1%81%20%D1%81%D0%B0%D0%B9%D1%82%D0%B0%20Psy%20Development%20Center" title="Откроется ваша почтовая программа с готовым письмом" data-consent-action="email">
            <div class="contact-label">Email</div>
            <div class="contact-value">s.romanchenko@psydc.world</div>
            <p>Откроется ваш почтовый клиент с готовым письмом. Напишите, если хотите подробно описать ситуацию.</p>
          </a>
          <article class="card card-tone-sand">
            <div class="contact-label">Встречи</div>
            <div class="contact-value">Очно и онлайн</div>
            <p>Проводим очные встречи и онлайн-сессии.</p>
          </article>
        </div>
        <p class="contact-terms">Условия работы и договор согласовываются индивидуально после знакомства.</p>
        <p class="emergency-note">Центр не оказывает экстренную психологическую или медицинскую помощь. При угрозе жизни обращайтесь в экстренные службы.</p>
      </div>
    </section>
  </main>'''

write_page(
    RU / "contacts.html",
    "Контакты Psy Development Center",
    "Связаться с Psy Development Center: Telegram и email. Очно и онлайн.",
    "contacts.html",
    "contacts.html",
    "contacts.html",
    1,
    contacts_main,
)


# ---------- TEAM (translate EN world team) ----------
team_main = '''  <main id="content">
    <section class="page-hero section-tint-cream">
      <div class="container">
        <p class="eyebrow">Команда</p>
        <h1>Наша команда</h1>
        <p class="lead">Специалисты центра сочетают клиническую, исследовательскую, образовательную и практическую экспертизу.</p>
        <p class="contact-routing">Заявки принимает координатор центра в Telegram — Александра Коккинаки. Напишите общее сообщение — мы поможем сориентироваться и подскажем подходящий формат. Это не личный чат с выбранным специалистом.</p>
      </div>
    </section>

    <section class="section section-tint-cream" aria-labelledby="team-title">
      <div class="container">
        <div class="section-intro">
          <h2 id="team-title">Команда</h2>
        </div>
        <div class="team-profiles">
          <article class="card person-card card-tone-lilac team-profile">
            <div class="person-photo photo-tone-lilac" data-initials="AD">
              <img src="../assets/images/team/alex-desatnikov.jpg?v=20260831c" alt="Dr. Alex Desatnik" width="660" height="1011" loading="lazy" onerror="this.setAttribute('data-failed','true')">
            </div>
            <div class="team-profile-copy">
              <h2>Dr. Alex Desatnik</h2>
              <p>Dr. Alex Desatnik — клинический психолог, консультант и старший исследователь из Лондона (Великобритания). Более двадцати лет он работает в области ментализационно-ориентированной терапии (MBT), психического здоровья подростков и вмешательств в системе «родитель–ребёнок». Он соединяет современные академические исследования с клинической практикой, работая с семьями, образовательными учреждениями и корпоративными организациями по всему миру.</p>
              <h3>Профессиональный опыт и статусы</h3>
              <ul>
                <li><strong>Клинический психолог и психотерапевт</strong> — частная практика и международное клиническое консультирование.</li>
                <li><strong>Старший исследователь и академический специалист</strong> — сотрудничество с ведущими мировыми институтами, включая University College London (UCL) и Anna Freud National Centre for Children and Families.</li>
                <li><strong>Сертифицированный практик и тренер MBT</strong> — специалист по ментализационно-ориентированной терапии для подростков (MBT-A) и семей (MBT-F) с 2008 года.</li>
                <li><strong>Организационный консультант и executive-коуч</strong> — консультирует руководителей, применяя психологические принципы к динамике команд и развитию лидерства.</li>
              </ul>
            </div>
          </article>

          <article class="card person-card card-tone-sand team-profile">
            <div class="person-photo photo-tone-sand" data-initials="YD">
              <img src="../assets/images/team/yulia-desyatnikova.jpg" alt="Yulia Desiatnikova" width="682" height="1024" loading="lazy" onerror="this.setAttribute('data-failed','true')">
            </div>
            <div class="team-profile-copy">
              <h2>Yulia Desiatnikova</h2>
              <p>Yulia Desiatnikova — практикующий психолог, международный образовательный новатор, бизнес-консультант и executive-коуч из Лондона (Великобритания). Более 30 лет она работает в сфере премиального образования и прикладной психологии и известна как основатель London Gates Education Group и Русской гимназии №1. Юлия соединяет глубокую психологическую экспертизу с развитием организаций, помогая владельцам бизнеса и руководителям решать управленческие задачи, выстраивать эффективные команды и находить баланс между работой и жизнью.</p>
              <h3>Профессиональный опыт и статусы</h3>
              <ul>
                <li><strong>Основатель и CEO, London Gates Education Group</strong> — создала сеть премиальных международных образовательных центров, готовящих студентов к поступлению в ведущие университеты (включая Oxford, Cambridge, Yale и Stanford).</li>
                <li><strong>Executive-коуч и бизнес-консультант</strong> — консультирует топ-менеджеров, предпринимателей и международных лидеров.</li>
                <li><strong>Практикующий психолог и психотерапевт</strong> — более трёх десятилетий консультативной практики: системная динамика, семейная психология и индивидуальное развитие.</li>
                <li><strong>Образовательный новатор</strong> — сооснователь одной из первых частных школ в постсоветской Москве и пионер языкового погружения и креативных образовательных форматов для детей на международном уровне.</li>
              </ul>
            </div>
          </article>

          <article class="card person-card card-tone-rose team-profile">
            <div class="person-photo photo-tone-rose" data-initials="AM">
              <img src="../assets/images/team/anna-malinovski.jpg" alt="Anna Malinovski" width="791" height="1024" loading="lazy" onerror="this.setAttribute('data-failed','true')">
            </div>
            <div class="team-profile-copy">
              <h2>Anna Malinovski</h2>
              <p>Anna Malinovski — лицензированный клинический психолог, специалист по КПТ и образовательной психической поддержке из Израиля. Более десяти лет клинической практики: психологическая диагностика, индивидуальная терапия и научно обоснованные вмешательства для подростков, молодых взрослых и родителей. В работе она соединяет когнитивно-поведенческие подходы с системной семейной динамикой, помогая клиентам проживать возрастные переходы, эмоциональную дисрегуляцию и трудности в отношениях. Анна гибко сочетает школьную психологическую поддержку и частную клиническую практику.</p>
              <h3>Профессиональный опыт и статусы</h3>
              <ul>
                <li><strong>Лицензированный клинический психолог</strong> — официальная регистрация и лицензия Министерства здравоохранения Израиля (Misrad HaBriut).</li>
                <li><strong>КПТ-психотерапевт</strong> — сертифицированный практик когнитивно-поведенческой терапии при тревожных и поведенческих трудностях.</li>
                <li><strong>Образовательный и школьный психолог</strong> — специалист по школьным вмешательствам, кризисной поддержке и психообразованию для сотрудников.</li>
                <li><strong>Консультант по родительству и ведущая групп</strong> — терапевтические мастерские, группы поддержки родителей и семейное консультирование.</li>
              </ul>
            </div>
          </article>

          <article class="card person-card card-tone-olive team-profile">
            <div class="person-photo photo-tone-olive" data-initials="KM">
              <img src="../assets/images/team/ksenia-makarova.jpg" alt="Ksenia Makarova" width="824" height="1024" loading="lazy" onerror="this.setAttribute('data-failed','true')">
            </div>
            <div class="team-profile-copy">
              <h2>Ksenia Makarova</h2>
              <p>Ksenia Makarova — клинический психолог, специалист по КПТ и детскому развитию из Москвы. Более 13 лет клинической практики: психологическое консультирование, когнитивно-поведенческие вмешательства и эмоциональная регуляция у детей, подростков и их семей. Ксения помогает семьям проходить возрастные кризисы, эмоциональное выгорание, тревогу и нейроотличность (включая СДВГ и РАС), выстраивая общение и взаимопонимание между родителями и детьми.</p>
              <h3>Профессиональный опыт и статусы</h3>
              <ul>
                <li><strong>Клинический психолог и КПТ-терапевт</strong> — доказательная индивидуальная и семейная психотерапия.</li>
                <li><strong>Специалист по психическому здоровью детей и подростков</strong> — нейроразвитие, управление тревогой и навыки совладания.</li>
                <li><strong>Родительский коуч и консультант</strong> — группы поддержки родителей, помощь при эмоциональном выгорании и системных семейных кризисах.</li>
              </ul>
            </div>
          </article>

          <article class="card person-card card-tone-sand team-profile">
            <div class="person-photo photo-tone-sand" data-initials="SR">
              <img src="../assets/images/team/svetlana-romanchenko.jpg" alt="Svetlana Romanchenko" width="728" height="1024" loading="lazy" onerror="this.setAttribute('data-failed','true')">
            </div>
            <div class="team-profile-copy">
              <h2>Svetlana Romanchenko</h2>
              <p>Svetlana Romanchenko — клинический психолог, специалист по ДБТ/КПТ и терапевт детей и подростков из Москвы. Работает с нейроотличностью, психологией развития и доказательной психотерапией с клиентами от 5 до 45 лет и их семьями. Клиническая практика направлена на сложные эмоциональные и поведенческие трудности через индивидуализированные, бережные и структурированные когнитивно-поведенческие подходы. Консультирует на русском и английском языках.</p>
              <h3>Профессиональный опыт и статусы</h3>
              <ul>
                <li><strong>Клинический психолог и детский психотерапевт</strong> — поддержка развития, эмоциональная регуляция и кризисная помощь.</li>
                <li><strong>Сертифицированный ДБТ- и КПТ-терапевт</strong> — диалектическая поведенческая терапия (ДБТ) и когнитивно-поведенческая терапия (КПТ) для детей, подростков и взрослых.</li>
                <li><strong>Специалист по нейроотличности</strong> — поддержка, социальная адаптация и терапия при РАС и СДВГ.</li>
                <li><strong>Член Ассоциации специалистов КПТ</strong></li>
              </ul>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section class="section section-tint-olive" id="history" aria-labelledby="history-title">
      <div class="container">
        <div class="split split-photo">
          <div>
            <div class="section-intro">
              <h2 id="history-title">История</h2>
            </div>
            <div class="history-prose">
              <p>Юлия Десятникова более 40 лет работает в сфере детского образования и считает, что самое важное, что мы можем дать детям, — свободу выбирать свой путь. Её проекты связаны с билингвизмом, международными программами и навыками будущего и объединяют сотни людей по всему миру.</p>
              <p>В 2017 году стало очевидно, что доказательной психологии в России всё ещё мало. Юлия Десятникова решила создать пространство для доказательной детской психологии.</p>
              <p>Психологический центр изначально возник как служба внутри образовательного центра LGEG, где психологическая экспертиза лежит в основе работы с людьми и программами.</p>
              <p>С первого дня клиническую работу вела Ксения Макарова. Первыми направлениями стали консультации по управлению тревогой, которые помогали детям справляться с экзаменационной тревогой и остаются востребованными до сих пор. Затем команда развила карьерную диагностику, чтобы подросткам было проще исследовать профессиональные пути.</p>
              <p>На каждом этапе — от первых наблюдений до сложных случаев — специалисты работали под постоянной супервизией. Этот принцип сохранял качество даже при росте нагрузки и появлении новых направлений.</p>
              <p>Юлия Десятникова заложила основу доказательного подхода к психологической помощи, а Ксения Макарова воплотила его в клинической практике — для детей и взрослых. То, что начиналось как поддержка обучения, выросло в психологический центр.</p>
            </div>
          </div>
          <figure class="section-photo">
            <img src="../assets/images/sections/history.webp" width="1280" height="914" alt="Юлия Десятникова, основатель центра" loading="lazy" decoding="async">
          </figure>
        </div>
      </div>
    </section>

  </main>'''

ld_team = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {"@type": "Person", "name": "Dr. Alex Desatnik", "jobTitle": "Clinical Psychologist"},
      {"@type": "Person", "name": "Yulia Desiatnikova", "jobTitle": "Practicing Psychologist"},
      {"@type": "Person", "name": "Anna Malinovski", "jobTitle": "Clinical Psychologist"},
      {"@type": "Person", "name": "Ksenia Makarova", "jobTitle": "Clinical Psychologist"},
      {"@type": "Person", "name": "Svetlana Romanchenko", "jobTitle": "Clinical Psychologist"}
    ]
  }
  </script>
'''

write_page(
    RU / "team.html",
    "Специалисты Psy Development Center",
    "Команда Psy Development Center: Dr. Alex Desatnik, Yulia Desiatnikova, Anna Malinovski, Ksenia Makarova и Svetlana Romanchenko.",
    "team.html",
    "team.html",
    "team.html",
    1,
    team_main,
    extra_head=ld_team,
    css_query="?v=20260831b",
)


# ---------- PRIVACY ----------
privacy_main = '''  <main id="content">
    <section class="section section-tint-cream">
      <div class="container legal">
        <header class="section-intro">
          <h1>Политика обработки персональных данных</h1>
          <p class="lead">Действующая редакция для сайта Psy Development Center (psydc.world).</p>
        </header>

        <div class="policy">
          <h2>1. Общие положения</h2>
          <p>1.1. Настоящая Политика обработки персональных данных разработана в соответствии с Федеральным законом от 27.07.2006 №&nbsp;152-ФЗ «О персональных данных» и определяет порядок обработки персональных данных оператором сайта Psy Development Center — индивидуальным предпринимателем Романченко Светланой Александровной (ИНН&nbsp;761106606366, ОГРНИП&nbsp;323762700057080; контакт для обращений по персональным данным: <a href="mailto:sar.romanchenko@gmail.com">sar.romanchenko@gmail.com</a>) (далее — «Оператор»).</p>
          <p>1.2. Политика действует в отношении всех персональных данных, которые Оператор получает от пользователей сайта <a href="https://psydc.world/ru/">psydc.world</a> (далее — «Сайт»).</p>
          <p>1.3. Использование Сайта означает согласие пользователя с настоящей Политикой. Отправляя сообщение через Telegram или электронную почту с Сайта, пользователь подтверждает ознакомление с Политикой и даёт согласие на обработку персональных данных (обязательная отметка на Сайте). Согласие на рассылку информационных материалов запрашивается отдельно и не является обязательным.</p>

          <h2>2. Состав персональных данных</h2>
          <p>Оператор обрабатывает следующие данные, предоставляемые пользователем при обращении через Сайт: имя, номер телефона, адрес электронной почты, а также иные сведения, которые пользователь добровольно указывает в тексте обращения.</p>

          <h2>3. Цели обработки</h2>
          <ul class="policy-list">
            <li>обработка заявок и обращений, поступивших через Сайт;</li>
            <li>связь с пользователем для уточнения запроса и согласования формата работы;</li>
            <li>направление информационных и рекламных рассылок — только при отдельном согласии пользователя (необязательная отметка на Сайте).</li>
          </ul>

          <h2>4. Способ сбора данных</h2>
          <p>Данные передаются пользователем напрямую на электронную почту Оператора (<a href="mailto:sar.romanchenko@gmail.com">sar.romanchenko@gmail.com</a>) либо через обращение в Telegram посредством почтового/мессенджер-клиента при отправке сообщения с Сайта. Перед отправкой пользователь подтверждает ознакомление с Политикой и согласие на обработку персональных данных обязательной отметкой на Сайте. Сторонние сервисы для приёма и обработки заявок (включая таблицы, CRM и конструкторы форм) Оператором не используются.</p>

          <h2>5. Передача третьим лицам</h2>
          <p>Персональные данные не передаются третьим лицам для обработки заявок. Сторонние сервисы веб-аналитики и cookie-файлы для отслеживания поведения пользователей на Сайте не используются. Трансграничная передача персональных данных Оператором не осуществляется. Обращение пользователя уходит из его почтового клиента напрямую на указанный адрес электронной почты Оператора.</p>

          <h2>6. Срок хранения</h2>
          <p>Персональные данные хранятся до отзыва согласия пользователем либо до достижения цели обработки.</p>

          <h2>7. Права пользователя</h2>
          <p>Пользователь вправе отозвать согласие на обработку персональных данных, запросить информацию об обработке своих данных, а также требовать их уточнения или удаления, направив письмо на адрес <a href="mailto:sar.romanchenko@gmail.com">sar.romanchenko@gmail.com</a>.</p>

          <h2>8. Контакты Оператора</h2>
          <p>
            Psy Development Center<br>
            Оператор: ИП Романченко Светлана Александровна<br>
            ОГРНИП: 323762700057080<br>
            ИНН: 761106606366<br>
            Email: <a href="mailto:s.romanchenko@psydc.world">s.romanchenko@psydc.world</a><br>
            Сайт: <a href="https://psydc.world/ru/">psydc.world</a>
          </p>
        </div>

        <p class="policy-actions">
          <a class="btn btn-secondary" href="contacts.html">Вернуться к контактам</a>
        </p>
      </div>
    </section>
  </main>'''

write_page(
    RU / "privacy.html",
    "Политика обработки персональных данных — Psy Development Center",
    "Политика обработки персональных данных Psy Development Center.",
    "privacy.html",
    "privacy.html",
    "",
    1,
    privacy_main,
)


# ---------- CONSENT ----------
consent_main = '''  <main id="content">
    <section class="section section-tint-cream">
      <div class="container legal">
        <header class="section-intro">
          <h1>Согласие на обработку персональных данных</h1>
        </header>

        <div class="policy">
          <p>Я, субъект персональных данных, в соответствии с Федеральным законом от 27.07.2006 №&nbsp;152-ФЗ «О персональных данных» даю согласие оператору сайта Psy Development Center — индивидуальному предпринимателю Романченко Светлане Александровне (ИНН&nbsp;761106606366, ОГРНИП&nbsp;323762700057080; контакт: <a href="mailto:sar.romanchenko@gmail.com">sar.romanchenko@gmail.com</a>) на обработку моих персональных данных на следующих условиях:</p>

          <h2>1. Перечень данных</h2>
          <p>Имя, номер телефона, адрес электронной почты, а также иные сведения, которые я добровольно указываю в тексте обращения.</p>

          <h2>2. Цели обработки</h2>
          <p>Обработка заявки, поступившей через сайт <a href="https://psydc.world/ru/">psydc.world</a>, связь со мной для уточнения деталей и оказания услуг; направление рассылок — только при отдельном (необязательном) согласии.</p>

          <h2>3. Способ обработки</h2>
          <p>Данные передаются мной напрямую на электронную почту Оператора (<a href="mailto:sar.romanchenko@gmail.com">sar.romanchenko@gmail.com</a>) либо через обращение в Telegram через мой собственный клиент при отправке сообщения с сайта. Перед отправкой я подтверждаю ознакомление с Политикой и согласие на обработку персональных данных обязательной отметкой на сайте. Согласие на рассылку информационных материалов даётся отдельно (необязательная отметка) и не требуется для отправки обращения. Согласие на обработку персональных данных считается предоставленным в момент отправки сообщения при наличии обязательной отметки. Сторонние сервисы приёма заявок и таблицы для сбора данных не используются.</p>

          <h2>4. Срок действия</h2>
          <p>Согласие действует до его отзыва мной или до достижения цели обработки.</p>

          <h2>5. Порядок отзыва</h2>
          <p>Согласие может быть отозвано в любой момент путём направления письма на адрес <a href="mailto:sar.romanchenko@gmail.com">sar.romanchenko@gmail.com</a>.</p>

          <h2>6. Сведения об Операторе</h2>
          <p>
            ИП Романченко Светлана Александровна<br>
            ОГРНИП: 323762700057080<br>
            ИНН: 761106606366<br>
            Email: <a href="mailto:sar.romanchenko@gmail.com">sar.romanchenko@gmail.com</a><br>
            Сайт: <a href="https://psydc.world/ru/">psydc.world</a>
          </p>
        </div>

        <p class="policy-actions">
          <a class="btn btn-secondary" href="contacts.html">Вернуться к контактам</a>
        </p>
      </div>
    </section>
  </main>'''

write_page(
    RU / "consent.html",
    "Согласие на обработку персональных данных — Psy Development Center",
    "Согласие на обработку персональных данных Psy Development Center.",
    "consent.html",
    "consent.html",
    "",
    1,
    consent_main,
)


# ---------- CONSULTATION RULES (from pravila, world-adapted) ----------
rules_main = '''  <main id="content">
    <section class="page-hero section-tint-olive">
      <div class="container rules-wrap">
        <p class="eyebrow">Для клиентов</p>
        <h1>Правила проведения консультаций</h1>
        <p class="lead">Отметьте согласие — после этого откроются условия встреч: формат, оплата, отмена и конфиденциальность.</p>
      </div>
    </section>

    <section class="section section-alt">
      <div class="container rules-wrap" data-consent-gate data-rules-gate>
        <div class="consent-panel">
          <p class="consent-lead">Чтобы открыть правила, подтвердите согласие с <a href="privacy.html">Политикой обработки персональных данных</a> и <a href="consent.html">Согласием на обработку персональных данных</a>.</p>
          <div class="consent-checks">
            <label class="consent-check consent-check-required">
              <input type="checkbox" name="consent-pd" data-consent-required required>
              <span>Ознакомлен(а) с политикой и согласен(а) на обработку персональных данных <abbr title="обязательно">*</abbr></span>
            </label>
          </div>
          <p class="consent-hint" data-consent-hint>Отметьте обязательный пункт, чтобы открыть правила консультаций.</p>
        </div>

        <article class="rules-doc card card-tone-sand" data-rules-doc aria-live="polite">
          <h2>Условия встреч</h2>
          <dl class="rules-facts">
            <div>
              <dt>Длительность встречи</dt>
              <dd>50 минут</dd>
            </div>
            <div>
              <dt>Формат занятия</dt>
              <dd>Очно в центре. Онлайн на платформе Zoom</dd>
            </div>
          </dl>

          <h3>Правила проведения консультаций</h3>
          <ul class="list-check">
            <li>Чтобы мы могли спокойно планировать работу и сохранять время для каждого клиента, консультации проводятся по предварительной оплате.</li>
            <li>Счёт направляется на электронную почту заранее. Пожалуйста, оплатите его не позднее чем за 24 часа до назначенной встречи. Если оплата не поступает в этот срок, мы будем вынуждены снять бронь времени.</li>
            <li>Если вам необходимо отменить или перенести консультацию, пожалуйста, сообщите об этом минимум за 24 часа до её начала. При более поздней отмене или переносе консультация оплачивается полностью — это связано с тем, что специалист заранее резервирует это время именно для вас.</li>
            <li>При необходимости мы можем договориться о ежемесячном выставлении одного счёта за уже проведённые занятия с полным перечнем услуг. При этом встречи, отменённые менее чем за 24 часа до начала, также включаются в счёт.</li>
            <li>Для контроля качества работы и безопасности клиентов консультации могут записываться на видео. Если вы не согласны на запись, пожалуйста, заранее сообщите об этом координатору.</li>
            <li>Всё, что обсуждается на консультациях, остаётся конфиденциальным между клиентом и психологическим центром. Исключение составляют ситуации, в которых возникает риск для жизни или здоровья ребёнка: в таком случае мы незамедлительно проинформируем родителей.</li>
          </ul>

          <p>Если у вас появятся вопросы, пожалуйста, свяжитесь со мной любым удобным способом.</p>

          <div class="rules-sign">
            <div class="person-photo photo-tone-olive" data-initials="АК">
              <img src="../assets/images/team/alexandra-kokkinaki.webp" alt="Александра Коккинаки" width="400" height="400" loading="lazy" onerror="this.setAttribute('data-failed','true')">
            </div>
            <div>
              <p class="rules-sign-name">Александра</p>
              <p class="person-role">координатор Psy Development Center</p>
              <p><a href="https://t.me/psydevcenter" rel="noopener noreferrer" target="_blank">Telegram: @psydevcenter</a></p>
            </div>
          </div>
        </article>
      </div>
    </section>
  </main>'''

write_page(
    RU / "consultation-rules.html",
    "Правила проведения консультаций — Psy Development Center",
    "Правила проведения консультаций Psy Development Center: формат, оплата, отмена и конфиденциальность.",
    "consultation-rules.html",
    "consultation-rules.html",
    "",
    1,
    rules_main,
    robots="noindex, nofollow",
)


# ---------- Update EN pages: nav-lang + hreflang ----------
EN_MAP = {
    "index.html": ("/ru/", "https://psydc.world/ru/"),
    "services.html": ("/ru/services.html", "https://psydc.world/ru/services.html"),
    "diagnostics.html": ("/ru/diagnostics.html", "https://psydc.world/ru/diagnostics.html"),
    "programs.html": ("/ru/programs.html", "https://psydc.world/ru/programs.html"),
    "team.html": ("/ru/team.html", "https://psydc.world/ru/team.html"),
    "articles.html": ("/ru/articles.html", "https://psydc.world/ru/articles.html"),
    "contacts.html": ("/ru/contacts.html", "https://psydc.world/ru/contacts.html"),
    "privacy.html": ("/ru/privacy.html", "https://psydc.world/ru/privacy.html"),
    "consent.html": ("/ru/consent.html", "https://psydc.world/ru/consent.html"),
    "consultation-rules.html": ("/ru/consultation-rules.html", "https://psydc.world/ru/consultation-rules.html"),
    "404.html": ("/ru/404.html", "https://psydc.world/ru/404.html"),
    "articles/ados-2-chto-eto.html": (
        "/ru/articles/ados-2-chto-eto.html",
        "https://psydc.world/ru/articles/ados-2-chto-eto.html",
    ),
    "articles/kak-nachat-rabotu-so-sluzhboy.html": (
        "/ru/articles/kak-nachat-rabotu-so-sluzhboy.html",
        "https://psydc.world/ru/articles/kak-nachat-rabotu-so-sluzhboy.html",
    ),
}

for rel, (nav_href, hreflang_ru) in EN_MAP.items():
    path = EN / rel
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r'<link rel="alternate" hreflang="ru" href="https://psydc\.org[^"]*">',
        f'<link rel="alternate" hreflang="ru" href="{hreflang_ru}">',
        text,
    )
    text = re.sub(
        r'<a class="nav-lang" href="https://psydc\.org[^"]*" hreflang="ru" lang="ru">Русский</a>',
        f'<a class="nav-lang" href="{nav_href}" hreflang="ru" lang="ru">Русский</a>',
        text,
    )
    # residual org urls
    if "psydc.org" in text:
        text = text.replace("https://psydc.org/", "https://psydc.world/ru/")
        text = text.replace("https://psydc.org", "https://psydc.world")
        text = text.replace("psydc.org", "psydc.world")
    path.write_text(text, encoding="utf-8")
    print(f"updated EN {rel}")


# ---------- sitemap ----------
sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://psydc.world/</loc></url>
  <url><loc>https://psydc.world/services.html</loc></url>
  <url><loc>https://psydc.world/diagnostics.html</loc></url>
  <url><loc>https://psydc.world/programs.html</loc></url>
  <url><loc>https://psydc.world/team.html</loc></url>
  <url><loc>https://psydc.world/articles.html</loc></url>
  <url><loc>https://psydc.world/articles/ados-2-chto-eto.html</loc></url>
  <url><loc>https://psydc.world/articles/kak-nachat-rabotu-so-sluzhboy.html</loc></url>
  <url><loc>https://psydc.world/contacts.html</loc></url>
  <url><loc>https://psydc.world/privacy.html</loc></url>
  <url><loc>https://psydc.world/consent.html</loc></url>
  <url><loc>https://psydc.world/consultation-rules.html</loc></url>
  <url><loc>https://psydc.world/ru/</loc></url>
  <url><loc>https://psydc.world/ru/services.html</loc></url>
  <url><loc>https://psydc.world/ru/diagnostics.html</loc></url>
  <url><loc>https://psydc.world/ru/programs.html</loc></url>
  <url><loc>https://psydc.world/ru/team.html</loc></url>
  <url><loc>https://psydc.world/ru/articles.html</loc></url>
  <url><loc>https://psydc.world/ru/articles/ados-2-chto-eto.html</loc></url>
  <url><loc>https://psydc.world/ru/articles/kak-nachat-rabotu-so-sluzhboy.html</loc></url>
  <url><loc>https://psydc.world/ru/contacts.html</loc></url>
  <url><loc>https://psydc.world/ru/privacy.html</loc></url>
  <url><loc>https://psydc.world/ru/consent.html</loc></url>
  <url><loc>https://psydc.world/ru/consultation-rules.html</loc></url>
</urlset>
'''
(EN / "sitemap.xml").write_text(sitemap, encoding="utf-8")
print("updated sitemap.xml")


# ---------- main.js lang-aware consent notes ----------
js_path = EN / "assets" / "js" / "main.js"
js = js_path.read_text(encoding="utf-8")
old = '''  const consentNotes = (marketing) => {
    const lines = ["I confirm consent to the processing of personal data."];
    if (marketing) lines.push("I agree to receive informational materials.");
    return lines.join("\\n");
  };'''
new = '''  const isRu = (document.documentElement.lang || "").toLowerCase().startsWith("ru");
  const consentNotes = (marketing) => {
    const lines = isRu
      ? ["Подтверждаю согласие на обработку персональных данных."]
      : ["I confirm consent to the processing of personal data."];
    if (marketing) {
      lines.push(
        isRu
          ? "Согласен(а) на получение информационных материалов."
          : "I agree to receive informational materials."
      );
    }
    return lines.join("\\n");
  };'''
# also localize default telegram greeting
old_hello = 'const text = url.searchParams.get("text") || "Hello! I am writing from the website.";'
new_hello = 'const text = url.searchParams.get("text") || (isRu ? "Здравствуйте! Пишу с сайта." : "Hello! I am writing from the website.");'
if old not in js:
    raise SystemExit("consentNotes block not found")
js = js.replace(old, new).replace(old_hello, new_hello)
# Fix contactsWriteUrl for /ru/ nested paths — when in /ru/articles/, contacts should be ../contacts.html
# Existing logic uses contacts.html#write relative which works for /ru/*.html; for articles depth=2 relative contacts.html is wrong.
# Improve:
old_contacts = '''  const contactsWriteUrl = (() => {
    const path = window.location.pathname || "";
    if (path.endsWith("contacts.html") || path.endsWith("/contacts")) return "#write";
    if (path.includes("/") && !path.endsWith("/") && path.split("/").pop()?.includes(".")) {
      return "contacts.html#write";
    }
    return "contacts.html#write";
  })();'''
new_contacts = '''  const contactsWriteUrl = (() => {
    const path = window.location.pathname || "";
    if (path.endsWith("contacts.html") || path.endsWith("/contacts")) return "#write";
    const parts = path.split("/").filter(Boolean);
    const inArticles = parts.includes("articles");
    const prefix = inArticles ? "../" : "";
    return `${prefix}contacts.html#write`;
  })();'''
if old_contacts in js:
    js = js.replace(old_contacts, new_contacts)
js_path.write_text(js, encoding="utf-8")
print("updated main.js")

print("DONE")
