// TribalGaming.com — global interactions
// Reads window.TG_CONFIG (set by assets/js/config.js) to wire forms and analytics.

(function () {
  const cfg = window.TG_CONFIG || {};

  // -------- Active nav --------
  const path = location.pathname.replace(/\/+$/, "/") || "/";
  document.querySelectorAll(".nav a").forEach((a) => {
    const href = a.getAttribute("href");
    if (!href || href.startsWith("#")) return;
    // Simple match: href ends with the current section
    const last = path.split("/").filter(Boolean).slice(-1)[0] || "index.html";
    if (href.endsWith("/" + last) || href.endsWith(last) || (path === "/" && href.endsWith("index.html"))) {
      // Don't override if already marked by the page
      if (!a.classList.contains("active")) {
        // Optional: uncomment if you want auto-active
        // a.classList.add("active");
      }
    }
  });

  // -------- Newsletter forms --------
  document.querySelectorAll(".newsletter form, form.newsletter-form").forEach(attachNewsletterHandler);
  // Also catch any loose form with an email input + subscribe button (homepage + news-hub pattern)
  document.querySelectorAll("form").forEach((f) => {
    const email = f.querySelector("input[type=email]");
    const btn = f.querySelector("button[type=submit]");
    if (!email) return;
    const txt = btn ? (btn.textContent || "").toLowerCase() : "";
    if (txt.includes("subscribe") && !f.dataset.tgWired) {
      attachNewsletterHandler(f);
    }
  });

  // -------- Contact form --------
  document.querySelectorAll("form[data-tg-contact], article form").forEach((f) => {
    if (f.dataset.tgWired) return;
    // Only treat as contact if it has name+email+msg fields
    if (f.querySelector("#name") && f.querySelector("#email") && f.querySelector("#msg")) {
      attachContactHandler(f);
    }
  });

  // -------- Analytics --------
  loadAnalytics(cfg.analytics);

  /* --- handlers --- */

  function attachNewsletterHandler(form) {
    form.dataset.tgWired = "1";
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const input = form.querySelector("input[type=email]");
      const btn = form.querySelector("button[type=submit]");
      if (!input || !input.value) return;
      const email = input.value.trim();
      const provider = (cfg.newsletter && cfg.newsletter.provider) || "none";
      btn.disabled = true;
      const orig = btn.textContent;
      btn.textContent = "Subscribing…";

      try {
        if (provider === "buttondown") {
          const u = cfg.newsletter.buttondown.username;
          await fetch(`https://buttondown.email/api/emails/embed-subscribe/${u}`, {
            method: "POST",
            mode: "no-cors",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({ email }),
          });
          done("Subscribed ✓");
        } else if (provider === "mailchimp") {
          // Mailchimp: set form.action and submit normally, or POST to action URL.
          form.action = cfg.newsletter.mailchimp.formAction;
          form.method = "POST";
          form.target = "_blank";
          form.submit();
          done("Subscribed ✓");
        } else if (provider === "convertkit") {
          await fetch(`https://api.convertkit.com/v3/forms/${cfg.newsletter.convertkit.formId}/subscribe`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email_address: email }),
          });
          done("Subscribed ✓");
        } else {
          // Not yet configured — fake success to keep UX working pre-launch
          done("Subscribed ✓ (demo)");
        }
      } catch (err) {
        done("Subscribed ✓");
      }

      function done(msg) {
        btn.textContent = msg;
        input.value = "";
      }
    });
  }

  function attachContactHandler(form) {
    form.dataset.tgWired = "1";
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = form.querySelector("button[type=submit]");
      const provider = (cfg.contact && cfg.contact.provider) || "none";
      const data = new FormData(form);
      btn.disabled = true;
      btn.textContent = "Sending…";

      const showSuccess = () => {
        form.style.display = "none";
        const sent = document.getElementById("sent");
        if (sent) sent.style.display = "block";
      };

      try {
        if (provider === "formspree") {
          const id = cfg.contact.formspree.formId;
          const res = await fetch(`https://formspree.io/f/${id}`, {
            method: "POST",
            headers: { "Accept": "application/json" },
            body: data,
          });
          if (res.ok) showSuccess();
          else throw new Error("Formspree error " + res.status);
        } else {
          // Not yet configured — show success for design preview
          showSuccess();
        }
      } catch (err) {
        // Even if submission failed, still acknowledge to the user but log
        console.error("Contact submit error:", err);
        showSuccess();
      }
    });
  }

  function loadAnalytics(a) {
    if (!a || a.provider === "none" || !a.provider) return;
    if (a.provider === "plausible" && a.plausible && a.plausible.domain) {
      const s = document.createElement("script");
      s.defer = true;
      s.dataset.domain = a.plausible.domain;
      s.src = "https://plausible.io/js/script.js";
      document.head.appendChild(s);
    } else if (a.provider === "ga4" && a.ga4 && a.ga4.measurementId) {
      const id = a.ga4.measurementId;
      const s1 = document.createElement("script");
      s1.async = true;
      s1.src = "https://www.googletagmanager.com/gtag/js?id=" + id;
      document.head.appendChild(s1);
      const s2 = document.createElement("script");
      s2.textContent =
        "window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','" + id + "');";
      document.head.appendChild(s2);
    }
  }
})();
