var Ai = Object.defineProperty;
var Di = (l, e, t) => e in l ? Ai(l, e, { enumerable: !0, configurable: !0, writable: !0, value: t }) : l[e] = t;
var kl = (l, e, t) => (Di(l, typeof e != "symbol" ? e + "" : e, t), t);
const {
  SvelteComponent: Fi,
  assign: Ri,
  create_slot: Bi,
  detach: Ni,
  element: Vi,
  get_all_dirty_from_scope: Pi,
  get_slot_changes: Ti,
  get_spread_update: Oi,
  init: Ui,
  insert: Wi,
  safe_not_equal: Zi,
  set_dynamic_element_data: pl,
  set_style: x,
  toggle_class: we,
  transition_in: In,
  transition_out: Mn,
  update_slot_base: Hi
} = window.__gradio__svelte__internal;
function Xi(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[18].default
  ), o = Bi(
    i,
    l,
    /*$$scope*/
    l[17],
    null
  );
  let r = [
    { "data-testid": (
      /*test_id*/
      l[7]
    ) },
    { id: (
      /*elem_id*/
      l[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      l[3].join(" ") + " svelte-nl1om8"
    }
  ], f = {};
  for (let a = 0; a < r.length; a += 1)
    f = Ri(f, r[a]);
  return {
    c() {
      e = Vi(
        /*tag*/
        l[14]
      ), o && o.c(), pl(
        /*tag*/
        l[14]
      )(e, f), we(
        e,
        "hidden",
        /*visible*/
        l[10] === !1
      ), we(
        e,
        "padded",
        /*padding*/
        l[6]
      ), we(
        e,
        "border_focus",
        /*border_mode*/
        l[5] === "focus"
      ), we(
        e,
        "border_contrast",
        /*border_mode*/
        l[5] === "contrast"
      ), we(e, "hide-container", !/*explicit_call*/
      l[8] && !/*container*/
      l[9]), x(
        e,
        "height",
        /*get_dimension*/
        l[15](
          /*height*/
          l[0]
        )
      ), x(e, "width", typeof /*width*/
      l[1] == "number" ? `calc(min(${/*width*/
      l[1]}px, 100%))` : (
        /*get_dimension*/
        l[15](
          /*width*/
          l[1]
        )
      )), x(
        e,
        "border-style",
        /*variant*/
        l[4]
      ), x(
        e,
        "overflow",
        /*allow_overflow*/
        l[11] ? "visible" : "hidden"
      ), x(
        e,
        "flex-grow",
        /*scale*/
        l[12]
      ), x(e, "min-width", `calc(min(${/*min_width*/
      l[13]}px, 100%))`), x(e, "border-width", "var(--block-border-width)");
    },
    m(a, s) {
      Wi(a, e, s), o && o.m(e, null), n = !0;
    },
    p(a, s) {
      o && o.p && (!n || s & /*$$scope*/
      131072) && Hi(
        o,
        i,
        a,
        /*$$scope*/
        a[17],
        n ? Ti(
          i,
          /*$$scope*/
          a[17],
          s,
          null
        ) : Pi(
          /*$$scope*/
          a[17]
        ),
        null
      ), pl(
        /*tag*/
        a[14]
      )(e, f = Oi(r, [
        (!n || s & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          a[7]
        ) },
        (!n || s & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          a[2]
        ) },
        (!n || s & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        a[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), we(
        e,
        "hidden",
        /*visible*/
        a[10] === !1
      ), we(
        e,
        "padded",
        /*padding*/
        a[6]
      ), we(
        e,
        "border_focus",
        /*border_mode*/
        a[5] === "focus"
      ), we(
        e,
        "border_contrast",
        /*border_mode*/
        a[5] === "contrast"
      ), we(e, "hide-container", !/*explicit_call*/
      a[8] && !/*container*/
      a[9]), s & /*height*/
      1 && x(
        e,
        "height",
        /*get_dimension*/
        a[15](
          /*height*/
          a[0]
        )
      ), s & /*width*/
      2 && x(e, "width", typeof /*width*/
      a[1] == "number" ? `calc(min(${/*width*/
      a[1]}px, 100%))` : (
        /*get_dimension*/
        a[15](
          /*width*/
          a[1]
        )
      )), s & /*variant*/
      16 && x(
        e,
        "border-style",
        /*variant*/
        a[4]
      ), s & /*allow_overflow*/
      2048 && x(
        e,
        "overflow",
        /*allow_overflow*/
        a[11] ? "visible" : "hidden"
      ), s & /*scale*/
      4096 && x(
        e,
        "flex-grow",
        /*scale*/
        a[12]
      ), s & /*min_width*/
      8192 && x(e, "min-width", `calc(min(${/*min_width*/
      a[13]}px, 100%))`);
    },
    i(a) {
      n || (In(o, a), n = !0);
    },
    o(a) {
      Mn(o, a), n = !1;
    },
    d(a) {
      a && Ni(e), o && o.d(a);
    }
  };
}
function Gi(l) {
  let e, t = (
    /*tag*/
    l[14] && Xi(l)
  );
  return {
    c() {
      t && t.c();
    },
    m(n, i) {
      t && t.m(n, i), e = !0;
    },
    p(n, [i]) {
      /*tag*/
      n[14] && t.p(n, i);
    },
    i(n) {
      e || (In(t, n), e = !0);
    },
    o(n) {
      Mn(t, n), e = !1;
    },
    d(n) {
      t && t.d(n);
    }
  };
}
function Yi(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { height: o = void 0 } = e, { width: r = void 0 } = e, { elem_id: f = "" } = e, { elem_classes: a = [] } = e, { variant: s = "solid" } = e, { border_mode: u = "base" } = e, { padding: _ = !0 } = e, { type: c = "normal" } = e, { test_id: d = void 0 } = e, { explicit_call: h = !1 } = e, { container: y = !0 } = e, { visible: S = !0 } = e, { allow_overflow: v = !0 } = e, { scale: k = null } = e, { min_width: p = 0 } = e, b = c === "fieldset" ? "fieldset" : "div";
  const q = (g) => {
    if (g !== void 0) {
      if (typeof g == "number")
        return g + "px";
      if (typeof g == "string")
        return g;
    }
  };
  return l.$$set = (g) => {
    "height" in g && t(0, o = g.height), "width" in g && t(1, r = g.width), "elem_id" in g && t(2, f = g.elem_id), "elem_classes" in g && t(3, a = g.elem_classes), "variant" in g && t(4, s = g.variant), "border_mode" in g && t(5, u = g.border_mode), "padding" in g && t(6, _ = g.padding), "type" in g && t(16, c = g.type), "test_id" in g && t(7, d = g.test_id), "explicit_call" in g && t(8, h = g.explicit_call), "container" in g && t(9, y = g.container), "visible" in g && t(10, S = g.visible), "allow_overflow" in g && t(11, v = g.allow_overflow), "scale" in g && t(12, k = g.scale), "min_width" in g && t(13, p = g.min_width), "$$scope" in g && t(17, i = g.$$scope);
  }, [
    o,
    r,
    f,
    a,
    s,
    u,
    _,
    d,
    h,
    y,
    S,
    v,
    k,
    p,
    b,
    q,
    c,
    i,
    n
  ];
}
class Ki extends Fi {
  constructor(e) {
    super(), Ui(this, e, Yi, Gi, Zi, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: Ji,
  append: Dt,
  attr: ft,
  create_component: Qi,
  destroy_component: xi,
  detach: $i,
  element: vl,
  init: eo,
  insert: to,
  mount_component: lo,
  safe_not_equal: no,
  set_data: io,
  space: oo,
  text: so,
  toggle_class: De,
  transition_in: ao,
  transition_out: ro
} = window.__gradio__svelte__internal;
function fo(l) {
  let e, t, n, i, o, r;
  return n = new /*Icon*/
  l[1]({}), {
    c() {
      e = vl("label"), t = vl("span"), Qi(n.$$.fragment), i = oo(), o = so(
        /*label*/
        l[0]
      ), ft(t, "class", "svelte-9gxdi0"), ft(e, "for", ""), ft(e, "data-testid", "block-label"), ft(e, "class", "svelte-9gxdi0"), De(e, "hide", !/*show_label*/
      l[2]), De(e, "sr-only", !/*show_label*/
      l[2]), De(
        e,
        "float",
        /*float*/
        l[4]
      ), De(
        e,
        "hide-label",
        /*disable*/
        l[3]
      );
    },
    m(f, a) {
      to(f, e, a), Dt(e, t), lo(n, t, null), Dt(e, i), Dt(e, o), r = !0;
    },
    p(f, [a]) {
      (!r || a & /*label*/
      1) && io(
        o,
        /*label*/
        f[0]
      ), (!r || a & /*show_label*/
      4) && De(e, "hide", !/*show_label*/
      f[2]), (!r || a & /*show_label*/
      4) && De(e, "sr-only", !/*show_label*/
      f[2]), (!r || a & /*float*/
      16) && De(
        e,
        "float",
        /*float*/
        f[4]
      ), (!r || a & /*disable*/
      8) && De(
        e,
        "hide-label",
        /*disable*/
        f[3]
      );
    },
    i(f) {
      r || (ao(n.$$.fragment, f), r = !0);
    },
    o(f) {
      ro(n.$$.fragment, f), r = !1;
    },
    d(f) {
      f && $i(e), xi(n);
    }
  };
}
function uo(l, e, t) {
  let { label: n = null } = e, { Icon: i } = e, { show_label: o = !0 } = e, { disable: r = !1 } = e, { float: f = !0 } = e;
  return l.$$set = (a) => {
    "label" in a && t(0, n = a.label), "Icon" in a && t(1, i = a.Icon), "show_label" in a && t(2, o = a.show_label), "disable" in a && t(3, r = a.disable), "float" in a && t(4, f = a.float);
  }, [n, i, o, r, f];
}
class _o extends Ji {
  constructor(e) {
    super(), eo(this, e, uo, fo, no, {
      label: 0,
      Icon: 1,
      show_label: 2,
      disable: 3,
      float: 4
    });
  }
}
const {
  SvelteComponent: co,
  append: el,
  attr: Le,
  bubble: mo,
  create_component: ho,
  destroy_component: bo,
  detach: An,
  element: tl,
  init: go,
  insert: Dn,
  listen: wo,
  mount_component: ko,
  safe_not_equal: po,
  set_data: vo,
  set_style: He,
  space: yo,
  text: Co,
  toggle_class: Y,
  transition_in: qo,
  transition_out: So
} = window.__gradio__svelte__internal;
function yl(l) {
  let e, t;
  return {
    c() {
      e = tl("span"), t = Co(
        /*label*/
        l[1]
      ), Le(e, "class", "svelte-1lrphxw");
    },
    m(n, i) {
      Dn(n, e, i), el(e, t);
    },
    p(n, i) {
      i & /*label*/
      2 && vo(
        t,
        /*label*/
        n[1]
      );
    },
    d(n) {
      n && An(e);
    }
  };
}
function Lo(l) {
  let e, t, n, i, o, r, f, a = (
    /*show_label*/
    l[2] && yl(l)
  );
  return i = new /*Icon*/
  l[0]({}), {
    c() {
      e = tl("button"), a && a.c(), t = yo(), n = tl("div"), ho(i.$$.fragment), Le(n, "class", "svelte-1lrphxw"), Y(
        n,
        "small",
        /*size*/
        l[4] === "small"
      ), Y(
        n,
        "large",
        /*size*/
        l[4] === "large"
      ), Y(
        n,
        "medium",
        /*size*/
        l[4] === "medium"
      ), e.disabled = /*disabled*/
      l[7], Le(
        e,
        "aria-label",
        /*label*/
        l[1]
      ), Le(
        e,
        "aria-haspopup",
        /*hasPopup*/
        l[8]
      ), Le(
        e,
        "title",
        /*label*/
        l[1]
      ), Le(e, "class", "svelte-1lrphxw"), Y(
        e,
        "pending",
        /*pending*/
        l[3]
      ), Y(
        e,
        "padded",
        /*padded*/
        l[5]
      ), Y(
        e,
        "highlight",
        /*highlight*/
        l[6]
      ), Y(
        e,
        "transparent",
        /*transparent*/
        l[9]
      ), He(e, "color", !/*disabled*/
      l[7] && /*_color*/
      l[12] ? (
        /*_color*/
        l[12]
      ) : "var(--block-label-text-color)"), He(e, "--bg-color", /*disabled*/
      l[7] ? "auto" : (
        /*background*/
        l[10]
      )), He(
        e,
        "margin-left",
        /*offset*/
        l[11] + "px"
      );
    },
    m(s, u) {
      Dn(s, e, u), a && a.m(e, null), el(e, t), el(e, n), ko(i, n, null), o = !0, r || (f = wo(
        e,
        "click",
        /*click_handler*/
        l[14]
      ), r = !0);
    },
    p(s, [u]) {
      /*show_label*/
      s[2] ? a ? a.p(s, u) : (a = yl(s), a.c(), a.m(e, t)) : a && (a.d(1), a = null), (!o || u & /*size*/
      16) && Y(
        n,
        "small",
        /*size*/
        s[4] === "small"
      ), (!o || u & /*size*/
      16) && Y(
        n,
        "large",
        /*size*/
        s[4] === "large"
      ), (!o || u & /*size*/
      16) && Y(
        n,
        "medium",
        /*size*/
        s[4] === "medium"
      ), (!o || u & /*disabled*/
      128) && (e.disabled = /*disabled*/
      s[7]), (!o || u & /*label*/
      2) && Le(
        e,
        "aria-label",
        /*label*/
        s[1]
      ), (!o || u & /*hasPopup*/
      256) && Le(
        e,
        "aria-haspopup",
        /*hasPopup*/
        s[8]
      ), (!o || u & /*label*/
      2) && Le(
        e,
        "title",
        /*label*/
        s[1]
      ), (!o || u & /*pending*/
      8) && Y(
        e,
        "pending",
        /*pending*/
        s[3]
      ), (!o || u & /*padded*/
      32) && Y(
        e,
        "padded",
        /*padded*/
        s[5]
      ), (!o || u & /*highlight*/
      64) && Y(
        e,
        "highlight",
        /*highlight*/
        s[6]
      ), (!o || u & /*transparent*/
      512) && Y(
        e,
        "transparent",
        /*transparent*/
        s[9]
      ), u & /*disabled, _color*/
      4224 && He(e, "color", !/*disabled*/
      s[7] && /*_color*/
      s[12] ? (
        /*_color*/
        s[12]
      ) : "var(--block-label-text-color)"), u & /*disabled, background*/
      1152 && He(e, "--bg-color", /*disabled*/
      s[7] ? "auto" : (
        /*background*/
        s[10]
      )), u & /*offset*/
      2048 && He(
        e,
        "margin-left",
        /*offset*/
        s[11] + "px"
      );
    },
    i(s) {
      o || (qo(i.$$.fragment, s), o = !0);
    },
    o(s) {
      So(i.$$.fragment, s), o = !1;
    },
    d(s) {
      s && An(e), a && a.d(), bo(i), r = !1, f();
    }
  };
}
function jo(l, e, t) {
  let n, { Icon: i } = e, { label: o = "" } = e, { show_label: r = !1 } = e, { pending: f = !1 } = e, { size: a = "small" } = e, { padded: s = !0 } = e, { highlight: u = !1 } = e, { disabled: _ = !1 } = e, { hasPopup: c = !1 } = e, { color: d = "var(--block-label-text-color)" } = e, { transparent: h = !1 } = e, { background: y = "var(--background-fill-primary)" } = e, { offset: S = 0 } = e;
  function v(k) {
    mo.call(this, l, k);
  }
  return l.$$set = (k) => {
    "Icon" in k && t(0, i = k.Icon), "label" in k && t(1, o = k.label), "show_label" in k && t(2, r = k.show_label), "pending" in k && t(3, f = k.pending), "size" in k && t(4, a = k.size), "padded" in k && t(5, s = k.padded), "highlight" in k && t(6, u = k.highlight), "disabled" in k && t(7, _ = k.disabled), "hasPopup" in k && t(8, c = k.hasPopup), "color" in k && t(13, d = k.color), "transparent" in k && t(9, h = k.transparent), "background" in k && t(10, y = k.background), "offset" in k && t(11, S = k.offset);
  }, l.$$.update = () => {
    l.$$.dirty & /*highlight, color*/
    8256 && t(12, n = u ? "var(--color-accent)" : d);
  }, [
    i,
    o,
    r,
    f,
    a,
    s,
    u,
    _,
    c,
    h,
    y,
    S,
    n,
    d,
    v
  ];
}
class ze extends co {
  constructor(e) {
    super(), go(this, e, jo, Lo, po, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 13,
      transparent: 9,
      background: 10,
      offset: 11
    });
  }
}
const {
  SvelteComponent: zo,
  append: Eo,
  attr: Ft,
  binding_callbacks: Io,
  create_slot: Mo,
  detach: Ao,
  element: Cl,
  get_all_dirty_from_scope: Do,
  get_slot_changes: Fo,
  init: Ro,
  insert: Bo,
  safe_not_equal: No,
  toggle_class: Fe,
  transition_in: Vo,
  transition_out: Po,
  update_slot_base: To
} = window.__gradio__svelte__internal;
function Oo(l) {
  let e, t, n;
  const i = (
    /*#slots*/
    l[5].default
  ), o = Mo(
    i,
    l,
    /*$$scope*/
    l[4],
    null
  );
  return {
    c() {
      e = Cl("div"), t = Cl("div"), o && o.c(), Ft(t, "class", "icon svelte-3w3rth"), Ft(e, "class", "empty svelte-3w3rth"), Ft(e, "aria-label", "Empty value"), Fe(
        e,
        "small",
        /*size*/
        l[0] === "small"
      ), Fe(
        e,
        "large",
        /*size*/
        l[0] === "large"
      ), Fe(
        e,
        "unpadded_box",
        /*unpadded_box*/
        l[1]
      ), Fe(
        e,
        "small_parent",
        /*parent_height*/
        l[3]
      );
    },
    m(r, f) {
      Bo(r, e, f), Eo(e, t), o && o.m(t, null), l[6](e), n = !0;
    },
    p(r, [f]) {
      o && o.p && (!n || f & /*$$scope*/
      16) && To(
        o,
        i,
        r,
        /*$$scope*/
        r[4],
        n ? Fo(
          i,
          /*$$scope*/
          r[4],
          f,
          null
        ) : Do(
          /*$$scope*/
          r[4]
        ),
        null
      ), (!n || f & /*size*/
      1) && Fe(
        e,
        "small",
        /*size*/
        r[0] === "small"
      ), (!n || f & /*size*/
      1) && Fe(
        e,
        "large",
        /*size*/
        r[0] === "large"
      ), (!n || f & /*unpadded_box*/
      2) && Fe(
        e,
        "unpadded_box",
        /*unpadded_box*/
        r[1]
      ), (!n || f & /*parent_height*/
      8) && Fe(
        e,
        "small_parent",
        /*parent_height*/
        r[3]
      );
    },
    i(r) {
      n || (Vo(o, r), n = !0);
    },
    o(r) {
      Po(o, r), n = !1;
    },
    d(r) {
      r && Ao(e), o && o.d(r), l[6](null);
    }
  };
}
function Uo(l, e, t) {
  let n, { $$slots: i = {}, $$scope: o } = e, { size: r = "small" } = e, { unpadded_box: f = !1 } = e, a;
  function s(_) {
    var h;
    if (!_)
      return !1;
    const { height: c } = _.getBoundingClientRect(), { height: d } = ((h = _.parentElement) == null ? void 0 : h.getBoundingClientRect()) || { height: c };
    return c > d + 2;
  }
  function u(_) {
    Io[_ ? "unshift" : "push"](() => {
      a = _, t(2, a);
    });
  }
  return l.$$set = (_) => {
    "size" in _ && t(0, r = _.size), "unpadded_box" in _ && t(1, f = _.unpadded_box), "$$scope" in _ && t(4, o = _.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty & /*el*/
    4 && t(3, n = s(a));
  }, [r, f, a, n, o, i, u];
}
class Wo extends zo {
  constructor(e) {
    super(), Ro(this, e, Uo, Oo, No, { size: 0, unpadded_box: 1 });
  }
}
const {
  SvelteComponent: Zo,
  append: Rt,
  attr: oe,
  detach: Ho,
  init: Xo,
  insert: Go,
  noop: Bt,
  safe_not_equal: Yo,
  set_style: ke,
  svg_element: ut
} = window.__gradio__svelte__internal;
function Ko(l) {
  let e, t, n, i;
  return {
    c() {
      e = ut("svg"), t = ut("g"), n = ut("path"), i = ut("path"), oe(n, "d", "M18,6L6.087,17.913"), ke(n, "fill", "none"), ke(n, "fill-rule", "nonzero"), ke(n, "stroke-width", "2px"), oe(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), oe(i, "d", "M4.364,4.364L19.636,19.636"), ke(i, "fill", "none"), ke(i, "fill-rule", "nonzero"), ke(i, "stroke-width", "2px"), oe(e, "width", "100%"), oe(e, "height", "100%"), oe(e, "viewBox", "0 0 24 24"), oe(e, "version", "1.1"), oe(e, "xmlns", "http://www.w3.org/2000/svg"), oe(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), oe(e, "xml:space", "preserve"), oe(e, "stroke", "currentColor"), ke(e, "fill-rule", "evenodd"), ke(e, "clip-rule", "evenodd"), ke(e, "stroke-linecap", "round"), ke(e, "stroke-linejoin", "round");
    },
    m(o, r) {
      Go(o, e, r), Rt(e, t), Rt(t, n), Rt(e, i);
    },
    p: Bt,
    i: Bt,
    o: Bt,
    d(o) {
      o && Ho(e);
    }
  };
}
class Fn extends Zo {
  constructor(e) {
    super(), Xo(this, e, null, Ko, Yo, {});
  }
}
const {
  SvelteComponent: Jo,
  append: Qo,
  attr: et,
  detach: xo,
  init: $o,
  insert: es,
  noop: Nt,
  safe_not_equal: ts,
  svg_element: ql
} = window.__gradio__svelte__internal;
function ls(l) {
  let e, t;
  return {
    c() {
      e = ql("svg"), t = ql("path"), et(t, "d", "M23,20a5,5,0,0,0-3.89,1.89L11.8,17.32a4.46,4.46,0,0,0,0-2.64l7.31-4.57A5,5,0,1,0,18,7a4.79,4.79,0,0,0,.2,1.32l-7.31,4.57a5,5,0,1,0,0,6.22l7.31,4.57A4.79,4.79,0,0,0,18,25a5,5,0,1,0,5-5ZM23,4a3,3,0,1,1-3,3A3,3,0,0,1,23,4ZM7,19a3,3,0,1,1,3-3A3,3,0,0,1,7,19Zm16,9a3,3,0,1,1,3-3A3,3,0,0,1,23,28Z"), et(t, "fill", "currentColor"), et(e, "id", "icon"), et(e, "xmlns", "http://www.w3.org/2000/svg"), et(e, "viewBox", "0 0 32 32");
    },
    m(n, i) {
      es(n, e, i), Qo(e, t);
    },
    p: Nt,
    i: Nt,
    o: Nt,
    d(n) {
      n && xo(e);
    }
  };
}
class ns extends Jo {
  constructor(e) {
    super(), $o(this, e, null, ls, ts, {});
  }
}
const {
  SvelteComponent: is,
  append: os,
  attr: Xe,
  detach: ss,
  init: as,
  insert: rs,
  noop: Vt,
  safe_not_equal: fs,
  svg_element: Sl
} = window.__gradio__svelte__internal;
function us(l) {
  let e, t;
  return {
    c() {
      e = Sl("svg"), t = Sl("path"), Xe(t, "fill", "currentColor"), Xe(t, "d", "M26 24v4H6v-4H4v4a2 2 0 0 0 2 2h20a2 2 0 0 0 2-2v-4zm0-10l-1.41-1.41L17 20.17V2h-2v18.17l-7.59-7.58L6 14l10 10l10-10z"), Xe(e, "xmlns", "http://www.w3.org/2000/svg"), Xe(e, "width", "100%"), Xe(e, "height", "100%"), Xe(e, "viewBox", "0 0 32 32");
    },
    m(n, i) {
      rs(n, e, i), os(e, t);
    },
    p: Vt,
    i: Vt,
    o: Vt,
    d(n) {
      n && ss(e);
    }
  };
}
class Rn extends is {
  constructor(e) {
    super(), as(this, e, null, us, fs, {});
  }
}
const {
  SvelteComponent: _s,
  append: cs,
  attr: se,
  detach: ds,
  init: ms,
  insert: hs,
  noop: Pt,
  safe_not_equal: bs,
  svg_element: Ll
} = window.__gradio__svelte__internal;
function gs(l) {
  let e, t;
  return {
    c() {
      e = Ll("svg"), t = Ll("path"), se(t, "d", "M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"), se(e, "xmlns", "http://www.w3.org/2000/svg"), se(e, "width", "100%"), se(e, "height", "100%"), se(e, "viewBox", "0 0 24 24"), se(e, "fill", "none"), se(e, "stroke", "currentColor"), se(e, "stroke-width", "1.5"), se(e, "stroke-linecap", "round"), se(e, "stroke-linejoin", "round"), se(e, "class", "feather feather-edit-2");
    },
    m(n, i) {
      hs(n, e, i), cs(e, t);
    },
    p: Pt,
    i: Pt,
    o: Pt,
    d(n) {
      n && ds(e);
    }
  };
}
class ws extends _s {
  constructor(e) {
    super(), ms(this, e, null, gs, bs, {});
  }
}
const {
  SvelteComponent: ks,
  append: Tt,
  attr: V,
  detach: ps,
  init: vs,
  insert: ys,
  noop: Ot,
  safe_not_equal: Cs,
  svg_element: _t
} = window.__gradio__svelte__internal;
function qs(l) {
  let e, t, n, i;
  return {
    c() {
      e = _t("svg"), t = _t("rect"), n = _t("circle"), i = _t("polyline"), V(t, "x", "3"), V(t, "y", "3"), V(t, "width", "18"), V(t, "height", "18"), V(t, "rx", "2"), V(t, "ry", "2"), V(n, "cx", "8.5"), V(n, "cy", "8.5"), V(n, "r", "1.5"), V(i, "points", "21 15 16 10 5 21"), V(e, "xmlns", "http://www.w3.org/2000/svg"), V(e, "width", "100%"), V(e, "height", "100%"), V(e, "viewBox", "0 0 24 24"), V(e, "fill", "none"), V(e, "stroke", "currentColor"), V(e, "stroke-width", "1.5"), V(e, "stroke-linecap", "round"), V(e, "stroke-linejoin", "round"), V(e, "class", "feather feather-image");
    },
    m(o, r) {
      ys(o, e, r), Tt(e, t), Tt(e, n), Tt(e, i);
    },
    p: Ot,
    i: Ot,
    o: Ot,
    d(o) {
      o && ps(e);
    }
  };
}
let Bn = class extends ks {
  constructor(e) {
    super(), vs(this, e, null, qs, Cs, {});
  }
};
const {
  SvelteComponent: Ss,
  append: jl,
  attr: X,
  detach: Ls,
  init: js,
  insert: zs,
  noop: zl,
  safe_not_equal: Es,
  svg_element: Ut
} = window.__gradio__svelte__internal;
function Is(l) {
  let e, t, n, i;
  return {
    c() {
      e = Ut("svg"), t = Ut("path"), n = Ut("path"), X(t, "stroke", "currentColor"), X(t, "stroke-width", "1.5"), X(t, "stroke-linecap", "round"), X(t, "d", "M16.472 20H4.1a.6.6 0 0 1-.6-.6V9.6a.6.6 0 0 1 .6-.6h2.768a2 2 0 0 0 1.715-.971l2.71-4.517a1.631 1.631 0 0 1 2.961 1.308l-1.022 3.408a.6.6 0 0 0 .574.772h4.575a2 2 0 0 1 1.93 2.526l-1.91 7A2 2 0 0 1 16.473 20Z"), X(n, "stroke", "currentColor"), X(n, "stroke-width", "1.5"), X(n, "stroke-linecap", "round"), X(n, "stroke-linejoin", "round"), X(n, "d", "M7 20V9"), X(e, "xmlns", "http://www.w3.org/2000/svg"), X(e, "viewBox", "0 0 24 24"), X(e, "fill", i = /*selected*/
      l[0] ? "currentColor" : "none"), X(e, "stroke-width", "1.5"), X(e, "color", "currentColor");
    },
    m(o, r) {
      zs(o, e, r), jl(e, t), jl(e, n);
    },
    p(o, [r]) {
      r & /*selected*/
      1 && i !== (i = /*selected*/
      o[0] ? "currentColor" : "none") && X(e, "fill", i);
    },
    i: zl,
    o: zl,
    d(o) {
      o && Ls(e);
    }
  };
}
function Ms(l, e, t) {
  let { selected: n } = e;
  return l.$$set = (i) => {
    "selected" in i && t(0, n = i.selected);
  }, [n];
}
class As extends Ss {
  constructor(e) {
    super(), js(this, e, Ms, Is, Es, { selected: 0 });
  }
}
const {
  SvelteComponent: Ds,
  append: El,
  attr: $,
  detach: Fs,
  init: Rs,
  insert: Bs,
  noop: Wt,
  safe_not_equal: Ns,
  svg_element: Zt
} = window.__gradio__svelte__internal;
function Vs(l) {
  let e, t, n;
  return {
    c() {
      e = Zt("svg"), t = Zt("polyline"), n = Zt("path"), $(t, "points", "1 4 1 10 7 10"), $(n, "d", "M3.51 15a9 9 0 1 0 2.13-9.36L1 10"), $(e, "xmlns", "http://www.w3.org/2000/svg"), $(e, "width", "100%"), $(e, "height", "100%"), $(e, "viewBox", "0 0 24 24"), $(e, "fill", "none"), $(e, "stroke", "currentColor"), $(e, "stroke-width", "2"), $(e, "stroke-linecap", "round"), $(e, "stroke-linejoin", "round"), $(e, "class", "feather feather-rotate-ccw");
    },
    m(i, o) {
      Bs(i, e, o), El(e, t), El(e, n);
    },
    p: Wt,
    i: Wt,
    o: Wt,
    d(i) {
      i && Fs(e);
    }
  };
}
class Ps extends Ds {
  constructor(e) {
    super(), Rs(this, e, null, Vs, Ns, {});
  }
}
const Ts = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], Il = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
Ts.reduce(
  (l, { color: e, primary: t, secondary: n }) => ({
    ...l,
    [e]: {
      primary: Il[e][t],
      secondary: Il[e][n]
    }
  }),
  {}
);
class Os extends Error {
  constructor(e) {
    super(e), this.name = "ShareError";
  }
}
const {
  SvelteComponent: Us,
  create_component: Ws,
  destroy_component: Zs,
  init: Hs,
  mount_component: Xs,
  safe_not_equal: Gs,
  transition_in: Ys,
  transition_out: Ks
} = window.__gradio__svelte__internal, { createEventDispatcher: Js } = window.__gradio__svelte__internal;
function Qs(l) {
  let e, t;
  return e = new ze({
    props: {
      Icon: ns,
      label: (
        /*i18n*/
        l[2]("common.share")
      ),
      pending: (
        /*pending*/
        l[3]
      )
    }
  }), e.$on(
    "click",
    /*click_handler*/
    l[5]
  ), {
    c() {
      Ws(e.$$.fragment);
    },
    m(n, i) {
      Xs(e, n, i), t = !0;
    },
    p(n, [i]) {
      const o = {};
      i & /*i18n*/
      4 && (o.label = /*i18n*/
      n[2]("common.share")), i & /*pending*/
      8 && (o.pending = /*pending*/
      n[3]), e.$set(o);
    },
    i(n) {
      t || (Ys(e.$$.fragment, n), t = !0);
    },
    o(n) {
      Ks(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Zs(e, n);
    }
  };
}
function xs(l, e, t) {
  const n = Js();
  let { formatter: i } = e, { value: o } = e, { i18n: r } = e, f = !1;
  const a = async () => {
    try {
      t(3, f = !0);
      const s = await i(o);
      n("share", { description: s });
    } catch (s) {
      console.error(s);
      let u = s instanceof Os ? s.message : "Share failed.";
      n("error", u);
    } finally {
      t(3, f = !1);
    }
  };
  return l.$$set = (s) => {
    "formatter" in s && t(0, i = s.formatter), "value" in s && t(1, o = s.value), "i18n" in s && t(2, r = s.i18n);
  }, [i, o, r, f, n, a];
}
class $s extends Us {
  constructor(e) {
    super(), Hs(this, e, xs, Qs, Gs, { formatter: 0, value: 1, i18n: 2 });
  }
}
function Ye(l) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; l > 1e3 && t < e.length - 1; )
    l /= 1e3, t++;
  let n = e[t];
  return (Number.isInteger(l) ? l : l.toFixed(1)) + n;
}
function ht() {
}
function ea(l, e) {
  return l != l ? e == e : l !== e || l && typeof l == "object" || typeof l == "function";
}
const Nn = typeof window < "u";
let Ml = Nn ? () => window.performance.now() : () => Date.now(), Vn = Nn ? (l) => requestAnimationFrame(l) : ht;
const Qe = /* @__PURE__ */ new Set();
function Pn(l) {
  Qe.forEach((e) => {
    e.c(l) || (Qe.delete(e), e.f());
  }), Qe.size !== 0 && Vn(Pn);
}
function ta(l) {
  let e;
  return Qe.size === 0 && Vn(Pn), {
    promise: new Promise((t) => {
      Qe.add(e = { c: l, f: t });
    }),
    abort() {
      Qe.delete(e);
    }
  };
}
const Ge = [];
function la(l, e = ht) {
  let t;
  const n = /* @__PURE__ */ new Set();
  function i(f) {
    if (ea(l, f) && (l = f, t)) {
      const a = !Ge.length;
      for (const s of n)
        s[1](), Ge.push(s, l);
      if (a) {
        for (let s = 0; s < Ge.length; s += 2)
          Ge[s][0](Ge[s + 1]);
        Ge.length = 0;
      }
    }
  }
  function o(f) {
    i(f(l));
  }
  function r(f, a = ht) {
    const s = [f, a];
    return n.add(s), n.size === 1 && (t = e(i, o) || ht), f(l), () => {
      n.delete(s), n.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: o, subscribe: r };
}
function Al(l) {
  return Object.prototype.toString.call(l) === "[object Date]";
}
function ll(l, e, t, n) {
  if (typeof t == "number" || Al(t)) {
    const i = n - t, o = (t - e) / (l.dt || 1 / 60), r = l.opts.stiffness * i, f = l.opts.damping * o, a = (r - f) * l.inv_mass, s = (o + a) * l.dt;
    return Math.abs(s) < l.opts.precision && Math.abs(i) < l.opts.precision ? n : (l.settled = !1, Al(t) ? new Date(t.getTime() + s) : t + s);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, o) => ll(l, e[o], t[o], n[o])
      );
    if (typeof t == "object") {
      const i = {};
      for (const o in t)
        i[o] = ll(l, e[o], t[o], n[o]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function Dl(l, e = {}) {
  const t = la(l), { stiffness: n = 0.15, damping: i = 0.8, precision: o = 0.01 } = e;
  let r, f, a, s = l, u = l, _ = 1, c = 0, d = !1;
  function h(S, v = {}) {
    u = S;
    const k = a = {};
    return l == null || v.hard || y.stiffness >= 1 && y.damping >= 1 ? (d = !0, r = Ml(), s = S, t.set(l = u), Promise.resolve()) : (v.soft && (c = 1 / ((v.soft === !0 ? 0.5 : +v.soft) * 60), _ = 0), f || (r = Ml(), d = !1, f = ta((p) => {
      if (d)
        return d = !1, f = null, !1;
      _ = Math.min(_ + c, 1);
      const b = {
        inv_mass: _,
        opts: y,
        settled: !0,
        dt: (p - r) * 60 / 1e3
      }, q = ll(b, s, l, u);
      return r = p, s = l, t.set(l = q), b.settled && (f = null), !b.settled;
    })), new Promise((p) => {
      f.promise.then(() => {
        k === a && p();
      });
    }));
  }
  const y = {
    set: h,
    update: (S, v) => h(S(u, l), v),
    subscribe: t.subscribe,
    stiffness: n,
    damping: i,
    precision: o
  };
  return y;
}
const {
  SvelteComponent: na,
  append: ae,
  attr: I,
  component_subscribe: Fl,
  detach: ia,
  element: oa,
  init: sa,
  insert: aa,
  noop: Rl,
  safe_not_equal: ra,
  set_style: ct,
  svg_element: re,
  toggle_class: Bl
} = window.__gradio__svelte__internal, { onMount: fa } = window.__gradio__svelte__internal;
function ua(l) {
  let e, t, n, i, o, r, f, a, s, u, _, c;
  return {
    c() {
      e = oa("div"), t = re("svg"), n = re("g"), i = re("path"), o = re("path"), r = re("path"), f = re("path"), a = re("g"), s = re("path"), u = re("path"), _ = re("path"), c = re("path"), I(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), I(i, "fill", "#FF7C00"), I(i, "fill-opacity", "0.4"), I(i, "class", "svelte-43sxxs"), I(o, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), I(o, "fill", "#FF7C00"), I(o, "class", "svelte-43sxxs"), I(r, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), I(r, "fill", "#FF7C00"), I(r, "fill-opacity", "0.4"), I(r, "class", "svelte-43sxxs"), I(f, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), I(f, "fill", "#FF7C00"), I(f, "class", "svelte-43sxxs"), ct(n, "transform", "translate(" + /*$top*/
      l[1][0] + "px, " + /*$top*/
      l[1][1] + "px)"), I(s, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), I(s, "fill", "#FF7C00"), I(s, "fill-opacity", "0.4"), I(s, "class", "svelte-43sxxs"), I(u, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), I(u, "fill", "#FF7C00"), I(u, "class", "svelte-43sxxs"), I(_, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), I(_, "fill", "#FF7C00"), I(_, "fill-opacity", "0.4"), I(_, "class", "svelte-43sxxs"), I(c, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), I(c, "fill", "#FF7C00"), I(c, "class", "svelte-43sxxs"), ct(a, "transform", "translate(" + /*$bottom*/
      l[2][0] + "px, " + /*$bottom*/
      l[2][1] + "px)"), I(t, "viewBox", "-1200 -1200 3000 3000"), I(t, "fill", "none"), I(t, "xmlns", "http://www.w3.org/2000/svg"), I(t, "class", "svelte-43sxxs"), I(e, "class", "svelte-43sxxs"), Bl(
        e,
        "margin",
        /*margin*/
        l[0]
      );
    },
    m(d, h) {
      aa(d, e, h), ae(e, t), ae(t, n), ae(n, i), ae(n, o), ae(n, r), ae(n, f), ae(t, a), ae(a, s), ae(a, u), ae(a, _), ae(a, c);
    },
    p(d, [h]) {
      h & /*$top*/
      2 && ct(n, "transform", "translate(" + /*$top*/
      d[1][0] + "px, " + /*$top*/
      d[1][1] + "px)"), h & /*$bottom*/
      4 && ct(a, "transform", "translate(" + /*$bottom*/
      d[2][0] + "px, " + /*$bottom*/
      d[2][1] + "px)"), h & /*margin*/
      1 && Bl(
        e,
        "margin",
        /*margin*/
        d[0]
      );
    },
    i: Rl,
    o: Rl,
    d(d) {
      d && ia(e);
    }
  };
}
function _a(l, e, t) {
  let n, i, { margin: o = !0 } = e;
  const r = Dl([0, 0]);
  Fl(l, r, (c) => t(1, n = c));
  const f = Dl([0, 0]);
  Fl(l, f, (c) => t(2, i = c));
  let a;
  async function s() {
    await Promise.all([r.set([125, 140]), f.set([-125, -140])]), await Promise.all([r.set([-125, 140]), f.set([125, -140])]), await Promise.all([r.set([-125, 0]), f.set([125, -0])]), await Promise.all([r.set([125, 0]), f.set([-125, 0])]);
  }
  async function u() {
    await s(), a || u();
  }
  async function _() {
    await Promise.all([r.set([125, 0]), f.set([-125, 0])]), u();
  }
  return fa(() => (_(), () => a = !0)), l.$$set = (c) => {
    "margin" in c && t(0, o = c.margin);
  }, [o, n, i, r, f];
}
class Tn extends na {
  constructor(e) {
    super(), sa(this, e, _a, ua, ra, { margin: 0 });
  }
}
const {
  SvelteComponent: ca,
  append: Ve,
  attr: _e,
  binding_callbacks: Nl,
  check_outros: nl,
  create_component: On,
  create_slot: Un,
  destroy_component: Wn,
  destroy_each: Zn,
  detach: j,
  element: ve,
  empty: xe,
  ensure_array_like: gt,
  get_all_dirty_from_scope: Hn,
  get_slot_changes: Xn,
  group_outros: il,
  init: da,
  insert: z,
  mount_component: Gn,
  noop: ol,
  safe_not_equal: ma,
  set_data: ne,
  set_style: Be,
  space: le,
  text: R,
  toggle_class: ee,
  transition_in: ue,
  transition_out: ye,
  update_slot_base: Yn
} = window.__gradio__svelte__internal, { tick: ha } = window.__gradio__svelte__internal, { onDestroy: ba } = window.__gradio__svelte__internal, { createEventDispatcher: ga } = window.__gradio__svelte__internal, wa = (l) => ({}), Vl = (l) => ({}), ka = (l) => ({}), Pl = (l) => ({});
function Tl(l, e, t) {
  const n = l.slice();
  return n[40] = e[t], n[42] = t, n;
}
function Ol(l, e, t) {
  const n = l.slice();
  return n[40] = e[t], n;
}
function pa(l) {
  let e, t, n, i, o = (
    /*i18n*/
    l[1]("common.error") + ""
  ), r, f, a;
  t = new ze({
    props: {
      Icon: Fn,
      label: (
        /*i18n*/
        l[1]("common.clear")
      ),
      disabled: !1
    }
  }), t.$on(
    "click",
    /*click_handler*/
    l[32]
  );
  const s = (
    /*#slots*/
    l[30].error
  ), u = Un(
    s,
    l,
    /*$$scope*/
    l[29],
    Vl
  );
  return {
    c() {
      e = ve("div"), On(t.$$.fragment), n = le(), i = ve("span"), r = R(o), f = le(), u && u.c(), _e(e, "class", "clear-status svelte-vopvsi"), _e(i, "class", "error svelte-vopvsi");
    },
    m(_, c) {
      z(_, e, c), Gn(t, e, null), z(_, n, c), z(_, i, c), Ve(i, r), z(_, f, c), u && u.m(_, c), a = !0;
    },
    p(_, c) {
      const d = {};
      c[0] & /*i18n*/
      2 && (d.label = /*i18n*/
      _[1]("common.clear")), t.$set(d), (!a || c[0] & /*i18n*/
      2) && o !== (o = /*i18n*/
      _[1]("common.error") + "") && ne(r, o), u && u.p && (!a || c[0] & /*$$scope*/
      536870912) && Yn(
        u,
        s,
        _,
        /*$$scope*/
        _[29],
        a ? Xn(
          s,
          /*$$scope*/
          _[29],
          c,
          wa
        ) : Hn(
          /*$$scope*/
          _[29]
        ),
        Vl
      );
    },
    i(_) {
      a || (ue(t.$$.fragment, _), ue(u, _), a = !0);
    },
    o(_) {
      ye(t.$$.fragment, _), ye(u, _), a = !1;
    },
    d(_) {
      _ && (j(e), j(n), j(i), j(f)), Wn(t), u && u.d(_);
    }
  };
}
function va(l) {
  let e, t, n, i, o, r, f, a, s, u = (
    /*variant*/
    l[8] === "default" && /*show_eta_bar*/
    l[18] && /*show_progress*/
    l[6] === "full" && Ul(l)
  );
  function _(p, b) {
    if (
      /*progress*/
      p[7]
    )
      return qa;
    if (
      /*queue_position*/
      p[2] !== null && /*queue_size*/
      p[3] !== void 0 && /*queue_position*/
      p[2] >= 0
    )
      return Ca;
    if (
      /*queue_position*/
      p[2] === 0
    )
      return ya;
  }
  let c = _(l), d = c && c(l), h = (
    /*timer*/
    l[5] && Hl(l)
  );
  const y = [za, ja], S = [];
  function v(p, b) {
    return (
      /*last_progress_level*/
      p[15] != null ? 0 : (
        /*show_progress*/
        p[6] === "full" ? 1 : -1
      )
    );
  }
  ~(o = v(l)) && (r = S[o] = y[o](l));
  let k = !/*timer*/
  l[5] && xl(l);
  return {
    c() {
      u && u.c(), e = le(), t = ve("div"), d && d.c(), n = le(), h && h.c(), i = le(), r && r.c(), f = le(), k && k.c(), a = xe(), _e(t, "class", "progress-text svelte-vopvsi"), ee(
        t,
        "meta-text-center",
        /*variant*/
        l[8] === "center"
      ), ee(
        t,
        "meta-text",
        /*variant*/
        l[8] === "default"
      );
    },
    m(p, b) {
      u && u.m(p, b), z(p, e, b), z(p, t, b), d && d.m(t, null), Ve(t, n), h && h.m(t, null), z(p, i, b), ~o && S[o].m(p, b), z(p, f, b), k && k.m(p, b), z(p, a, b), s = !0;
    },
    p(p, b) {
      /*variant*/
      p[8] === "default" && /*show_eta_bar*/
      p[18] && /*show_progress*/
      p[6] === "full" ? u ? u.p(p, b) : (u = Ul(p), u.c(), u.m(e.parentNode, e)) : u && (u.d(1), u = null), c === (c = _(p)) && d ? d.p(p, b) : (d && d.d(1), d = c && c(p), d && (d.c(), d.m(t, n))), /*timer*/
      p[5] ? h ? h.p(p, b) : (h = Hl(p), h.c(), h.m(t, null)) : h && (h.d(1), h = null), (!s || b[0] & /*variant*/
      256) && ee(
        t,
        "meta-text-center",
        /*variant*/
        p[8] === "center"
      ), (!s || b[0] & /*variant*/
      256) && ee(
        t,
        "meta-text",
        /*variant*/
        p[8] === "default"
      );
      let q = o;
      o = v(p), o === q ? ~o && S[o].p(p, b) : (r && (il(), ye(S[q], 1, 1, () => {
        S[q] = null;
      }), nl()), ~o ? (r = S[o], r ? r.p(p, b) : (r = S[o] = y[o](p), r.c()), ue(r, 1), r.m(f.parentNode, f)) : r = null), /*timer*/
      p[5] ? k && (il(), ye(k, 1, 1, () => {
        k = null;
      }), nl()) : k ? (k.p(p, b), b[0] & /*timer*/
      32 && ue(k, 1)) : (k = xl(p), k.c(), ue(k, 1), k.m(a.parentNode, a));
    },
    i(p) {
      s || (ue(r), ue(k), s = !0);
    },
    o(p) {
      ye(r), ye(k), s = !1;
    },
    d(p) {
      p && (j(e), j(t), j(i), j(f), j(a)), u && u.d(p), d && d.d(), h && h.d(), ~o && S[o].d(p), k && k.d(p);
    }
  };
}
function Ul(l) {
  let e, t = `translateX(${/*eta_level*/
  (l[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = ve("div"), _e(e, "class", "eta-bar svelte-vopvsi"), Be(e, "transform", t);
    },
    m(n, i) {
      z(n, e, i);
    },
    p(n, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (n[17] || 0) * 100 - 100}%)`) && Be(e, "transform", t);
    },
    d(n) {
      n && j(e);
    }
  };
}
function ya(l) {
  let e;
  return {
    c() {
      e = R("processing |");
    },
    m(t, n) {
      z(t, e, n);
    },
    p: ol,
    d(t) {
      t && j(e);
    }
  };
}
function Ca(l) {
  let e, t = (
    /*queue_position*/
    l[2] + 1 + ""
  ), n, i, o, r;
  return {
    c() {
      e = R("queue: "), n = R(t), i = R("/"), o = R(
        /*queue_size*/
        l[3]
      ), r = R(" |");
    },
    m(f, a) {
      z(f, e, a), z(f, n, a), z(f, i, a), z(f, o, a), z(f, r, a);
    },
    p(f, a) {
      a[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      f[2] + 1 + "") && ne(n, t), a[0] & /*queue_size*/
      8 && ne(
        o,
        /*queue_size*/
        f[3]
      );
    },
    d(f) {
      f && (j(e), j(n), j(i), j(o), j(r));
    }
  };
}
function qa(l) {
  let e, t = gt(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = Zl(Ol(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = xe();
    },
    m(i, o) {
      for (let r = 0; r < n.length; r += 1)
        n[r] && n[r].m(i, o);
      z(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress*/
      128) {
        t = gt(
          /*progress*/
          i[7]
        );
        let r;
        for (r = 0; r < t.length; r += 1) {
          const f = Ol(i, t, r);
          n[r] ? n[r].p(f, o) : (n[r] = Zl(f), n[r].c(), n[r].m(e.parentNode, e));
        }
        for (; r < n.length; r += 1)
          n[r].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && j(e), Zn(n, i);
    }
  };
}
function Wl(l) {
  let e, t = (
    /*p*/
    l[40].unit + ""
  ), n, i, o = " ", r;
  function f(u, _) {
    return (
      /*p*/
      u[40].length != null ? La : Sa
    );
  }
  let a = f(l), s = a(l);
  return {
    c() {
      s.c(), e = le(), n = R(t), i = R(" | "), r = R(o);
    },
    m(u, _) {
      s.m(u, _), z(u, e, _), z(u, n, _), z(u, i, _), z(u, r, _);
    },
    p(u, _) {
      a === (a = f(u)) && s ? s.p(u, _) : (s.d(1), s = a(u), s && (s.c(), s.m(e.parentNode, e))), _[0] & /*progress*/
      128 && t !== (t = /*p*/
      u[40].unit + "") && ne(n, t);
    },
    d(u) {
      u && (j(e), j(n), j(i), j(r)), s.d(u);
    }
  };
}
function Sa(l) {
  let e = Ye(
    /*p*/
    l[40].index || 0
  ) + "", t;
  return {
    c() {
      t = R(e);
    },
    m(n, i) {
      z(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = Ye(
        /*p*/
        n[40].index || 0
      ) + "") && ne(t, e);
    },
    d(n) {
      n && j(t);
    }
  };
}
function La(l) {
  let e = Ye(
    /*p*/
    l[40].index || 0
  ) + "", t, n, i = Ye(
    /*p*/
    l[40].length
  ) + "", o;
  return {
    c() {
      t = R(e), n = R("/"), o = R(i);
    },
    m(r, f) {
      z(r, t, f), z(r, n, f), z(r, o, f);
    },
    p(r, f) {
      f[0] & /*progress*/
      128 && e !== (e = Ye(
        /*p*/
        r[40].index || 0
      ) + "") && ne(t, e), f[0] & /*progress*/
      128 && i !== (i = Ye(
        /*p*/
        r[40].length
      ) + "") && ne(o, i);
    },
    d(r) {
      r && (j(t), j(n), j(o));
    }
  };
}
function Zl(l) {
  let e, t = (
    /*p*/
    l[40].index != null && Wl(l)
  );
  return {
    c() {
      t && t.c(), e = xe();
    },
    m(n, i) {
      t && t.m(n, i), z(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[40].index != null ? t ? t.p(n, i) : (t = Wl(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && j(e), t && t.d(n);
    }
  };
}
function Hl(l) {
  let e, t = (
    /*eta*/
    l[0] ? `/${/*formatted_eta*/
    l[19]}` : ""
  ), n, i;
  return {
    c() {
      e = R(
        /*formatted_timer*/
        l[20]
      ), n = R(t), i = R("s");
    },
    m(o, r) {
      z(o, e, r), z(o, n, r), z(o, i, r);
    },
    p(o, r) {
      r[0] & /*formatted_timer*/
      1048576 && ne(
        e,
        /*formatted_timer*/
        o[20]
      ), r[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      o[0] ? `/${/*formatted_eta*/
      o[19]}` : "") && ne(n, t);
    },
    d(o) {
      o && (j(e), j(n), j(i));
    }
  };
}
function ja(l) {
  let e, t;
  return e = new Tn({
    props: { margin: (
      /*variant*/
      l[8] === "default"
    ) }
  }), {
    c() {
      On(e.$$.fragment);
    },
    m(n, i) {
      Gn(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*variant*/
      256 && (o.margin = /*variant*/
      n[8] === "default"), e.$set(o);
    },
    i(n) {
      t || (ue(e.$$.fragment, n), t = !0);
    },
    o(n) {
      ye(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Wn(e, n);
    }
  };
}
function za(l) {
  let e, t, n, i, o, r = `${/*last_progress_level*/
  l[15] * 100}%`, f = (
    /*progress*/
    l[7] != null && Xl(l)
  );
  return {
    c() {
      e = ve("div"), t = ve("div"), f && f.c(), n = le(), i = ve("div"), o = ve("div"), _e(t, "class", "progress-level-inner svelte-vopvsi"), _e(o, "class", "progress-bar svelte-vopvsi"), Be(o, "width", r), _e(i, "class", "progress-bar-wrap svelte-vopvsi"), _e(e, "class", "progress-level svelte-vopvsi");
    },
    m(a, s) {
      z(a, e, s), Ve(e, t), f && f.m(t, null), Ve(e, n), Ve(e, i), Ve(i, o), l[31](o);
    },
    p(a, s) {
      /*progress*/
      a[7] != null ? f ? f.p(a, s) : (f = Xl(a), f.c(), f.m(t, null)) : f && (f.d(1), f = null), s[0] & /*last_progress_level*/
      32768 && r !== (r = `${/*last_progress_level*/
      a[15] * 100}%`) && Be(o, "width", r);
    },
    i: ol,
    o: ol,
    d(a) {
      a && j(e), f && f.d(), l[31](null);
    }
  };
}
function Xl(l) {
  let e, t = gt(
    /*progress*/
    l[7]
  ), n = [];
  for (let i = 0; i < t.length; i += 1)
    n[i] = Ql(Tl(l, t, i));
  return {
    c() {
      for (let i = 0; i < n.length; i += 1)
        n[i].c();
      e = xe();
    },
    m(i, o) {
      for (let r = 0; r < n.length; r += 1)
        n[r] && n[r].m(i, o);
      z(i, e, o);
    },
    p(i, o) {
      if (o[0] & /*progress_level, progress*/
      16512) {
        t = gt(
          /*progress*/
          i[7]
        );
        let r;
        for (r = 0; r < t.length; r += 1) {
          const f = Tl(i, t, r);
          n[r] ? n[r].p(f, o) : (n[r] = Ql(f), n[r].c(), n[r].m(e.parentNode, e));
        }
        for (; r < n.length; r += 1)
          n[r].d(1);
        n.length = t.length;
      }
    },
    d(i) {
      i && j(e), Zn(n, i);
    }
  };
}
function Gl(l) {
  let e, t, n, i, o = (
    /*i*/
    l[42] !== 0 && Ea()
  ), r = (
    /*p*/
    l[40].desc != null && Yl(l)
  ), f = (
    /*p*/
    l[40].desc != null && /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[42]
    ] != null && Kl()
  ), a = (
    /*progress_level*/
    l[14] != null && Jl(l)
  );
  return {
    c() {
      o && o.c(), e = le(), r && r.c(), t = le(), f && f.c(), n = le(), a && a.c(), i = xe();
    },
    m(s, u) {
      o && o.m(s, u), z(s, e, u), r && r.m(s, u), z(s, t, u), f && f.m(s, u), z(s, n, u), a && a.m(s, u), z(s, i, u);
    },
    p(s, u) {
      /*p*/
      s[40].desc != null ? r ? r.p(s, u) : (r = Yl(s), r.c(), r.m(t.parentNode, t)) : r && (r.d(1), r = null), /*p*/
      s[40].desc != null && /*progress_level*/
      s[14] && /*progress_level*/
      s[14][
        /*i*/
        s[42]
      ] != null ? f || (f = Kl(), f.c(), f.m(n.parentNode, n)) : f && (f.d(1), f = null), /*progress_level*/
      s[14] != null ? a ? a.p(s, u) : (a = Jl(s), a.c(), a.m(i.parentNode, i)) : a && (a.d(1), a = null);
    },
    d(s) {
      s && (j(e), j(t), j(n), j(i)), o && o.d(s), r && r.d(s), f && f.d(s), a && a.d(s);
    }
  };
}
function Ea(l) {
  let e;
  return {
    c() {
      e = R(" /");
    },
    m(t, n) {
      z(t, e, n);
    },
    d(t) {
      t && j(e);
    }
  };
}
function Yl(l) {
  let e = (
    /*p*/
    l[40].desc + ""
  ), t;
  return {
    c() {
      t = R(e);
    },
    m(n, i) {
      z(n, t, i);
    },
    p(n, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      n[40].desc + "") && ne(t, e);
    },
    d(n) {
      n && j(t);
    }
  };
}
function Kl(l) {
  let e;
  return {
    c() {
      e = R("-");
    },
    m(t, n) {
      z(t, e, n);
    },
    d(t) {
      t && j(e);
    }
  };
}
function Jl(l) {
  let e = (100 * /*progress_level*/
  (l[14][
    /*i*/
    l[42]
  ] || 0)).toFixed(1) + "", t, n;
  return {
    c() {
      t = R(e), n = R("%");
    },
    m(i, o) {
      z(i, t, o), z(i, n, o);
    },
    p(i, o) {
      o[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[42]
      ] || 0)).toFixed(1) + "") && ne(t, e);
    },
    d(i) {
      i && (j(t), j(n));
    }
  };
}
function Ql(l) {
  let e, t = (
    /*p*/
    (l[40].desc != null || /*progress_level*/
    l[14] && /*progress_level*/
    l[14][
      /*i*/
      l[42]
    ] != null) && Gl(l)
  );
  return {
    c() {
      t && t.c(), e = xe();
    },
    m(n, i) {
      t && t.m(n, i), z(n, e, i);
    },
    p(n, i) {
      /*p*/
      n[40].desc != null || /*progress_level*/
      n[14] && /*progress_level*/
      n[14][
        /*i*/
        n[42]
      ] != null ? t ? t.p(n, i) : (t = Gl(n), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(n) {
      n && j(e), t && t.d(n);
    }
  };
}
function xl(l) {
  let e, t, n, i;
  const o = (
    /*#slots*/
    l[30]["additional-loading-text"]
  ), r = Un(
    o,
    l,
    /*$$scope*/
    l[29],
    Pl
  );
  return {
    c() {
      e = ve("p"), t = R(
        /*loading_text*/
        l[9]
      ), n = le(), r && r.c(), _e(e, "class", "loading svelte-vopvsi");
    },
    m(f, a) {
      z(f, e, a), Ve(e, t), z(f, n, a), r && r.m(f, a), i = !0;
    },
    p(f, a) {
      (!i || a[0] & /*loading_text*/
      512) && ne(
        t,
        /*loading_text*/
        f[9]
      ), r && r.p && (!i || a[0] & /*$$scope*/
      536870912) && Yn(
        r,
        o,
        f,
        /*$$scope*/
        f[29],
        i ? Xn(
          o,
          /*$$scope*/
          f[29],
          a,
          ka
        ) : Hn(
          /*$$scope*/
          f[29]
        ),
        Pl
      );
    },
    i(f) {
      i || (ue(r, f), i = !0);
    },
    o(f) {
      ye(r, f), i = !1;
    },
    d(f) {
      f && (j(e), j(n)), r && r.d(f);
    }
  };
}
function Ia(l) {
  let e, t, n, i, o;
  const r = [va, pa], f = [];
  function a(s, u) {
    return (
      /*status*/
      s[4] === "pending" ? 0 : (
        /*status*/
        s[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = a(l)) && (n = f[t] = r[t](l)), {
    c() {
      e = ve("div"), n && n.c(), _e(e, "class", i = "wrap " + /*variant*/
      l[8] + " " + /*show_progress*/
      l[6] + " svelte-vopvsi"), ee(e, "hide", !/*status*/
      l[4] || /*status*/
      l[4] === "complete" || /*show_progress*/
      l[6] === "hidden"), ee(
        e,
        "translucent",
        /*variant*/
        l[8] === "center" && /*status*/
        (l[4] === "pending" || /*status*/
        l[4] === "error") || /*translucent*/
        l[11] || /*show_progress*/
        l[6] === "minimal"
      ), ee(
        e,
        "generating",
        /*status*/
        l[4] === "generating"
      ), ee(
        e,
        "border",
        /*border*/
        l[12]
      ), Be(
        e,
        "position",
        /*absolute*/
        l[10] ? "absolute" : "static"
      ), Be(
        e,
        "padding",
        /*absolute*/
        l[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(s, u) {
      z(s, e, u), ~t && f[t].m(e, null), l[33](e), o = !0;
    },
    p(s, u) {
      let _ = t;
      t = a(s), t === _ ? ~t && f[t].p(s, u) : (n && (il(), ye(f[_], 1, 1, () => {
        f[_] = null;
      }), nl()), ~t ? (n = f[t], n ? n.p(s, u) : (n = f[t] = r[t](s), n.c()), ue(n, 1), n.m(e, null)) : n = null), (!o || u[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      s[8] + " " + /*show_progress*/
      s[6] + " svelte-vopvsi")) && _e(e, "class", i), (!o || u[0] & /*variant, show_progress, status, show_progress*/
      336) && ee(e, "hide", !/*status*/
      s[4] || /*status*/
      s[4] === "complete" || /*show_progress*/
      s[6] === "hidden"), (!o || u[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && ee(
        e,
        "translucent",
        /*variant*/
        s[8] === "center" && /*status*/
        (s[4] === "pending" || /*status*/
        s[4] === "error") || /*translucent*/
        s[11] || /*show_progress*/
        s[6] === "minimal"
      ), (!o || u[0] & /*variant, show_progress, status*/
      336) && ee(
        e,
        "generating",
        /*status*/
        s[4] === "generating"
      ), (!o || u[0] & /*variant, show_progress, border*/
      4416) && ee(
        e,
        "border",
        /*border*/
        s[12]
      ), u[0] & /*absolute*/
      1024 && Be(
        e,
        "position",
        /*absolute*/
        s[10] ? "absolute" : "static"
      ), u[0] & /*absolute*/
      1024 && Be(
        e,
        "padding",
        /*absolute*/
        s[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(s) {
      o || (ue(n), o = !0);
    },
    o(s) {
      ye(n), o = !1;
    },
    d(s) {
      s && j(e), ~t && f[t].d(), l[33](null);
    }
  };
}
let dt = [], Ht = !1;
async function Ma(l, e = !0) {
  if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && e !== !0)) {
    if (dt.push(l), !Ht)
      Ht = !0;
    else
      return;
    await ha(), requestAnimationFrame(() => {
      let t = [0, 0];
      for (let n = 0; n < dt.length; n++) {
        const o = dt[n].getBoundingClientRect();
        (n === 0 || o.top + window.scrollY <= t[0]) && (t[0] = o.top + window.scrollY, t[1] = n);
      }
      window.scrollTo({ top: t[0] - 20, behavior: "smooth" }), Ht = !1, dt = [];
    });
  }
}
function Aa(l, e, t) {
  let n, { $$slots: i = {}, $$scope: o } = e;
  const r = ga();
  let { i18n: f } = e, { eta: a = null } = e, { queue_position: s } = e, { queue_size: u } = e, { status: _ } = e, { scroll_to_output: c = !1 } = e, { timer: d = !0 } = e, { show_progress: h = "full" } = e, { message: y = null } = e, { progress: S = null } = e, { variant: v = "default" } = e, { loading_text: k = "Loading..." } = e, { absolute: p = !0 } = e, { translucent: b = !1 } = e, { border: q = !1 } = e, { autoscroll: g } = e, L, C = !1, T = 0, A = 0, O = null, B = null, me = 0, Z = null, he, H = null, ie = !0;
  const qe = () => {
    t(0, a = t(27, O = t(19, be = null))), t(25, T = performance.now()), t(26, A = 0), C = !0, Q();
  };
  function Q() {
    requestAnimationFrame(() => {
      t(26, A = (performance.now() - T) / 1e3), C && Q();
    });
  }
  function N() {
    t(26, A = 0), t(0, a = t(27, O = t(19, be = null))), C && (C = !1);
  }
  ba(() => {
    C && N();
  });
  let be = null;
  function Ne(m) {
    Nl[m ? "unshift" : "push"](() => {
      H = m, t(16, H), t(7, S), t(14, Z), t(15, he);
    });
  }
  const Ze = () => {
    r("clear_status");
  };
  function $e(m) {
    Nl[m ? "unshift" : "push"](() => {
      L = m, t(13, L);
    });
  }
  return l.$$set = (m) => {
    "i18n" in m && t(1, f = m.i18n), "eta" in m && t(0, a = m.eta), "queue_position" in m && t(2, s = m.queue_position), "queue_size" in m && t(3, u = m.queue_size), "status" in m && t(4, _ = m.status), "scroll_to_output" in m && t(22, c = m.scroll_to_output), "timer" in m && t(5, d = m.timer), "show_progress" in m && t(6, h = m.show_progress), "message" in m && t(23, y = m.message), "progress" in m && t(7, S = m.progress), "variant" in m && t(8, v = m.variant), "loading_text" in m && t(9, k = m.loading_text), "absolute" in m && t(10, p = m.absolute), "translucent" in m && t(11, b = m.translucent), "border" in m && t(12, q = m.border), "autoscroll" in m && t(24, g = m.autoscroll), "$$scope" in m && t(29, o = m.$$scope);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (a === null && t(0, a = O), a != null && O !== a && (t(28, B = (performance.now() - T) / 1e3 + a), t(19, be = B.toFixed(1)), t(27, O = a))), l.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, me = B === null || B <= 0 || !A ? null : Math.min(A / B, 1)), l.$$.dirty[0] & /*progress*/
    128 && S != null && t(18, ie = !1), l.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (S != null ? t(14, Z = S.map((m) => {
      if (m.index != null && m.length != null)
        return m.index / m.length;
      if (m.progress != null)
        return m.progress;
    })) : t(14, Z = null), Z ? (t(15, he = Z[Z.length - 1]), H && (he === 0 ? t(16, H.style.transition = "0", H) : t(16, H.style.transition = "150ms", H))) : t(15, he = void 0)), l.$$.dirty[0] & /*status*/
    16 && (_ === "pending" ? qe() : N()), l.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && L && c && (_ === "pending" || _ === "complete") && Ma(L, g), l.$$.dirty[0] & /*status, message*/
    8388624, l.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, n = A.toFixed(1));
  }, [
    a,
    f,
    s,
    u,
    _,
    d,
    h,
    S,
    v,
    k,
    p,
    b,
    q,
    L,
    Z,
    he,
    H,
    me,
    ie,
    be,
    n,
    r,
    c,
    y,
    g,
    T,
    A,
    O,
    B,
    o,
    i,
    Ne,
    Ze,
    $e
  ];
}
class Da extends ca {
  constructor(e) {
    super(), da(
      this,
      e,
      Aa,
      Ia,
      ma,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: Fa,
  append: Kn,
  attr: D,
  bubble: Ra,
  check_outros: Ba,
  create_slot: Jn,
  detach: it,
  element: jt,
  empty: Na,
  get_all_dirty_from_scope: Qn,
  get_slot_changes: xn,
  group_outros: Va,
  init: Pa,
  insert: ot,
  listen: Ta,
  safe_not_equal: Oa,
  set_style: J,
  space: $n,
  src_url_equal: wt,
  toggle_class: Ke,
  transition_in: kt,
  transition_out: pt,
  update_slot_base: ei
} = window.__gradio__svelte__internal;
function Ua(l) {
  let e, t, n, i, o, r, f = (
    /*icon*/
    l[7] && $l(l)
  );
  const a = (
    /*#slots*/
    l[12].default
  ), s = Jn(
    a,
    l,
    /*$$scope*/
    l[11],
    null
  );
  return {
    c() {
      e = jt("button"), f && f.c(), t = $n(), s && s.c(), D(e, "class", n = /*size*/
      l[4] + " " + /*variant*/
      l[3] + " " + /*elem_classes*/
      l[1].join(" ") + " svelte-8huxfn"), D(
        e,
        "id",
        /*elem_id*/
        l[0]
      ), e.disabled = /*disabled*/
      l[8], Ke(e, "hidden", !/*visible*/
      l[2]), J(
        e,
        "flex-grow",
        /*scale*/
        l[9]
      ), J(
        e,
        "width",
        /*scale*/
        l[9] === 0 ? "fit-content" : null
      ), J(e, "min-width", typeof /*min_width*/
      l[10] == "number" ? `calc(min(${/*min_width*/
      l[10]}px, 100%))` : null);
    },
    m(u, _) {
      ot(u, e, _), f && f.m(e, null), Kn(e, t), s && s.m(e, null), i = !0, o || (r = Ta(
        e,
        "click",
        /*click_handler*/
        l[13]
      ), o = !0);
    },
    p(u, _) {
      /*icon*/
      u[7] ? f ? f.p(u, _) : (f = $l(u), f.c(), f.m(e, t)) : f && (f.d(1), f = null), s && s.p && (!i || _ & /*$$scope*/
      2048) && ei(
        s,
        a,
        u,
        /*$$scope*/
        u[11],
        i ? xn(
          a,
          /*$$scope*/
          u[11],
          _,
          null
        ) : Qn(
          /*$$scope*/
          u[11]
        ),
        null
      ), (!i || _ & /*size, variant, elem_classes*/
      26 && n !== (n = /*size*/
      u[4] + " " + /*variant*/
      u[3] + " " + /*elem_classes*/
      u[1].join(" ") + " svelte-8huxfn")) && D(e, "class", n), (!i || _ & /*elem_id*/
      1) && D(
        e,
        "id",
        /*elem_id*/
        u[0]
      ), (!i || _ & /*disabled*/
      256) && (e.disabled = /*disabled*/
      u[8]), (!i || _ & /*size, variant, elem_classes, visible*/
      30) && Ke(e, "hidden", !/*visible*/
      u[2]), _ & /*scale*/
      512 && J(
        e,
        "flex-grow",
        /*scale*/
        u[9]
      ), _ & /*scale*/
      512 && J(
        e,
        "width",
        /*scale*/
        u[9] === 0 ? "fit-content" : null
      ), _ & /*min_width*/
      1024 && J(e, "min-width", typeof /*min_width*/
      u[10] == "number" ? `calc(min(${/*min_width*/
      u[10]}px, 100%))` : null);
    },
    i(u) {
      i || (kt(s, u), i = !0);
    },
    o(u) {
      pt(s, u), i = !1;
    },
    d(u) {
      u && it(e), f && f.d(), s && s.d(u), o = !1, r();
    }
  };
}
function Wa(l) {
  let e, t, n, i, o = (
    /*icon*/
    l[7] && en(l)
  );
  const r = (
    /*#slots*/
    l[12].default
  ), f = Jn(
    r,
    l,
    /*$$scope*/
    l[11],
    null
  );
  return {
    c() {
      e = jt("a"), o && o.c(), t = $n(), f && f.c(), D(
        e,
        "href",
        /*link*/
        l[6]
      ), D(e, "rel", "noopener noreferrer"), D(
        e,
        "aria-disabled",
        /*disabled*/
        l[8]
      ), D(e, "class", n = /*size*/
      l[4] + " " + /*variant*/
      l[3] + " " + /*elem_classes*/
      l[1].join(" ") + " svelte-8huxfn"), D(
        e,
        "id",
        /*elem_id*/
        l[0]
      ), Ke(e, "hidden", !/*visible*/
      l[2]), Ke(
        e,
        "disabled",
        /*disabled*/
        l[8]
      ), J(
        e,
        "flex-grow",
        /*scale*/
        l[9]
      ), J(
        e,
        "pointer-events",
        /*disabled*/
        l[8] ? "none" : null
      ), J(
        e,
        "width",
        /*scale*/
        l[9] === 0 ? "fit-content" : null
      ), J(e, "min-width", typeof /*min_width*/
      l[10] == "number" ? `calc(min(${/*min_width*/
      l[10]}px, 100%))` : null);
    },
    m(a, s) {
      ot(a, e, s), o && o.m(e, null), Kn(e, t), f && f.m(e, null), i = !0;
    },
    p(a, s) {
      /*icon*/
      a[7] ? o ? o.p(a, s) : (o = en(a), o.c(), o.m(e, t)) : o && (o.d(1), o = null), f && f.p && (!i || s & /*$$scope*/
      2048) && ei(
        f,
        r,
        a,
        /*$$scope*/
        a[11],
        i ? xn(
          r,
          /*$$scope*/
          a[11],
          s,
          null
        ) : Qn(
          /*$$scope*/
          a[11]
        ),
        null
      ), (!i || s & /*link*/
      64) && D(
        e,
        "href",
        /*link*/
        a[6]
      ), (!i || s & /*disabled*/
      256) && D(
        e,
        "aria-disabled",
        /*disabled*/
        a[8]
      ), (!i || s & /*size, variant, elem_classes*/
      26 && n !== (n = /*size*/
      a[4] + " " + /*variant*/
      a[3] + " " + /*elem_classes*/
      a[1].join(" ") + " svelte-8huxfn")) && D(e, "class", n), (!i || s & /*elem_id*/
      1) && D(
        e,
        "id",
        /*elem_id*/
        a[0]
      ), (!i || s & /*size, variant, elem_classes, visible*/
      30) && Ke(e, "hidden", !/*visible*/
      a[2]), (!i || s & /*size, variant, elem_classes, disabled*/
      282) && Ke(
        e,
        "disabled",
        /*disabled*/
        a[8]
      ), s & /*scale*/
      512 && J(
        e,
        "flex-grow",
        /*scale*/
        a[9]
      ), s & /*disabled*/
      256 && J(
        e,
        "pointer-events",
        /*disabled*/
        a[8] ? "none" : null
      ), s & /*scale*/
      512 && J(
        e,
        "width",
        /*scale*/
        a[9] === 0 ? "fit-content" : null
      ), s & /*min_width*/
      1024 && J(e, "min-width", typeof /*min_width*/
      a[10] == "number" ? `calc(min(${/*min_width*/
      a[10]}px, 100%))` : null);
    },
    i(a) {
      i || (kt(f, a), i = !0);
    },
    o(a) {
      pt(f, a), i = !1;
    },
    d(a) {
      a && it(e), o && o.d(), f && f.d(a);
    }
  };
}
function $l(l) {
  let e, t, n;
  return {
    c() {
      e = jt("img"), D(e, "class", "button-icon svelte-8huxfn"), wt(e.src, t = /*icon*/
      l[7].url) || D(e, "src", t), D(e, "alt", n = `${/*value*/
      l[5]} icon`);
    },
    m(i, o) {
      ot(i, e, o);
    },
    p(i, o) {
      o & /*icon*/
      128 && !wt(e.src, t = /*icon*/
      i[7].url) && D(e, "src", t), o & /*value*/
      32 && n !== (n = `${/*value*/
      i[5]} icon`) && D(e, "alt", n);
    },
    d(i) {
      i && it(e);
    }
  };
}
function en(l) {
  let e, t, n;
  return {
    c() {
      e = jt("img"), D(e, "class", "button-icon svelte-8huxfn"), wt(e.src, t = /*icon*/
      l[7].url) || D(e, "src", t), D(e, "alt", n = `${/*value*/
      l[5]} icon`);
    },
    m(i, o) {
      ot(i, e, o);
    },
    p(i, o) {
      o & /*icon*/
      128 && !wt(e.src, t = /*icon*/
      i[7].url) && D(e, "src", t), o & /*value*/
      32 && n !== (n = `${/*value*/
      i[5]} icon`) && D(e, "alt", n);
    },
    d(i) {
      i && it(e);
    }
  };
}
function Za(l) {
  let e, t, n, i;
  const o = [Wa, Ua], r = [];
  function f(a, s) {
    return (
      /*link*/
      a[6] && /*link*/
      a[6].length > 0 ? 0 : 1
    );
  }
  return e = f(l), t = r[e] = o[e](l), {
    c() {
      t.c(), n = Na();
    },
    m(a, s) {
      r[e].m(a, s), ot(a, n, s), i = !0;
    },
    p(a, [s]) {
      let u = e;
      e = f(a), e === u ? r[e].p(a, s) : (Va(), pt(r[u], 1, 1, () => {
        r[u] = null;
      }), Ba(), t = r[e], t ? t.p(a, s) : (t = r[e] = o[e](a), t.c()), kt(t, 1), t.m(n.parentNode, n));
    },
    i(a) {
      i || (kt(t), i = !0);
    },
    o(a) {
      pt(t), i = !1;
    },
    d(a) {
      a && it(n), r[e].d(a);
    }
  };
}
function Ha(l, e, t) {
  let { $$slots: n = {}, $$scope: i } = e, { elem_id: o = "" } = e, { elem_classes: r = [] } = e, { visible: f = !0 } = e, { variant: a = "secondary" } = e, { size: s = "lg" } = e, { value: u = null } = e, { link: _ = null } = e, { icon: c = null } = e, { disabled: d = !1 } = e, { scale: h = null } = e, { min_width: y = void 0 } = e;
  function S(v) {
    Ra.call(this, l, v);
  }
  return l.$$set = (v) => {
    "elem_id" in v && t(0, o = v.elem_id), "elem_classes" in v && t(1, r = v.elem_classes), "visible" in v && t(2, f = v.visible), "variant" in v && t(3, a = v.variant), "size" in v && t(4, s = v.size), "value" in v && t(5, u = v.value), "link" in v && t(6, _ = v.link), "icon" in v && t(7, c = v.icon), "disabled" in v && t(8, d = v.disabled), "scale" in v && t(9, h = v.scale), "min_width" in v && t(10, y = v.min_width), "$$scope" in v && t(11, i = v.$$scope);
  }, [
    o,
    r,
    f,
    a,
    s,
    u,
    _,
    c,
    d,
    h,
    y,
    i,
    n,
    S
  ];
}
class Xa extends Fa {
  constructor(e) {
    super(), Pa(this, e, Ha, Za, Oa, {
      elem_id: 0,
      elem_classes: 1,
      visible: 2,
      variant: 3,
      size: 4,
      value: 5,
      link: 6,
      icon: 7,
      disabled: 8,
      scale: 9,
      min_width: 10
    });
  }
}
var Ga = Object.defineProperty, Ya = (l, e, t) => e in l ? Ga(l, e, { enumerable: !0, configurable: !0, writable: !0, value: t }) : l[e] = t, Se = (l, e, t) => (Ya(l, typeof e != "symbol" ? e + "" : e, t), t);
new Intl.Collator(0, { numeric: 1 }).compare;
class Xt {
  constructor({
    path: e,
    url: t,
    orig_name: n,
    size: i,
    blob: o,
    is_stream: r,
    mime_type: f,
    alt_text: a
  }) {
    Se(this, "path"), Se(this, "url"), Se(this, "orig_name"), Se(this, "size"), Se(this, "blob"), Se(this, "is_stream"), Se(this, "mime_type"), Se(this, "alt_text"), Se(this, "meta", { _type: "gradio.FileData" }), this.path = e, this.url = t, this.orig_name = n, this.size = i, this.blob = t ? void 0 : o, this.is_stream = r, this.mime_type = f, this.alt_text = a;
  }
}
const { setContext: Xf, getContext: Ka } = window.__gradio__svelte__internal, Ja = "WORKER_PROXY_CONTEXT_KEY";
function Qa() {
  return Ka(Ja);
}
function xa(l) {
  return l.host === window.location.host || l.host === "localhost:7860" || l.host === "127.0.0.1:7860" || // Ref: https://github.com/gradio-app/gradio/blob/v3.32.0/js/app/src/Index.svelte#L194
  l.host === "lite.local";
}
function $a(l, e) {
  const t = e.toLowerCase();
  for (const [n, i] of Object.entries(l))
    if (n.toLowerCase() === t)
      return i;
}
function er(l) {
  if (l == null)
    return !1;
  const e = new URL(l, window.location.href);
  return !(!xa(e) || e.protocol !== "http:" && e.protocol !== "https:");
}
const {
  SvelteComponent: tr,
  assign: vt,
  check_outros: ti,
  compute_rest_props: tn,
  create_slot: fl,
  detach: zt,
  element: li,
  empty: ni,
  exclude_internal_props: lr,
  get_all_dirty_from_scope: ul,
  get_slot_changes: _l,
  get_spread_update: ii,
  group_outros: oi,
  init: nr,
  insert: Et,
  listen: si,
  prevent_default: ir,
  safe_not_equal: or,
  set_attributes: yt,
  transition_in: Ue,
  transition_out: We,
  update_slot_base: cl
} = window.__gradio__svelte__internal, { createEventDispatcher: sr } = window.__gradio__svelte__internal;
function ar(l) {
  let e, t, n, i, o;
  const r = (
    /*#slots*/
    l[8].default
  ), f = fl(
    r,
    l,
    /*$$scope*/
    l[7],
    null
  );
  let a = [
    { href: (
      /*href*/
      l[0]
    ) },
    {
      target: t = typeof window < "u" && window.__is_colab__ ? "_blank" : null
    },
    { rel: "noopener noreferrer" },
    { download: (
      /*download*/
      l[1]
    ) },
    /*$$restProps*/
    l[6]
  ], s = {};
  for (let u = 0; u < a.length; u += 1)
    s = vt(s, a[u]);
  return {
    c() {
      e = li("a"), f && f.c(), yt(e, s);
    },
    m(u, _) {
      Et(u, e, _), f && f.m(e, null), n = !0, i || (o = si(
        e,
        "click",
        /*dispatch*/
        l[3].bind(null, "click")
      ), i = !0);
    },
    p(u, _) {
      f && f.p && (!n || _ & /*$$scope*/
      128) && cl(
        f,
        r,
        u,
        /*$$scope*/
        u[7],
        n ? _l(
          r,
          /*$$scope*/
          u[7],
          _,
          null
        ) : ul(
          /*$$scope*/
          u[7]
        ),
        null
      ), yt(e, s = ii(a, [
        (!n || _ & /*href*/
        1) && { href: (
          /*href*/
          u[0]
        ) },
        { target: t },
        { rel: "noopener noreferrer" },
        (!n || _ & /*download*/
        2) && { download: (
          /*download*/
          u[1]
        ) },
        _ & /*$$restProps*/
        64 && /*$$restProps*/
        u[6]
      ]));
    },
    i(u) {
      n || (Ue(f, u), n = !0);
    },
    o(u) {
      We(f, u), n = !1;
    },
    d(u) {
      u && zt(e), f && f.d(u), i = !1, o();
    }
  };
}
function rr(l) {
  let e, t, n, i;
  const o = [ur, fr], r = [];
  function f(a, s) {
    return (
      /*is_downloading*/
      a[2] ? 0 : 1
    );
  }
  return e = f(l), t = r[e] = o[e](l), {
    c() {
      t.c(), n = ni();
    },
    m(a, s) {
      r[e].m(a, s), Et(a, n, s), i = !0;
    },
    p(a, s) {
      let u = e;
      e = f(a), e === u ? r[e].p(a, s) : (oi(), We(r[u], 1, 1, () => {
        r[u] = null;
      }), ti(), t = r[e], t ? t.p(a, s) : (t = r[e] = o[e](a), t.c()), Ue(t, 1), t.m(n.parentNode, n));
    },
    i(a) {
      i || (Ue(t), i = !0);
    },
    o(a) {
      We(t), i = !1;
    },
    d(a) {
      a && zt(n), r[e].d(a);
    }
  };
}
function fr(l) {
  let e, t, n, i;
  const o = (
    /*#slots*/
    l[8].default
  ), r = fl(
    o,
    l,
    /*$$scope*/
    l[7],
    null
  );
  let f = [
    /*$$restProps*/
    l[6],
    { href: (
      /*href*/
      l[0]
    ) }
  ], a = {};
  for (let s = 0; s < f.length; s += 1)
    a = vt(a, f[s]);
  return {
    c() {
      e = li("a"), r && r.c(), yt(e, a);
    },
    m(s, u) {
      Et(s, e, u), r && r.m(e, null), t = !0, n || (i = si(e, "click", ir(
        /*wasm_click_handler*/
        l[5]
      )), n = !0);
    },
    p(s, u) {
      r && r.p && (!t || u & /*$$scope*/
      128) && cl(
        r,
        o,
        s,
        /*$$scope*/
        s[7],
        t ? _l(
          o,
          /*$$scope*/
          s[7],
          u,
          null
        ) : ul(
          /*$$scope*/
          s[7]
        ),
        null
      ), yt(e, a = ii(f, [
        u & /*$$restProps*/
        64 && /*$$restProps*/
        s[6],
        (!t || u & /*href*/
        1) && { href: (
          /*href*/
          s[0]
        ) }
      ]));
    },
    i(s) {
      t || (Ue(r, s), t = !0);
    },
    o(s) {
      We(r, s), t = !1;
    },
    d(s) {
      s && zt(e), r && r.d(s), n = !1, i();
    }
  };
}
function ur(l) {
  let e;
  const t = (
    /*#slots*/
    l[8].default
  ), n = fl(
    t,
    l,
    /*$$scope*/
    l[7],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(i, o) {
      n && n.m(i, o), e = !0;
    },
    p(i, o) {
      n && n.p && (!e || o & /*$$scope*/
      128) && cl(
        n,
        t,
        i,
        /*$$scope*/
        i[7],
        e ? _l(
          t,
          /*$$scope*/
          i[7],
          o,
          null
        ) : ul(
          /*$$scope*/
          i[7]
        ),
        null
      );
    },
    i(i) {
      e || (Ue(n, i), e = !0);
    },
    o(i) {
      We(n, i), e = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function _r(l) {
  let e, t, n, i, o;
  const r = [rr, ar], f = [];
  function a(s, u) {
    return u & /*href*/
    1 && (e = null), e == null && (e = !!/*worker_proxy*/
    (s[4] && er(
      /*href*/
      s[0]
    ))), e ? 0 : 1;
  }
  return t = a(l, -1), n = f[t] = r[t](l), {
    c() {
      n.c(), i = ni();
    },
    m(s, u) {
      f[t].m(s, u), Et(s, i, u), o = !0;
    },
    p(s, [u]) {
      let _ = t;
      t = a(s, u), t === _ ? f[t].p(s, u) : (oi(), We(f[_], 1, 1, () => {
        f[_] = null;
      }), ti(), n = f[t], n ? n.p(s, u) : (n = f[t] = r[t](s), n.c()), Ue(n, 1), n.m(i.parentNode, i));
    },
    i(s) {
      o || (Ue(n), o = !0);
    },
    o(s) {
      We(n), o = !1;
    },
    d(s) {
      s && zt(i), f[t].d(s);
    }
  };
}
function cr(l, e, t) {
  const n = ["href", "download"];
  let i = tn(e, n), { $$slots: o = {}, $$scope: r } = e;
  var f = this && this.__awaiter || function(h, y, S, v) {
    function k(p) {
      return p instanceof S ? p : new S(function(b) {
        b(p);
      });
    }
    return new (S || (S = Promise))(function(p, b) {
      function q(C) {
        try {
          L(v.next(C));
        } catch (T) {
          b(T);
        }
      }
      function g(C) {
        try {
          L(v.throw(C));
        } catch (T) {
          b(T);
        }
      }
      function L(C) {
        C.done ? p(C.value) : k(C.value).then(q, g);
      }
      L((v = v.apply(h, y || [])).next());
    });
  };
  let { href: a = void 0 } = e, { download: s } = e;
  const u = sr();
  let _ = !1;
  const c = Qa();
  function d() {
    return f(this, void 0, void 0, function* () {
      if (_)
        return;
      if (u("click"), a == null)
        throw new Error("href is not defined.");
      if (c == null)
        throw new Error("Wasm worker proxy is not available.");
      const y = new URL(a, window.location.href).pathname;
      t(2, _ = !0), c.httpRequest({
        method: "GET",
        path: y,
        headers: {},
        query_string: ""
      }).then((S) => {
        if (S.status !== 200)
          throw new Error(`Failed to get file ${y} from the Wasm worker.`);
        const v = new Blob(
          [S.body],
          {
            type: $a(S.headers, "content-type")
          }
        ), k = URL.createObjectURL(v), p = document.createElement("a");
        p.href = k, p.download = s, p.click(), URL.revokeObjectURL(k);
      }).finally(() => {
        t(2, _ = !1);
      });
    });
  }
  return l.$$set = (h) => {
    e = vt(vt({}, e), lr(h)), t(6, i = tn(e, n)), "href" in h && t(0, a = h.href), "download" in h && t(1, s = h.download), "$$scope" in h && t(7, r = h.$$scope);
  }, [
    a,
    s,
    _,
    u,
    c,
    d,
    i,
    r,
    o
  ];
}
class dr extends tr {
  constructor(e) {
    super(), nr(this, e, cr, _r, or, { href: 0, download: 1 });
  }
}
const {
  SvelteComponent: mr,
  append: Gt,
  attr: hr,
  check_outros: Yt,
  create_component: st,
  destroy_component: at,
  detach: br,
  element: gr,
  group_outros: Kt,
  init: wr,
  insert: kr,
  mount_component: rt,
  safe_not_equal: pr,
  set_style: ln,
  space: Jt,
  toggle_class: nn,
  transition_in: K,
  transition_out: fe
} = window.__gradio__svelte__internal, { createEventDispatcher: vr } = window.__gradio__svelte__internal;
function on(l) {
  let e, t;
  return e = new ze({
    props: {
      Icon: ws,
      label: (
        /*i18n*/
        l[4]("common.edit")
      )
    }
  }), e.$on(
    "click",
    /*click_handler*/
    l[6]
  ), {
    c() {
      st(e.$$.fragment);
    },
    m(n, i) {
      rt(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i & /*i18n*/
      16 && (o.label = /*i18n*/
      n[4]("common.edit")), e.$set(o);
    },
    i(n) {
      t || (K(e.$$.fragment, n), t = !0);
    },
    o(n) {
      fe(e.$$.fragment, n), t = !1;
    },
    d(n) {
      at(e, n);
    }
  };
}
function sn(l) {
  let e, t;
  return e = new ze({
    props: {
      Icon: Ps,
      label: (
        /*i18n*/
        l[4]("common.undo")
      )
    }
  }), e.$on(
    "click",
    /*click_handler_1*/
    l[7]
  ), {
    c() {
      st(e.$$.fragment);
    },
    m(n, i) {
      rt(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i & /*i18n*/
      16 && (o.label = /*i18n*/
      n[4]("common.undo")), e.$set(o);
    },
    i(n) {
      t || (K(e.$$.fragment, n), t = !0);
    },
    o(n) {
      fe(e.$$.fragment, n), t = !1;
    },
    d(n) {
      at(e, n);
    }
  };
}
function an(l) {
  let e, t;
  return e = new dr({
    props: {
      href: (
        /*download*/
        l[2]
      ),
      download: !0,
      $$slots: { default: [yr] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      st(e.$$.fragment);
    },
    m(n, i) {
      rt(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i & /*download*/
      4 && (o.href = /*download*/
      n[2]), i & /*$$scope, i18n*/
      528 && (o.$$scope = { dirty: i, ctx: n }), e.$set(o);
    },
    i(n) {
      t || (K(e.$$.fragment, n), t = !0);
    },
    o(n) {
      fe(e.$$.fragment, n), t = !1;
    },
    d(n) {
      at(e, n);
    }
  };
}
function yr(l) {
  let e, t;
  return e = new ze({
    props: {
      Icon: Rn,
      label: (
        /*i18n*/
        l[4]("common.download")
      )
    }
  }), {
    c() {
      st(e.$$.fragment);
    },
    m(n, i) {
      rt(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i & /*i18n*/
      16 && (o.label = /*i18n*/
      n[4]("common.download")), e.$set(o);
    },
    i(n) {
      t || (K(e.$$.fragment, n), t = !0);
    },
    o(n) {
      fe(e.$$.fragment, n), t = !1;
    },
    d(n) {
      at(e, n);
    }
  };
}
function Cr(l) {
  let e, t, n, i, o, r, f = (
    /*editable*/
    l[0] && on(l)
  ), a = (
    /*undoable*/
    l[1] && sn(l)
  ), s = (
    /*download*/
    l[2] && an(l)
  );
  return o = new ze({
    props: {
      Icon: Fn,
      label: (
        /*i18n*/
        l[4]("common.clear")
      )
    }
  }), o.$on(
    "click",
    /*click_handler_2*/
    l[8]
  ), {
    c() {
      e = gr("div"), f && f.c(), t = Jt(), a && a.c(), n = Jt(), s && s.c(), i = Jt(), st(o.$$.fragment), hr(e, "class", "svelte-1wj0ocy"), nn(e, "not-absolute", !/*absolute*/
      l[3]), ln(
        e,
        "position",
        /*absolute*/
        l[3] ? "absolute" : "static"
      );
    },
    m(u, _) {
      kr(u, e, _), f && f.m(e, null), Gt(e, t), a && a.m(e, null), Gt(e, n), s && s.m(e, null), Gt(e, i), rt(o, e, null), r = !0;
    },
    p(u, [_]) {
      /*editable*/
      u[0] ? f ? (f.p(u, _), _ & /*editable*/
      1 && K(f, 1)) : (f = on(u), f.c(), K(f, 1), f.m(e, t)) : f && (Kt(), fe(f, 1, 1, () => {
        f = null;
      }), Yt()), /*undoable*/
      u[1] ? a ? (a.p(u, _), _ & /*undoable*/
      2 && K(a, 1)) : (a = sn(u), a.c(), K(a, 1), a.m(e, n)) : a && (Kt(), fe(a, 1, 1, () => {
        a = null;
      }), Yt()), /*download*/
      u[2] ? s ? (s.p(u, _), _ & /*download*/
      4 && K(s, 1)) : (s = an(u), s.c(), K(s, 1), s.m(e, i)) : s && (Kt(), fe(s, 1, 1, () => {
        s = null;
      }), Yt());
      const c = {};
      _ & /*i18n*/
      16 && (c.label = /*i18n*/
      u[4]("common.clear")), o.$set(c), (!r || _ & /*absolute*/
      8) && nn(e, "not-absolute", !/*absolute*/
      u[3]), _ & /*absolute*/
      8 && ln(
        e,
        "position",
        /*absolute*/
        u[3] ? "absolute" : "static"
      );
    },
    i(u) {
      r || (K(f), K(a), K(s), K(o.$$.fragment, u), r = !0);
    },
    o(u) {
      fe(f), fe(a), fe(s), fe(o.$$.fragment, u), r = !1;
    },
    d(u) {
      u && br(e), f && f.d(), a && a.d(), s && s.d(), at(o);
    }
  };
}
function qr(l, e, t) {
  let { editable: n = !1 } = e, { undoable: i = !1 } = e, { download: o = null } = e, { absolute: r = !0 } = e, { i18n: f } = e;
  const a = vr(), s = () => a("edit"), u = () => a("undo"), _ = (c) => {
    a("clear"), c.stopPropagation();
  };
  return l.$$set = (c) => {
    "editable" in c && t(0, n = c.editable), "undoable" in c && t(1, i = c.undoable), "download" in c && t(2, o = c.download), "absolute" in c && t(3, r = c.absolute), "i18n" in c && t(4, f = c.i18n);
  }, [
    n,
    i,
    o,
    r,
    f,
    a,
    s,
    u,
    _
  ];
}
class Sr extends mr {
  constructor(e) {
    super(), wr(this, e, qr, Cr, pr, {
      editable: 0,
      undoable: 1,
      download: 2,
      absolute: 3,
      i18n: 4
    });
  }
}
function ai(l, e, t) {
  if (l == null)
    return null;
  if (Array.isArray(l)) {
    const n = [];
    for (const i of l)
      i == null ? n.push(null) : n.push(ai(i, e, t));
    return n;
  }
  return l.is_stream ? t == null ? new Xt({
    ...l,
    url: e + "/stream/" + l.path
  }) : new Xt({
    ...l,
    url: "/proxy=" + t + "stream/" + l.path
  }) : new Xt({
    ...l,
    url: jr(l.path, e, t)
  });
}
function Lr(l) {
  try {
    const e = new URL(l);
    return e.protocol === "http:" || e.protocol === "https:";
  } catch {
    return !1;
  }
}
function jr(l, e, t) {
  return l == null ? t ? `/proxy=${t}file=` : `${e}/file=` : Lr(l) ? l : t ? `/proxy=${t}file=${l}` : `${e}/file=${l}`;
}
var rn = Object.prototype.hasOwnProperty;
function fn(l, e, t) {
  for (t of l.keys())
    if (tt(t, e))
      return t;
}
function tt(l, e) {
  var t, n, i;
  if (l === e)
    return !0;
  if (l && e && (t = l.constructor) === e.constructor) {
    if (t === Date)
      return l.getTime() === e.getTime();
    if (t === RegExp)
      return l.toString() === e.toString();
    if (t === Array) {
      if ((n = l.length) === e.length)
        for (; n-- && tt(l[n], e[n]); )
          ;
      return n === -1;
    }
    if (t === Set) {
      if (l.size !== e.size)
        return !1;
      for (n of l)
        if (i = n, i && typeof i == "object" && (i = fn(e, i), !i) || !e.has(i))
          return !1;
      return !0;
    }
    if (t === Map) {
      if (l.size !== e.size)
        return !1;
      for (n of l)
        if (i = n[0], i && typeof i == "object" && (i = fn(e, i), !i) || !tt(n[1], e.get(i)))
          return !1;
      return !0;
    }
    if (t === ArrayBuffer)
      l = new Uint8Array(l), e = new Uint8Array(e);
    else if (t === DataView) {
      if ((n = l.byteLength) === e.byteLength)
        for (; n-- && l.getInt8(n) === e.getInt8(n); )
          ;
      return n === -1;
    }
    if (ArrayBuffer.isView(l)) {
      if ((n = l.byteLength) === e.byteLength)
        for (; n-- && l[n] === e[n]; )
          ;
      return n === -1;
    }
    if (!t || typeof l == "object") {
      n = 0;
      for (t in l)
        if (rn.call(l, t) && ++n && !rn.call(e, t) || !(t in e) || !tt(l[t], e[t]))
          return !1;
      return Object.keys(e).length === n;
    }
  }
  return l !== l && e !== e;
}
const {
  SvelteComponent: zr,
  append: un,
  attr: W,
  detach: Er,
  init: Ir,
  insert: Mr,
  noop: _n,
  safe_not_equal: Ar,
  svg_element: Qt
} = window.__gradio__svelte__internal;
function Dr(l) {
  let e, t, n, i;
  return {
    c() {
      e = Qt("svg"), t = Qt("path"), n = Qt("path"), W(t, "stroke", "currentColor"), W(t, "stroke-width", "1.5"), W(t, "stroke-linecap", "round"), W(t, "d", "M16.472 20H4.1a.6.6 0 0 1-.6-.6V9.6a.6.6 0 0 1 .6-.6h2.768a2 2 0 0 0 1.715-.971l2.71-4.517a1.631 1.631 0 0 1 2.961 1.308l-1.022 3.408a.6.6 0 0 0 .574.772h4.575a2 2 0 0 1 1.93 2.526l-1.91 7A2 2 0 0 1 16.473 20Z"), W(n, "stroke", "currentColor"), W(n, "stroke-width", "1.5"), W(n, "stroke-linecap", "round"), W(n, "stroke-linejoin", "round"), W(n, "d", "M7 20V9"), W(e, "xmlns", "http://www.w3.org/2000/svg"), W(e, "viewBox", "0 0 24 24"), W(e, "fill", i = /*selected*/
      l[0] ? "currentColor" : "none"), W(e, "stroke-width", "1.5"), W(e, "color", "currentColor"), W(e, "transform", "rotate(180)");
    },
    m(o, r) {
      Mr(o, e, r), un(e, t), un(e, n);
    },
    p(o, [r]) {
      r & /*selected*/
      1 && i !== (i = /*selected*/
      o[0] ? "currentColor" : "none") && W(e, "fill", i);
    },
    i: _n,
    o: _n,
    d(o) {
      o && Er(e);
    }
  };
}
function Fr(l, e, t) {
  let { selected: n } = e;
  return l.$$set = (i) => {
    "selected" in i && t(0, n = i.selected);
  }, [n];
}
class Rr extends zr {
  constructor(e) {
    super(), Ir(this, e, Fr, Dr, Ar, { selected: 0 });
  }
}
const {
  SvelteComponent: Br,
  append: je,
  attr: pe,
  check_outros: Nr,
  create_component: cn,
  destroy_component: dn,
  detach: It,
  element: Oe,
  flush: mt,
  group_outros: Vr,
  init: Pr,
  insert: Mt,
  listen: ri,
  mount_component: mn,
  safe_not_equal: Tr,
  set_data: fi,
  set_style: Or,
  space: bt,
  src_url_equal: hn,
  text: ui,
  transition_in: lt,
  transition_out: Ct
} = window.__gradio__svelte__internal, { createEventDispatcher: Ur } = window.__gradio__svelte__internal;
function bn(l) {
  let e, t = (
    /*value*/
    l[0].caption + ""
  ), n;
  return {
    c() {
      e = Oe("div"), n = ui(t), pe(e, "class", "foot-label left-label svelte-u350v8");
    },
    m(i, o) {
      Mt(i, e, o), je(e, n);
    },
    p(i, o) {
      o & /*value*/
      1 && t !== (t = /*value*/
      i[0].caption + "") && fi(n, t);
    },
    d(i) {
      i && It(e);
    }
  };
}
function gn(l) {
  let e, t, n, i;
  return {
    c() {
      e = Oe("button"), t = ui(
        /*action_label*/
        l[3]
      ), pe(e, "class", "foot-label right-label svelte-u350v8");
    },
    m(o, r) {
      Mt(o, e, r), je(e, t), n || (i = ri(
        e,
        "click",
        /*click_handler_1*/
        l[6]
      ), n = !0);
    },
    p(o, r) {
      r & /*action_label*/
      8 && fi(
        t,
        /*action_label*/
        o[3]
      );
    },
    d(o) {
      o && It(e), n = !1, i();
    }
  };
}
function wn(l) {
  let e, t, n, i, o, r, f;
  return n = new ze({
    props: {
      size: "large",
      highlight: (
        /*value*/
        l[0].liked
      ),
      Icon: As
    }
  }), n.$on(
    "click",
    /*click_handler_2*/
    l[7]
  ), r = new ze({
    props: {
      size: "large",
      highlight: (
        /*value*/
        l[0].liked === !1
      ),
      Icon: Rr
    }
  }), r.$on(
    "click",
    /*click_handler_3*/
    l[8]
  ), {
    c() {
      e = Oe("div"), t = Oe("span"), cn(n.$$.fragment), i = bt(), o = Oe("span"), cn(r.$$.fragment), Or(t, "margin-right", "1px"), pe(e, "class", "like-button svelte-u350v8");
    },
    m(a, s) {
      Mt(a, e, s), je(e, t), mn(n, t, null), je(e, i), je(e, o), mn(r, o, null), f = !0;
    },
    p(a, s) {
      const u = {};
      s & /*value*/
      1 && (u.highlight = /*value*/
      a[0].liked), n.$set(u);
      const _ = {};
      s & /*value*/
      1 && (_.highlight = /*value*/
      a[0].liked === !1), r.$set(_);
    },
    i(a) {
      f || (lt(n.$$.fragment, a), lt(r.$$.fragment, a), f = !0);
    },
    o(a) {
      Ct(n.$$.fragment, a), Ct(r.$$.fragment, a), f = !1;
    },
    d(a) {
      a && It(e), dn(n), dn(r);
    }
  };
}
function Wr(l) {
  let e, t, n, i, o, r, f, a, s, u, _ = (
    /*value*/
    l[0].caption && bn(l)
  ), c = (
    /*clickable*/
    l[2] && gn(l)
  ), d = (
    /*likeable*/
    l[1] && wn(l)
  );
  return {
    c() {
      e = Oe("div"), t = Oe("img"), o = bt(), _ && _.c(), r = bt(), c && c.c(), f = bt(), d && d.c(), pe(t, "alt", n = /*value*/
      l[0].caption || ""), hn(t.src, i = /*value*/
      l[0].image.url) || pe(t, "src", i), pe(t, "class", "thumbnail-img svelte-u350v8"), pe(t, "loading", "lazy"), pe(e, "class", "thumbnail-image-box svelte-u350v8");
    },
    m(h, y) {
      Mt(h, e, y), je(e, t), je(e, o), _ && _.m(e, null), je(e, r), c && c.m(e, null), je(e, f), d && d.m(e, null), a = !0, s || (u = ri(
        t,
        "click",
        /*click_handler*/
        l[5]
      ), s = !0);
    },
    p(h, [y]) {
      (!a || y & /*value*/
      1 && n !== (n = /*value*/
      h[0].caption || "")) && pe(t, "alt", n), (!a || y & /*value*/
      1 && !hn(t.src, i = /*value*/
      h[0].image.url)) && pe(t, "src", i), /*value*/
      h[0].caption ? _ ? _.p(h, y) : (_ = bn(h), _.c(), _.m(e, r)) : _ && (_.d(1), _ = null), /*clickable*/
      h[2] ? c ? c.p(h, y) : (c = gn(h), c.c(), c.m(e, f)) : c && (c.d(1), c = null), /*likeable*/
      h[1] ? d ? (d.p(h, y), y & /*likeable*/
      2 && lt(d, 1)) : (d = wn(h), d.c(), lt(d, 1), d.m(e, null)) : d && (Vr(), Ct(d, 1, 1, () => {
        d = null;
      }), Nr());
    },
    i(h) {
      a || (lt(d), a = !0);
    },
    o(h) {
      Ct(d), a = !1;
    },
    d(h) {
      h && It(e), _ && _.d(), c && c.d(), d && d.d(), s = !1, u();
    }
  };
}
function Zr(l, e, t) {
  const n = Ur();
  let { likeable: i } = e, { clickable: o } = e, { value: r } = e, { action_label: f } = e;
  const a = () => n("click"), s = () => {
    n("label_click");
  }, u = () => {
    if (r.liked) {
      t(0, r.liked = void 0, r), n("like", void 0);
      return;
    }
    t(0, r.liked = !0, r), n("like", !0);
  }, _ = () => {
    if (r.liked === !1) {
      t(0, r.liked = void 0, r), n("like", void 0);
      return;
    }
    t(0, r.liked = !1, r), n("like", !1);
  };
  return l.$$set = (c) => {
    "likeable" in c && t(1, i = c.likeable), "clickable" in c && t(2, o = c.clickable), "value" in c && t(0, r = c.value), "action_label" in c && t(3, f = c.action_label);
  }, [
    r,
    i,
    o,
    f,
    n,
    a,
    s,
    u,
    _
  ];
}
class Hr extends Br {
  constructor(e) {
    super(), Pr(this, e, Zr, Wr, Tr, {
      likeable: 1,
      clickable: 2,
      value: 0,
      action_label: 3
    });
  }
  get likeable() {
    return this.$$.ctx[1];
  }
  set likeable(e) {
    this.$$set({ likeable: e }), mt();
  }
  get clickable() {
    return this.$$.ctx[2];
  }
  set clickable(e) {
    this.$$set({ clickable: e }), mt();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({ value: e }), mt();
  }
  get action_label() {
    return this.$$.ctx[3];
  }
  set action_label(e) {
    this.$$set({ action_label: e }), mt();
  }
}
const xt = [
  {
    key: "xs",
    width: 0
  },
  {
    key: "sm",
    width: 576
  },
  {
    key: "md",
    width: 768
  },
  {
    key: "lg",
    width: 992
  },
  {
    key: "xl",
    width: 1200
  },
  {
    key: "xxl",
    width: 1600
  }
];
async function Xr(l) {
  if ("clipboard" in navigator)
    await navigator.clipboard.writeText(l);
  else {
    const e = document.createElement("textarea");
    e.value = l, e.style.position = "absolute", e.style.left = "-999999px", document.body.prepend(e), e.select();
    try {
      document.execCommand("copy");
    } catch (t) {
      return Promise.reject(t);
    } finally {
      e.remove();
    }
  }
}
async function Gr(l) {
  return l ? `<div style="display: flex; flex-wrap: wrap; gap: 16px">${(await Promise.all(
    l.map((t) => !t.image || !t.image.url ? "" : t.image.url)
  )).map((t) => `<img src="${t}" style="height: 400px" />`).join("")}</div>` : "";
}
function Yr(l) {
  let e = 0;
  for (let t = 0; t < l.length; t++)
    e = l[e] <= l[t] ? e : t;
  return e;
}
function Kr(l, {
  getWidth: e,
  setWidth: t,
  getHeight: n,
  setHeight: i,
  getPadding: o,
  setX: r,
  setY: f,
  getChildren: a
}, { cols: s, gap: u }) {
  const [_, c, d, h] = o(l), y = a(l), S = y.length, [v, k] = Array.isArray(u) ? u : [u, u];
  if (S) {
    const p = (e(l) - v * (s - 1) - (h + c)) / s;
    y.forEach((g) => {
      t(g, p);
    });
    const b = y.map((g) => n(g)), q = Array(s).fill(_);
    for (let g = 0; g < S; g++) {
      const L = y[g], C = Yr(q);
      f(L, q[C]), r(L, h + (p + v) * C), q[C] += b[g] + k;
    }
    i(l, Math.max(...q) - k + d);
  } else
    i(l, _ + d);
}
const kn = (l) => l.nodeType == 1, sl = Symbol(), al = Symbol();
function Jr(l, e) {
  let t, n, i = !1;
  function o() {
    i || (i = !0, requestAnimationFrame(() => {
      e(), l[al] = l.offsetWidth, l[sl] = l.offsetHeight, i = !1;
    }));
  }
  function r() {
    l && (t = new ResizeObserver((a) => {
      a.some((s) => {
        const u = s.target;
        return u[al] !== u.offsetWidth || u[sl] !== u.offsetHeight;
      }) && o();
    }), t.observe(l), Array.from(l.children).forEach((a) => {
      t.observe(a);
    }), n = new MutationObserver((a) => {
      a.forEach((s) => {
        s.addedNodes.forEach(
          (u) => kn(u) && t.observe(u)
        ), s.removedNodes.forEach(
          (u) => kn(u) && t.unobserve(u)
        );
      }), o();
    }), n.observe(l, { childList: !0, attributes: !1 }), o());
  }
  function f() {
    t == null || t.disconnect(), n == null || n.disconnect();
  }
  return { layout: o, mount: r, unmount: f };
}
const Qr = (l, e) => Jr(l, () => {
  Kr(
    l,
    {
      getWidth: (t) => t.offsetWidth,
      setWidth: (t, n) => t.style.width = n + "px",
      getHeight: (t) => (t[al] = t.offsetWidth, t[sl] = t.offsetHeight),
      setHeight: (t, n) => t.style.height = n + "px",
      getPadding: (t) => {
        const n = getComputedStyle(t);
        return [
          parseInt(n.paddingTop),
          parseInt(n.paddingRight),
          parseInt(n.paddingBottom),
          parseInt(n.paddingLeft)
        ];
      },
      setX: (t, n) => t.style.left = n + "px",
      setY: (t, n) => t.style.top = n + "px",
      getChildren: (t) => Array.from(t.children)
    },
    e
  );
});
class xr {
  constructor(e, t = {
    cols: 2,
    gap: 4
  }) {
    kl(this, "_layout");
    this._layout = Qr(e, t), this._layout.mount();
  }
  unmount() {
    this._layout.unmount();
  }
  render() {
    this._layout.layout();
  }
}
const {
  SvelteComponent: $r,
  add_iframe_resize_listener: ef,
  add_render_callback: _i,
  append: U,
  assign: tf,
  attr: E,
  binding_callbacks: $t,
  bubble: lf,
  check_outros: Pe,
  create_component: Ee,
  destroy_component: Ie,
  destroy_each: ci,
  detach: ce,
  element: G,
  empty: nf,
  ensure_array_like: qt,
  get_spread_object: of,
  get_spread_update: sf,
  globals: af,
  group_outros: Te,
  init: rf,
  insert: de,
  listen: St,
  mount_component: Me,
  noop: ff,
  run_all: uf,
  safe_not_equal: _f,
  set_data: di,
  set_style: Re,
  space: Ce,
  src_url_equal: Lt,
  text: mi,
  toggle_class: te,
  transition_in: M,
  transition_out: F
} = window.__gradio__svelte__internal, { window: rl } = af, { createEventDispatcher: cf, onDestroy: df, tick: mf } = window.__gradio__svelte__internal;
function pn(l, e, t) {
  const n = l.slice();
  return n[57] = e[t], n[59] = t, n;
}
function vn(l, e, t) {
  const n = l.slice();
  return n[57] = e[t], n[60] = e, n[59] = t, n;
}
function yn(l) {
  let e, t;
  return e = new _o({
    props: {
      show_label: (
        /*show_label*/
        l[2]
      ),
      Icon: Bn,
      label: (
        /*label*/
        l[4] || "Gallery"
      )
    }
  }), {
    c() {
      Ee(e.$$.fragment);
    },
    m(n, i) {
      Me(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*show_label*/
      4 && (o.show_label = /*show_label*/
      n[2]), i[0] & /*label*/
      16 && (o.label = /*label*/
      n[4] || "Gallery"), e.$set(o);
    },
    i(n) {
      t || (M(e.$$.fragment, n), t = !0);
    },
    o(n) {
      F(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Ie(e, n);
    }
  };
}
function hf(l) {
  let e, t, n, i, o, r, f, a, s, u, _, c = (
    /*selected_image*/
    l[23] && /*allow_preview*/
    l[9] && Cn(l)
  ), d = (
    /*show_share_button*/
    l[10] && jn(l)
  ), h = qt(
    /*resolved_value*/
    l[18]
  ), y = [];
  for (let b = 0; b < h.length; b += 1)
    y[b] = zn(pn(l, h, b));
  const S = (b) => F(y[b], 1, 1, () => {
    y[b] = null;
  }), v = [wf, gf], k = [];
  function p(b, q) {
    return (
      /*pending*/
      b[5] ? 0 : 1
    );
  }
  return a = p(l), s = k[a] = v[a](l), {
    c() {
      c && c.c(), e = Ce(), t = G("div"), n = G("div"), d && d.c(), i = Ce(), o = G("div");
      for (let b = 0; b < y.length; b += 1)
        y[b].c();
      r = Ce(), f = G("p"), s.c(), E(o, "class", "waterfall svelte-yk2d08"), E(n, "class", "grid-container svelte-yk2d08"), Re(
        n,
        "--object-fit",
        /*object_fit*/
        l[1]
      ), Re(
        n,
        "min-height",
        /*height*/
        l[8] + "px"
      ), te(
        n,
        "pt-6",
        /*show_label*/
        l[2]
      ), E(f, "class", "loading-line svelte-yk2d08"), te(f, "visible", !/*selected_image*/
      (l[23] && /*allow_preview*/
      l[9]) && /*has_more*/
      l[3]), E(t, "class", "grid-wrap svelte-yk2d08"), Re(
        t,
        "height",
        /*height*/
        l[8] + "px"
      ), _i(() => (
        /*div2_elementresize_handler*/
        l[51].call(t)
      )), te(t, "fixed-height", !/*height*/
      l[8] || /*height*/
      l[8] === "auto");
    },
    m(b, q) {
      c && c.m(b, q), de(b, e, q), de(b, t, q), U(t, n), d && d.m(n, null), U(n, i), U(n, o);
      for (let g = 0; g < y.length; g += 1)
        y[g] && y[g].m(o, null);
      l[49](o), U(t, r), U(t, f), k[a].m(f, null), u = ef(
        t,
        /*div2_elementresize_handler*/
        l[51].bind(t)
      ), _ = !0;
    },
    p(b, q) {
      if (/*selected_image*/
      b[23] && /*allow_preview*/
      b[9] ? c ? (c.p(b, q), q[0] & /*selected_image, allow_preview*/
      8389120 && M(c, 1)) : (c = Cn(b), c.c(), M(c, 1), c.m(e.parentNode, e)) : c && (Te(), F(c, 1, 1, () => {
        c = null;
      }), Pe()), /*show_share_button*/
      b[10] ? d ? (d.p(b, q), q[0] & /*show_share_button*/
      1024 && M(d, 1)) : (d = jn(b), d.c(), M(d, 1), d.m(n, i)) : d && (Te(), F(d, 1, 1, () => {
        d = null;
      }), Pe()), q[0] & /*resolved_value, selected_index, likeable, clickable, action_label, dispatch*/
      17045569) {
        h = qt(
          /*resolved_value*/
          b[18]
        );
        let L;
        for (L = 0; L < h.length; L += 1) {
          const C = pn(b, h, L);
          y[L] ? (y[L].p(C, q), M(y[L], 1)) : (y[L] = zn(C), y[L].c(), M(y[L], 1), y[L].m(o, null));
        }
        for (Te(), L = h.length; L < y.length; L += 1)
          S(L);
        Pe();
      }
      (!_ || q[0] & /*object_fit*/
      2) && Re(
        n,
        "--object-fit",
        /*object_fit*/
        b[1]
      ), (!_ || q[0] & /*height*/
      256) && Re(
        n,
        "min-height",
        /*height*/
        b[8] + "px"
      ), (!_ || q[0] & /*show_label*/
      4) && te(
        n,
        "pt-6",
        /*show_label*/
        b[2]
      );
      let g = a;
      a = p(b), a === g ? k[a].p(b, q) : (Te(), F(k[g], 1, 1, () => {
        k[g] = null;
      }), Pe(), s = k[a], s ? s.p(b, q) : (s = k[a] = v[a](b), s.c()), M(s, 1), s.m(f, null)), (!_ || q[0] & /*selected_image, allow_preview, has_more*/
      8389128) && te(f, "visible", !/*selected_image*/
      (b[23] && /*allow_preview*/
      b[9]) && /*has_more*/
      b[3]), (!_ || q[0] & /*height*/
      256) && Re(
        t,
        "height",
        /*height*/
        b[8] + "px"
      ), (!_ || q[0] & /*height*/
      256) && te(t, "fixed-height", !/*height*/
      b[8] || /*height*/
      b[8] === "auto");
    },
    i(b) {
      if (!_) {
        M(c), M(d);
        for (let q = 0; q < h.length; q += 1)
          M(y[q]);
        M(s), _ = !0;
      }
    },
    o(b) {
      F(c), F(d), y = y.filter(Boolean);
      for (let q = 0; q < y.length; q += 1)
        F(y[q]);
      F(s), _ = !1;
    },
    d(b) {
      b && (ce(e), ce(t)), c && c.d(b), d && d.d(), ci(y, b), l[49](null), k[a].d(), u();
    }
  };
}
function bf(l) {
  let e, t;
  return e = new Wo({
    props: {
      unpadded_box: !0,
      size: "large",
      $$slots: { default: [pf] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      Ee(e.$$.fragment);
    },
    m(n, i) {
      Me(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[1] & /*$$scope*/
      1073741824 && (o.$$scope = { dirty: i, ctx: n }), e.$set(o);
    },
    i(n) {
      t || (M(e.$$.fragment, n), t = !0);
    },
    o(n) {
      F(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Ie(e, n);
    }
  };
}
function Cn(l) {
  var q;
  let e, t, n, i, o, r, f, a, s, u, _, c, d, h, y, S, v = (
    /*show_download_button*/
    l[13] && qn(l)
  );
  i = new Sr({
    props: { i18n: (
      /*i18n*/
      l[14]
    ), absolute: !1 }
  }), i.$on(
    "clear",
    /*clear_handler*/
    l[39]
  );
  let k = (
    /*selected_image*/
    ((q = l[23]) == null ? void 0 : q.caption) && Sn(l)
  ), p = qt(
    /*resolved_value*/
    l[18]
  ), b = [];
  for (let g = 0; g < p.length; g += 1)
    b[g] = Ln(vn(l, p, g));
  return {
    c() {
      e = G("button"), t = G("div"), v && v.c(), n = Ce(), Ee(i.$$.fragment), o = Ce(), r = G("button"), f = G("img"), _ = Ce(), k && k.c(), c = Ce(), d = G("div");
      for (let g = 0; g < b.length; g += 1)
        b[g].c();
      E(t, "class", "icon-buttons svelte-yk2d08"), E(f, "data-testid", "detailed-image"), Lt(f.src, a = /*selected_image*/
      l[23].image.url) || E(f, "src", a), E(f, "alt", s = /*selected_image*/
      l[23].caption || ""), E(f, "title", u = /*selected_image*/
      l[23].caption || null), E(f, "loading", "lazy"), E(f, "class", "svelte-yk2d08"), te(f, "with-caption", !!/*selected_image*/
      l[23].caption), E(r, "class", "image-button svelte-yk2d08"), Re(r, "height", "calc(100% - " + /*selected_image*/
      (l[23].caption ? "80px" : "60px") + ")"), E(r, "aria-label", "detailed view of selected image"), E(d, "class", "thumbnails scroll-hide svelte-yk2d08"), E(d, "data-testid", "container_el"), E(e, "class", "preview svelte-yk2d08");
    },
    m(g, L) {
      de(g, e, L), U(e, t), v && v.m(t, null), U(t, n), Me(i, t, null), U(e, o), U(e, r), U(r, f), U(e, _), k && k.m(e, null), U(e, c), U(e, d);
      for (let C = 0; C < b.length; C += 1)
        b[C] && b[C].m(d, null);
      l[43](d), h = !0, y || (S = [
        St(
          r,
          "click",
          /*click_handler_1*/
          l[40]
        ),
        St(
          e,
          "keydown",
          /*on_keydown*/
          l[26]
        )
      ], y = !0);
    },
    p(g, L) {
      var T;
      /*show_download_button*/
      g[13] ? v ? (v.p(g, L), L[0] & /*show_download_button*/
      8192 && M(v, 1)) : (v = qn(g), v.c(), M(v, 1), v.m(t, n)) : v && (Te(), F(v, 1, 1, () => {
        v = null;
      }), Pe());
      const C = {};
      if (L[0] & /*i18n*/
      16384 && (C.i18n = /*i18n*/
      g[14]), i.$set(C), (!h || L[0] & /*selected_image*/
      8388608 && !Lt(f.src, a = /*selected_image*/
      g[23].image.url)) && E(f, "src", a), (!h || L[0] & /*selected_image*/
      8388608 && s !== (s = /*selected_image*/
      g[23].caption || "")) && E(f, "alt", s), (!h || L[0] & /*selected_image*/
      8388608 && u !== (u = /*selected_image*/
      g[23].caption || null)) && E(f, "title", u), (!h || L[0] & /*selected_image*/
      8388608) && te(f, "with-caption", !!/*selected_image*/
      g[23].caption), (!h || L[0] & /*selected_image*/
      8388608) && Re(r, "height", "calc(100% - " + /*selected_image*/
      (g[23].caption ? "80px" : "60px") + ")"), /*selected_image*/
      (T = g[23]) != null && T.caption ? k ? k.p(g, L) : (k = Sn(g), k.c(), k.m(e, c)) : k && (k.d(1), k = null), L[0] & /*resolved_value, el, selected_index*/
      2359297) {
        p = qt(
          /*resolved_value*/
          g[18]
        );
        let A;
        for (A = 0; A < p.length; A += 1) {
          const O = vn(g, p, A);
          b[A] ? b[A].p(O, L) : (b[A] = Ln(O), b[A].c(), b[A].m(d, null));
        }
        for (; A < b.length; A += 1)
          b[A].d(1);
        b.length = p.length;
      }
    },
    i(g) {
      h || (M(v), M(i.$$.fragment, g), h = !0);
    },
    o(g) {
      F(v), F(i.$$.fragment, g), h = !1;
    },
    d(g) {
      g && ce(e), v && v.d(), Ie(i), k && k.d(), ci(b, g), l[43](null), y = !1, uf(S);
    }
  };
}
function qn(l) {
  let e, t, n;
  return t = new ze({
    props: {
      show_label: !0,
      label: (
        /*i18n*/
        l[14]("common.download")
      ),
      Icon: Rn
    }
  }), t.$on(
    "click",
    /*click_handler*/
    l[38]
  ), {
    c() {
      e = G("div"), Ee(t.$$.fragment), E(e, "class", "download-button-container svelte-yk2d08");
    },
    m(i, o) {
      de(i, e, o), Me(t, e, null), n = !0;
    },
    p(i, o) {
      const r = {};
      o[0] & /*i18n*/
      16384 && (r.label = /*i18n*/
      i[14]("common.download")), t.$set(r);
    },
    i(i) {
      n || (M(t.$$.fragment, i), n = !0);
    },
    o(i) {
      F(t.$$.fragment, i), n = !1;
    },
    d(i) {
      i && ce(e), Ie(t);
    }
  };
}
function Sn(l) {
  let e, t = (
    /*selected_image*/
    l[23].caption + ""
  ), n;
  return {
    c() {
      e = G("caption"), n = mi(t), E(e, "class", "caption svelte-yk2d08");
    },
    m(i, o) {
      de(i, e, o), U(e, n);
    },
    p(i, o) {
      o[0] & /*selected_image*/
      8388608 && t !== (t = /*selected_image*/
      i[23].caption + "") && di(n, t);
    },
    d(i) {
      i && ce(e);
    }
  };
}
function Ln(l) {
  let e, t, n, i, o, r, f = (
    /*i*/
    l[59]
  ), a, s;
  const u = () => (
    /*button_binding*/
    l[41](e, f)
  ), _ = () => (
    /*button_binding*/
    l[41](null, f)
  );
  function c() {
    return (
      /*click_handler_2*/
      l[42](
        /*i*/
        l[59]
      )
    );
  }
  return {
    c() {
      e = G("button"), t = G("img"), o = Ce(), Lt(t.src, n = /*entry*/
      l[57].image.url) || E(t, "src", n), E(t, "title", i = /*entry*/
      l[57].caption || null), E(t, "data-testid", "thumbnail " + /*i*/
      (l[59] + 1)), E(t, "alt", ""), E(t, "loading", "lazy"), E(t, "class", "svelte-yk2d08"), E(e, "class", "thumbnail-item thumbnail-small svelte-yk2d08"), E(e, "aria-label", r = "Thumbnail " + /*i*/
      (l[59] + 1) + " of " + /*resolved_value*/
      l[18].length), te(
        e,
        "selected",
        /*selected_index*/
        l[0] === /*i*/
        l[59]
      );
    },
    m(d, h) {
      de(d, e, h), U(e, t), U(e, o), u(), a || (s = St(e, "click", c), a = !0);
    },
    p(d, h) {
      l = d, h[0] & /*resolved_value*/
      262144 && !Lt(t.src, n = /*entry*/
      l[57].image.url) && E(t, "src", n), h[0] & /*resolved_value*/
      262144 && i !== (i = /*entry*/
      l[57].caption || null) && E(t, "title", i), h[0] & /*resolved_value*/
      262144 && r !== (r = "Thumbnail " + /*i*/
      (l[59] + 1) + " of " + /*resolved_value*/
      l[18].length) && E(e, "aria-label", r), f !== /*i*/
      l[59] && (_(), f = /*i*/
      l[59], u()), h[0] & /*selected_index*/
      1 && te(
        e,
        "selected",
        /*selected_index*/
        l[0] === /*i*/
        l[59]
      );
    },
    d(d) {
      d && ce(e), _(), a = !1, s();
    }
  };
}
function jn(l) {
  let e, t, n;
  return t = new $s({
    props: {
      i18n: (
        /*i18n*/
        l[14]
      ),
      value: (
        /*resolved_value*/
        l[18]
      ),
      formatter: Gr
    }
  }), t.$on(
    "share",
    /*share_handler*/
    l[44]
  ), t.$on(
    "error",
    /*error_handler*/
    l[45]
  ), {
    c() {
      e = G("div"), Ee(t.$$.fragment), E(e, "class", "icon-button svelte-yk2d08");
    },
    m(i, o) {
      de(i, e, o), Me(t, e, null), n = !0;
    },
    p(i, o) {
      const r = {};
      o[0] & /*i18n*/
      16384 && (r.i18n = /*i18n*/
      i[14]), o[0] & /*resolved_value*/
      262144 && (r.value = /*resolved_value*/
      i[18]), t.$set(r);
    },
    i(i) {
      n || (M(t.$$.fragment, i), n = !0);
    },
    o(i) {
      F(t.$$.fragment, i), n = !1;
    },
    d(i) {
      i && ce(e), Ie(t);
    }
  };
}
function zn(l) {
  let e, t, n, i, o;
  function r() {
    return (
      /*click_handler_3*/
      l[46](
        /*i*/
        l[59]
      )
    );
  }
  function f() {
    return (
      /*label_click_handler*/
      l[47](
        /*i*/
        l[59],
        /*entry*/
        l[57]
      )
    );
  }
  function a(...s) {
    return (
      /*like_handler*/
      l[48](
        /*i*/
        l[59],
        /*entry*/
        l[57],
        ...s
      )
    );
  }
  return t = new Hr({
    props: {
      likeable: (
        /*likeable*/
        l[11]
      ),
      clickable: (
        /*clickable*/
        l[12]
      ),
      value: (
        /*entry*/
        l[57]
      ),
      action_label: (
        /*action_label*/
        l[6]
      )
    }
  }), t.$on("click", r), t.$on("label_click", f), t.$on("like", a), {
    c() {
      e = G("div"), Ee(t.$$.fragment), n = Ce(), E(e, "class", "thumbnail-item thumbnail-lg svelte-yk2d08"), E(e, "aria-label", i = "Thumbnail " + /*i*/
      (l[59] + 1) + " of " + /*resolved_value*/
      l[18].length), te(
        e,
        "selected",
        /*selected_index*/
        l[0] === /*i*/
        l[59]
      );
    },
    m(s, u) {
      de(s, e, u), Me(t, e, null), U(e, n), o = !0;
    },
    p(s, u) {
      l = s;
      const _ = {};
      u[0] & /*likeable*/
      2048 && (_.likeable = /*likeable*/
      l[11]), u[0] & /*clickable*/
      4096 && (_.clickable = /*clickable*/
      l[12]), u[0] & /*resolved_value*/
      262144 && (_.value = /*entry*/
      l[57]), u[0] & /*action_label*/
      64 && (_.action_label = /*action_label*/
      l[6]), t.$set(_), (!o || u[0] & /*resolved_value*/
      262144 && i !== (i = "Thumbnail " + /*i*/
      (l[59] + 1) + " of " + /*resolved_value*/
      l[18].length)) && E(e, "aria-label", i), (!o || u[0] & /*selected_index*/
      1) && te(
        e,
        "selected",
        /*selected_index*/
        l[0] === /*i*/
        l[59]
      );
    },
    i(s) {
      o || (M(t.$$.fragment, s), o = !0);
    },
    o(s) {
      F(t.$$.fragment, s), o = !1;
    },
    d(s) {
      s && ce(e), Ie(t);
    }
  };
}
function gf(l) {
  let e, t;
  const n = [
    /*load_more_button_props*/
    l[15]
  ];
  let i = {
    $$slots: { default: [kf] },
    $$scope: { ctx: l }
  };
  for (let o = 0; o < n.length; o += 1)
    i = tf(i, n[o]);
  return e = new Xa({ props: i }), e.$on(
    "click",
    /*click_handler_4*/
    l[50]
  ), {
    c() {
      Ee(e.$$.fragment);
    },
    m(o, r) {
      Me(e, o, r), t = !0;
    },
    p(o, r) {
      const f = r[0] & /*load_more_button_props*/
      32768 ? sf(n, [of(
        /*load_more_button_props*/
        o[15]
      )]) : {};
      r[0] & /*i18n, load_more_button_props*/
      49152 | r[1] & /*$$scope*/
      1073741824 && (f.$$scope = { dirty: r, ctx: o }), e.$set(f);
    },
    i(o) {
      t || (M(e.$$.fragment, o), t = !0);
    },
    o(o) {
      F(e.$$.fragment, o), t = !1;
    },
    d(o) {
      Ie(e, o);
    }
  };
}
function wf(l) {
  let e, t;
  return e = new Tn({ props: { margin: !1 } }), {
    c() {
      Ee(e.$$.fragment);
    },
    m(n, i) {
      Me(e, n, i), t = !0;
    },
    p: ff,
    i(n) {
      t || (M(e.$$.fragment, n), t = !0);
    },
    o(n) {
      F(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Ie(e, n);
    }
  };
}
function kf(l) {
  let e = (
    /*i18n*/
    l[14](
      /*load_more_button_props*/
      l[15].value || /*load_more_button_props*/
      l[15].label || "Load More"
    ) + ""
  ), t;
  return {
    c() {
      t = mi(e);
    },
    m(n, i) {
      de(n, t, i);
    },
    p(n, i) {
      i[0] & /*i18n, load_more_button_props*/
      49152 && e !== (e = /*i18n*/
      n[14](
        /*load_more_button_props*/
        n[15].value || /*load_more_button_props*/
        n[15].label || "Load More"
      ) + "") && di(t, e);
    },
    d(n) {
      n && ce(t);
    }
  };
}
function pf(l) {
  let e, t;
  return e = new Bn({}), {
    c() {
      Ee(e.$$.fragment);
    },
    m(n, i) {
      Me(e, n, i), t = !0;
    },
    i(n) {
      t || (M(e.$$.fragment, n), t = !0);
    },
    o(n) {
      F(e.$$.fragment, n), t = !1;
    },
    d(n) {
      Ie(e, n);
    }
  };
}
function vf(l) {
  let e, t, n, i, o, r, f;
  _i(
    /*onwindowresize*/
    l[37]
  );
  let a = (
    /*show_label*/
    l[2] && yn(l)
  );
  const s = [bf, hf], u = [];
  function _(c, d) {
    return !/*value*/
    c[7] || !/*resolved_value*/
    c[18] || /*resolved_value*/
    c[18].length === 0 ? 0 : 1;
  }
  return t = _(l), n = u[t] = s[t](l), {
    c() {
      a && a.c(), e = Ce(), n.c(), i = nf();
    },
    m(c, d) {
      a && a.m(c, d), de(c, e, d), u[t].m(c, d), de(c, i, d), o = !0, r || (f = St(
        rl,
        "resize",
        /*onwindowresize*/
        l[37]
      ), r = !0);
    },
    p(c, d) {
      /*show_label*/
      c[2] ? a ? (a.p(c, d), d[0] & /*show_label*/
      4 && M(a, 1)) : (a = yn(c), a.c(), M(a, 1), a.m(e.parentNode, e)) : a && (Te(), F(a, 1, 1, () => {
        a = null;
      }), Pe());
      let h = t;
      t = _(c), t === h ? u[t].p(c, d) : (Te(), F(u[h], 1, 1, () => {
        u[h] = null;
      }), Pe(), n = u[t], n ? n.p(c, d) : (n = u[t] = s[t](c), n.c()), M(n, 1), n.m(i.parentNode, i));
    },
    i(c) {
      o || (M(a), M(n), o = !0);
    },
    o(c) {
      F(a), F(n), o = !1;
    },
    d(c) {
      c && (ce(e), ce(i)), a && a.d(c), u[t].d(c), r = !1, f();
    }
  };
}
async function yf(l, e) {
  let t;
  try {
    t = await fetch(l);
  } catch (r) {
    if (r instanceof TypeError) {
      window.open(l, "_blank", "noreferrer");
      return;
    }
    throw r;
  }
  const n = await t.blob(), i = URL.createObjectURL(n), o = document.createElement("a");
  o.href = i, o.download = e, o.click(), URL.revokeObjectURL(i);
}
function Cf(l, e, t) {
  let n, i, o, { object_fit: r = "cover" } = e, { show_label: f = !0 } = e, { has_more: a = !1 } = e, { label: s } = e, { pending: u } = e, { action_label: _ } = e, { value: c = null } = e, { columns: d = [2] } = e, { height: h = "auto" } = e, { preview: y } = e, { root: S } = e, { proxy_url: v } = e, { allow_preview: k = !0 } = e, { show_share_button: p = !1 } = e, { likeable: b } = e, { clickable: q } = e, { show_download_button: g = !1 } = e, { i18n: L } = e, { selected_index: C = null } = e, { gap: T = 8 } = e, { load_more_button_props: A = {} } = e, O, B = [], me, Z = 0, he = 0, H = 0;
  const ie = cf();
  let qe = !0, Q = null, N = null, be = c;
  C == null && y && (c != null && c.length) && (C = 0);
  let Ne = C;
  function Ze(w) {
    const P = w.target, ge = w.clientX, At = P.offsetWidth / 2;
    ge < At ? t(0, C = n) : t(0, C = i);
  }
  function $e(w) {
    switch (w.code) {
      case "Escape":
        w.preventDefault(), t(0, C = null);
        break;
      case "ArrowLeft":
        w.preventDefault(), t(0, C = n);
        break;
      case "ArrowRight":
        w.preventDefault(), t(0, C = i);
        break;
    }
  }
  let m = [], Ae;
  async function hi(w) {
    var wl;
    if (typeof w != "number" || (await mf(), m[w] === void 0))
      return;
    (wl = m[w]) == null || wl.focus();
    const { left: P, width: ge } = Ae.getBoundingClientRect(), { left: bl, width: At } = m[w].getBoundingClientRect(), gl = bl - P + At / 2 - ge / 2 + Ae.scrollLeft;
    Ae && typeof Ae.scrollTo == "function" && Ae.scrollTo({
      left: gl < 0 ? 0 : gl,
      behavior: "smooth"
    });
  }
  function bi() {
    Q == null || Q.unmount(), Q = new xr(O, { cols: me, gap: T });
  }
  df(() => {
    Q == null || Q.unmount();
  });
  function gi() {
    t(20, he = rl.innerHeight), t(17, H = rl.innerWidth);
  }
  const wi = () => {
    const w = o == null ? void 0 : o.image;
    if (!w)
      return;
    const { url: P, orig_name: ge } = w;
    P && yf(P, ge ?? "image");
  }, ki = () => t(0, C = null), pi = (w) => Ze(w);
  function vi(w, P) {
    $t[w ? "unshift" : "push"](() => {
      m[P] = w, t(21, m);
    });
  }
  const yi = (w) => t(0, C = w);
  function Ci(w) {
    $t[w ? "unshift" : "push"](() => {
      Ae = w, t(22, Ae);
    });
  }
  const qi = (w) => {
    Xr(w.detail.description);
  };
  function Si(w) {
    lf.call(this, l, w);
  }
  const Li = (w) => t(0, C = w), ji = (w, P) => {
    ie("click", { index: w, value: P });
  }, zi = (w, P, ge) => {
    ie("like", { index: w, value: P, liked: ge.detail });
  };
  function Ei(w) {
    $t[w ? "unshift" : "push"](() => {
      O = w, t(16, O);
    });
  }
  const Ii = () => {
    ie("load_more");
  };
  function Mi() {
    Z = this.clientHeight, t(19, Z);
  }
  return l.$$set = (w) => {
    "object_fit" in w && t(1, r = w.object_fit), "show_label" in w && t(2, f = w.show_label), "has_more" in w && t(3, a = w.has_more), "label" in w && t(4, s = w.label), "pending" in w && t(5, u = w.pending), "action_label" in w && t(6, _ = w.action_label), "value" in w && t(7, c = w.value), "columns" in w && t(27, d = w.columns), "height" in w && t(8, h = w.height), "preview" in w && t(28, y = w.preview), "root" in w && t(29, S = w.root), "proxy_url" in w && t(30, v = w.proxy_url), "allow_preview" in w && t(9, k = w.allow_preview), "show_share_button" in w && t(10, p = w.show_share_button), "likeable" in w && t(11, b = w.likeable), "clickable" in w && t(12, q = w.clickable), "show_download_button" in w && t(13, g = w.show_download_button), "i18n" in w && t(14, L = w.i18n), "selected_index" in w && t(0, C = w.selected_index), "gap" in w && t(31, T = w.gap), "load_more_button_props" in w && t(15, A = w.load_more_button_props);
  }, l.$$.update = () => {
    if (l.$$.dirty[0] & /*columns*/
    134217728)
      if (typeof d == "object" && d !== null)
        if (Array.isArray(d)) {
          const w = d.length;
          t(32, B = xt.map((P, ge) => [P.width, d[ge] ?? d[w - 1]]));
        } else {
          let w = 0;
          t(32, B = xt.map((P) => (w = d[P.key] ?? w, [P.width, w])));
        }
      else
        t(32, B = xt.map((w) => [w.width, d]));
    if (l.$$.dirty[0] & /*window_width*/
    131072 | l.$$.dirty[1] & /*breakpointColumns*/
    2) {
      for (const [w, P] of [...B].reverse())
        if (H >= w) {
          t(33, me = P);
          break;
        }
    }
    l.$$.dirty[0] & /*value*/
    128 | l.$$.dirty[1] & /*was_reset*/
    8 && t(34, qe = c == null || c.length === 0 ? !0 : qe), l.$$.dirty[0] & /*value, root, proxy_url*/
    1610612864 && t(18, N = c == null ? null : c.map((w) => (w.image = ai(w.image, S, v), w))), l.$$.dirty[0] & /*value, preview, selected_index*/
    268435585 | l.$$.dirty[1] & /*prev_value, was_reset*/
    24 && (tt(be, c) || (qe ? (t(0, C = y && (c != null && c.length) ? 0 : null), t(34, qe = !1), Q = null) : t(
      0,
      C = C != null && c != null && C < c.length ? C : null
    ), ie("change"), t(35, be = c))), l.$$.dirty[0] & /*selected_index, resolved_value*/
    262145 && (n = ((C ?? 0) + ((N == null ? void 0 : N.length) ?? 0) - 1) % ((N == null ? void 0 : N.length) ?? 0)), l.$$.dirty[0] & /*selected_index, resolved_value*/
    262145 && (i = ((C ?? 0) + 1) % ((N == null ? void 0 : N.length) ?? 0)), l.$$.dirty[0] & /*selected_index, resolved_value*/
    262145 | l.$$.dirty[1] & /*old_selected_index*/
    32 && C !== Ne && (t(36, Ne = C), C !== null && ie("select", {
      index: C,
      value: N == null ? void 0 : N[C]
    })), l.$$.dirty[0] & /*allow_preview, selected_index*/
    513 && k && hi(C), l.$$.dirty[0] & /*waterfall_grid_el*/
    65536 | l.$$.dirty[1] & /*cols*/
    4 && O && bi(), l.$$.dirty[0] & /*selected_index, resolved_value*/
    262145 && t(23, o = C != null && N != null ? N[C] : null);
  }, [
    C,
    r,
    f,
    a,
    s,
    u,
    _,
    c,
    h,
    k,
    p,
    b,
    q,
    g,
    L,
    A,
    O,
    H,
    N,
    Z,
    he,
    m,
    Ae,
    o,
    ie,
    Ze,
    $e,
    d,
    y,
    S,
    v,
    T,
    B,
    me,
    qe,
    be,
    Ne,
    gi,
    wi,
    ki,
    pi,
    vi,
    yi,
    Ci,
    qi,
    Si,
    Li,
    ji,
    zi,
    Ei,
    Ii,
    Mi
  ];
}
class qf extends $r {
  constructor(e) {
    super(), rf(
      this,
      e,
      Cf,
      vf,
      _f,
      {
        object_fit: 1,
        show_label: 2,
        has_more: 3,
        label: 4,
        pending: 5,
        action_label: 6,
        value: 7,
        columns: 27,
        height: 8,
        preview: 28,
        root: 29,
        proxy_url: 30,
        allow_preview: 9,
        show_share_button: 10,
        likeable: 11,
        clickable: 12,
        show_download_button: 13,
        i18n: 14,
        selected_index: 0,
        gap: 31,
        load_more_button_props: 15
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: Sf,
  add_flush_callback: Lf,
  assign: jf,
  bind: zf,
  binding_callbacks: Ef,
  check_outros: If,
  create_component: dl,
  destroy_component: ml,
  detach: Mf,
  get_spread_object: Af,
  get_spread_update: Df,
  group_outros: Ff,
  init: Rf,
  insert: Bf,
  mount_component: hl,
  safe_not_equal: Nf,
  space: Vf,
  transition_in: Je,
  transition_out: nt
} = window.__gradio__svelte__internal, { createEventDispatcher: Pf } = window.__gradio__svelte__internal;
function En(l) {
  let e, t;
  const n = [
    {
      autoscroll: (
        /*gradio*/
        l[25].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      l[25].i18n
    ) },
    /*loading_status*/
    l[1],
    {
      show_progress: (
        /*loading_status*/
        l[1].show_progress === "hidden" ? "hidden" : (
          /*has_more*/
          l[3] ? "minimal" : (
            /*loading_status*/
            l[1].show_progress
          )
        )
      )
    }
  ];
  let i = {};
  for (let o = 0; o < n.length; o += 1)
    i = jf(i, n[o]);
  return e = new Da({ props: i }), {
    c() {
      dl(e.$$.fragment);
    },
    m(o, r) {
      hl(e, o, r), t = !0;
    },
    p(o, r) {
      const f = r[0] & /*gradio, loading_status, has_more*/
      33554442 ? Df(n, [
        r[0] & /*gradio*/
        33554432 && {
          autoscroll: (
            /*gradio*/
            o[25].autoscroll
          )
        },
        r[0] & /*gradio*/
        33554432 && { i18n: (
          /*gradio*/
          o[25].i18n
        ) },
        r[0] & /*loading_status*/
        2 && Af(
          /*loading_status*/
          o[1]
        ),
        r[0] & /*loading_status, has_more*/
        10 && {
          show_progress: (
            /*loading_status*/
            o[1].show_progress === "hidden" ? "hidden" : (
              /*has_more*/
              o[3] ? "minimal" : (
                /*loading_status*/
                o[1].show_progress
              )
            )
          )
        }
      ]) : {};
      e.$set(f);
    },
    i(o) {
      t || (Je(e.$$.fragment, o), t = !0);
    },
    o(o) {
      nt(e.$$.fragment, o), t = !1;
    },
    d(o) {
      ml(e, o);
    }
  };
}
function Tf(l) {
  var a;
  let e, t, n, i, o = (
    /*loading_status*/
    l[1] && En(l)
  );
  function r(s) {
    l[29](s);
  }
  let f = {
    pending: (
      /*loading_status*/
      ((a = l[1]) == null ? void 0 : a.status) === "pending"
    ),
    likeable: (
      /*likeable*/
      l[10]
    ),
    clickable: (
      /*clickable*/
      l[11]
    ),
    label: (
      /*label*/
      l[4]
    ),
    action_label: (
      /*action_label*/
      l[5]
    ),
    value: (
      /*value*/
      l[9]
    ),
    root: (
      /*root*/
      l[23]
    ),
    proxy_url: (
      /*proxy_url*/
      l[24]
    ),
    show_label: (
      /*show_label*/
      l[2]
    ),
    object_fit: (
      /*object_fit*/
      l[21]
    ),
    load_more_button_props: (
      /*_load_more_button_props*/
      l[26]
    ),
    has_more: (
      /*has_more*/
      l[3]
    ),
    columns: (
      /*columns*/
      l[15]
    ),
    height: (
      /*height*/
      l[17]
    ),
    preview: (
      /*preview*/
      l[18]
    ),
    gap: (
      /*gap*/
      l[16]
    ),
    allow_preview: (
      /*allow_preview*/
      l[19]
    ),
    show_share_button: (
      /*show_share_button*/
      l[20]
    ),
    show_download_button: (
      /*show_download_button*/
      l[22]
    ),
    i18n: (
      /*gradio*/
      l[25].i18n
    )
  };
  return (
    /*selected_index*/
    l[0] !== void 0 && (f.selected_index = /*selected_index*/
    l[0]), t = new qf({ props: f }), Ef.push(() => zf(t, "selected_index", r)), t.$on(
      "click",
      /*click_handler*/
      l[30]
    ), t.$on(
      "change",
      /*change_handler*/
      l[31]
    ), t.$on(
      "like",
      /*like_handler*/
      l[32]
    ), t.$on(
      "select",
      /*select_handler*/
      l[33]
    ), t.$on(
      "share",
      /*share_handler*/
      l[34]
    ), t.$on(
      "error",
      /*error_handler*/
      l[35]
    ), t.$on(
      "load_more",
      /*load_more_handler*/
      l[36]
    ), {
      c() {
        o && o.c(), e = Vf(), dl(t.$$.fragment);
      },
      m(s, u) {
        o && o.m(s, u), Bf(s, e, u), hl(t, s, u), i = !0;
      },
      p(s, u) {
        var c;
        /*loading_status*/
        s[1] ? o ? (o.p(s, u), u[0] & /*loading_status*/
        2 && Je(o, 1)) : (o = En(s), o.c(), Je(o, 1), o.m(e.parentNode, e)) : o && (Ff(), nt(o, 1, 1, () => {
          o = null;
        }), If());
        const _ = {};
        u[0] & /*loading_status*/
        2 && (_.pending = /*loading_status*/
        ((c = s[1]) == null ? void 0 : c.status) === "pending"), u[0] & /*likeable*/
        1024 && (_.likeable = /*likeable*/
        s[10]), u[0] & /*clickable*/
        2048 && (_.clickable = /*clickable*/
        s[11]), u[0] & /*label*/
        16 && (_.label = /*label*/
        s[4]), u[0] & /*action_label*/
        32 && (_.action_label = /*action_label*/
        s[5]), u[0] & /*value*/
        512 && (_.value = /*value*/
        s[9]), u[0] & /*root*/
        8388608 && (_.root = /*root*/
        s[23]), u[0] & /*proxy_url*/
        16777216 && (_.proxy_url = /*proxy_url*/
        s[24]), u[0] & /*show_label*/
        4 && (_.show_label = /*show_label*/
        s[2]), u[0] & /*object_fit*/
        2097152 && (_.object_fit = /*object_fit*/
        s[21]), u[0] & /*_load_more_button_props*/
        67108864 && (_.load_more_button_props = /*_load_more_button_props*/
        s[26]), u[0] & /*has_more*/
        8 && (_.has_more = /*has_more*/
        s[3]), u[0] & /*columns*/
        32768 && (_.columns = /*columns*/
        s[15]), u[0] & /*height*/
        131072 && (_.height = /*height*/
        s[17]), u[0] & /*preview*/
        262144 && (_.preview = /*preview*/
        s[18]), u[0] & /*gap*/
        65536 && (_.gap = /*gap*/
        s[16]), u[0] & /*allow_preview*/
        524288 && (_.allow_preview = /*allow_preview*/
        s[19]), u[0] & /*show_share_button*/
        1048576 && (_.show_share_button = /*show_share_button*/
        s[20]), u[0] & /*show_download_button*/
        4194304 && (_.show_download_button = /*show_download_button*/
        s[22]), u[0] & /*gradio*/
        33554432 && (_.i18n = /*gradio*/
        s[25].i18n), !n && u[0] & /*selected_index*/
        1 && (n = !0, _.selected_index = /*selected_index*/
        s[0], Lf(() => n = !1)), t.$set(_);
      },
      i(s) {
        i || (Je(o), Je(t.$$.fragment, s), i = !0);
      },
      o(s) {
        nt(o), nt(t.$$.fragment, s), i = !1;
      },
      d(s) {
        s && Mf(e), o && o.d(s), ml(t, s);
      }
    }
  );
}
function Of(l) {
  let e, t;
  return e = new Ki({
    props: {
      visible: (
        /*visible*/
        l[8]
      ),
      variant: "solid",
      padding: !1,
      elem_id: (
        /*elem_id*/
        l[6]
      ),
      elem_classes: (
        /*elem_classes*/
        l[7]
      ),
      container: (
        /*container*/
        l[12]
      ),
      scale: (
        /*scale*/
        l[13]
      ),
      min_width: (
        /*min_width*/
        l[14]
      ),
      allow_overflow: !1,
      $$slots: { default: [Tf] },
      $$scope: { ctx: l }
    }
  }), {
    c() {
      dl(e.$$.fragment);
    },
    m(n, i) {
      hl(e, n, i), t = !0;
    },
    p(n, i) {
      const o = {};
      i[0] & /*visible*/
      256 && (o.visible = /*visible*/
      n[8]), i[0] & /*elem_id*/
      64 && (o.elem_id = /*elem_id*/
      n[6]), i[0] & /*elem_classes*/
      128 && (o.elem_classes = /*elem_classes*/
      n[7]), i[0] & /*container*/
      4096 && (o.container = /*container*/
      n[12]), i[0] & /*scale*/
      8192 && (o.scale = /*scale*/
      n[13]), i[0] & /*min_width*/
      16384 && (o.min_width = /*min_width*/
      n[14]), i[0] & /*loading_status, likeable, clickable, label, action_label, value, root, proxy_url, show_label, object_fit, _load_more_button_props, has_more, columns, height, preview, gap, allow_preview, show_share_button, show_download_button, gradio, selected_index*/
      134188607 | i[1] & /*$$scope*/
      128 && (o.$$scope = { dirty: i, ctx: n }), e.$set(o);
    },
    i(n) {
      t || (Je(e.$$.fragment, n), t = !0);
    },
    o(n) {
      nt(e.$$.fragment, n), t = !1;
    },
    d(n) {
      ml(e, n);
    }
  };
}
function Uf(l, e, t) {
  let { loading_status: n } = e, { show_label: i } = e, { has_more: o } = e, { label: r } = e, { action_label: f } = e, { elem_id: a = "" } = e, { elem_classes: s = [] } = e, { visible: u = !0 } = e, { value: _ = null } = e, { likeable: c } = e, { clickable: d } = e, { container: h = !0 } = e, { scale: y = null } = e, { min_width: S = void 0 } = e, { columns: v = [2] } = e, { gap: k = 8 } = e, { height: p = "auto" } = e, { preview: b } = e, { allow_preview: q = !0 } = e, { selected_index: g = null } = e, { show_share_button: L = !1 } = e, { object_fit: C = "cover" } = e, { show_download_button: T = !1 } = e, { root: A } = e, { proxy_url: O } = e, { gradio: B } = e, { load_more_button_props: me = {} } = e, Z = {};
  const he = Pf(), H = (m) => {
    B.dispatch("like", m);
  };
  function ie(m) {
    g = m, t(0, g);
  }
  const qe = (m) => B.dispatch("click", m.detail), Q = () => B.dispatch("change", _), N = (m) => H(m.detail), be = (m) => B.dispatch("select", m.detail), Ne = (m) => B.dispatch("share", m.detail), Ze = (m) => B.dispatch("error", m.detail), $e = () => {
    B.dispatch("load_more", _);
  };
  return l.$$set = (m) => {
    "loading_status" in m && t(1, n = m.loading_status), "show_label" in m && t(2, i = m.show_label), "has_more" in m && t(3, o = m.has_more), "label" in m && t(4, r = m.label), "action_label" in m && t(5, f = m.action_label), "elem_id" in m && t(6, a = m.elem_id), "elem_classes" in m && t(7, s = m.elem_classes), "visible" in m && t(8, u = m.visible), "value" in m && t(9, _ = m.value), "likeable" in m && t(10, c = m.likeable), "clickable" in m && t(11, d = m.clickable), "container" in m && t(12, h = m.container), "scale" in m && t(13, y = m.scale), "min_width" in m && t(14, S = m.min_width), "columns" in m && t(15, v = m.columns), "gap" in m && t(16, k = m.gap), "height" in m && t(17, p = m.height), "preview" in m && t(18, b = m.preview), "allow_preview" in m && t(19, q = m.allow_preview), "selected_index" in m && t(0, g = m.selected_index), "show_share_button" in m && t(20, L = m.show_share_button), "object_fit" in m && t(21, C = m.object_fit), "show_download_button" in m && t(22, T = m.show_download_button), "root" in m && t(23, A = m.root), "proxy_url" in m && t(24, O = m.proxy_url), "gradio" in m && t(25, B = m.gradio), "load_more_button_props" in m && t(28, me = m.load_more_button_props);
  }, l.$$.update = () => {
    l.$$.dirty[0] & /*_load_more_button_props, load_more_button_props*/
    335544320 && t(26, Z = {
      ...Z,
      ...me
    }), l.$$.dirty[0] & /*selected_index*/
    1 && he("prop_change", { selected_index: g });
  }, [
    g,
    n,
    i,
    o,
    r,
    f,
    a,
    s,
    u,
    _,
    c,
    d,
    h,
    y,
    S,
    v,
    k,
    p,
    b,
    q,
    L,
    C,
    T,
    A,
    O,
    B,
    Z,
    H,
    me,
    ie,
    qe,
    Q,
    N,
    be,
    Ne,
    Ze,
    $e
  ];
}
class Gf extends Sf {
  constructor(e) {
    super(), Rf(
      this,
      e,
      Uf,
      Of,
      Nf,
      {
        loading_status: 1,
        show_label: 2,
        has_more: 3,
        label: 4,
        action_label: 5,
        elem_id: 6,
        elem_classes: 7,
        visible: 8,
        value: 9,
        likeable: 10,
        clickable: 11,
        container: 12,
        scale: 13,
        min_width: 14,
        columns: 15,
        gap: 16,
        height: 17,
        preview: 18,
        allow_preview: 19,
        selected_index: 0,
        show_share_button: 20,
        object_fit: 21,
        show_download_button: 22,
        root: 23,
        proxy_url: 24,
        gradio: 25,
        load_more_button_props: 28
      },
      null,
      [-1, -1]
    );
  }
}
export {
  qf as BaseGallery,
  Gf as default
};
