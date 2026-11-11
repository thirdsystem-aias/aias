// Driver for the offline mock test (items JSON made from packets_all.csv by mock_run.sh).
// r2 (2026-11-11): also prints the questions and options of R01's first item (QCHECK), the sign-up
// form's description (SIGNUP), and the parsed labels of one response per tone option (TONECHECK).
var rows = JSON.parse(read(ITEMS_JSON));
SHEETS.items = new Sheet('items'); SHEETS.items.v = rows;
buildLabelForms();
var tr = SHEETS.tracker.v, nForms = tr.length - 1;
print('forms built', nForms, 'status', JSON.stringify(tr.slice(1).map(function (r) { return r[2]; })
  .filter(function (s, i, a) { return a.indexOf(s) === i; })));
var f1 = FORMS[tr[1][3]], kinds = {}, maxHelp = 0, req = 0;
f1.items.forEach(function (it) { kinds[it.kind] = (kinds[it.kind] || 0) + 1; if (it.req) req++;
  if (it.setHelpText && it.setHelpText.length > maxHelp) maxHelp = it.setHelpText.length; });
print('form R01 items by kind', JSON.stringify(kinds), 'required', req, 'max helpText', maxHelp);
print('map rows', SHEETS.map.v.length - 1);
var q = f1.items.filter(function (it) { return it.kind === 'addMultipleChoiceItem'; }).slice(0, 4)
  .map(function (it) { return { title: it.setTitle, choices: it.setChoiceValues, help: it.setHelpText || '' }; });
print('QCHECK ' + JSON.stringify(q));
print('DESC_HAS_STATEMENT ' + (f1.setDescription.indexOf(STATEMENT) >= 0));
buildSignupForm();
var su = null; for (var k in FORMS) if (FORMS[k].title.indexOf('sign up') >= 0) su = FORMS[k];
print('SIGNUP ' + JSON.stringify({ title: su.title, equals_statement: su.setDescription === STATEMENT }));
// Simulate: R01 answers everything (twice: the second must be ignored); R02 never submits.
function respond(form, ts, pick) {
  var irs = form.items.filter(function (it) { return it.kind === 'addMultipleChoiceItem' || it.kind === 'addTextItem'; })
    .map(function (it, k) { var ch = Array.isArray(it.setChoiceValues) ? it.setChoiceValues : null; var val = ch ? ch[pick(k, ch.length)] : 'note ' + k;
      return { getItem: function () { return it; }, getResponse: function () { return val; } }; });
  form.responses.push({ getTimestamp: function () { return ts; }, getItemResponses: function () { return irs; } });
}
// k counts answer fields (5 per item); item i's tone answer is field 5i, so item i gets TONE[i % 6].
respond(f1, new Date(2026, 10, 30), function (k, n) { return n === 6 ? (k / 5) % 6 : k % n; });
respond(f1, new Date(2026, 11, 1), function () { return 0; });
collectLabels();
var lab = SHEETS.labels.v;
print('label rows', lab.length - 1, 'expected', tr[1][1]);
print('TONECHECK ' + JSON.stringify(lab.slice(1).filter(function (r) { return r[1] <= 6; })
  .map(function (r) { return [r[3], r[4], r[5]]; })));
print(JSON.stringify(lab[0])); print(JSON.stringify(lab[1]));
print('tracker R01', JSON.stringify(tr[1].slice(8)), 'R02', JSON.stringify(tr[2].slice(8)));
