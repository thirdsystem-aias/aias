// Offline mock test of Code.gs (run with macOS jsc after concatenating Code.gs + this file).
// Mocks just enough of FormApp / SpreadsheetApp / DriveApp / Logger to exercise build + collect.
var _id = 0, FORMS = {}, LOG = [];
function Item(form, kind) { this.id = ++_id; this.kind = kind; this.req = false; form.items.push(this); }
['setTitle', 'setHelpText', 'setChoiceValues', 'setValidation'].forEach(function (m) {
  Item.prototype[m] = function (v) { this[m] = v; return this; };
});
Item.prototype.setRequired = function (v) { this.req = v; return this; };
Item.prototype.getId = function () { return this.id; };
function Form(title) { this.title = title; this.items = []; this.id = 'F' + (++_id); this.responses = []; }
['setDescription', 'setProgressBar', 'setCollectEmail', 'setAllowResponseEdits', 'setShowLinkToRespondAgain',
 'setPublishingSummary', 'setShuffleQuestions', 'setConfirmationMessage', 'setAcceptingResponses',
 'setCustomClosedFormMessage'].forEach(function (m) { Form.prototype[m] = function (v) { this[m] = v; return this; }; });
['addPageBreakItem', 'addSectionHeaderItem', 'addMultipleChoiceItem', 'addTextItem', 'addCheckboxItem']
  .forEach(function (m) { Form.prototype[m] = function () { return new Item(this, m); }; });
Form.prototype.getId = function () { return this.id; };
Form.prototype.getPublishedUrl = function () { return 'https://forms/' + this.id; };
Form.prototype.getEditUrl = function () { return 'https://forms/' + this.id + '/edit'; };
Form.prototype.getResponses = function () { return this.responses.slice(); };
var FormApp = {
  create: function (t) { var f = new Form(t); FORMS[f.id] = f; return f; },
  openById: function (id) { return FORMS[id]; },
  createTextValidation: function () { return { requireTextIsEmail: function () { return this; },
    setHelpText: function () { return this; }, build: function () { return {}; } }; },
};
var DriveApp = { getFileById: function () { return { setTrashed: function () {}, moveTo: function () {} }; } };
var Logger = { log: function (s) { LOG.push(s); print('LOG: ' + s); } };
function Sheet(name) { this.name = name; this.v = []; }
Sheet.prototype.appendRow = function (r) { this.v.push(r.slice()); };
Sheet.prototype.setFrozenRows = function () {};
Sheet.prototype.clear = function () { this.v = []; };
Sheet.prototype.getLastRow = function () { return this.v.length; };
Sheet.prototype.deleteRow = function (i) { this.v.splice(i - 1, 1); };
Sheet.prototype.getDataRange = function () { var s = this; return { getValues: function () {
  return s.v.map(function (r) { return r.slice(); }); } }; };
Sheet.prototype.getRange = function (r, c, nr, nc) { var s = this; nr = nr || 1; nc = nc || 1; return {
  setValues: function (vals) { for (var i = 0; i < nr; i++) { s.v[r - 1 + i] = s.v[r - 1 + i] || [];
    for (var j = 0; j < nc; j++) s.v[r - 1 + i][c - 1 + j] = vals[i][j]; } },
  setValue: function (x) { s.v[r - 1] = s.v[r - 1] || []; s.v[r - 1][c - 1] = x; } }; };
var SHEETS = {};
var SpreadsheetApp = { flush: function () {}, getActive: function () { return {
  getSheetByName: function (n) { return SHEETS[n] || null; },
  insertSheet: function (n) { return (SHEETS[n] = new Sheet(n)); } }; } };
