const test = require('node:test');
const assert = require('node:assert/strict');
const { shipping, dispatch } = require('../../storefront-v2/preview/assets/purchase-policy.js');
const config = { enabled: true, eligible: true, calendar: {
  verified: true, from: '2026-09-01', to: '2026-09-30', closedDates: ['2026-09-21']
} }; // Synthetic warehouse closure, not an official holiday calendar.
test('coupon does not revoke earned free shipping; threshold uses selling price', () => {
  assert.deepEqual(shipping(30000, 3000), { shipping: 0, remaining: 0, payable: 27000 });
  assert.equal(shipping(29999, 3000).shipping, 3000);
  assert.equal(shipping(30001, 20000).shipping, 0);
  assert.equal(shipping(14400 * 2, 0).remaining, 1200);
  assert.equal(shipping(0, 0).shipping, 0);
  assert.throws(() => shipping(NaN), RangeError);
});
test('14:00 Korean payment cutoff including seconds and timezone', () => {
  assert.equal(dispatch(new Date('2026-09-17T04:59:59Z'), config).state, 'today');
  assert.equal(dispatch(new Date('2026-09-17T05:00:00Z'), config).date, '2026-09-18');
  assert.equal(dispatch(new Date('2026-09-17T23:30:00-07:00'), config).date, '2026-09-22');
});
test('weekends and warehouse closures are skipped after cutoff', () => {
  for (const date of ['2026-09-18T05:00:00Z', '2026-09-19T03:00:00Z', '2026-09-21T03:00:00Z'])
    assert.equal(dispatch(new Date(date), config).date, '2026-09-22');
});
test('unknown/expired calendar, unavailable stock or missing policy cannot promise today', () => {
  const now = new Date('2026-09-17T03:00:00Z');
  for (const c of [null, { ...config, enabled: false }, { ...config, eligible: false },
    { ...config, calendar: null }, { ...config, calendar: { verified: true } },
    { ...config, calendar: { ...config.calendar, verified: false } }])
    assert.equal(dispatch(now, c).state, 'unverified');
  assert.equal(dispatch(new Date('2026-10-01T03:00:00Z'), config).state, 'unverified');
  assert.equal(dispatch(new Date('2026-09-30T05:00:00Z'), config).state, 'unverified');
});
