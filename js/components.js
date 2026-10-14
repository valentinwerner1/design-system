// components.js: behaviour for the components that need it (toast, menu keys and
// pickers, toggles, table sort and filters, number steppers). Load at the end of <body>.
// Everything else is CSS plus native <dialog> and the popover attribute.
(function () {
  // Toasts are for results of background work and for Undo. Timings from loquol:
  // an action must still be there when you look up from the call, errors linger.
  var host = null;
  window.toast = function (message, opts) {
    opts = opts || {};
    if (!host) {
      host = document.createElement("div");
      host.className = "toast-host";
      host.setAttribute("role", "status");
      host.setAttribute("aria-live", "polite");
      document.body.appendChild(host);
    }
    var el = document.createElement("div");
    el.className = "toast" + (opts.kind ? " " + opts.kind : "");
    if (opts.title) {
      var t = document.createElement("span");
      t.className = "kind";
      t.textContent = opts.title;
      el.appendChild(t);
    }
    el.appendChild(document.createTextNode(message));
    function hide() { el.classList.remove("show"); setTimeout(function () { el.remove(); }, 250); }
    if (opts.action) {
      var b = document.createElement("button");
      b.type = "button";
      b.textContent = opts.action.label;
      b.addEventListener("click", function () { hide(); opts.action.run(); });
      el.appendChild(b);
    }
    host.appendChild(el);
    requestAnimationFrame(function () { el.classList.add("show"); });
    setTimeout(hide, opts.kind === "error" ? 10000 : opts.action ? 12000 : 4200);
  };

  // Menus: arrow keys move between items, Home/End jump, the first item gets focus on open.
  document.addEventListener("toggle", function (e) {
    var m = e.target;
    if (!m.classList || !m.classList.contains("menu") || e.newState !== "open") return;
    var first = m.querySelector("button, a");
    if (first) first.focus();
  }, true);
  document.addEventListener("keydown", function (e) {
    var m = e.target.closest && e.target.closest(".menu");
    if (!m) return;
    var items = Array.prototype.slice.call(m.querySelectorAll("button, a"));
    var i = items.indexOf(document.activeElement);
    if (e.key === "ArrowDown") { e.preventDefault(); items[(i + 1) % items.length].focus(); }
    if (e.key === "ArrowUp") { e.preventDefault(); items[(i - 1 + items.length) % items.length].focus(); }
    if (e.key === "Home") { e.preventDefault(); items[0].focus(); }
    if (e.key === "End") { e.preventDefault(); items[items.length - 1].focus(); }
  });

  // A menu of options (role=menuitemradio) ticks the chosen one and closes.
  document.addEventListener("click", function (e) {
    var item = e.target.closest && e.target.closest('.menu [role="menuitemradio"]');
    if (!item) return;
    var menu = item.parentElement;
    menu.querySelectorAll('[role="menuitemradio"]').forEach(function (x) {
      x.setAttribute("aria-checked", String(x === item));
    });
    // A picker shows its current value: the trigger's .v takes the item's text.
    var v = document.querySelector('[popovertarget="' + menu.id + '"] .v');
    if (v) v.textContent = item.dataset.short || item.textContent;
    if (menu.hidePopover) menu.hidePopover();
  });

  // Toggles: the sort direction, on/off filters, find options.
  document.addEventListener("click", function (e) {
    var t = e.target.closest && e.target.closest(".sort .dir, .picker[aria-pressed], .find .opt");
    if (!t) return;
    e.preventDefault();
    t.setAttribute("aria-pressed", String(t.getAttribute("aria-pressed") !== "true"));
  });

  // Tables: number and date headers sort (click again to reverse); text columns filter
  // from the row under the header. Sort keys come from data-v when the text isn't one.
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest(".table .th-sort");
    if (!b) return;
    var th = b.closest("th"), table = th.closest("table"), col = th.cellIndex;
    var asc = th.getAttribute("aria-sort") === "descending";
    table.querySelectorAll("th[aria-sort]").forEach(function (x) { x.removeAttribute("aria-sort"); });
    th.setAttribute("aria-sort", asc ? "ascending" : "descending");
    var body = table.tBodies[0];
    var rows = Array.prototype.slice.call(body.rows);
    function key(r) { var c = r.cells[col]; return parseFloat(c.dataset.v || c.textContent); }
    rows.sort(function (a, z) { return asc ? key(a) - key(z) : key(z) - key(a); });
    rows.forEach(function (r) { body.appendChild(r); });
  });
  // Column filters, all on the column name. Text: the magnifier opens a narrow search over
  // the header. A few repeating values: a funnel menu of checkboxes. Dates: a funnel with
  // presets ("Last 7 days"), counted back from the table's data-today. Any active filter
  // marks its column (.filtered), so a narrowed table never passes for the whole one.
  function dayNum(v) { v = String(v); return Date.UTC(+v.slice(0, 4), +v.slice(4, 6) - 1, +v.slice(6, 8)) / 864e5; }
  function filterTable(table) {
    var tests = Array.prototype.map.call(table.tHead.rows[0].cells, function (th) {
      var test = null, search = th.querySelector(".th-search"), menu = th.querySelector(".menu[data-filter]");
      if (search && search.value.trim()) {
        var t = search.value.trim().toLowerCase();
        test = function (c) { return c.textContent.toLowerCase().indexOf(t) >= 0; };
      } else if (menu && menu.dataset.filter === "set") {
        var items = menu.querySelectorAll("[data-value]"), on = [];
        items.forEach(function (x) { if (x.getAttribute("aria-checked") === "true") on.push(x.dataset.value); });
        if (on.length < items.length) test = function (c) { return on.indexOf(c.textContent.trim()) >= 0; };
      } else if (menu && menu.dataset.filter === "days") {
        var pick = menu.querySelector('[aria-checked="true"]'), n = pick ? +pick.dataset.days : 0;
        if (n) test = function (c) { return dayNum(table.dataset.today) - dayNum(c.dataset.v) < n; };
      }
      th.classList.toggle("filtered", !!test);
      return test;
    });
    Array.prototype.forEach.call(table.tBodies[0].rows, function (r) {
      r.hidden = tests.some(function (test, i) { return test && !test(r.cells[i]); });
    });
  }
  // Checkbox items stay open so several can be toggled; radio items close (handled above).
  document.addEventListener("click", function (e) {
    var item = e.target.closest && e.target.closest('.table .menu [role^="menuitem"]');
    if (!item) return;
    if (item.getAttribute("role") === "menuitemcheckbox") {
      item.setAttribute("aria-checked", String(item.getAttribute("aria-checked") !== "true"));
    }
    filterTable(item.closest("table"));
  });
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest(".table .th-find");
    if (!b) return;
    var input = b.parentElement.querySelector(".th-search");
    input.hidden = false;
    input.focus();
  });
  document.addEventListener("input", function (e) {
    if (!e.target.classList || !e.target.classList.contains("th-search")) return;
    filterTable(e.target.closest("table"));
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && e.target.classList && e.target.classList.contains("th-search")) e.target.blur();
  });
  document.addEventListener("focusout", function (e) {
    if (e.target.classList && e.target.classList.contains("th-search")) e.target.hidden = true;
  });

  // Number stepper: the buttons sit outside the field and keep within min and max.
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest(".stepper-input > button");
    if (!b) return;
    var input = b.parentElement.querySelector("input");
    if (b === b.parentElement.firstElementChild) input.stepDown(); else input.stepUp();
  });
})();
