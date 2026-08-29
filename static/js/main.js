// main.js – minimal interactions for the interview UI

// Utility: debounce for input events
function debounce(fn, delay) {
  let timeout;
  return function (...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn.apply(this, args), delay);
  };
}

// Example: focus style for inputs (already handled by CSS, but we add a class toggle)
document.addEventListener('focusin', (e) => {
  if (e.target.matches('input, textarea, select')) {
    e.target.classList.add('focused');
  }
});

document.addEventListener('focusout', (e) => {
  if (e.target.matches('input, textarea, select')) {
    e.target.classList.remove('focused');
  }
});

// Placeholder for interview timer – will be hooked by backend via data attributes
function initTimer(elementId, seconds) {
  const el = document.getElementById(elementId);
  if (!el) return;
  let remaining = seconds;
  const interval = setInterval(() => {
    const mins = Math.floor(remaining / 60);
    const secs = remaining % 60;
    el.textContent = `${mins}:${secs.toString().padStart(2, '0')}`;
    if (remaining <= 0) {
      clearInterval(interval);
      el.dispatchEvent(new Event('timer-ended'));
    }
    remaining--;
  }, 1000);
}

// Example: button hover subtle animation (handled by CSS, but we ensure pointer cursor)
document.querySelectorAll('button, .btn').forEach((btn) => {
  btn.style.cursor = 'pointer';
});

// Export for potential module usage (if using ES modules later)
export { debounce, initTimer };
