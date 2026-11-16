(() => {
  'use strict';
  const slides = Array.from(document.querySelectorAll('.slide'));
  const prev = document.getElementById('prevBtn');
  const next = document.getElementById('nextBtn');
  const fill = document.getElementById('progressFill');
  const counter = document.getElementById('progressText');
  let active = 0;
  function show(index, updateHash = true) {
    active = Math.max(0, Math.min(slides.length - 1, index));
    slides.forEach((slide, i) => { slide.hidden = i !== active; });
    prev.disabled = active === 0;
    next.disabled = active === slides.length - 1;
    fill.style.width = `${(active+1) / slides.length * 100}%`;
    counter.innerHTML = `${String(active+1).padStart(2,'0')} <i>/</i> ${slides.length}`;
    if (updateHash) history.replaceState(null, '', `#slide-${active + 1}`);
  }
  prev.addEventListener('click', () => show(active - 1));
  next.addEventListener('click', () => show(active + 1));
  document.addEventListener('keydown', event => {
    if (event.altKey || event.ctrlKey || event.metaKey) return;
    const tag = document.activeElement?.tagName?.toLowerCase();
    if (tag === 'input' || tag === 'textarea') return;
    if (event.key === 'ArrowRight' || event.key === 'PageDown') { event.preventDefault(); show(active + 1); }
    if (event.key === 'ArrowLeft' || event.key === 'PageUp') { event.preventDefault(); show(active - 1); }
    if (event.key === 'Home') { event.preventDefault(); show(0); }
    if (event.key === 'End') { event.preventDefault(); show(slides.length - 1); }
  });
  window.addEventListener('hashchange', () => {
    const m = location.hash.match(/^#slide-(\d+)$/);
    if (m) show(Number(m[1]) - 1, false);
  });
  const reveal = document.getElementById('dividendReveal');
  const explanation = document.getElementById('dividendExplanation');
  reveal.addEventListener('click', () => {
    explanation.hidden = !explanation.hidden;
    reveal.setAttribute('aria-expanded', String(!explanation.hidden));
    reveal.textContent = explanation.hidden ? '點我看：為什麼不是多賺 5 元？ ↓' : '收起解釋 ↑';
  });
  document.getElementById('quizCheck').addEventListener('click', () => {
    const questions = Array.from(document.querySelectorAll('.quiz-question'));
    const answered = questions.map(q => q.querySelector('input:checked'));
    const result = document.getElementById('quizResult');
    if (answered.some(x => !x)) { result.textContent = '請先完成全部 3 題再檢查。'; return; }
    const correct = questions.reduce((sum, q, i) => sum + Number(answered[i].value === q.dataset.answer), 0);
    result.textContent = `答對 ${correct} / ${questions.length} 題。` + (correct === questions.length ? ' 太好了！' : ' 可回 Wiki 複習再試。');
  });
  const initial = location.hash.match(/^#slide-(\d+)$/);
  show(initial ? Number(initial[1]) - 1 : 0, Boolean(initial));
})();
