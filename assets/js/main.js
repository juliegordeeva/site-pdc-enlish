(() => {
  const header = document.querySelector(".site-header");
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector("#site-nav");
  const year = document.querySelector("[data-year]");

  if (year) {
    year.textContent = String(new Date().getFullYear());
  }

  const onScroll = () => {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 8);
  };

  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  if (toggle && nav) {
    let lastFocused = null;

    const getFocusable = () => {
      const inNav = [...nav.querySelectorAll('a, button, [tabindex]:not([tabindex="-1"])')];
      return [toggle, ...inNav].filter(
        (el) => el && !el.hasAttribute("disabled") && el.getAttribute("aria-hidden") !== "true"
      );
    };

    const setOpen = (open) => {
      toggle.setAttribute("aria-expanded", String(open));
      nav.classList.toggle("is-open", open);
      document.body.style.overflow = open ? "hidden" : "";

      if (open) {
        lastFocused = document.activeElement;
        const focusable = getFocusable();
        (focusable[0] || nav).focus?.();
      } else if (lastFocused && typeof lastFocused.focus === "function") {
        lastFocused.focus();
        lastFocused = null;
      } else {
        toggle.focus();
      }
    };

    toggle.addEventListener("click", () => {
      const open = toggle.getAttribute("aria-expanded") !== "true";
      setOpen(open);
    });

    nav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => setOpen(false));
    });

    document.addEventListener("keydown", (event) => {
      if (toggle.getAttribute("aria-expanded") !== "true") return;

      if (event.key === "Escape") {
        event.preventDefault();
        setOpen(false);
        return;
      }

      if (event.key !== "Tab") return;

      const focusable = getFocusable();
      if (!focusable.length) return;

      const first = focusable[0];
      const last = focusable[focusable.length - 1];

      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });
  }

  document.querySelectorAll(".person-photo img").forEach((img) => {
    const markFailed = () => {
      img.setAttribute("data-failed", "true");
      img.closest(".person-photo")?.classList.add("is-placeholder");
    };

    if (img.complete && img.naturalWidth === 0) {
      markFailed();
      return;
    }

    img.addEventListener("error", markFailed);
  });

  const CONSENT_PD_KEY = "pdc-consent-pd";
  const CONSENT_MARKETING_KEY = "pdc-consent-marketing";

  const getConsentPd = () => sessionStorage.getItem(CONSENT_PD_KEY) === "1";
  const getConsentMarketing = () => sessionStorage.getItem(CONSENT_MARKETING_KEY) === "1";

  const setConsentPd = (value) => {
    sessionStorage.setItem(CONSENT_PD_KEY, value ? "1" : "0");
  };

  const setConsentMarketing = (value) => {
    sessionStorage.setItem(CONSENT_MARKETING_KEY, value ? "1" : "0");
  };

  const contactsWriteUrl = (() => {
    const path = window.location.pathname || "";
    if (path.endsWith("contacts.html") || path.endsWith("/contacts")) return "#write";
    if (path.includes("/") && !path.endsWith("/") && path.split("/").pop()?.includes(".")) {
      return "contacts.html#write";
    }
    return "contacts.html#write";
  })();

  const consentNotes = (marketing) => {
    const lines = ["I confirm consent to the processing of personal data."];
    if (marketing) lines.push("I agree to receive informational materials.");
    return lines.join("\n");
  };

  const withConsentParams = (href, marketing) => {
    const notes = consentNotes(marketing);

    try {
      if (href.startsWith("mailto:")) {
        const [base, query = ""] = href.split("?");
        const params = new URLSearchParams(query);
        const body = params.get("body") || "";
        params.set("body", body ? `${body}\n\n${notes}` : notes);
        return `${base}?${params.toString()}`;
      }

      if (href.includes("t.me/")) {
        const url = new URL(href);
        const text = url.searchParams.get("text") || "Hello! I am writing from the website.";
        url.searchParams.set("text", `${text}\n\n${notes}`);
        return url.toString();
      }
    } catch (_) {
      return href;
    }

    return href;
  };

  const syncGate = (gate) => {
    const required = gate.querySelector("[data-consent-required]");
    const marketing = gate.querySelector("[data-consent-marketing]");
    const hint = gate.querySelector("[data-consent-hint]");
    const allowed = Boolean(required?.checked);

    if (required) setConsentPd(required.checked);
    if (marketing) setConsentMarketing(marketing.checked);

    gate.querySelectorAll("[data-consent-action]").forEach((action) => {
      action.classList.toggle("is-consent-disabled", !allowed);
      action.setAttribute("aria-disabled", allowed ? "false" : "true");
      if (allowed) {
        action.removeAttribute("tabindex");
      } else {
        action.setAttribute("tabindex", "-1");
      }
    });

    if (hint) hint.hidden = allowed;
  };

  document.querySelectorAll("[data-consent-gate]").forEach((gate) => {
    const required = gate.querySelector("[data-consent-required]");
    const marketing = gate.querySelector("[data-consent-marketing]");

    if (required) required.checked = getConsentPd();
    if (marketing) marketing.checked = getConsentMarketing();

    syncGate(gate);

    gate.addEventListener("change", (event) => {
      if (!(event.target instanceof HTMLInputElement)) return;
      syncGate(gate);
      document.querySelectorAll("[data-consent-gate]").forEach((other) => {
        if (other === gate) return;
        const otherRequired = other.querySelector("[data-consent-required]");
        const otherMarketing = other.querySelector("[data-consent-marketing]");
        if (otherRequired) otherRequired.checked = getConsentPd();
        if (otherMarketing) otherMarketing.checked = getConsentMarketing();
        syncGate(other);
      });

      if (gate.hasAttribute("data-rules-gate") && event.target.hasAttribute("data-consent-required") && event.target.checked) {
        gate.querySelector("[data-rules-doc]")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });

  document.addEventListener("click", (event) => {
    const action = event.target.closest("a[data-consent-action], a[href*='t.me/psydevcenter'], a[href^='mailto:']");
    if (!(action instanceof HTMLAnchorElement)) return;
    if (action.closest(".footer-bottom, .policy, .legal, .consent-lead")) return;

    const isTelegram = action.href.includes("t.me/psydevcenter");
    const isEmail = action.getAttribute("href")?.startsWith("mailto:") || action.href.startsWith("mailto:");
    if (!isTelegram && !isEmail && !action.hasAttribute("data-consent-action")) return;

    const gate = action.closest("[data-consent-gate]");

    if (!getConsentPd()) {
      event.preventDefault();
      if (gate) {
        const hint = gate.querySelector("[data-consent-hint]");
        if (hint) hint.hidden = false;
        gate.querySelector(".consent-panel")?.scrollIntoView({ behavior: "smooth", block: "center" });
        gate.querySelector("[data-consent-required]")?.focus();
        return;
      }
      window.location.href = contactsWriteUrl;
      return;
    }

    const rawHref = action.getAttribute("href") || action.href;
    const next = withConsentParams(rawHref, getConsentMarketing());
    if (next === rawHref) return;

    event.preventDefault();
    if (action.target === "_blank") {
      window.open(next, "_blank", "noopener,noreferrer");
    } else {
      window.location.href = next;
    }
  });

  const filterButtons = document.querySelectorAll(".article-filter");
  const articleCards = document.querySelectorAll(".article-card[data-author]");
  const articlesEmpty = document.querySelector("[data-articles-empty]");

  const applyAuthorFilter = (author) => {
    let visible = 0;
    articleCards.forEach((card) => {
      const match = author === "all" || card.getAttribute("data-author") === author;
      card.hidden = !match;
      if (match) visible += 1;
    });
    filterButtons.forEach((btn) => {
      btn.classList.toggle("is-active", btn.getAttribute("data-author-filter") === author);
    });
    if (articlesEmpty) articlesEmpty.hidden = visible > 0;
  };

  filterButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      applyAuthorFilter(btn.getAttribute("data-author-filter") || "all");
    });
  });

  document.querySelectorAll("[data-author-filter]").forEach((el) => {
    if (el.matches("button.article-filter")) return;
    el.addEventListener("click", () => {
      const author = el.getAttribute("data-author-filter");
      if (!author || !articleCards.length) return;
      applyAuthorFilter(author);
    });
  });
})();
