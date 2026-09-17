/* Shared presentation rules. Cafe24 remains the authority for order totals. */
(function (root) {
  'use strict';
  function shipping(subtotal, coupon = 0, threshold = 30000, fee = 3000) {
    if (![subtotal, coupon, threshold, fee].every(Number.isFinite) ||
        subtotal < 0 || coupon < 0 || threshold <= 0 || fee < 0) throw new RangeError('Invalid amount');
    return { shipping: subtotal === 0 || subtotal >= threshold ? 0 : fee,
      remaining: Math.max(0, threshold - subtotal), payable: Math.max(0, subtotal - coupon) +
        (subtotal === 0 || subtotal >= threshold ? 0 : fee) };
  }
  function koreanDate(now) {
    const parts = new Intl.DateTimeFormat('en-CA', { timeZone: 'Asia/Seoul',
      year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit',
      minute: '2-digit', hourCycle: 'h23' }).formatToParts(now);
    const v = Object.fromEntries(parts.map(x => [x.type, x.value]));
    return { date: `${v.year}-${v.month}-${v.day}`, hour: Number(v.hour), minute: Number(v.minute) };
  }
  function dispatch(now, config) {
    const fallback = { state: 'unverified', title: '출고 일정은 상품별 안내를 확인해 주세요.' };
    if (!config?.enabled || !config.eligible) return fallback;
    const local = koreanDate(now), calendar = config.calendar;
    if (!calendar?.verified || !/^\d{4}-\d{2}-\d{2}$/.test(calendar.from || '') ||
        !/^\d{4}-\d{2}-\d{2}$/.test(calendar.to || '') || !Array.isArray(calendar.closedDates) ||
        local.date < calendar.from || local.date > calendar.to) return fallback;
    const workday = date => {
      const day = new Date(date + 'T12:00:00Z').getUTCDay();
      return day !== 0 && day !== 6 && !(calendar.closedDates || []).includes(date);
    };
    if (workday(local.date) && local.hour * 60 + local.minute < 14 * 60)
      return { state: 'today', title: '오후 2시 이전 결제 완료 시 오늘 출고', date: local.date };
    let date = new Date(local.date + 'T12:00:00Z');
    for (let i = 0; i < 31; i++) {
      date.setUTCDate(date.getUTCDate() + 1);
      const key = date.toISOString().slice(0, 10);
      if (key > calendar.to) return fallback;
      if (workday(key)) return { state: 'next', title: `${date.getUTCMonth() + 1}월 ${date.getUTCDate()}일 출고 예정`, date: key };
    }
    return fallback;
  }
  const api = { shipping, dispatch, koreanDate };
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.TamPurchasePolicy = api;
})(typeof window === 'undefined' ? globalThis : window);
