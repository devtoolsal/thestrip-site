(function () {
  const API_BASE = String(window.THESTRIP_API_BASE || "").replace(/\/$/, "");
  const EMAIL = "hello@thestripphotobooth.co.za";

  const navToggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector("header nav");
  if (navToggle && nav) {
    const setOpen = (open) => {
      nav.classList.toggle("open", open);
      navToggle.setAttribute("aria-expanded", String(open));
      navToggle.textContent = open ? "Close" : "Menu";
    };
    navToggle.addEventListener("click", () => setOpen(!nav.classList.contains("open")));
    nav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => setOpen(false));
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") setOpen(false);
    });
  }

  document.querySelectorAll("[data-year]").forEach((element) => {
    element.textContent = new Date().getFullYear();
  });

  (function gallery() {
    const track = document.getElementById("track");
    const pauseButton = document.getElementById("pause-gallery");
    const prevButton = document.getElementById("prev");
    const nextButton = document.getElementById("next");
    const count = document.getElementById("count");
    if (!track || !pauseButton || !prevButton || !nextButton || !count) return;

    const originals = [...track.children];
    originals.forEach((photo) => {
      const copy = photo.cloneNode(true);
      copy.setAttribute("aria-hidden", "true");
      track.appendChild(copy);
    });

    const motionPreference = window.matchMedia("(prefers-reduced-motion: reduce)");
    let paused = motionPreference.matches;
    let offset = 0;
    let step = 0;
    let cycle = 0;
    let base = 0;
    let lastTime = 0;

    function render() {
      if (!cycle) return;
      offset = ((offset % cycle) + cycle) % cycle;
      track.style.transform = `translate3d(${-base - offset}px,0,0)`;
      count.textContent = `${String(Math.floor(offset / step) + 1).padStart(2, "0")} — ${String(originals.length).padStart(2, "0")}`;
    }

    function measure() {
      const progress = cycle ? offset / cycle : 0;
      const gap = parseFloat(getComputedStyle(track).columnGap) || 0;
      step = originals[0].getBoundingClientRect().width + gap;
      cycle = step * originals.length;
      base = (window.matchMedia("(max-width: 900px), (orientation: landscape) and (max-height: 500px)").matches ? 18 : 7) * window.innerWidth / 100;
      offset = progress * cycle;
      render();
    }

    function updatePause() {
      pauseButton.textContent = paused ? "▶" : "Ⅱ";
      pauseButton.setAttribute("aria-label", paused ? "Play photo animation" : "Pause photo animation");
      pauseButton.setAttribute("aria-pressed", String(paused));
    }

    pauseButton.addEventListener("click", () => {
      paused = !paused;
      updatePause();
    });
    motionPreference.addEventListener("change", (event) => {
      paused = event.matches;
      updatePause();
    });
    nextButton.addEventListener("click", () => {
      offset += step;
      render();
    });
    prevButton.addEventListener("click", () => {
      offset -= step;
      render();
    });

    function animate(time) {
      const elapsed = lastTime ? Math.min(time - lastTime, 50) : 0;
      lastTime = time;
      if (!paused && !document.hidden) {
        offset += elapsed * 0.028;
        render();
      }
      requestAnimationFrame(animate);
    }

    window.addEventListener("resize", measure);
    measure();
    updatePause();
    requestAnimationFrame(animate);
  })();

  (function lightbox() {
    const grid = document.querySelector(".gallery-grid");
    const dialog = document.getElementById("lightbox");
    if (!grid || !dialog) return;

    const triggers = [...grid.querySelectorAll("[data-lightbox]")];
    const image = dialog.querySelector("img");
    const caption = dialog.querySelector(".caption");
    let index = 0;

    function show(nextIndex) {
      index = (nextIndex + triggers.length) % triggers.length;
      const trigger = triggers[index];
      image.src = trigger.getAttribute("href");
      image.alt = trigger.dataset.alt || "";
      caption.textContent = trigger.dataset.alt || "";
    }

    triggers.forEach((trigger, triggerIndex) => {
      trigger.addEventListener("click", (event) => {
        event.preventDefault();
        show(triggerIndex);
        if (!dialog.open) dialog.showModal();
      });
    });

    dialog.querySelector("[data-close]").addEventListener("click", () => dialog.close());
    dialog.querySelector("[data-prev]").addEventListener("click", () => show(index - 1));
    dialog.querySelector("[data-next]").addEventListener("click", () => show(index + 1));
    dialog.addEventListener("keydown", (event) => {
      if (event.key === "ArrowLeft") show(index - 1);
      if (event.key === "ArrowRight") show(index + 1);
    });
    dialog.addEventListener("click", (event) => {
      if (event.target === dialog) dialog.close();
    });
  })();

  (function enquiry() {
    const form = document.getElementById("enquiry-form");
    if (!form) return;

    const status = document.getElementById("form-status");
    const success = document.getElementById("form-success");
    const startedAt = document.getElementById("startedAt");
    if (startedAt) startedAt.value = new Date().toISOString();

    const dateInput = form.querySelector('[name="date"]');
    if (dateInput) {
      const today = new Date();
      dateInput.min = [today.getFullYear(), String(today.getMonth() + 1).padStart(2, "0"), String(today.getDate()).padStart(2, "0")].join("-");
    }

    const turnstileSiteKey = window.THESTRIP_TURNSTILE_SITE_KEY || "";
    const turnstileSlot = document.getElementById("turnstile-slot");
    if (turnstileSiteKey && turnstileSlot) {
      const script = document.createElement("script");
      script.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit";
      script.async = true;
      script.defer = true;
      script.onload = () => {
        if (window.turnstile) window.turnstile.render(turnstileSlot, { sitekey: turnstileSiteKey });
      };
      document.head.appendChild(script);
    }

    const field = (name) => form.querySelector(`[name="${name}"]`);
    const errorFor = (name) => form.querySelector(`[data-error-for="${name}"]`);

    function setError(name, message) {
      const input = field(name);
      const error = errorFor(name);
      if (input) input.setAttribute("aria-invalid", message ? "true" : "false");
      if (error) error.textContent = message || "";
    }

    function clearErrors() {
      ["name", "email", "date", "location", "consent"].forEach((name) => setError(name, ""));
      if (status) {
        status.textContent = "";
        status.className = "form-status";
      }
    }

    ["name", "email", "date", "location", "consent"].forEach((name) => {
      const input = field(name);
      if (!input) return;
      const eventName = input.type === "checkbox" || input.tagName === "SELECT" ? "change" : "input";
      input.addEventListener(eventName, () => setError(name, ""));
    });

    function validate() {
      const errors = [];
      const name = (field("name")?.value || "").trim();
      const email = (field("email")?.value || "").trim();
      const date = field("date")?.value || "";
      const location = (field("location")?.value || "").trim();
      const consent = field("consent")?.checked;

      if (name.length < 2) errors.push(["name", "Please tell us your name."]);
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) errors.push(["email", "Please enter a valid email address."]);
      if (!date) {
        errors.push(["date", "Please choose a date."]);
      } else {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        if (new Date(date + "T00:00:00") < today) errors.push(["date", "Please choose a future date."]);
      }
      if (location.length < 2) errors.push(["location", "Please tell us where the party is."]);
      if (!consent) errors.push(["consent", "Please confirm we can contact you."]);

      errors.forEach(([name, message]) => setError(name, message));
      if (errors.length) {
        const first = field(errors[0][0]);
        if (first) first.focus();
        if (status) {
          status.textContent = "Please check the highlighted fields.";
          status.className = "form-status error";
        }
        return false;
      }
      return true;
    }

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      clearErrors();
      if (!validate()) return;

      const data = new FormData(form);
      if (data.get("website")) return;

      const payload = {
        name: String(data.get("name") || "").trim(),
        email: String(data.get("email") || "").trim(),
        phone: String(data.get("phone") || "").trim() || undefined,
        eventDate: String(data.get("date") || "").trim() || undefined,
        occasion: String(data.get("occasion") || "").trim() || undefined,
        location: String(data.get("location") || "").trim() || undefined,
        message: String(data.get("message") || "").trim() || undefined,
        consent: true,
        startedAt: String(data.get("startedAt") || "").trim() || undefined,
        turnstileToken: turnstileSiteKey && window.turnstile ? window.turnstile.getResponse(turnstileSlot) : undefined,
        website: String(data.get("website") || "").trim() || undefined
      };

      const subject = `The Strip enquiry — ${payload.occasion || "Event"} — ${payload.eventDate || "date tbc"}`;
      const body = [
        "Hello The Strip,",
        "",
        "I'd love to enquire about the photobooth for my event.",
        "",
        `Name: ${payload.name}`,
        `Email: ${payload.email}`,
        payload.phone ? `Phone: ${payload.phone}` : "",
        `Occasion: ${payload.occasion || ""}`,
        `Date: ${payload.eventDate || ""}`,
        `Venue / town: ${payload.location || ""}`,
        "",
        payload.message || "",
        "",
        "Please let me know about availability and pricing.",
        "",
        "Thank you!"
      ].filter((line) => line !== "").join("\n");
      const mailto = `mailto:${EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;

      if (!API_BASE) {
        if (status) {
          status.className = "form-status error";
          status.innerHTML = `We couldn't send that automatically. <a href="${mailto}">Email us directly</a>.`;
        }
        return;
      }

      try {
        const response = await fetch(API_BASE + "/public/enquiries", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        if (!response.ok) {
          const error = await response.json().catch(() => ({}));
          if (response.status === 429) throw new Error("Too many enquiries from this connection. Please try again shortly.");
          throw new Error(error.message || "Could not send the enquiry");
        }
        form.classList.add("hidden");
        if (success) {
          success.classList.remove("hidden");
          success.scrollIntoView({ behavior: "smooth", block: "center" });
        }
      } catch (error) {
        if (status) {
          status.className = "form-status error";
          status.innerHTML = `We couldn't send that automatically. <a href="${mailto}">Email us directly</a> or try again.`;
        }
      }
    });
  })();
})();
