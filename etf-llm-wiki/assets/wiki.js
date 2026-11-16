(() => {
  'use strict';
  const search = document.getElementById('topicSearch');
  const articles = [...document.querySelectorAll('.wiki-article')];
  const result = document.getElementById('searchCount');
  const empty = document.getElementById('noResults');
  if (!search) return;
  search.addEventListener('input', () => {
    const q = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    articles.forEach(article => {
      const match = !q || (article.dataset.search || '').toLocaleLowerCase().includes(q);
      article.hidden = !match;
      if (match) visible++;
    });
    result.textContent = `顯示 ${visible} / ${articles.length} 個主題`;
    empty.hidden = visible !== 0;
  });
})();
