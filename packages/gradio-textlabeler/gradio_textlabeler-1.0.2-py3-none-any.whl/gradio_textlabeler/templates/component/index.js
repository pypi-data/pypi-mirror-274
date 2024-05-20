const {
  SvelteComponent: st,
  assign: at,
  create_slot: _t,
  detach: rt,
  element: ut,
  get_all_dirty_from_scope: ct,
  get_slot_changes: dt,
  get_spread_update: mt,
  init: bt,
  insert: ht,
  safe_not_equal: gt,
  set_dynamic_element_data: ll,
  set_style: H,
  toggle_class: X,
  transition_in: Ol,
  transition_out: Pl,
  update_slot_base: wt
} = window.__gradio__svelte__internal;
function kt(n) {
  let e, l, t;
  const i = (
    /*#slots*/
    n[18].default
  ), f = _t(
    i,
    n,
    /*$$scope*/
    n[17],
    null
  );
  let o = [
    { "data-testid": (
      /*test_id*/
      n[7]
    ) },
    { id: (
      /*elem_id*/
      n[2]
    ) },
    {
      class: l = "block " + /*elem_classes*/
      n[3].join(" ") + " svelte-nl1om8"
    }
  ], a = {};
  for (let s = 0; s < o.length; s += 1)
    a = at(a, o[s]);
  return {
    c() {
      e = ut(
        /*tag*/
        n[14]
      ), f && f.c(), ll(
        /*tag*/
        n[14]
      )(e, a), X(
        e,
        "hidden",
        /*visible*/
        n[10] === !1
      ), X(
        e,
        "padded",
        /*padding*/
        n[6]
      ), X(
        e,
        "border_focus",
        /*border_mode*/
        n[5] === "focus"
      ), X(
        e,
        "border_contrast",
        /*border_mode*/
        n[5] === "contrast"
      ), X(e, "hide-container", !/*explicit_call*/
      n[8] && !/*container*/
      n[9]), H(
        e,
        "height",
        /*get_dimension*/
        n[15](
          /*height*/
          n[0]
        )
      ), H(e, "width", typeof /*width*/
      n[1] == "number" ? `calc(min(${/*width*/
      n[1]}px, 100%))` : (
        /*get_dimension*/
        n[15](
          /*width*/
          n[1]
        )
      )), H(
        e,
        "border-style",
        /*variant*/
        n[4]
      ), H(
        e,
        "overflow",
        /*allow_overflow*/
        n[11] ? "visible" : "hidden"
      ), H(
        e,
        "flex-grow",
        /*scale*/
        n[12]
      ), H(e, "min-width", `calc(min(${/*min_width*/
      n[13]}px, 100%))`), H(e, "border-width", "var(--block-border-width)");
    },
    m(s, _) {
      ht(s, e, _), f && f.m(e, null), t = !0;
    },
    p(s, _) {
      f && f.p && (!t || _ & /*$$scope*/
      131072) && wt(
        f,
        i,
        s,
        /*$$scope*/
        s[17],
        t ? dt(
          i,
          /*$$scope*/
          s[17],
          _,
          null
        ) : ct(
          /*$$scope*/
          s[17]
        ),
        null
      ), ll(
        /*tag*/
        s[14]
      )(e, a = mt(o, [
        (!t || _ & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          s[7]
        ) },
        (!t || _ & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          s[2]
        ) },
        (!t || _ & /*elem_classes*/
        8 && l !== (l = "block " + /*elem_classes*/
        s[3].join(" ") + " svelte-nl1om8")) && { class: l }
      ])), X(
        e,
        "hidden",
        /*visible*/
        s[10] === !1
      ), X(
        e,
        "padded",
        /*padding*/
        s[6]
      ), X(
        e,
        "border_focus",
        /*border_mode*/
        s[5] === "focus"
      ), X(
        e,
        "border_contrast",
        /*border_mode*/
        s[5] === "contrast"
      ), X(e, "hide-container", !/*explicit_call*/
      s[8] && !/*container*/
      s[9]), _ & /*height*/
      1 && H(
        e,
        "height",
        /*get_dimension*/
        s[15](
          /*height*/
          s[0]
        )
      ), _ & /*width*/
      2 && H(e, "width", typeof /*width*/
      s[1] == "number" ? `calc(min(${/*width*/
      s[1]}px, 100%))` : (
        /*get_dimension*/
        s[15](
          /*width*/
          s[1]
        )
      )), _ & /*variant*/
      16 && H(
        e,
        "border-style",
        /*variant*/
        s[4]
      ), _ & /*allow_overflow*/
      2048 && H(
        e,
        "overflow",
        /*allow_overflow*/
        s[11] ? "visible" : "hidden"
      ), _ & /*scale*/
      4096 && H(
        e,
        "flex-grow",
        /*scale*/
        s[12]
      ), _ & /*min_width*/
      8192 && H(e, "min-width", `calc(min(${/*min_width*/
      s[13]}px, 100%))`);
    },
    i(s) {
      t || (Ol(f, s), t = !0);
    },
    o(s) {
      Pl(f, s), t = !1;
    },
    d(s) {
      s && rt(e), f && f.d(s);
    }
  };
}
function vt(n) {
  let e, l = (
    /*tag*/
    n[14] && kt(n)
  );
  return {
    c() {
      l && l.c();
    },
    m(t, i) {
      l && l.m(t, i), e = !0;
    },
    p(t, [i]) {
      /*tag*/
      t[14] && l.p(t, i);
    },
    i(t) {
      e || (Ol(l, t), e = !0);
    },
    o(t) {
      Pl(l, t), e = !1;
    },
    d(t) {
      l && l.d(t);
    }
  };
}
function pt(n, e, l) {
  let { $$slots: t = {}, $$scope: i } = e, { height: f = void 0 } = e, { width: o = void 0 } = e, { elem_id: a = "" } = e, { elem_classes: s = [] } = e, { variant: _ = "solid" } = e, { border_mode: r = "base" } = e, { padding: u = !0 } = e, { type: c = "normal" } = e, { test_id: d = void 0 } = e, { explicit_call: m = !1 } = e, { container: w = !0 } = e, { visible: C = !0 } = e, { allow_overflow: S = !0 } = e, { scale: b = null } = e, { min_width: h = 0 } = e, q = c === "fieldset" ? "fieldset" : "div";
  const N = (v) => {
    if (v !== void 0) {
      if (typeof v == "number")
        return v + "px";
      if (typeof v == "string")
        return v;
    }
  };
  return n.$$set = (v) => {
    "height" in v && l(0, f = v.height), "width" in v && l(1, o = v.width), "elem_id" in v && l(2, a = v.elem_id), "elem_classes" in v && l(3, s = v.elem_classes), "variant" in v && l(4, _ = v.variant), "border_mode" in v && l(5, r = v.border_mode), "padding" in v && l(6, u = v.padding), "type" in v && l(16, c = v.type), "test_id" in v && l(7, d = v.test_id), "explicit_call" in v && l(8, m = v.explicit_call), "container" in v && l(9, w = v.container), "visible" in v && l(10, C = v.visible), "allow_overflow" in v && l(11, S = v.allow_overflow), "scale" in v && l(12, b = v.scale), "min_width" in v && l(13, h = v.min_width), "$$scope" in v && l(17, i = v.$$scope);
  }, [
    f,
    o,
    a,
    s,
    _,
    r,
    u,
    d,
    m,
    w,
    C,
    S,
    b,
    h,
    q,
    N,
    c,
    i,
    t
  ];
}
class yt extends st {
  constructor(e) {
    super(), bt(this, e, pt, vt, gt, {
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
  SvelteComponent: Ct,
  attr: qt,
  create_slot: Lt,
  detach: St,
  element: Ft,
  get_all_dirty_from_scope: Vt,
  get_slot_changes: Nt,
  init: zt,
  insert: Mt,
  safe_not_equal: Ht,
  transition_in: Dt,
  transition_out: It,
  update_slot_base: Zt
} = window.__gradio__svelte__internal;
function jt(n) {
  let e, l;
  const t = (
    /*#slots*/
    n[1].default
  ), i = Lt(
    t,
    n,
    /*$$scope*/
    n[0],
    null
  );
  return {
    c() {
      e = Ft("div"), i && i.c(), qt(e, "class", "svelte-1hnfib2");
    },
    m(f, o) {
      Mt(f, e, o), i && i.m(e, null), l = !0;
    },
    p(f, [o]) {
      i && i.p && (!l || o & /*$$scope*/
      1) && Zt(
        i,
        t,
        f,
        /*$$scope*/
        f[0],
        l ? Nt(
          t,
          /*$$scope*/
          f[0],
          o,
          null
        ) : Vt(
          /*$$scope*/
          f[0]
        ),
        null
      );
    },
    i(f) {
      l || (Dt(i, f), l = !0);
    },
    o(f) {
      It(i, f), l = !1;
    },
    d(f) {
      f && St(e), i && i.d(f);
    }
  };
}
function Ot(n, e, l) {
  let { $$slots: t = {}, $$scope: i } = e;
  return n.$$set = (f) => {
    "$$scope" in f && l(0, i = f.$$scope);
  }, [i, t];
}
class Pt extends Ct {
  constructor(e) {
    super(), zt(this, e, Ot, jt, Ht, {});
  }
}
const {
  SvelteComponent: Bt,
  attr: tl,
  check_outros: Wt,
  create_component: At,
  create_slot: Tt,
  destroy_component: Et,
  detach: Le,
  element: Xt,
  empty: Yt,
  get_all_dirty_from_scope: Gt,
  get_slot_changes: Rt,
  group_outros: Jt,
  init: Kt,
  insert: Se,
  mount_component: Qt,
  safe_not_equal: Ut,
  set_data: xt,
  space: $t,
  text: en,
  toggle_class: se,
  transition_in: he,
  transition_out: Fe,
  update_slot_base: ln
} = window.__gradio__svelte__internal;
function nl(n) {
  let e, l;
  return e = new Pt({
    props: {
      $$slots: { default: [tn] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      At(e.$$.fragment);
    },
    m(t, i) {
      Qt(e, t, i), l = !0;
    },
    p(t, i) {
      const f = {};
      i & /*$$scope, info*/
      10 && (f.$$scope = { dirty: i, ctx: t }), e.$set(f);
    },
    i(t) {
      l || (he(e.$$.fragment, t), l = !0);
    },
    o(t) {
      Fe(e.$$.fragment, t), l = !1;
    },
    d(t) {
      Et(e, t);
    }
  };
}
function tn(n) {
  let e;
  return {
    c() {
      e = en(
        /*info*/
        n[1]
      );
    },
    m(l, t) {
      Se(l, e, t);
    },
    p(l, t) {
      t & /*info*/
      2 && xt(
        e,
        /*info*/
        l[1]
      );
    },
    d(l) {
      l && Le(e);
    }
  };
}
function nn(n) {
  let e, l, t, i;
  const f = (
    /*#slots*/
    n[2].default
  ), o = Tt(
    f,
    n,
    /*$$scope*/
    n[3],
    null
  );
  let a = (
    /*info*/
    n[1] && nl(n)
  );
  return {
    c() {
      e = Xt("span"), o && o.c(), l = $t(), a && a.c(), t = Yt(), tl(e, "data-testid", "block-info"), tl(e, "class", "svelte-22c38v"), se(e, "sr-only", !/*show_label*/
      n[0]), se(e, "hide", !/*show_label*/
      n[0]), se(
        e,
        "has-info",
        /*info*/
        n[1] != null
      );
    },
    m(s, _) {
      Se(s, e, _), o && o.m(e, null), Se(s, l, _), a && a.m(s, _), Se(s, t, _), i = !0;
    },
    p(s, [_]) {
      o && o.p && (!i || _ & /*$$scope*/
      8) && ln(
        o,
        f,
        s,
        /*$$scope*/
        s[3],
        i ? Rt(
          f,
          /*$$scope*/
          s[3],
          _,
          null
        ) : Gt(
          /*$$scope*/
          s[3]
        ),
        null
      ), (!i || _ & /*show_label*/
      1) && se(e, "sr-only", !/*show_label*/
      s[0]), (!i || _ & /*show_label*/
      1) && se(e, "hide", !/*show_label*/
      s[0]), (!i || _ & /*info*/
      2) && se(
        e,
        "has-info",
        /*info*/
        s[1] != null
      ), /*info*/
      s[1] ? a ? (a.p(s, _), _ & /*info*/
      2 && he(a, 1)) : (a = nl(s), a.c(), he(a, 1), a.m(t.parentNode, t)) : a && (Jt(), Fe(a, 1, 1, () => {
        a = null;
      }), Wt());
    },
    i(s) {
      i || (he(o, s), he(a), i = !0);
    },
    o(s) {
      Fe(o, s), Fe(a), i = !1;
    },
    d(s) {
      s && (Le(e), Le(l), Le(t)), o && o.d(s), a && a.d(s);
    }
  };
}
function fn(n, e, l) {
  let { $$slots: t = {}, $$scope: i } = e, { show_label: f = !0 } = e, { info: o = void 0 } = e;
  return n.$$set = (a) => {
    "show_label" in a && l(0, f = a.show_label), "info" in a && l(1, o = a.info), "$$scope" in a && l(3, i = a.$$scope);
  }, [f, o, t, i];
}
class on extends Bt {
  constructor(e) {
    super(), Kt(this, e, fn, nn, Ut, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: sn,
  append: We,
  attr: K,
  bubble: an,
  create_component: _n,
  destroy_component: rn,
  detach: Bl,
  element: Ae,
  init: un,
  insert: Wl,
  listen: cn,
  mount_component: dn,
  safe_not_equal: mn,
  set_data: bn,
  set_style: ae,
  space: hn,
  text: gn,
  toggle_class: z,
  transition_in: wn,
  transition_out: kn
} = window.__gradio__svelte__internal;
function il(n) {
  let e, l;
  return {
    c() {
      e = Ae("span"), l = gn(
        /*label*/
        n[1]
      ), K(e, "class", "svelte-1lrphxw");
    },
    m(t, i) {
      Wl(t, e, i), We(e, l);
    },
    p(t, i) {
      i & /*label*/
      2 && bn(
        l,
        /*label*/
        t[1]
      );
    },
    d(t) {
      t && Bl(e);
    }
  };
}
function vn(n) {
  let e, l, t, i, f, o, a, s = (
    /*show_label*/
    n[2] && il(n)
  );
  return i = new /*Icon*/
  n[0]({}), {
    c() {
      e = Ae("button"), s && s.c(), l = hn(), t = Ae("div"), _n(i.$$.fragment), K(t, "class", "svelte-1lrphxw"), z(
        t,
        "small",
        /*size*/
        n[4] === "small"
      ), z(
        t,
        "large",
        /*size*/
        n[4] === "large"
      ), z(
        t,
        "medium",
        /*size*/
        n[4] === "medium"
      ), e.disabled = /*disabled*/
      n[7], K(
        e,
        "aria-label",
        /*label*/
        n[1]
      ), K(
        e,
        "aria-haspopup",
        /*hasPopup*/
        n[8]
      ), K(
        e,
        "title",
        /*label*/
        n[1]
      ), K(e, "class", "svelte-1lrphxw"), z(
        e,
        "pending",
        /*pending*/
        n[3]
      ), z(
        e,
        "padded",
        /*padded*/
        n[5]
      ), z(
        e,
        "highlight",
        /*highlight*/
        n[6]
      ), z(
        e,
        "transparent",
        /*transparent*/
        n[9]
      ), ae(e, "color", !/*disabled*/
      n[7] && /*_color*/
      n[12] ? (
        /*_color*/
        n[12]
      ) : "var(--block-label-text-color)"), ae(e, "--bg-color", /*disabled*/
      n[7] ? "auto" : (
        /*background*/
        n[10]
      )), ae(
        e,
        "margin-left",
        /*offset*/
        n[11] + "px"
      );
    },
    m(_, r) {
      Wl(_, e, r), s && s.m(e, null), We(e, l), We(e, t), dn(i, t, null), f = !0, o || (a = cn(
        e,
        "click",
        /*click_handler*/
        n[14]
      ), o = !0);
    },
    p(_, [r]) {
      /*show_label*/
      _[2] ? s ? s.p(_, r) : (s = il(_), s.c(), s.m(e, l)) : s && (s.d(1), s = null), (!f || r & /*size*/
      16) && z(
        t,
        "small",
        /*size*/
        _[4] === "small"
      ), (!f || r & /*size*/
      16) && z(
        t,
        "large",
        /*size*/
        _[4] === "large"
      ), (!f || r & /*size*/
      16) && z(
        t,
        "medium",
        /*size*/
        _[4] === "medium"
      ), (!f || r & /*disabled*/
      128) && (e.disabled = /*disabled*/
      _[7]), (!f || r & /*label*/
      2) && K(
        e,
        "aria-label",
        /*label*/
        _[1]
      ), (!f || r & /*hasPopup*/
      256) && K(
        e,
        "aria-haspopup",
        /*hasPopup*/
        _[8]
      ), (!f || r & /*label*/
      2) && K(
        e,
        "title",
        /*label*/
        _[1]
      ), (!f || r & /*pending*/
      8) && z(
        e,
        "pending",
        /*pending*/
        _[3]
      ), (!f || r & /*padded*/
      32) && z(
        e,
        "padded",
        /*padded*/
        _[5]
      ), (!f || r & /*highlight*/
      64) && z(
        e,
        "highlight",
        /*highlight*/
        _[6]
      ), (!f || r & /*transparent*/
      512) && z(
        e,
        "transparent",
        /*transparent*/
        _[9]
      ), r & /*disabled, _color*/
      4224 && ae(e, "color", !/*disabled*/
      _[7] && /*_color*/
      _[12] ? (
        /*_color*/
        _[12]
      ) : "var(--block-label-text-color)"), r & /*disabled, background*/
      1152 && ae(e, "--bg-color", /*disabled*/
      _[7] ? "auto" : (
        /*background*/
        _[10]
      )), r & /*offset*/
      2048 && ae(
        e,
        "margin-left",
        /*offset*/
        _[11] + "px"
      );
    },
    i(_) {
      f || (wn(i.$$.fragment, _), f = !0);
    },
    o(_) {
      kn(i.$$.fragment, _), f = !1;
    },
    d(_) {
      _ && Bl(e), s && s.d(), rn(i), o = !1, a();
    }
  };
}
function pn(n, e, l) {
  let t, { Icon: i } = e, { label: f = "" } = e, { show_label: o = !1 } = e, { pending: a = !1 } = e, { size: s = "small" } = e, { padded: _ = !0 } = e, { highlight: r = !1 } = e, { disabled: u = !1 } = e, { hasPopup: c = !1 } = e, { color: d = "var(--block-label-text-color)" } = e, { transparent: m = !1 } = e, { background: w = "var(--background-fill-primary)" } = e, { offset: C = 0 } = e;
  function S(b) {
    an.call(this, n, b);
  }
  return n.$$set = (b) => {
    "Icon" in b && l(0, i = b.Icon), "label" in b && l(1, f = b.label), "show_label" in b && l(2, o = b.show_label), "pending" in b && l(3, a = b.pending), "size" in b && l(4, s = b.size), "padded" in b && l(5, _ = b.padded), "highlight" in b && l(6, r = b.highlight), "disabled" in b && l(7, u = b.disabled), "hasPopup" in b && l(8, c = b.hasPopup), "color" in b && l(13, d = b.color), "transparent" in b && l(9, m = b.transparent), "background" in b && l(10, w = b.background), "offset" in b && l(11, C = b.offset);
  }, n.$$.update = () => {
    n.$$.dirty & /*highlight, color*/
    8256 && l(12, t = r ? "var(--color-accent)" : d);
  }, [
    i,
    f,
    o,
    a,
    s,
    _,
    r,
    u,
    c,
    m,
    w,
    C,
    t,
    d,
    S
  ];
}
class yn extends sn {
  constructor(e) {
    super(), un(this, e, pn, vn, mn, {
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
  SvelteComponent: Cn,
  append: Oe,
  attr: j,
  detach: qn,
  init: Ln,
  insert: Sn,
  noop: Pe,
  safe_not_equal: Fn,
  set_style: Y,
  svg_element: ye
} = window.__gradio__svelte__internal;
function Vn(n) {
  let e, l, t, i;
  return {
    c() {
      e = ye("svg"), l = ye("g"), t = ye("path"), i = ye("path"), j(t, "d", "M18,6L6.087,17.913"), Y(t, "fill", "none"), Y(t, "fill-rule", "nonzero"), Y(t, "stroke-width", "2px"), j(l, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), j(i, "d", "M4.364,4.364L19.636,19.636"), Y(i, "fill", "none"), Y(i, "fill-rule", "nonzero"), Y(i, "stroke-width", "2px"), j(e, "width", "100%"), j(e, "height", "100%"), j(e, "viewBox", "0 0 24 24"), j(e, "version", "1.1"), j(e, "xmlns", "http://www.w3.org/2000/svg"), j(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), j(e, "xml:space", "preserve"), j(e, "stroke", "currentColor"), Y(e, "fill-rule", "evenodd"), Y(e, "clip-rule", "evenodd"), Y(e, "stroke-linecap", "round"), Y(e, "stroke-linejoin", "round");
    },
    m(f, o) {
      Sn(f, e, o), Oe(e, l), Oe(l, t), Oe(e, i);
    },
    p: Pe,
    i: Pe,
    o: Pe,
    d(f) {
      f && qn(e);
    }
  };
}
class Nn extends Cn {
  constructor(e) {
    super(), Ln(this, e, null, Vn, Fn, {});
  }
}
const zn = [
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
], fl = {
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
zn.reduce(
  (n, { color: e, primary: l, secondary: t }) => ({
    ...n,
    [e]: {
      primary: fl[e][l],
      secondary: fl[e][t]
    }
  }),
  {}
);
function re(n) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], l = 0;
  for (; n > 1e3 && l < e.length - 1; )
    n /= 1e3, l++;
  let t = e[l];
  return (Number.isInteger(n) ? n : n.toFixed(1)) + t;
}
function Ve() {
}
function Mn(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
const Al = typeof window < "u";
let ol = Al ? () => window.performance.now() : () => Date.now(), Tl = Al ? (n) => requestAnimationFrame(n) : Ve;
const ce = /* @__PURE__ */ new Set();
function El(n) {
  ce.forEach((e) => {
    e.c(n) || (ce.delete(e), e.f());
  }), ce.size !== 0 && Tl(El);
}
function Hn(n) {
  let e;
  return ce.size === 0 && Tl(El), {
    promise: new Promise((l) => {
      ce.add(e = { c: n, f: l });
    }),
    abort() {
      ce.delete(e);
    }
  };
}
const _e = [];
function Dn(n, e = Ve) {
  let l;
  const t = /* @__PURE__ */ new Set();
  function i(a) {
    if (Mn(n, a) && (n = a, l)) {
      const s = !_e.length;
      for (const _ of t)
        _[1](), _e.push(_, n);
      if (s) {
        for (let _ = 0; _ < _e.length; _ += 2)
          _e[_][0](_e[_ + 1]);
        _e.length = 0;
      }
    }
  }
  function f(a) {
    i(a(n));
  }
  function o(a, s = Ve) {
    const _ = [a, s];
    return t.add(_), t.size === 1 && (l = e(i, f) || Ve), a(n), () => {
      t.delete(_), t.size === 0 && l && (l(), l = null);
    };
  }
  return { set: i, update: f, subscribe: o };
}
function sl(n) {
  return Object.prototype.toString.call(n) === "[object Date]";
}
function Te(n, e, l, t) {
  if (typeof l == "number" || sl(l)) {
    const i = t - l, f = (l - e) / (n.dt || 1 / 60), o = n.opts.stiffness * i, a = n.opts.damping * f, s = (o - a) * n.inv_mass, _ = (f + s) * n.dt;
    return Math.abs(_) < n.opts.precision && Math.abs(i) < n.opts.precision ? t : (n.settled = !1, sl(l) ? new Date(l.getTime() + _) : l + _);
  } else {
    if (Array.isArray(l))
      return l.map(
        (i, f) => Te(n, e[f], l[f], t[f])
      );
    if (typeof l == "object") {
      const i = {};
      for (const f in l)
        i[f] = Te(n, e[f], l[f], t[f]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof l} values`);
  }
}
function al(n, e = {}) {
  const l = Dn(n), { stiffness: t = 0.15, damping: i = 0.8, precision: f = 0.01 } = e;
  let o, a, s, _ = n, r = n, u = 1, c = 0, d = !1;
  function m(C, S = {}) {
    r = C;
    const b = s = {};
    return n == null || S.hard || w.stiffness >= 1 && w.damping >= 1 ? (d = !0, o = ol(), _ = C, l.set(n = r), Promise.resolve()) : (S.soft && (c = 1 / ((S.soft === !0 ? 0.5 : +S.soft) * 60), u = 0), a || (o = ol(), d = !1, a = Hn((h) => {
      if (d)
        return d = !1, a = null, !1;
      u = Math.min(u + c, 1);
      const q = {
        inv_mass: u,
        opts: w,
        settled: !0,
        dt: (h - o) * 60 / 1e3
      }, N = Te(q, _, n, r);
      return o = h, _ = n, l.set(n = N), q.settled && (a = null), !q.settled;
    })), new Promise((h) => {
      a.promise.then(() => {
        b === s && h();
      });
    }));
  }
  const w = {
    set: m,
    update: (C, S) => m(C(r, n), S),
    subscribe: l.subscribe,
    stiffness: t,
    damping: i,
    precision: f
  };
  return w;
}
const {
  SvelteComponent: In,
  append: O,
  attr: L,
  component_subscribe: _l,
  detach: Zn,
  element: jn,
  init: On,
  insert: Pn,
  noop: rl,
  safe_not_equal: Bn,
  set_style: Ce,
  svg_element: P,
  toggle_class: ul
} = window.__gradio__svelte__internal, { onMount: Wn } = window.__gradio__svelte__internal;
function An(n) {
  let e, l, t, i, f, o, a, s, _, r, u, c;
  return {
    c() {
      e = jn("div"), l = P("svg"), t = P("g"), i = P("path"), f = P("path"), o = P("path"), a = P("path"), s = P("g"), _ = P("path"), r = P("path"), u = P("path"), c = P("path"), L(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), L(i, "fill", "#FF7C00"), L(i, "fill-opacity", "0.4"), L(i, "class", "svelte-43sxxs"), L(f, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), L(f, "fill", "#FF7C00"), L(f, "class", "svelte-43sxxs"), L(o, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), L(o, "fill", "#FF7C00"), L(o, "fill-opacity", "0.4"), L(o, "class", "svelte-43sxxs"), L(a, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), L(a, "fill", "#FF7C00"), L(a, "class", "svelte-43sxxs"), Ce(t, "transform", "translate(" + /*$top*/
      n[1][0] + "px, " + /*$top*/
      n[1][1] + "px)"), L(_, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), L(_, "fill", "#FF7C00"), L(_, "fill-opacity", "0.4"), L(_, "class", "svelte-43sxxs"), L(r, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), L(r, "fill", "#FF7C00"), L(r, "class", "svelte-43sxxs"), L(u, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), L(u, "fill", "#FF7C00"), L(u, "fill-opacity", "0.4"), L(u, "class", "svelte-43sxxs"), L(c, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), L(c, "fill", "#FF7C00"), L(c, "class", "svelte-43sxxs"), Ce(s, "transform", "translate(" + /*$bottom*/
      n[2][0] + "px, " + /*$bottom*/
      n[2][1] + "px)"), L(l, "viewBox", "-1200 -1200 3000 3000"), L(l, "fill", "none"), L(l, "xmlns", "http://www.w3.org/2000/svg"), L(l, "class", "svelte-43sxxs"), L(e, "class", "svelte-43sxxs"), ul(
        e,
        "margin",
        /*margin*/
        n[0]
      );
    },
    m(d, m) {
      Pn(d, e, m), O(e, l), O(l, t), O(t, i), O(t, f), O(t, o), O(t, a), O(l, s), O(s, _), O(s, r), O(s, u), O(s, c);
    },
    p(d, [m]) {
      m & /*$top*/
      2 && Ce(t, "transform", "translate(" + /*$top*/
      d[1][0] + "px, " + /*$top*/
      d[1][1] + "px)"), m & /*$bottom*/
      4 && Ce(s, "transform", "translate(" + /*$bottom*/
      d[2][0] + "px, " + /*$bottom*/
      d[2][1] + "px)"), m & /*margin*/
      1 && ul(
        e,
        "margin",
        /*margin*/
        d[0]
      );
    },
    i: rl,
    o: rl,
    d(d) {
      d && Zn(e);
    }
  };
}
function Tn(n, e, l) {
  let t, i;
  var f = this && this.__awaiter || function(d, m, w, C) {
    function S(b) {
      return b instanceof w ? b : new w(function(h) {
        h(b);
      });
    }
    return new (w || (w = Promise))(function(b, h) {
      function q(g) {
        try {
          v(C.next(g));
        } catch (J) {
          h(J);
        }
      }
      function N(g) {
        try {
          v(C.throw(g));
        } catch (J) {
          h(J);
        }
      }
      function v(g) {
        g.done ? b(g.value) : S(g.value).then(q, N);
      }
      v((C = C.apply(d, m || [])).next());
    });
  };
  let { margin: o = !0 } = e;
  const a = al([0, 0]);
  _l(n, a, (d) => l(1, t = d));
  const s = al([0, 0]);
  _l(n, s, (d) => l(2, i = d));
  let _;
  function r() {
    return f(this, void 0, void 0, function* () {
      yield Promise.all([a.set([125, 140]), s.set([-125, -140])]), yield Promise.all([a.set([-125, 140]), s.set([125, -140])]), yield Promise.all([a.set([-125, 0]), s.set([125, -0])]), yield Promise.all([a.set([125, 0]), s.set([-125, 0])]);
    });
  }
  function u() {
    return f(this, void 0, void 0, function* () {
      yield r(), _ || u();
    });
  }
  function c() {
    return f(this, void 0, void 0, function* () {
      yield Promise.all([a.set([125, 0]), s.set([-125, 0])]), u();
    });
  }
  return Wn(() => (c(), () => _ = !0)), n.$$set = (d) => {
    "margin" in d && l(0, o = d.margin);
  }, [o, t, i, a, s];
}
class En extends In {
  constructor(e) {
    super(), On(this, e, Tn, An, Bn, { margin: 0 });
  }
}
const {
  SvelteComponent: Xn,
  append: te,
  attr: A,
  binding_callbacks: cl,
  check_outros: Ee,
  create_component: Xl,
  create_slot: Yl,
  destroy_component: Gl,
  destroy_each: Rl,
  detach: p,
  element: G,
  empty: de,
  ensure_array_like: Ne,
  get_all_dirty_from_scope: Jl,
  get_slot_changes: Kl,
  group_outros: Xe,
  init: Yn,
  insert: y,
  mount_component: Ql,
  noop: Ye,
  safe_not_equal: Gn,
  set_data: Z,
  set_style: U,
  space: I,
  text: F,
  toggle_class: D,
  transition_in: W,
  transition_out: R,
  update_slot_base: Ul
} = window.__gradio__svelte__internal, { tick: Rn } = window.__gradio__svelte__internal, { onDestroy: Jn } = window.__gradio__svelte__internal, { createEventDispatcher: Kn } = window.__gradio__svelte__internal, Qn = (n) => ({}), dl = (n) => ({}), Un = (n) => ({}), ml = (n) => ({});
function bl(n, e, l) {
  const t = n.slice();
  return t[41] = e[l], t[43] = l, t;
}
function hl(n, e, l) {
  const t = n.slice();
  return t[41] = e[l], t;
}
function xn(n) {
  let e, l, t, i, f = (
    /*i18n*/
    n[1]("common.error") + ""
  ), o, a, s;
  l = new yn({
    props: {
      Icon: Nn,
      label: (
        /*i18n*/
        n[1]("common.clear")
      ),
      disabled: !1
    }
  }), l.$on(
    "click",
    /*click_handler*/
    n[32]
  );
  const _ = (
    /*#slots*/
    n[30].error
  ), r = Yl(
    _,
    n,
    /*$$scope*/
    n[29],
    dl
  );
  return {
    c() {
      e = G("div"), Xl(l.$$.fragment), t = I(), i = G("span"), o = F(f), a = I(), r && r.c(), A(e, "class", "clear-status svelte-vopvsi"), A(i, "class", "error svelte-vopvsi");
    },
    m(u, c) {
      y(u, e, c), Ql(l, e, null), y(u, t, c), y(u, i, c), te(i, o), y(u, a, c), r && r.m(u, c), s = !0;
    },
    p(u, c) {
      const d = {};
      c[0] & /*i18n*/
      2 && (d.label = /*i18n*/
      u[1]("common.clear")), l.$set(d), (!s || c[0] & /*i18n*/
      2) && f !== (f = /*i18n*/
      u[1]("common.error") + "") && Z(o, f), r && r.p && (!s || c[0] & /*$$scope*/
      536870912) && Ul(
        r,
        _,
        u,
        /*$$scope*/
        u[29],
        s ? Kl(
          _,
          /*$$scope*/
          u[29],
          c,
          Qn
        ) : Jl(
          /*$$scope*/
          u[29]
        ),
        dl
      );
    },
    i(u) {
      s || (W(l.$$.fragment, u), W(r, u), s = !0);
    },
    o(u) {
      R(l.$$.fragment, u), R(r, u), s = !1;
    },
    d(u) {
      u && (p(e), p(t), p(i), p(a)), Gl(l), r && r.d(u);
    }
  };
}
function $n(n) {
  let e, l, t, i, f, o, a, s, _, r = (
    /*variant*/
    n[8] === "default" && /*show_eta_bar*/
    n[18] && /*show_progress*/
    n[6] === "full" && gl(n)
  );
  function u(h, q) {
    if (
      /*progress*/
      h[7]
    )
      return ti;
    if (
      /*queue_position*/
      h[2] !== null && /*queue_size*/
      h[3] !== void 0 && /*queue_position*/
      h[2] >= 0
    )
      return li;
    if (
      /*queue_position*/
      h[2] === 0
    )
      return ei;
  }
  let c = u(n), d = c && c(n), m = (
    /*timer*/
    n[5] && vl(n)
  );
  const w = [oi, fi], C = [];
  function S(h, q) {
    return (
      /*last_progress_level*/
      h[15] != null ? 0 : (
        /*show_progress*/
        h[6] === "full" ? 1 : -1
      )
    );
  }
  ~(f = S(n)) && (o = C[f] = w[f](n));
  let b = !/*timer*/
  n[5] && Fl(n);
  return {
    c() {
      r && r.c(), e = I(), l = G("div"), d && d.c(), t = I(), m && m.c(), i = I(), o && o.c(), a = I(), b && b.c(), s = de(), A(l, "class", "progress-text svelte-vopvsi"), D(
        l,
        "meta-text-center",
        /*variant*/
        n[8] === "center"
      ), D(
        l,
        "meta-text",
        /*variant*/
        n[8] === "default"
      );
    },
    m(h, q) {
      r && r.m(h, q), y(h, e, q), y(h, l, q), d && d.m(l, null), te(l, t), m && m.m(l, null), y(h, i, q), ~f && C[f].m(h, q), y(h, a, q), b && b.m(h, q), y(h, s, q), _ = !0;
    },
    p(h, q) {
      /*variant*/
      h[8] === "default" && /*show_eta_bar*/
      h[18] && /*show_progress*/
      h[6] === "full" ? r ? r.p(h, q) : (r = gl(h), r.c(), r.m(e.parentNode, e)) : r && (r.d(1), r = null), c === (c = u(h)) && d ? d.p(h, q) : (d && d.d(1), d = c && c(h), d && (d.c(), d.m(l, t))), /*timer*/
      h[5] ? m ? m.p(h, q) : (m = vl(h), m.c(), m.m(l, null)) : m && (m.d(1), m = null), (!_ || q[0] & /*variant*/
      256) && D(
        l,
        "meta-text-center",
        /*variant*/
        h[8] === "center"
      ), (!_ || q[0] & /*variant*/
      256) && D(
        l,
        "meta-text",
        /*variant*/
        h[8] === "default"
      );
      let N = f;
      f = S(h), f === N ? ~f && C[f].p(h, q) : (o && (Xe(), R(C[N], 1, 1, () => {
        C[N] = null;
      }), Ee()), ~f ? (o = C[f], o ? o.p(h, q) : (o = C[f] = w[f](h), o.c()), W(o, 1), o.m(a.parentNode, a)) : o = null), /*timer*/
      h[5] ? b && (Xe(), R(b, 1, 1, () => {
        b = null;
      }), Ee()) : b ? (b.p(h, q), q[0] & /*timer*/
      32 && W(b, 1)) : (b = Fl(h), b.c(), W(b, 1), b.m(s.parentNode, s));
    },
    i(h) {
      _ || (W(o), W(b), _ = !0);
    },
    o(h) {
      R(o), R(b), _ = !1;
    },
    d(h) {
      h && (p(e), p(l), p(i), p(a), p(s)), r && r.d(h), d && d.d(), m && m.d(), ~f && C[f].d(h), b && b.d(h);
    }
  };
}
function gl(n) {
  let e, l = `translateX(${/*eta_level*/
  (n[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = G("div"), A(e, "class", "eta-bar svelte-vopvsi"), U(e, "transform", l);
    },
    m(t, i) {
      y(t, e, i);
    },
    p(t, i) {
      i[0] & /*eta_level*/
      131072 && l !== (l = `translateX(${/*eta_level*/
      (t[17] || 0) * 100 - 100}%)`) && U(e, "transform", l);
    },
    d(t) {
      t && p(e);
    }
  };
}
function ei(n) {
  let e;
  return {
    c() {
      e = F("processing |");
    },
    m(l, t) {
      y(l, e, t);
    },
    p: Ye,
    d(l) {
      l && p(e);
    }
  };
}
function li(n) {
  let e, l = (
    /*queue_position*/
    n[2] + 1 + ""
  ), t, i, f, o;
  return {
    c() {
      e = F("queue: "), t = F(l), i = F("/"), f = F(
        /*queue_size*/
        n[3]
      ), o = F(" |");
    },
    m(a, s) {
      y(a, e, s), y(a, t, s), y(a, i, s), y(a, f, s), y(a, o, s);
    },
    p(a, s) {
      s[0] & /*queue_position*/
      4 && l !== (l = /*queue_position*/
      a[2] + 1 + "") && Z(t, l), s[0] & /*queue_size*/
      8 && Z(
        f,
        /*queue_size*/
        a[3]
      );
    },
    d(a) {
      a && (p(e), p(t), p(i), p(f), p(o));
    }
  };
}
function ti(n) {
  let e, l = Ne(
    /*progress*/
    n[7]
  ), t = [];
  for (let i = 0; i < l.length; i += 1)
    t[i] = kl(hl(n, l, i));
  return {
    c() {
      for (let i = 0; i < t.length; i += 1)
        t[i].c();
      e = de();
    },
    m(i, f) {
      for (let o = 0; o < t.length; o += 1)
        t[o] && t[o].m(i, f);
      y(i, e, f);
    },
    p(i, f) {
      if (f[0] & /*progress*/
      128) {
        l = Ne(
          /*progress*/
          i[7]
        );
        let o;
        for (o = 0; o < l.length; o += 1) {
          const a = hl(i, l, o);
          t[o] ? t[o].p(a, f) : (t[o] = kl(a), t[o].c(), t[o].m(e.parentNode, e));
        }
        for (; o < t.length; o += 1)
          t[o].d(1);
        t.length = l.length;
      }
    },
    d(i) {
      i && p(e), Rl(t, i);
    }
  };
}
function wl(n) {
  let e, l = (
    /*p*/
    n[41].unit + ""
  ), t, i, f = " ", o;
  function a(r, u) {
    return (
      /*p*/
      r[41].length != null ? ii : ni
    );
  }
  let s = a(n), _ = s(n);
  return {
    c() {
      _.c(), e = I(), t = F(l), i = F(" | "), o = F(f);
    },
    m(r, u) {
      _.m(r, u), y(r, e, u), y(r, t, u), y(r, i, u), y(r, o, u);
    },
    p(r, u) {
      s === (s = a(r)) && _ ? _.p(r, u) : (_.d(1), _ = s(r), _ && (_.c(), _.m(e.parentNode, e))), u[0] & /*progress*/
      128 && l !== (l = /*p*/
      r[41].unit + "") && Z(t, l);
    },
    d(r) {
      r && (p(e), p(t), p(i), p(o)), _.d(r);
    }
  };
}
function ni(n) {
  let e = re(
    /*p*/
    n[41].index || 0
  ) + "", l;
  return {
    c() {
      l = F(e);
    },
    m(t, i) {
      y(t, l, i);
    },
    p(t, i) {
      i[0] & /*progress*/
      128 && e !== (e = re(
        /*p*/
        t[41].index || 0
      ) + "") && Z(l, e);
    },
    d(t) {
      t && p(l);
    }
  };
}
function ii(n) {
  let e = re(
    /*p*/
    n[41].index || 0
  ) + "", l, t, i = re(
    /*p*/
    n[41].length
  ) + "", f;
  return {
    c() {
      l = F(e), t = F("/"), f = F(i);
    },
    m(o, a) {
      y(o, l, a), y(o, t, a), y(o, f, a);
    },
    p(o, a) {
      a[0] & /*progress*/
      128 && e !== (e = re(
        /*p*/
        o[41].index || 0
      ) + "") && Z(l, e), a[0] & /*progress*/
      128 && i !== (i = re(
        /*p*/
        o[41].length
      ) + "") && Z(f, i);
    },
    d(o) {
      o && (p(l), p(t), p(f));
    }
  };
}
function kl(n) {
  let e, l = (
    /*p*/
    n[41].index != null && wl(n)
  );
  return {
    c() {
      l && l.c(), e = de();
    },
    m(t, i) {
      l && l.m(t, i), y(t, e, i);
    },
    p(t, i) {
      /*p*/
      t[41].index != null ? l ? l.p(t, i) : (l = wl(t), l.c(), l.m(e.parentNode, e)) : l && (l.d(1), l = null);
    },
    d(t) {
      t && p(e), l && l.d(t);
    }
  };
}
function vl(n) {
  let e, l = (
    /*eta*/
    n[0] ? `/${/*formatted_eta*/
    n[19]}` : ""
  ), t, i;
  return {
    c() {
      e = F(
        /*formatted_timer*/
        n[20]
      ), t = F(l), i = F("s");
    },
    m(f, o) {
      y(f, e, o), y(f, t, o), y(f, i, o);
    },
    p(f, o) {
      o[0] & /*formatted_timer*/
      1048576 && Z(
        e,
        /*formatted_timer*/
        f[20]
      ), o[0] & /*eta, formatted_eta*/
      524289 && l !== (l = /*eta*/
      f[0] ? `/${/*formatted_eta*/
      f[19]}` : "") && Z(t, l);
    },
    d(f) {
      f && (p(e), p(t), p(i));
    }
  };
}
function fi(n) {
  let e, l;
  return e = new En({
    props: { margin: (
      /*variant*/
      n[8] === "default"
    ) }
  }), {
    c() {
      Xl(e.$$.fragment);
    },
    m(t, i) {
      Ql(e, t, i), l = !0;
    },
    p(t, i) {
      const f = {};
      i[0] & /*variant*/
      256 && (f.margin = /*variant*/
      t[8] === "default"), e.$set(f);
    },
    i(t) {
      l || (W(e.$$.fragment, t), l = !0);
    },
    o(t) {
      R(e.$$.fragment, t), l = !1;
    },
    d(t) {
      Gl(e, t);
    }
  };
}
function oi(n) {
  let e, l, t, i, f, o = `${/*last_progress_level*/
  n[15] * 100}%`, a = (
    /*progress*/
    n[7] != null && pl(n)
  );
  return {
    c() {
      e = G("div"), l = G("div"), a && a.c(), t = I(), i = G("div"), f = G("div"), A(l, "class", "progress-level-inner svelte-vopvsi"), A(f, "class", "progress-bar svelte-vopvsi"), U(f, "width", o), A(i, "class", "progress-bar-wrap svelte-vopvsi"), A(e, "class", "progress-level svelte-vopvsi");
    },
    m(s, _) {
      y(s, e, _), te(e, l), a && a.m(l, null), te(e, t), te(e, i), te(i, f), n[31](f);
    },
    p(s, _) {
      /*progress*/
      s[7] != null ? a ? a.p(s, _) : (a = pl(s), a.c(), a.m(l, null)) : a && (a.d(1), a = null), _[0] & /*last_progress_level*/
      32768 && o !== (o = `${/*last_progress_level*/
      s[15] * 100}%`) && U(f, "width", o);
    },
    i: Ye,
    o: Ye,
    d(s) {
      s && p(e), a && a.d(), n[31](null);
    }
  };
}
function pl(n) {
  let e, l = Ne(
    /*progress*/
    n[7]
  ), t = [];
  for (let i = 0; i < l.length; i += 1)
    t[i] = Sl(bl(n, l, i));
  return {
    c() {
      for (let i = 0; i < t.length; i += 1)
        t[i].c();
      e = de();
    },
    m(i, f) {
      for (let o = 0; o < t.length; o += 1)
        t[o] && t[o].m(i, f);
      y(i, e, f);
    },
    p(i, f) {
      if (f[0] & /*progress_level, progress*/
      16512) {
        l = Ne(
          /*progress*/
          i[7]
        );
        let o;
        for (o = 0; o < l.length; o += 1) {
          const a = bl(i, l, o);
          t[o] ? t[o].p(a, f) : (t[o] = Sl(a), t[o].c(), t[o].m(e.parentNode, e));
        }
        for (; o < t.length; o += 1)
          t[o].d(1);
        t.length = l.length;
      }
    },
    d(i) {
      i && p(e), Rl(t, i);
    }
  };
}
function yl(n) {
  let e, l, t, i, f = (
    /*i*/
    n[43] !== 0 && si()
  ), o = (
    /*p*/
    n[41].desc != null && Cl(n)
  ), a = (
    /*p*/
    n[41].desc != null && /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[43]
    ] != null && ql()
  ), s = (
    /*progress_level*/
    n[14] != null && Ll(n)
  );
  return {
    c() {
      f && f.c(), e = I(), o && o.c(), l = I(), a && a.c(), t = I(), s && s.c(), i = de();
    },
    m(_, r) {
      f && f.m(_, r), y(_, e, r), o && o.m(_, r), y(_, l, r), a && a.m(_, r), y(_, t, r), s && s.m(_, r), y(_, i, r);
    },
    p(_, r) {
      /*p*/
      _[41].desc != null ? o ? o.p(_, r) : (o = Cl(_), o.c(), o.m(l.parentNode, l)) : o && (o.d(1), o = null), /*p*/
      _[41].desc != null && /*progress_level*/
      _[14] && /*progress_level*/
      _[14][
        /*i*/
        _[43]
      ] != null ? a || (a = ql(), a.c(), a.m(t.parentNode, t)) : a && (a.d(1), a = null), /*progress_level*/
      _[14] != null ? s ? s.p(_, r) : (s = Ll(_), s.c(), s.m(i.parentNode, i)) : s && (s.d(1), s = null);
    },
    d(_) {
      _ && (p(e), p(l), p(t), p(i)), f && f.d(_), o && o.d(_), a && a.d(_), s && s.d(_);
    }
  };
}
function si(n) {
  let e;
  return {
    c() {
      e = F(" /");
    },
    m(l, t) {
      y(l, e, t);
    },
    d(l) {
      l && p(e);
    }
  };
}
function Cl(n) {
  let e = (
    /*p*/
    n[41].desc + ""
  ), l;
  return {
    c() {
      l = F(e);
    },
    m(t, i) {
      y(t, l, i);
    },
    p(t, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      t[41].desc + "") && Z(l, e);
    },
    d(t) {
      t && p(l);
    }
  };
}
function ql(n) {
  let e;
  return {
    c() {
      e = F("-");
    },
    m(l, t) {
      y(l, e, t);
    },
    d(l) {
      l && p(e);
    }
  };
}
function Ll(n) {
  let e = (100 * /*progress_level*/
  (n[14][
    /*i*/
    n[43]
  ] || 0)).toFixed(1) + "", l, t;
  return {
    c() {
      l = F(e), t = F("%");
    },
    m(i, f) {
      y(i, l, f), y(i, t, f);
    },
    p(i, f) {
      f[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[43]
      ] || 0)).toFixed(1) + "") && Z(l, e);
    },
    d(i) {
      i && (p(l), p(t));
    }
  };
}
function Sl(n) {
  let e, l = (
    /*p*/
    (n[41].desc != null || /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[43]
    ] != null) && yl(n)
  );
  return {
    c() {
      l && l.c(), e = de();
    },
    m(t, i) {
      l && l.m(t, i), y(t, e, i);
    },
    p(t, i) {
      /*p*/
      t[41].desc != null || /*progress_level*/
      t[14] && /*progress_level*/
      t[14][
        /*i*/
        t[43]
      ] != null ? l ? l.p(t, i) : (l = yl(t), l.c(), l.m(e.parentNode, e)) : l && (l.d(1), l = null);
    },
    d(t) {
      t && p(e), l && l.d(t);
    }
  };
}
function Fl(n) {
  let e, l, t, i;
  const f = (
    /*#slots*/
    n[30]["additional-loading-text"]
  ), o = Yl(
    f,
    n,
    /*$$scope*/
    n[29],
    ml
  );
  return {
    c() {
      e = G("p"), l = F(
        /*loading_text*/
        n[9]
      ), t = I(), o && o.c(), A(e, "class", "loading svelte-vopvsi");
    },
    m(a, s) {
      y(a, e, s), te(e, l), y(a, t, s), o && o.m(a, s), i = !0;
    },
    p(a, s) {
      (!i || s[0] & /*loading_text*/
      512) && Z(
        l,
        /*loading_text*/
        a[9]
      ), o && o.p && (!i || s[0] & /*$$scope*/
      536870912) && Ul(
        o,
        f,
        a,
        /*$$scope*/
        a[29],
        i ? Kl(
          f,
          /*$$scope*/
          a[29],
          s,
          Un
        ) : Jl(
          /*$$scope*/
          a[29]
        ),
        ml
      );
    },
    i(a) {
      i || (W(o, a), i = !0);
    },
    o(a) {
      R(o, a), i = !1;
    },
    d(a) {
      a && (p(e), p(t)), o && o.d(a);
    }
  };
}
function ai(n) {
  let e, l, t, i, f;
  const o = [$n, xn], a = [];
  function s(_, r) {
    return (
      /*status*/
      _[4] === "pending" ? 0 : (
        /*status*/
        _[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(l = s(n)) && (t = a[l] = o[l](n)), {
    c() {
      e = G("div"), t && t.c(), A(e, "class", i = "wrap " + /*variant*/
      n[8] + " " + /*show_progress*/
      n[6] + " svelte-vopvsi"), D(e, "hide", !/*status*/
      n[4] || /*status*/
      n[4] === "complete" || /*show_progress*/
      n[6] === "hidden"), D(
        e,
        "translucent",
        /*variant*/
        n[8] === "center" && /*status*/
        (n[4] === "pending" || /*status*/
        n[4] === "error") || /*translucent*/
        n[11] || /*show_progress*/
        n[6] === "minimal"
      ), D(
        e,
        "generating",
        /*status*/
        n[4] === "generating"
      ), D(
        e,
        "border",
        /*border*/
        n[12]
      ), U(
        e,
        "position",
        /*absolute*/
        n[10] ? "absolute" : "static"
      ), U(
        e,
        "padding",
        /*absolute*/
        n[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(_, r) {
      y(_, e, r), ~l && a[l].m(e, null), n[33](e), f = !0;
    },
    p(_, r) {
      let u = l;
      l = s(_), l === u ? ~l && a[l].p(_, r) : (t && (Xe(), R(a[u], 1, 1, () => {
        a[u] = null;
      }), Ee()), ~l ? (t = a[l], t ? t.p(_, r) : (t = a[l] = o[l](_), t.c()), W(t, 1), t.m(e, null)) : t = null), (!f || r[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      _[8] + " " + /*show_progress*/
      _[6] + " svelte-vopvsi")) && A(e, "class", i), (!f || r[0] & /*variant, show_progress, status, show_progress*/
      336) && D(e, "hide", !/*status*/
      _[4] || /*status*/
      _[4] === "complete" || /*show_progress*/
      _[6] === "hidden"), (!f || r[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && D(
        e,
        "translucent",
        /*variant*/
        _[8] === "center" && /*status*/
        (_[4] === "pending" || /*status*/
        _[4] === "error") || /*translucent*/
        _[11] || /*show_progress*/
        _[6] === "minimal"
      ), (!f || r[0] & /*variant, show_progress, status*/
      336) && D(
        e,
        "generating",
        /*status*/
        _[4] === "generating"
      ), (!f || r[0] & /*variant, show_progress, border*/
      4416) && D(
        e,
        "border",
        /*border*/
        _[12]
      ), r[0] & /*absolute*/
      1024 && U(
        e,
        "position",
        /*absolute*/
        _[10] ? "absolute" : "static"
      ), r[0] & /*absolute*/
      1024 && U(
        e,
        "padding",
        /*absolute*/
        _[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(_) {
      f || (W(t), f = !0);
    },
    o(_) {
      R(t), f = !1;
    },
    d(_) {
      _ && p(e), ~l && a[l].d(), n[33](null);
    }
  };
}
var _i = function(n, e, l, t) {
  function i(f) {
    return f instanceof l ? f : new l(function(o) {
      o(f);
    });
  }
  return new (l || (l = Promise))(function(f, o) {
    function a(r) {
      try {
        _(t.next(r));
      } catch (u) {
        o(u);
      }
    }
    function s(r) {
      try {
        _(t.throw(r));
      } catch (u) {
        o(u);
      }
    }
    function _(r) {
      r.done ? f(r.value) : i(r.value).then(a, s);
    }
    _((t = t.apply(n, e || [])).next());
  });
};
let qe = [], Be = !1;
function ri(n) {
  return _i(this, arguments, void 0, function* (e, l = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && l !== !0)) {
      if (qe.push(e), !Be)
        Be = !0;
      else
        return;
      yield Rn(), requestAnimationFrame(() => {
        let t = [0, 0];
        for (let i = 0; i < qe.length; i++) {
          const o = qe[i].getBoundingClientRect();
          (i === 0 || o.top + window.scrollY <= t[0]) && (t[0] = o.top + window.scrollY, t[1] = i);
        }
        window.scrollTo({ top: t[0] - 20, behavior: "smooth" }), Be = !1, qe = [];
      });
    }
  });
}
function ui(n, e, l) {
  let t, { $$slots: i = {}, $$scope: f } = e;
  this && this.__awaiter;
  const o = Kn();
  let { i18n: a } = e, { eta: s = null } = e, { queue_position: _ } = e, { queue_size: r } = e, { status: u } = e, { scroll_to_output: c = !1 } = e, { timer: d = !0 } = e, { show_progress: m = "full" } = e, { message: w = null } = e, { progress: C = null } = e, { variant: S = "default" } = e, { loading_text: b = "Loading..." } = e, { absolute: h = !0 } = e, { translucent: q = !1 } = e, { border: N = !1 } = e, { autoscroll: v } = e, g, J = !1, ge = 0, x = 0, fe = null, oe = null, Ue = 0, $ = null, me, Q = null, xe = !0;
  const $l = () => {
    l(0, s = l(27, fe = l(19, we = null))), l(25, ge = performance.now()), l(26, x = 0), J = !0, $e();
  };
  function $e() {
    requestAnimationFrame(() => {
      l(26, x = (performance.now() - ge) / 1e3), J && $e();
    });
  }
  function el() {
    l(26, x = 0), l(0, s = l(27, fe = l(19, we = null))), J && (J = !1);
  }
  Jn(() => {
    J && el();
  });
  let we = null;
  function et(k) {
    cl[k ? "unshift" : "push"](() => {
      Q = k, l(16, Q), l(7, C), l(14, $), l(15, me);
    });
  }
  const lt = () => {
    o("clear_status");
  };
  function tt(k) {
    cl[k ? "unshift" : "push"](() => {
      g = k, l(13, g);
    });
  }
  return n.$$set = (k) => {
    "i18n" in k && l(1, a = k.i18n), "eta" in k && l(0, s = k.eta), "queue_position" in k && l(2, _ = k.queue_position), "queue_size" in k && l(3, r = k.queue_size), "status" in k && l(4, u = k.status), "scroll_to_output" in k && l(22, c = k.scroll_to_output), "timer" in k && l(5, d = k.timer), "show_progress" in k && l(6, m = k.show_progress), "message" in k && l(23, w = k.message), "progress" in k && l(7, C = k.progress), "variant" in k && l(8, S = k.variant), "loading_text" in k && l(9, b = k.loading_text), "absolute" in k && l(10, h = k.absolute), "translucent" in k && l(11, q = k.translucent), "border" in k && l(12, N = k.border), "autoscroll" in k && l(24, v = k.autoscroll), "$$scope" in k && l(29, f = k.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (s === null && l(0, s = fe), s != null && fe !== s && (l(28, oe = (performance.now() - ge) / 1e3 + s), l(19, we = oe.toFixed(1)), l(27, fe = s))), n.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && l(17, Ue = oe === null || oe <= 0 || !x ? null : Math.min(x / oe, 1)), n.$$.dirty[0] & /*progress*/
    128 && C != null && l(18, xe = !1), n.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (C != null ? l(14, $ = C.map((k) => {
      if (k.index != null && k.length != null)
        return k.index / k.length;
      if (k.progress != null)
        return k.progress;
    })) : l(14, $ = null), $ ? (l(15, me = $[$.length - 1]), Q && (me === 0 ? l(16, Q.style.transition = "0", Q) : l(16, Q.style.transition = "150ms", Q))) : l(15, me = void 0)), n.$$.dirty[0] & /*status*/
    16 && (u === "pending" ? $l() : el()), n.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && g && c && (u === "pending" || u === "complete") && ri(g, v), n.$$.dirty[0] & /*status, message*/
    8388624, n.$$.dirty[0] & /*timer_diff*/
    67108864 && l(20, t = x.toFixed(1));
  }, [
    s,
    a,
    _,
    r,
    u,
    d,
    m,
    C,
    S,
    b,
    h,
    q,
    N,
    g,
    $,
    me,
    Q,
    Ue,
    xe,
    we,
    t,
    o,
    c,
    w,
    v,
    ge,
    x,
    fe,
    oe,
    f,
    i,
    et,
    lt,
    tt
  ];
}
class ci extends Xn {
  constructor(e) {
    super(), Yn(
      this,
      e,
      ui,
      ai,
      Gn,
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
  SvelteComponent: di,
  append: V,
  attr: B,
  destroy_each: xl,
  detach: T,
  element: M,
  empty: Qe,
  ensure_array_like: ze,
  init: mi,
  insert: E,
  listen: bi,
  noop: Vl,
  safe_not_equal: hi,
  select_option: Nl,
  set_data: ne,
  set_input_value: Ge,
  set_style: Re,
  space: Me,
  text: ie
} = window.__gradio__svelte__internal;
function zl(n, e, l) {
  const t = n.slice();
  return t[11] = e[l], t[13] = l, t;
}
function Ml(n, e, l) {
  const t = n.slice();
  return t[14] = e[l], t;
}
function gi(n) {
  let e, l, t, i, f, o, a, s, _, r, u = ze(
    /*value*/
    n[0]
  ), c = [];
  for (let d = 0; d < u.length; d += 1)
    c[d] = Il(zl(n, u, d));
  return {
    c() {
      e = M("table"), l = M("thead"), t = M("tr"), i = M("th"), f = ie(
        /*textColumnHeader*/
        n[5]
      ), o = Me(), a = M("th"), s = ie(
        /*labelColumnHeader*/
        n[7]
      ), _ = Me(), r = M("tbody");
      for (let d = 0; d < c.length; d += 1)
        c[d].c();
      B(i, "class", "svelte-1i7yt9n"), B(a, "class", "svelte-1i7yt9n"), B(t, "class", "svelte-1i7yt9n"), B(l, "class", "svelte-1i7yt9n"), B(r, "class", "svelte-1i7yt9n"), B(e, "width", "100%"), Re(e, "text-align", "left"), B(e, "class", "svelte-1i7yt9n");
    },
    m(d, m) {
      E(d, e, m), V(e, l), V(l, t), V(t, i), V(i, f), V(t, o), V(t, a), V(a, s), V(e, _), V(e, r);
      for (let w = 0; w < c.length; w += 1)
        c[w] && c[w].m(r, null);
    },
    p(d, m) {
      if (m & /*textColumnHeader*/
      32 && ne(
        f,
        /*textColumnHeader*/
        d[5]
      ), m & /*labelColumnHeader*/
      128 && ne(
        s,
        /*labelColumnHeader*/
        d[7]
      ), m & /*value, handleLabelChange, labels, onlySelectLabelOnce, selectedLabels, unlabelledValueDisplay, interactive, textColumnWidth*/
      863) {
        u = ze(
          /*value*/
          d[0]
        );
        let w;
        for (w = 0; w < u.length; w += 1) {
          const C = zl(d, u, w);
          c[w] ? c[w].p(C, m) : (c[w] = Il(C), c[w].c(), c[w].m(r, null));
        }
        for (; w < c.length; w += 1)
          c[w].d(1);
        c.length = u.length;
      }
    },
    d(d) {
      d && T(e), xl(c, d);
    }
  };
}
function wi(n) {
  let e;
  function l(f, o) {
    return (
      /*interactive*/
      f[2] ? Ci : yi
    );
  }
  let t = l(n), i = t(n);
  return {
    c() {
      i.c(), e = Qe();
    },
    m(f, o) {
      i.m(f, o), E(f, e, o);
    },
    p(f, o) {
      t !== (t = l(f)) && (i.d(1), i = t(f), i && (i.c(), i.m(e.parentNode, e)));
    },
    d(f) {
      f && T(e), i.d(f);
    }
  };
}
function ki(n) {
  let e = (
    /*valueItem*/
    n[11].label + ""
  ), l;
  return {
    c() {
      l = ie(e);
    },
    m(t, i) {
      E(t, l, i);
    },
    p(t, i) {
      i & /*value*/
      1 && e !== (e = /*valueItem*/
      t[11].label + "") && ne(l, e);
    },
    d(t) {
      t && T(l);
    }
  };
}
function vi(n) {
  let e;
  return {
    c() {
      e = ie(
        /*unlabelledValueDisplay*/
        n[4]
      );
    },
    m(l, t) {
      E(l, e, t);
    },
    p(l, t) {
      t & /*unlabelledValueDisplay*/
      16 && ne(
        e,
        /*unlabelledValueDisplay*/
        l[4]
      );
    },
    d(l) {
      l && T(e);
    }
  };
}
function pi(n) {
  let e, l, t, i, f, o, a = ze(
    /*labels*/
    n[3]
  ), s = [];
  for (let r = 0; r < a.length; r += 1)
    s[r] = Dl(Ml(n, a, r));
  function _(...r) {
    return (
      /*change_handler*/
      n[10](
        /*i*/
        n[13],
        ...r
      )
    );
  }
  return {
    c() {
      e = M("select"), l = M("option"), t = ie(
        /*unlabelledValueDisplay*/
        n[4]
      );
      for (let r = 0; r < s.length; r += 1)
        s[r].c();
      l.__value = "!!unlabeled", Ge(l, l.__value), B(e, "class", "svelte-1i7yt9n");
    },
    m(r, u) {
      E(r, e, u), V(e, l), V(l, t);
      for (let c = 0; c < s.length; c += 1)
        s[c] && s[c].m(e, null);
      Nl(
        e,
        /*valueItem*/
        n[11].label === null ? "!!unlabeled" : (
          /*valueItem*/
          n[11].label
        )
      ), f || (o = bi(e, "change", _), f = !0);
    },
    p(r, u) {
      if (n = r, u & /*unlabelledValueDisplay*/
      16 && ne(
        t,
        /*unlabelledValueDisplay*/
        n[4]
      ), u & /*labels, onlySelectLabelOnce, selectedLabels, value*/
      267) {
        a = ze(
          /*labels*/
          n[3]
        );
        let c;
        for (c = 0; c < a.length; c += 1) {
          const d = Ml(n, a, c);
          s[c] ? s[c].p(d, u) : (s[c] = Dl(d), s[c].c(), s[c].m(e, null));
        }
        for (; c < s.length; c += 1)
          s[c].d(1);
        s.length = a.length;
      }
      u & /*value, labels*/
      9 && i !== (i = /*valueItem*/
      n[11].label === null ? "!!unlabeled" : (
        /*valueItem*/
        n[11].label
      )) && Nl(
        e,
        /*valueItem*/
        n[11].label === null ? "!!unlabeled" : (
          /*valueItem*/
          n[11].label
        )
      );
    },
    d(r) {
      r && T(e), xl(s, r), f = !1, o();
    }
  };
}
function Hl(n) {
  let e, l = (
    /*label*/
    n[14] + ""
  ), t, i;
  return {
    c() {
      e = M("option"), t = ie(l), e.__value = i = /*label*/
      n[14], Ge(e, e.__value);
    },
    m(f, o) {
      E(f, e, o), V(e, t);
    },
    p(f, o) {
      o & /*labels*/
      8 && l !== (l = /*label*/
      f[14] + "") && ne(t, l), o & /*labels*/
      8 && i !== (i = /*label*/
      f[14]) && (e.__value = i, Ge(e, e.__value));
    },
    d(f) {
      f && T(e);
    }
  };
}
function Dl(n) {
  let e = !/*onlySelectLabelOnce*/
  n[1] || !/*selectedLabels*/
  n[8].has(
    /*label*/
    n[14]
  ) || /*label*/
  n[14] === /*valueItem*/
  n[11].label, l, t = e && Hl(n);
  return {
    c() {
      t && t.c(), l = Qe();
    },
    m(i, f) {
      t && t.m(i, f), E(i, l, f);
    },
    p(i, f) {
      f & /*onlySelectLabelOnce, selectedLabels, labels, value*/
      267 && (e = !/*onlySelectLabelOnce*/
      i[1] || !/*selectedLabels*/
      i[8].has(
        /*label*/
        i[14]
      ) || /*label*/
      i[14] === /*valueItem*/
      i[11].label), e ? t ? t.p(i, f) : (t = Hl(i), t.c(), t.m(l.parentNode, l)) : t && (t.d(1), t = null);
    },
    d(i) {
      i && T(l), t && t.d(i);
    }
  };
}
function Il(n) {
  let e, l, t = (
    /*valueItem*/
    n[11].text + ""
  ), i, f, o, a;
  function s(u, c) {
    return (
      /*interactive*/
      u[2] ? pi : (
        /*valueItem*/
        u[11].label === null ? vi : ki
      )
    );
  }
  let _ = s(n), r = _(n);
  return {
    c() {
      e = M("tr"), l = M("td"), i = ie(t), f = Me(), o = M("td"), r.c(), a = Me(), Re(
        l,
        "width",
        /*textColumnWidth*/
        n[6]
      ), B(l, "class", "svelte-1i7yt9n"), B(o, "class", "svelte-1i7yt9n"), B(e, "class", "svelte-1i7yt9n");
    },
    m(u, c) {
      E(u, e, c), V(e, l), V(l, i), V(e, f), V(e, o), r.m(o, null), V(e, a);
    },
    p(u, c) {
      c & /*value*/
      1 && t !== (t = /*valueItem*/
      u[11].text + "") && ne(i, t), c & /*textColumnWidth*/
      64 && Re(
        l,
        "width",
        /*textColumnWidth*/
        u[6]
      ), _ === (_ = s(u)) && r ? r.p(u, c) : (r.d(1), r = _(u), r && (r.c(), r.m(o, null)));
    },
    d(u) {
      u && T(e), r.d();
    }
  };
}
function yi(n) {
  let e;
  return {
    c() {
      e = M("p"), e.textContent = "No labeling data to show";
    },
    m(l, t) {
      E(l, e, t);
    },
    d(l) {
      l && T(e);
    }
  };
}
function Ci(n) {
  let e;
  return {
    c() {
      e = M("p"), e.textContent = "No data to label";
    },
    m(l, t) {
      E(l, e, t);
    },
    d(l) {
      l && T(e);
    }
  };
}
function qi(n) {
  let e;
  function l(f, o) {
    return (
      /*value*/
      f[0].length === 0 ? wi : gi
    );
  }
  let t = l(n), i = t(n);
  return {
    c() {
      i.c(), e = Qe();
    },
    m(f, o) {
      i.m(f, o), E(f, e, o);
    },
    p(f, [o]) {
      t === (t = l(f)) && i ? i.p(f, o) : (i.d(1), i = t(f), i && (i.c(), i.m(e.parentNode, e)));
    },
    i: Vl,
    o: Vl,
    d(f) {
      f && T(e), i.d(f);
    }
  };
}
function Li(n, e, l) {
  let { onlySelectLabelOnce: t = !1 } = e, { value: i } = e, { interactive: f = !1 } = e, { labels: o } = e, { unlabelledValueDisplay: a } = e, { textColumnHeader: s } = e, { textColumnWidth: _ } = e, { labelColumnHeader: r } = e, u = /* @__PURE__ */ new Set();
  function c(m, w) {
    let C = i[w].label, S = m.target.value === "!!unlabeled" ? null : m.target.value;
    t && (u.delete(C), u.add(S), l(8, u = new Set(u))), l(0, i = [
      ...i.slice(0, w),
      { ...i[w], label: S },
      ...i.slice(w + 1)
    ]);
  }
  const d = (m, w) => c(w, m);
  return n.$$set = (m) => {
    "onlySelectLabelOnce" in m && l(1, t = m.onlySelectLabelOnce), "value" in m && l(0, i = m.value), "interactive" in m && l(2, f = m.interactive), "labels" in m && l(3, o = m.labels), "unlabelledValueDisplay" in m && l(4, a = m.unlabelledValueDisplay), "textColumnHeader" in m && l(5, s = m.textColumnHeader), "textColumnWidth" in m && l(6, _ = m.textColumnWidth), "labelColumnHeader" in m && l(7, r = m.labelColumnHeader);
  }, n.$$.update = () => {
    n.$$.dirty & /*onlySelectLabelOnce, value*/
    3 && t && l(8, u = new Set(i.map((m) => m.label)));
  }, [
    i,
    t,
    f,
    o,
    a,
    s,
    _,
    r,
    u,
    c,
    d
  ];
}
class Si extends di {
  constructor(e) {
    super(), mi(this, e, Li, qi, hi, {
      onlySelectLabelOnce: 1,
      value: 0,
      interactive: 2,
      labels: 3,
      unlabelledValueDisplay: 4,
      textColumnHeader: 5,
      textColumnWidth: 6,
      labelColumnHeader: 7
    });
  }
}
const {
  SvelteComponent: Fi,
  add_flush_callback: Vi,
  assign: Ni,
  bind: zi,
  binding_callbacks: Mi,
  check_outros: Hi,
  create_component: He,
  destroy_component: De,
  detach: Je,
  get_spread_object: Di,
  get_spread_update: Ii,
  group_outros: Zi,
  init: ji,
  insert: Ke,
  mount_component: Ie,
  safe_not_equal: Oi,
  set_data: Pi,
  space: Zl,
  text: Bi,
  transition_in: le,
  transition_out: ue
} = window.__gradio__svelte__internal;
function jl(n) {
  let e, l;
  const t = [
    {
      autoscroll: (
        /*gradio*/
        n[15].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      n[15].i18n
    ) },
    /*loading_status*/
    n[14]
  ];
  let i = {};
  for (let f = 0; f < t.length; f += 1)
    i = Ni(i, t[f]);
  return e = new ci({ props: i }), e.$on(
    "clear_status",
    /*clear_status_handler*/
    n[17]
  ), {
    c() {
      He(e.$$.fragment);
    },
    m(f, o) {
      Ie(e, f, o), l = !0;
    },
    p(f, o) {
      const a = o & /*gradio, loading_status*/
      49152 ? Ii(t, [
        o & /*gradio*/
        32768 && {
          autoscroll: (
            /*gradio*/
            f[15].autoscroll
          )
        },
        o & /*gradio*/
        32768 && { i18n: (
          /*gradio*/
          f[15].i18n
        ) },
        o & /*loading_status*/
        16384 && Di(
          /*loading_status*/
          f[14]
        )
      ]) : {};
      e.$set(a);
    },
    i(f) {
      l || (le(e.$$.fragment, f), l = !0);
    },
    o(f) {
      ue(e.$$.fragment, f), l = !1;
    },
    d(f) {
      De(e, f);
    }
  };
}
function Wi(n) {
  let e;
  return {
    c() {
      e = Bi(
        /*label*/
        n[1]
      );
    },
    m(l, t) {
      Ke(l, e, t);
    },
    p(l, t) {
      t & /*label*/
      2 && Pi(
        e,
        /*label*/
        l[1]
      );
    },
    d(l) {
      l && Je(e);
    }
  };
}
function Ai(n) {
  let e, l, t, i, f, o, a = (
    /*loading_status*/
    n[14] && jl(n)
  );
  l = new on({
    props: {
      show_label: (
        /*show_label*/
        n[11]
      ),
      info: void 0,
      $$slots: { default: [Wi] },
      $$scope: { ctx: n }
    }
  });
  function s(r) {
    n[18](r);
  }
  let _ = {
    labels: (
      /*label_choices*/
      n[5]
    ),
    onlySelectLabelOnce: !/*allow_duplicate_labels*/
    n[7],
    textColumnHeader: (
      /*text_column_header*/
      n[9]
    ),
    textColumnWidth: (
      /*text_column_width*/
      n[6]
    ),
    labelColumnHeader: (
      /*label_column_header*/
      n[10]
    ),
    unlabelledValueDisplay: (
      /*unlabelled_value_display*/
      n[8]
    ),
    interactive: (
      /*interactive*/
      n[16]
    )
  };
  return (
    /*value*/
    n[0] !== void 0 && (_.value = /*value*/
    n[0]), i = new Si({ props: _ }), Mi.push(() => zi(i, "value", s)), {
      c() {
        a && a.c(), e = Zl(), He(l.$$.fragment), t = Zl(), He(i.$$.fragment);
      },
      m(r, u) {
        a && a.m(r, u), Ke(r, e, u), Ie(l, r, u), Ke(r, t, u), Ie(i, r, u), o = !0;
      },
      p(r, u) {
        /*loading_status*/
        r[14] ? a ? (a.p(r, u), u & /*loading_status*/
        16384 && le(a, 1)) : (a = jl(r), a.c(), le(a, 1), a.m(e.parentNode, e)) : a && (Zi(), ue(a, 1, 1, () => {
          a = null;
        }), Hi());
        const c = {};
        u & /*show_label*/
        2048 && (c.show_label = /*show_label*/
        r[11]), u & /*$$scope, label*/
        1048578 && (c.$$scope = { dirty: u, ctx: r }), l.$set(c);
        const d = {};
        u & /*label_choices*/
        32 && (d.labels = /*label_choices*/
        r[5]), u & /*allow_duplicate_labels*/
        128 && (d.onlySelectLabelOnce = !/*allow_duplicate_labels*/
        r[7]), u & /*text_column_header*/
        512 && (d.textColumnHeader = /*text_column_header*/
        r[9]), u & /*text_column_width*/
        64 && (d.textColumnWidth = /*text_column_width*/
        r[6]), u & /*label_column_header*/
        1024 && (d.labelColumnHeader = /*label_column_header*/
        r[10]), u & /*unlabelled_value_display*/
        256 && (d.unlabelledValueDisplay = /*unlabelled_value_display*/
        r[8]), u & /*interactive*/
        65536 && (d.interactive = /*interactive*/
        r[16]), !f && u & /*value*/
        1 && (f = !0, d.value = /*value*/
        r[0], Vi(() => f = !1)), i.$set(d);
      },
      i(r) {
        o || (le(a), le(l.$$.fragment, r), le(i.$$.fragment, r), o = !0);
      },
      o(r) {
        ue(a), ue(l.$$.fragment, r), ue(i.$$.fragment, r), o = !1;
      },
      d(r) {
        r && (Je(e), Je(t)), a && a.d(r), De(l, r), De(i, r);
      }
    }
  );
}
function Ti(n) {
  let e, l;
  return e = new yt({
    props: {
      visible: (
        /*visible*/
        n[4]
      ),
      elem_id: (
        /*elem_id*/
        n[2]
      ),
      elem_classes: (
        /*elem_classes*/
        n[3]
      ),
      padding: Ei,
      allow_overflow: !1,
      scale: (
        /*scale*/
        n[12]
      ),
      min_width: (
        /*min_width*/
        n[13]
      ),
      $$slots: { default: [Ai] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      He(e.$$.fragment);
    },
    m(t, i) {
      Ie(e, t, i), l = !0;
    },
    p(t, [i]) {
      const f = {};
      i & /*visible*/
      16 && (f.visible = /*visible*/
      t[4]), i & /*elem_id*/
      4 && (f.elem_id = /*elem_id*/
      t[2]), i & /*elem_classes*/
      8 && (f.elem_classes = /*elem_classes*/
      t[3]), i & /*scale*/
      4096 && (f.scale = /*scale*/
      t[12]), i & /*min_width*/
      8192 && (f.min_width = /*min_width*/
      t[13]), i & /*$$scope, label_choices, allow_duplicate_labels, text_column_header, text_column_width, label_column_header, unlabelled_value_display, interactive, value, show_label, label, gradio, loading_status*/
      1167331 && (f.$$scope = { dirty: i, ctx: t }), e.$set(f);
    },
    i(t) {
      l || (le(e.$$.fragment, t), l = !0);
    },
    o(t) {
      ue(e.$$.fragment, t), l = !1;
    },
    d(t) {
      De(e, t);
    }
  };
}
const Ei = !0;
function Xi(n, e, l) {
  let { label: t = "TextLabeler" } = e, { elem_id: i = "" } = e, { elem_classes: f = [] } = e, { visible: o = !0 } = e, { value: a } = e, { label_choices: s } = e, { text_column_width: _ } = e, { allow_duplicate_labels: r } = e, { unlabelled_value_display: u } = e, { text_column_header: c } = e, { label_column_header: d } = e, { show_label: m } = e, { scale: w = null } = e, { min_width: C = void 0 } = e, { loading_status: S } = e, { gradio: b } = e, { interactive: h } = e;
  function q() {
    b.dispatch("change");
  }
  const N = () => b.dispatch("clear_status", S);
  function v(g) {
    a = g, l(0, a);
  }
  return n.$$set = (g) => {
    "label" in g && l(1, t = g.label), "elem_id" in g && l(2, i = g.elem_id), "elem_classes" in g && l(3, f = g.elem_classes), "visible" in g && l(4, o = g.visible), "value" in g && l(0, a = g.value), "label_choices" in g && l(5, s = g.label_choices), "text_column_width" in g && l(6, _ = g.text_column_width), "allow_duplicate_labels" in g && l(7, r = g.allow_duplicate_labels), "unlabelled_value_display" in g && l(8, u = g.unlabelled_value_display), "text_column_header" in g && l(9, c = g.text_column_header), "label_column_header" in g && l(10, d = g.label_column_header), "show_label" in g && l(11, m = g.show_label), "scale" in g && l(12, w = g.scale), "min_width" in g && l(13, C = g.min_width), "loading_status" in g && l(14, S = g.loading_status), "gradio" in g && l(15, b = g.gradio), "interactive" in g && l(16, h = g.interactive);
  }, n.$$.update = () => {
    n.$$.dirty & /*value*/
    1 && q();
  }, [
    a,
    t,
    i,
    f,
    o,
    s,
    _,
    r,
    u,
    c,
    d,
    m,
    w,
    C,
    S,
    b,
    h,
    N,
    v
  ];
}
class Yi extends Fi {
  constructor(e) {
    super(), ji(this, e, Xi, Ti, Oi, {
      label: 1,
      elem_id: 2,
      elem_classes: 3,
      visible: 4,
      value: 0,
      label_choices: 5,
      text_column_width: 6,
      allow_duplicate_labels: 7,
      unlabelled_value_display: 8,
      text_column_header: 9,
      label_column_header: 10,
      show_label: 11,
      scale: 12,
      min_width: 13,
      loading_status: 14,
      gradio: 15,
      interactive: 16
    });
  }
}
export {
  Yi as default
};
