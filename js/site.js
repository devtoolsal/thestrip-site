(function () {
  const API_BASE = String(window.THESTRIP_API_BASE || "").replace(/\/$/, "");
  const EMAIL = "hello@thestripphotobooth.co.za";

  const navToggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector("header nav");
  if (navToggle && nav) {
    navToggle.addEventListener("click", () => {
      const open = nav.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", String(open));
    });
    nav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        nav.classList.remove("open");
        navToggle.setAttribute("aria-expanded", "false");
      });
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
      base = (window.matchMedia("(max-width: 820px)").matches ? 18 : 7) * window.innerWidth / 100;
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
    const dateInput = form.querySelector('[name="date"]');
    if (dateInput) {
      const today = new Date();
      dateInput.min = [today.getFullYear(), String(today.getMonth() + 1).padStart(2, "0"), String(today.getDate()).padStart(2, "0")].join("-");
    }

    function showError(message) {
      if (!status) return;
      status.className = "form-status error";
      status.innerHTML = message;
    }

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const data = new FormData(form);

      if (data.get("website")) return;
      if (!data.get("consent")) {
        showError("Please confirm you're happy for us to contact you about this enquiry.");
        return;
      }

      const payload = {
        name: String(data.get("name") || "").trim(),
        email: String(data.get("email") || "").trim(),
        phone: String(data.get("phone") || "").trim() || undefined,
        eventDate: String(data.get("date") || "").trim() || undefined,
        occasion: String(data.get("occasion") || "").trim() || undefined,
        location: String(data.get("location") || "").trim() || undefined,
        message: String(data.get("message") || "").trim() || undefined,
        consent: true,
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
        showError(`We couldn't send that automatically. <a href="${mailto}">Email us directly</a>.`);
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
          throw new Error(error.message || "Could not send the enquiry");
        }
        form.classList.add("hidden");
        if (success) {
          success.classList.remove("hidden");
          success.scrollIntoView({ behavior: "smooth", block: "center" });
        }
      } catch (error) {
        showError(`We couldn't send that automatically. <a href="${mailto}">Email us directly</a> or try again.`);
      }
    });
  })();
})();
