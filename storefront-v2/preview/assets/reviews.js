/* 상품 상세 고객 리뷰 (v3, 2026-09-21)
   실제 쇼핑몰 리뷰 모듈 구조: 평점 요약 -> 포토 후기 모음 -> [전체 / 포토] 탭 + 정렬 -> 목록 -> 페이지 번호.
   데이터: assets/reviews-data/p{상품번호}.js (window.TAM_REVIEWS). 사진은 공식몰과 같은 스냅 서버 주소를 그대로 불러온다.
   + 화면을 내려도 따라다니는 리뷰 버튼. */
(function () {
  const section = document.getElementById('review');
  const jump = document.querySelector('[data-review-jump]');

  if (section && jump && 'IntersectionObserver' in window) {
    const buy = document.querySelector('.detail-product');
    let buyVisible = Boolean(buy);
    let reviewVisible = false;
    const update = () => {
      const show = !buyVisible && !reviewVisible;
      jump.hidden = !show;
      if (!show) return;
      const arrow = jump.querySelector('[data-arrow]');
      if (arrow)
        arrow.textContent = section.getBoundingClientRect().top < 0 ? '↑' : '↓';
    };
    if (buy) {
      new IntersectionObserver((entries) => {
        buyVisible = entries[0].isIntersecting;
        update();
      }).observe(buy);
    }
    new IntersectionObserver((entries) => {
      reviewVisible = entries[0].isIntersecting;
      update();
    }).observe(section);
  }

  const data = window.TAM_REVIEWS;
  const body = section && section.querySelector('[data-reviews-body]');
  if (!data || !body) return;

  const PER_PAGE = 8;
  const state = { tab: 'all', sort: 'best', page: 1 };
  const el = (tag, cls, text) => {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  };
  const stars = (n) => '★'.repeat(n) + '☆'.repeat(5 - n);
  const day = (d) => d.slice(0, 10).split('-').join('.');
  const newer = (a, b) => (a.d < b.d ? 1 : a.d > b.d ? -1 : b.i - a.i);
  const sorters = {
    best: (a, b) =>
      (b.p.length > 0) - (a.p.length > 0) ||
      b.r - a.r ||
      b.t.length - a.t.length ||
      newer(a, b),
    new: newer,
    score: (a, b) => b.s - a.s || newer(a, b),
  };
  const photoItems = data.items.filter((item) => item.p.length);
  const num = (n) => n.toLocaleString('ko-KR');

  /* 1. 평점 요약 */
  const summary = el('div', 'rvs');
  const score = el('div', 'rvs-score');
  score.append(
    el('b', '', data.avg.toFixed(1)),
    el('span', 'rv-star', '★★★★★'),
    el('span', 'rvs-count', num(data.count) + '개 후기'),
  );
  const bars = el('ul', 'rvs-bars');
  [5, 4, 3, 2, 1].forEach((n) => {
    const count = data.dist[n] || 0;
    const row = el('li');
    const bar = el('span', 'rvs-bar');
    const fill = el('i');
    fill.style.width = (data.count ? (count / data.count) * 100 : 0) + '%';
    bar.append(fill);
    row.append(
      el('span', 'rvs-label', n + '점'),
      bar,
      el('span', 'rvs-num', num(count)),
    );
    bars.append(row);
  });
  summary.append(score, bars);
  body.append(summary);

  /* 2. 포토 후기 모음 */
  if (photoItems.length) {
    const strip = el('div', 'rvp');
    const head = el('div', 'rvp-head');
    const title = el('h3', '', '포토 후기 ');
    title.append(el('span', '', num(photoItems.length)));
    const only = el('button', 'rvp-only', '포토 후기만 보기');
    only.type = 'button';
    only.addEventListener('click', () => go({ tab: 'photo', page: 1 }, true));
    head.append(title, only);
    const thumbs = el('ul', 'rvp-list');
    photoItems
      .slice()
      .sort(sorters.best)
      .slice(0, 12)
      .forEach((item) => {
        const li = el('li');
        const button = el('button');
        button.type = 'button';
        button.setAttribute('aria-label', '포토 후기 보기');
        const img = el('img');
        img.src = item.p[0];
        img.alt = '';
        img.loading = 'lazy';
        img.decoding = 'async';
        button.append(img);
        button.addEventListener('click', () =>
          go({ tab: 'photo', page: 1 }, true),
        );
        li.append(button);
        thumbs.append(li);
      });
    strip.append(head, thumbs);
    body.append(strip);
  }

  /* 3. 탭 + 정렬 */
  const controls = el('div', 'rvc');
  const tabs = el('div', 'rvc-tabs');
  tabs.setAttribute('role', 'group');
  tabs.setAttribute('aria-label', '후기 종류');
  const sorts = el('div', 'rvc-sort');
  sorts.setAttribute('role', 'group');
  sorts.setAttribute('aria-label', '정렬');
  [
    ['all', '전체', data.count],
    ['photo', '포토', photoItems.length],
  ].forEach(([key, label, count]) => {
    const button = el('button', '', label + ' ');
    button.type = 'button';
    button.dataset.tab = key;
    button.disabled = !count;
    button.append(el('span', '', num(count)));
    button.addEventListener('click', () => go({ tab: key, page: 1 }));
    tabs.append(button);
  });
  [
    ['best', '추천순'],
    ['new', '최신순'],
    ['score', '평점순'],
  ].forEach(([key, label]) => {
    const button = el('button', '', label);
    button.type = 'button';
    button.dataset.sort = key;
    button.addEventListener('click', () => go({ sort: key, page: 1 }));
    sorts.append(button);
  });
  controls.append(tabs, sorts);

  /* 4. 목록 + 5. 페이지 번호 */
  const list = el('ol', 'rvl');
  const pager = el('nav', 'rvg');
  pager.setAttribute('aria-label', '후기 페이지');
  body.append(controls, list, pager);

  function row(item) {
    const li = el('li', 'rvl-item');
    const meta = el('div', 'rvl-meta');
    const star = el('span', 'rv-star', stars(item.s));
    star.setAttribute('aria-label', '별점 ' + item.s + '점');
    meta.append(
      star,
      el('span', 'rvl-user', item.u || '구매자'),
      el('span', 'rvl-date', day(item.d)),
    );
    const main = el('div', 'rvl-main');
    if (item.t) main.append(el('p', 'rvl-text', item.t));
    if (item.p.length) {
      const photos = el('div', 'rvl-photos');
      item.p.forEach((src) => {
        const button = el('button');
        button.type = 'button';
        button.setAttribute('aria-label', '사진 크게 보기');
        const img = el('img');
        img.src = src;
        img.alt = data.title + ' 구매 후기 사진';
        img.loading = 'lazy';
        img.decoding = 'async';
        button.append(img);
        button.addEventListener('click', () =>
          photos.classList.toggle('is-zoom'),
        );
        photos.append(button);
      });
      main.append(photos);
    }
    li.append(meta, main);
    return li;
  }

  function pageButton(label, page, opts) {
    const button = el('button', opts.cls, label);
    button.type = 'button';
    if (opts.aria) button.setAttribute('aria-label', opts.aria);
    if (opts.current) button.setAttribute('aria-current', 'page');
    if (opts.disabled) button.disabled = true;
    else button.addEventListener('click', () => go({ page }, true));
    return button;
  }

  function render() {
    const items = (state.tab === 'photo' ? photoItems : data.items)
      .slice()
      .sort(sorters[state.sort]);
    const pages = Math.max(1, Math.ceil(items.length / PER_PAGE));
    state.page = Math.min(Math.max(1, state.page), pages);
    tabs
      .querySelectorAll('button')
      .forEach((b) =>
        b.setAttribute('aria-pressed', String(b.dataset.tab === state.tab)),
      );
    sorts
      .querySelectorAll('button')
      .forEach((b) =>
        b.setAttribute('aria-pressed', String(b.dataset.sort === state.sort)),
      );
    list.replaceChildren(
      ...items
        .slice((state.page - 1) * PER_PAGE, state.page * PER_PAGE)
        .map(row),
    );
    const first = Math.max(1, Math.min(state.page - 2, pages - 4));
    const last = Math.min(pages, first + 4);
    const buttons = [
      pageButton('‹', state.page - 1, {
        cls: 'rvg-arrow',
        aria: '이전 페이지',
        disabled: state.page === 1,
      }),
    ];
    for (let n = first; n <= last; n += 1) {
      buttons.push(
        pageButton(String(n), n, {
          current: n === state.page,
          aria: n + '페이지',
        }),
      );
    }
    buttons.push(
      pageButton('›', state.page + 1, {
        cls: 'rvg-arrow',
        aria: '다음 페이지',
        disabled: state.page === pages,
      }),
    );
    pager.replaceChildren(...buttons);
    pager.hidden = pages < 2;
  }

  function go(change, scroll) {
    Object.assign(state, change);
    render();
    if (scroll) controls.scrollIntoView({ block: 'start' });
  }

  render();
})();
