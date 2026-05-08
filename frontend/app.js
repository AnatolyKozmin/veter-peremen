(() => {
  "use strict";

  const form = document.getElementById("reg-form");
  const studentWrap = document.getElementById("student-of-wrap");
  const studentInput = document.getElementById("student_of");
  const submitBtn = form.querySelector(".btn--submit");
  const statusEl = document.getElementById("form-status");
  const successScreen = document.getElementById("success-screen");
  const registerSection = document.getElementById("register");
  const successBack = document.getElementById("success-back");

  /* Подсветка/скрытие поля «где учишься» */
  form.addEventListener("change", (e) => {
    if (e.target.name !== "is_student") return;
    const isStudent = e.target.value === "yes";
    studentWrap.classList.toggle("field--hidden", !isStudent);
    if (!isStudent) {
      studentInput.value = "";
      clearError("student_of");
    }
  });

  /* Сброс ошибки при правке поля */
  form.addEventListener("input", (e) => {
    if (e.target.name) clearError(e.target.name);
  });

  function clearError(name) {
    const err = form.querySelector(`.field__error[data-for="${name}"]`);
    if (err) err.textContent = "";
    const input = form.querySelector(`[name="${name}"]`);
    if (input) input.classList.remove("invalid");
  }

  function setError(name, msg) {
    const err = form.querySelector(`.field__error[data-for="${name}"]`);
    if (err) err.textContent = msg;
    const input = form.querySelector(`[name="${name}"]`);
    if (input && input.tagName === "INPUT") input.classList.add("invalid");
  }

  function validate(data) {
    let ok = true;

    if (!data.full_name || data.full_name.length < 2) {
      setError("full_name", "минимум 2 символа");
      ok = false;
    }

    if (!data.age_group) {
      setError("age_group", "выбери возраст");
      ok = false;
    }

    if (data.is_student && !data.student_of) {
      setError("student_of", "укажи, где учишься");
      ok = false;
    }

    return ok;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    statusEl.textContent = "";
    statusEl.classList.remove("success");

    const fd = new FormData(form);
    const isStudentRaw = fd.get("is_student");
    const data = {
      full_name: (fd.get("full_name") || "").toString().trim(),
      age_group: fd.get("age_group"),
      is_student: isStudentRaw === "yes",
      student_of:
        isStudentRaw === "yes"
          ? (fd.get("student_of") || "").toString().trim() || null
          : null,
    };

    if (!validate(data)) {
      statusEl.textContent = "проверь поля выше";
      return;
    }

    submitBtn.dataset.loading = "1";
    submitBtn.disabled = true;

    try {
      const res = await fetch("/registration/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!res.ok) {
        let msg = "что-то пошло не так";
        try {
          const j = await res.json();
          if (j && j.detail) {
            if (Array.isArray(j.detail)) {
              j.detail.forEach((d) => {
                const field = (d.loc || []).slice(-1)[0];
                if (field) setError(field, d.msg);
              });
              msg = "проверь поля выше";
            } else {
              msg = String(j.detail);
            }
          }
        } catch (_) {}
        statusEl.textContent = msg;
        return;
      }

      registerSection.hidden = true;
      successScreen.hidden = false;
      successScreen.scrollIntoView({ behavior: "smooth", block: "start" });

      // Если внутри Telegram — мягкая обратная связь
      try {
        if (window.Telegram && window.Telegram.WebApp) {
          window.Telegram.WebApp.HapticFeedback?.notificationOccurred("success");
        }
      } catch (_) {}
    } catch (err) {
      statusEl.textContent = "сеть недоступна, попробуй позже";
    } finally {
      submitBtn.dataset.loading = "0";
      submitBtn.disabled = false;
    }
  });

  successBack.addEventListener("click", () => {
    successScreen.hidden = true;
    registerSection.hidden = false;
    form.reset();
    studentWrap.classList.add("field--hidden");
    statusEl.textContent = "";
    registerSection.scrollIntoView({ behavior: "smooth", block: "start" });
  });

  /* Telegram WebApp интеграция */
  try {
    if (window.Telegram && window.Telegram.WebApp) {
      window.Telegram.WebApp.ready();
      window.Telegram.WebApp.expand();
    }
  } catch (_) {}
})();
