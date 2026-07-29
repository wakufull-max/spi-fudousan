/**
 * ============================================================
 *  fengshui-engine.js
 *  風水評価エンジン v2.0
 * ============================================================
 *
 *  設計方針
 *  --------
 *  1. 評価項目は「モジュール」として独立実装する。
 *     追加・削除・重み変更が他モジュールに影響しない。
 *
 *  2. 評価対象（Subject）は階層を問わず同じ形を取る。
 *       region → ward → town → address → building → unit
 *     モジュールは自分が必要とするデータと最小階層を宣言し、
 *     データが無ければ null を返して評価から自動的に外れる。
 *     外れた分の重みは残りのモジュールへ再配分され、
 *     「データ充足率（coverage）」として利用者に開示される。
 *
 *  3. すべてのモジュールは score だけでなく
 *     reason（なぜその評価か）と evidence（根拠データと出典）を返す。
 *     UI はこれをそのまま表示できる。
 *
 *  4. 居住者との相性（九星気学・四柱推命）は
 *     物件固有スコアには合算しない。別レイヤーとして計算し、
 *     必要なときだけ personalTotal として合成する。
 *     （物件固有スコアは誰が見ても同じ値である必要があるため）
 *
 *  スコアの意味
 *  ------------
 *    0–100。50 が中立。50 を上回れば加点要因、下回れば減点要因。
 *    impact = (score - 50) × 実効重み  → 強み / 弱みの判定に使う。
 * ============================================================
 */
(function (global) {
  "use strict";

  /* ══════════════════════════════════════════════════════════
     0. ユーティリティ
     ══════════════════════════════════════════════════════════ */
  const clamp = (x, lo = 0, hi = 100) => Math.max(lo, Math.min(hi, x));
  const round1 = x => Math.round(x * 10) / 10;
  const get = (obj, path) =>
    path.split(".").reduce((o, k) => (o == null ? undefined : o[k]), obj);

  const LEVELS = ["region", "ward", "town", "address", "building", "unit"];
  const LEVEL_JP = {
    region: "地方", ward: "区市", town: "町丁目",
    address: "地番", building: "建物", unit: "住戸"
  };
  const levelIdx = l => LEVELS.indexOf(l);

  /* ══════════════════════════════════════════════════════════
     1. 暦エンジン（四柱推命・九星気学の基盤）
     ══════════════════════════════════════════════════════════ */
  const D2R = Math.PI / 180;
  const mod360 = x => ((x % 360) + 360) % 360;

  function toJD(y, m, d, h = 0) {
    if (m <= 2) { y -= 1; m += 12; }
    const A = Math.floor(y / 100), B = 2 - A + Math.floor(A / 4);
    return Math.floor(365.25 * (y + 4716)) + Math.floor(30.6001 * (m + 1))
         + d + B - 1524.5 + h / 24;
  }
  function toJDN(y, m, d) {
    const a = Math.floor((14 - m) / 12), yy = y + 4800 - a, mm = m + 12 * a - 3;
    return d + Math.floor((153 * mm + 2) / 5) + 365 * yy
         + Math.floor(yy / 4) - Math.floor(yy / 100) + Math.floor(yy / 400) - 32045;
  }
  /** 見かけの太陽黄経（Meeus 簡略式・誤差約0.01°≒15分） */
  function solarLon(jd) {
    const T = (jd - 2451545) / 36525;
    const L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T * T;
    const M = (357.52911 + 35999.05029 * T - 0.0001537 * T * T) * D2R;
    const C = (1.914602 - 0.004817 * T - 0.000014 * T * T) * Math.sin(M)
            + (0.019993 - 0.000101 * T) * Math.sin(2 * M)
            + 0.000289 * Math.sin(3 * M);
    const om = (125.04 - 1934.136 * T) * D2R;
    return mod360(L0 + C - 0.00569 - 0.00478 * Math.sin(om));
  }
  /** 均時差（分） */
  function eqTime(jd) {
    const T = (jd - 2451545) / 36525;
    const eps = (23.439291 - 0.0130042 * T) * D2R;
    const L0 = mod360(280.46646 + 36000.76983 * T) * D2R;
    const M = (357.52911 + 35999.05029 * T) * D2R;
    const e = 0.016708634 - 0.000042037 * T;
    const y = Math.pow(Math.tan(eps / 2), 2);
    const E = y * Math.sin(2 * L0) - 2 * e * Math.sin(M)
            + 4 * e * y * Math.sin(M) * Math.cos(2 * L0)
            - 0.5 * y * y * Math.sin(4 * L0) - 1.25 * e * e * Math.sin(2 * M);
    return (E / D2R) * 4;
  }
  /** 指定黄経に達する瞬間（JD, UT）を二分探索 */
  function termJD(year, target, guessMonth) {
    let lo = toJD(year, guessMonth, 1) - 3, hi = toJD(year, guessMonth, 28) + 3;
    const f = jd => { const d = solarLon(jd) - target; return ((d + 180) % 360 + 360) % 360 - 180; };
    for (let i = 0; i < 60; i++) { const m = (lo + hi) / 2; if (f(m) < 0) lo = m; else hi = m; }
    return (lo + hi) / 2;
  }
  function jdToParts(jd) {
    const z = Math.floor(jd + 0.5), f = jd + 0.5 - z;
    let a = z;
    if (z >= 2299161) { const al = Math.floor((z - 1867216.25) / 36524.25); a = z + 1 + al - Math.floor(al / 4); }
    const b = a + 1524, c = Math.floor((b - 122.1) / 365.25),
          d = Math.floor(365.25 * c), e = Math.floor((b - d) / 30.6001);
    const day = b - d - Math.floor(30.6001 * e) + f;
    const mo = e < 14 ? e - 1 : e - 13, yr = mo > 2 ? c - 4716 : c - 4715;
    const dd = Math.floor(day), hr = (day - dd) * 24;
    return { y: yr, m: mo, d: dd, h: Math.floor(hr), mi: Math.round((hr - Math.floor(hr)) * 60) };
  }

  /** 12の「節」。中気は含めない（月柱は節で切り替わる） */
  const SEKKI = [
    { lon: 285, cm: 1,  branch: 1,  name: "小寒" },
    { lon: 315, cm: 2,  branch: 2,  name: "立春" },
    { lon: 345, cm: 3,  branch: 3,  name: "啓蟄" },
    { lon: 15,  cm: 4,  branch: 4,  name: "清明" },
    { lon: 45,  cm: 5,  branch: 5,  name: "立夏" },
    { lon: 75,  cm: 6,  branch: 6,  name: "芒種" },
    { lon: 105, cm: 7,  branch: 7,  name: "小暑" },
    { lon: 135, cm: 8,  branch: 8,  name: "立秋" },
    { lon: 165, cm: 9,  branch: 9,  name: "白露" },
    { lon: 195, cm: 10, branch: 10, name: "寒露" },
    { lon: 225, cm: 11, branch: 11, name: "立冬" },
    { lon: 255, cm: 12, branch: 0,  name: "大雪" }
  ];
  const STEM = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"];
  const BRANCH = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"];
  const STEM_EL = ["木","木","火","火","土","土","金","金","水","水"];
  const BRANCH_EL = ["水","土","木","木","土","火","火","土","金","金","土","水"];
  const STEM_YIN = [0,1,0,1,0,1,0,1,0,1];  // 0=陽 1=陰

  const SHENG = { 木:"火", 火:"土", 土:"金", 金:"水", 水:"木" }; // 生
  const KE    = { 木:"土", 土:"水", 水:"火", 火:"金", 金:"木" }; // 剋
  const SHENG_FROM = { 火:"木", 土:"火", 金:"土", 水:"金", 木:"水" };
  const KE_FROM    = { 土:"木", 水:"土", 火:"水", 金:"火", 木:"金" };

  /**
   * 四柱を算出する。
   * 真太陽時補正（経度差＋均時差）を必ず適用する。日本標準時は東経135°基準のため
   * 東京(139.69°)では +18.8分、加えて均時差が±16分動く。合計で最大35分ずれ、
   * 23時境界をまたぐと日柱ごと変わる。ここを省くと結果が根本から変わる。
   */
  function fourPillars(dateStr, timeStr, lng) {
    const [Y, M, D] = dateStr.split("-").map(Number);
    const hasTime = !!timeStr;
    const [hh, mm] = hasTime ? timeStr.split(":").map(Number) : [12, 0];
    lng = (lng == null ? 139.6917 : lng);

    // 。 真太陽時
    const jdNoon = toJD(Y, M, D, 3);              // JST12時 ≒ UT3時
    const lngCorr = (lng - 135) * 4;              // 分
    const eot = eqTime(jdNoon);                   // 分
    const trueMin = hh * 60 + mm + lngCorr + eot;
    let tsHour = Math.floor(((trueMin % 1440) + 1440) % 1440 / 60);
    const dayShift = Math.floor(trueMin / 1440);

    // 。 節入り一覧（前後年を含めて時系列で並べる）
    const birthJD = toJD(Y, M, D, (hh + mm / 60) - 9);   // UT
    const terms = [];
    for (const y of [Y - 1, Y, Y + 1]) {
      for (const t of SEKKI) terms.push({ jd: termJD(y, t.lon, t.cm), branch: t.branch, name: t.name, y });
    }
    terms.sort((a, b) => a.jd - b.jd);
    let cur = terms[0];
    for (const t of terms) if (t.jd <= birthJD) cur = t; else break;

    // 。 年柱（立春で切り替わる）
    const risshunThisYear = termJD(Y, 315, 2);
    const solarYear = birthJD < risshunThisYear ? Y - 1 : Y;
    const yStem = ((solarYear - 4) % 10 + 10) % 10;
    const yBranch = ((solarYear - 4) % 12 + 12) % 12;

    // 。 月柱（節入り基準・五虎遁）
    const mBranch = cur.branch;
    const tigerStem = ((yStem % 5) * 2 + 2) % 10;          // 寅月の天干
    const offset = ((mBranch - 2) % 12 + 12) % 12;
    const mStem = (tigerStem + offset) % 10;

    // 。 日柱（ユリウス通日／23時以降は翌日扱い＝晩子時）
    let jdn = toJDN(Y, M, D) + dayShift;
    if (tsHour >= 23) jdn += 1;
    const dStem = ((jdn + 9) % 10 + 10) % 10;
    const dBranch = ((jdn + 1) % 12 + 12) % 12;

    // 。 時柱（五鼠遁）
    const hBranch = Math.floor((((tsHour + 1) % 24) + 24) % 24 / 2);
    const ratStem = (dStem % 5) * 2;
    const hStem = (ratStem + hBranch) % 10;

    // 。 五行の数（天干＋地支本気）
    const tally = { 木: 0, 火: 0, 土: 0, 金: 0, 水: 0 };
    const stems = [yStem, mStem, dStem, hStem];
    const branches = [yBranch, mBranch, dBranch, hBranch];
    const useHour = hasTime;
    stems.slice(0, useHour ? 4 : 3).forEach(s => tally[STEM_EL[s]]++);
    branches.slice(0, useHour ? 4 : 3).forEach(b => tally[BRANCH_EL[b]]++);

    // 。 身強・身弱（簡易：日主と印星の合計で判定）
    const dayEl = STEM_EL[dStem];
    const inEl = SHENG_FROM[dayEl];
    const support = tally[dayEl] + tally[inEl];
    const totalCount = useHour ? 8 : 6;
    const strong = support >= totalCount * 0.45;

    const yojin = strong ? [KE[dayEl], KE_FROM[dayEl], SHENG[dayEl]] : [dayEl, inEl];
    const kijin = strong ? [dayEl, inEl] : [KE[dayEl], KE_FROM[dayEl]];

    return {
      pillars: {
        year:  { stem: STEM[yStem], branch: BRANCH[yBranch] },
        month: { stem: STEM[mStem], branch: BRANCH[mBranch] },
        day:   { stem: STEM[dStem], branch: BRANCH[dBranch] },
        hour:  useHour ? { stem: STEM[hStem], branch: BRANCH[hBranch] } : null
      },
      dayMaster: STEM[dStem],
      dayElement: dayEl,
      yin: STEM_YIN[dStem] === 1,
      tally, strong, yojin, kijin,
      solarYear,
      sekki: { name: cur.name, at: jdToParts(cur.jd + 9 / 24) },
      risshun: jdToParts(risshunThisYear + 9 / 24),
      shiftedYear: birthJD < risshunThisYear,
      trueSolar: {
        lngCorrection: round1(lngCorr),
        equationOfTime: round1(eot),
        totalMinutes: round1(lngCorr + eot),
        appliedTime: hasTime
          ? String(tsHour).padStart(2, "0") + ":" + String(Math.round(((trueMin % 60) + 60) % 60)).padStart(2, "0")
          : null
      },
      hasTime
    };
  }

  /* 。 九星気学 。 */
  const STAR_NAME = ["", "一白水星","二黒土星","三碧木星","四緑木星","五黄土星",
                     "六白金星","七赤金星","八白土星","九紫火星"];
  const STAR_EL = ["", "水","土","木","木","土","金","金","土","火"];
  const KA = {
    1:{n:"坎",dir:"北",grp:"east"},   2:{n:"坤",dir:"南西",grp:"west"},
    3:{n:"震",dir:"東",grp:"east"},   4:{n:"巽",dir:"南東",grp:"east"},
    6:{n:"乾",dir:"北西",grp:"west"}, 7:{n:"兌",dir:"西",grp:"west"},
    8:{n:"艮",dir:"北東",grp:"west"}, 9:{n:"離",dir:"南",grp:"east"}
  };
  const GOOD_DIR = { east: ["北","南","東","南東"], west: ["西","北西","北東","南西"] };
  const digitRoot = n => { while (n > 9) n = String(n).split("").reduce((a, c) => a + +c, 0); return n; };

  function kyusei(dateStr, gender) {
    const [Y, M, D] = dateStr.split("-").map(Number);
    const rs = jdToParts(termJD(Y, 315, 2) + 9 / 24);
    const before = (M < rs.m) || (M === rs.m && D < rs.d);
    const solarYear = before ? Y - 1 : Y;
    const S = digitRoot(solarYear);
    let star = 11 - S; if (star > 9) star -= 9;
    let k;
    if (gender === "m") k = (star === 5 ? 2 : star);
    else { let f = S + 4; if (f > 9) f -= 9; k = (f === 5 ? 8 : f); }
    const ka = KA[k];
    return {
      solarYear, star, starName: STAR_NAME[star], element: STAR_EL[star],
      ka: ka.n, kaDir: ka.dir, group: ka.grp,
      groupJP: ka.grp === "east" ? "東四命" : "西四命",
      goodDirections: GOOD_DIR[ka.grp],
      risshun: rs, shifted: before
    };
  }

  /* ══════════════════════════════════════════════════════════
     2. モジュール基盤
     ══════════════════════════════════════════════════════════ */
  const categories = [];
  const modules = [];

  function defineCategory(def) { categories.push(def); return def; }
  function defineModule(def) {
    if (modules.some(m => m.id === def.id)) throw new Error("duplicate module: " + def.id);
    modules.push(Object.assign({ weight: 1, minLevel: "region", requires: [] }, def));
    return def;
  }

  /* 。 カテゴリ定義（配点はここだけで調整する） 。 */
  defineCategory({ id: "terrain",     label: "地形・自然", en: "Terrain",     weight: 34 });
  defineCategory({ id: "history",     label: "歴史・土地", en: "Land History", weight: 16 });
  defineCategory({ id: "environment", label: "周辺環境",   en: "Environment", weight: 32 });
  defineCategory({ id: "building",    label: "建物",       en: "Building",    weight: 18 });

  /* ══════════════════════════════════════════════════════════
     3. 評価モジュール 。 地形・自然
     ══════════════════════════════════════════════════════════ */
  const VEIN_JP = { major: "大龍脈", middle: "中龍脈", minor: "小龍脈", none: "龍脈の外" };
  const VEIN_BASE = { major: 96, middle: 76, minor: 58, none: 34 };

  defineModule({
    id: "terrain.dragonVein", category: "terrain", label: "龍脈", en: "Dragon Vein",
    weight: 10, minLevel: "ward", requires: ["terrain.dragonVein"],
    evaluate(s) {
      const dv = get(s, "terrain.dragonVein"); if (!dv || !dv.grade) return null;
      const base = VEIN_BASE[dv.grade]; if (base == null) return null;
      const cont = dv.continuity == null ? 0.5 : dv.continuity;
      const score = clamp(base * 0.72 + cont * 100 * 0.28);
      return {
        score,
        reason: `${VEIN_JP[dv.grade]}上に位置します。DEMから抽出した尾根線の連続性は ${(cont * 100).toFixed(0)}％で、`
              + (cont >= .8 ? "気の通り道が途切れずに繋がっています。"
                 : cont >= .55 ? "おおむね繋がっていますが、途中に鞍部（谷の切れ込み）があります。"
                 : "尾根が細かく分断されており、気の流れは断続的です。")
              + (dv.source ? `主脈は${dv.source}から伸びています。` : ""),
        evidence: [
          { label: "龍脈の格", value: VEIN_JP[dv.grade] },
          { label: "尾根連続性", value: cont.toFixed(2) },
          { label: "出典", value: "国土地理院 基盤地図情報 5mDEM ／ 尾根線抽出" }
        ]
      };
    }
  });

  defineModule({
    id: "terrain.ryuketsu", category: "terrain", label: "龍穴", en: "Dragon Lair",
    weight: 5, minLevel: "town", requires: ["terrain.ryuketsu"],
    evaluate(s) {
      const r = get(s, "terrain.ryuketsu"); if (r == null) return null;
      if (r.present) {
        return {
          score: clamp(78 + (r.strength || 0) * 20),
          reason: `龍穴の条件（尾根の末端で気が留まり、左右から抱かれる地形）を満たします。${r.note || ""}`,
          evidence: [{ label: "判定", value: "該当" }, { label: "強度", value: (r.strength ?? 0).toFixed(2) },
                     { label: "出典", value: "DEM 凹凸解析（曲率・流域）" }]
        };
      }
      return {
        score: 50,
        reason: "龍穴の条件には該当しません。尾根上ではありますが、気が留まる窪みの形が確認できないため中立評価とします。",
        evidence: [{ label: "判定", value: "非該当" }, { label: "出典", value: "DEM 凹凸解析（曲率・流域）" }]
      };
    }
  });

  const LANDFORM = {
    ridge:      { s: 92, jp: "尾根",     t: "尾根筋にあたり、水はけがよく気が滞りません。古典が最上とする地形です。" },
    plateau:    { s: 84, jp: "台地上",   t: "台地の平坦面。安定した地盤の上にあり、標高差による減点も受けません。" },
    slope:      { s: 62, jp: "斜面",     t: "傾斜地にあたります。向きによって評価が分かれ、南〜南東向きの斜面は加点、北向きは減点です。" },
    plain:      { s: 52, jp: "平地",     t: "起伏の乏しい平坦地。加点も減点も生じにくい地形です。" },
    valley:     { s: 28, jp: "谷地",     t: "谷底にあたります。冷気と湿気が滞留しやすく、古典が避けるべきとする地形です。" },
    reclaimed:  { s: 24, jp: "埋立地",   t: "人工的な埋立地。地の気が浅く、地盤・浸水の両面で減点が入ります。" }
  };

  defineModule({
    id: "terrain.landform", category: "terrain", label: "尾根・谷地形", en: "Landform",
    weight: 8, minLevel: "ward", requires: ["terrain.landform"],
    evaluate(s) {
      const lf = get(s, "terrain.landform"); const def = LANDFORM[lf]; if (!def) return null;
      let score = def.s, extra = "";
      const asp = get(s, "terrain.slopeAspect");
      if (lf === "slope" && asp != null) {
        const d = Math.abs(((asp - 157.5 + 540) % 360) - 180);   // 南南東からのずれ
        const adj = Math.round((1 - d / 180) * 24 - 12);
        score = clamp(score + adj);
        extra = `斜面の向きは${asp}°で、${adj >= 0 ? `南寄りのため ${adj} 点の加点` : `北寄りのため ${adj} 点の減点`}です。`;
      }
      return {
        score,
        reason: def.t + extra,
        evidence: [{ label: "地形分類", value: def.jp },
                   asp != null ? { label: "斜面方位", value: asp + "°" } : null,
                   { label: "出典", value: "国土地理院 地形分類（自然地形）" }].filter(Boolean)
      };
    }
  });

  defineModule({
    id: "terrain.elevation", category: "terrain", label: "標高", en: "Elevation",
    weight: 8, minLevel: "ward", requires: ["terrain.elevation"],
    evaluate(s) {
      const e = get(s, "terrain.elevation"); if (e == null) return null;
      const rel = get(s, "terrain.relativeHeight");
      // 標高そのものより「周囲との比高」を重く見る
      let score = e >= 30 ? 88 : e >= 20 ? 76 : e >= 12 ? 62 : e >= 6 ? 46 : e >= 3 ? 34 : 22;
      let extra = "";
      if (rel != null) {
        const adj = clamp(Math.round(rel * 0.5), -10, 14);
        score = clamp(score + adj);
        extra = `周囲の低地との比高は ${rel}m で、${adj >= 0 ? `+${adj}` : adj} 点の補正が入ります。`;
      }
      return {
        score,
        reason: `標高 ${e}m。` + (e >= 20
          ? "古典が「高処に居る」とする条件を満たし、湿気と水害の双方から距離が取れます。"
          : e >= 6 ? "中位の標高です。周囲の地形との関係で評価が変わります。"
          : "低地にあたります。地勢による加点は望めず、水勢と方位で補う構造になります。") + extra,
        evidence: [{ label: "標高", value: e + "m" },
                   rel != null ? { label: "周囲との比高", value: rel + "m" } : null,
                   { label: "出典", value: "国土地理院 標高API（5mメッシュ）" }].filter(Boolean)
      };
    }
  });

  defineModule({
    id: "terrain.water", category: "terrain", label: "水脈", en: "Water Vein",
    weight: 6, minLevel: "town", requires: ["terrain.water"],
    evaluate(s) {
      const w = get(s, "terrain.water"); if (!w) return null;
      const rivers = w.rivers || [];
      if (!rivers.length && w.seaDistance == null) return null;
      let score = 50, notes = [];
      rivers.forEach(r => {
        const near = r.distance <= 300;
        if (r.curvature === "concave") {                 // 環抱水（内側）
          score += near ? 22 : 12;
          notes.push(`${r.name}のカーブ内側（環抱水）にあたり、水が土地を抱く吉形です`);
        } else if (r.curvature === "convex") {           // 反弓水（外側）
          score -= near ? 20 : 10;
          notes.push(`${r.name}のカーブ外側（反弓水）にあたり、水が土地を削る形です`);
        } else {
          score += near ? 6 : 3;
          notes.push(`${r.name}が ${r.distance}m の距離を直線的に流れます`);
        }
      });
      if (w.seaDistance != null && w.seaDistance < 1500) {
        score += 6; notes.push(`東京湾まで約${(w.seaDistance / 1000).toFixed(1)}kmで、面水の条件を満たします`);
      }
      return {
        score: clamp(score),
        reason: notes.join("。") + "。水は財の気を運ぶとされ、距離よりも「どちら側に曲がっているか」が評価を分けます。",
        evidence: rivers.map(r => ({ label: r.name, value: `${r.distance}m ／ ${r.curvature === "concave" ? "環抱（吉）" : r.curvature === "convex" ? "反弓（凶）" : "直流"}` }))
          .concat([{ label: "出典", value: "国土数値情報 河川データ ／ OSM waterway" }])
      };
    }
  });

  defineModule({
    id: "terrain.culvert", category: "terrain", label: "暗渠", en: "Culvert",
    weight: 4, minLevel: "town", requires: ["terrain.culverts"],
    evaluate(s) {
      const c = get(s, "terrain.culverts"); if (!c) return null;
      if (!c.length) {
        return { score: 58, reason: "敷地周辺に暗渠は確認できません。旧河道由来の軟弱地盤や湿気の懸念がない分、わずかに加点します。",
                 evidence: [{ label: "判定", value: "暗渠なし" }, { label: "出典", value: "旧版地形図 ／ 東京都下水道台帳" }] };
      }
      const under = c.some(x => x.underSite);
      const min = Math.min(...c.map(x => x.distance));
      const score = under ? 26 : min < 50 ? 38 : min < 150 ? 48 : 56;
      return {
        score,
        reason: under
          ? `敷地直下を暗渠（${c[0].name}）が通過します。旧河道であり、地盤の含水と沈下の履歴を確認すべき条件です。風水では水脈が地下を走ることを一概に凶とはしませんが、建物直下は気の安定を欠くとされます。`
          : `最寄りの暗渠（${c[0].name}）まで ${min}m。直下ではないため影響は限定的ですが、旧河道の縁にあたるため地盤資料の確認を勧めます。`,
        evidence: c.map(x => ({ label: x.name, value: x.underSite ? "敷地直下を通過" : `${x.distance}m` }))
          .concat([{ label: "出典", value: "旧版地形図（明治・大正）との重ね合わせ" }])
      };
    }
  });

  defineModule({
    id: "terrain.spring", category: "terrain", label: "湧水", en: "Spring",
    weight: 3, minLevel: "town", requires: ["terrain.springs"],
    evaluate(s) {
      const sp = get(s, "terrain.springs"); if (!sp) return null;
      if (!sp.length) return { score: 50, reason: "周辺に湧水地点は確認できません。加点も減点もありません。",
                               evidence: [{ label: "判定", value: "該当なし" }, { label: "出典", value: "東京都湧水マップ" }] };
      const min = Math.min(...sp.map(x => x.distance));
      const score = min < 300 ? 82 : min < 800 ? 68 : 56;
      return {
        score,
        reason: `${sp[0].name}まで ${min}m。湧水は崖線から地下水が地表に出る点で、台地の縁を示す指標でもあります。生気が湧く場所として古典が重視する要素です。`,
        evidence: sp.map(x => ({ label: x.name, value: x.distance + "m" }))
          .concat([{ label: "出典", value: "東京都環境局 湧水・地下水データ" }])
      };
    }
  });

  const GROUND = {
    "台地・ローム": { s: 88, t: "関東ローム層に覆われた台地。支持層が浅く、地盤としては都内最良の部類です。" },
    "段丘礫層":     { s: 80, t: "段丘の礫層。締まりがよく安定しています。" },
    "扇状地":       { s: 66, t: "扇状地性の堆積。おおむね安定しますが局所差があります。" },
    "谷底低地":     { s: 34, t: "谷底の沖積層。軟弱層が厚く、液状化と沈下の双方に注意が要ります。" },
    "後背湿地":     { s: 28, t: "旧湿地。粘性土が厚く堆積し、地盤としては弱い部類です。" },
    "埋立地":       { s: 22, t: "人工の埋立層。液状化リスクが高く、地の気も浅いと判断します。" }
  };
  defineModule({
    id: "terrain.ground", category: "terrain", label: "地盤", en: "Ground",
    weight: 6, minLevel: "ward", requires: ["terrain.ground"],
    evaluate(s) {
      const g = get(s, "terrain.ground"); if (!g || !g.classification) return null;
      const def = GROUND[g.classification]; if (!def) return null;
      let score = def.s, extra = "";
      if (g.liquefaction) {
        const adj = { 低: 6, 中: -6, 高: -16 }[g.liquefaction] || 0;
        score = clamp(score + adj);
        extra = `液状化の可能性は「${g.liquefaction}」で ${adj >= 0 ? "+" : ""}${adj} 点。`;
      }
      return {
        score, reason: def.t + extra,
        evidence: [{ label: "地形分類", value: g.classification },
                   g.liquefaction ? { label: "液状化可能性", value: g.liquefaction } : null,
                   { label: "出典", value: "国土地理院 治水地形分類図 ／ 東京都液状化予測図" }].filter(Boolean)
      };
    }
  });

  /* ══════════════════════════════════════════════════════════
     4. 評価モジュール 。 歴史・土地情報
     ══════════════════════════════════════════════════════════ */
  const FORMER_USE = {
    "武家屋敷":   { s: 92, t: "江戸期の武家地。台地の良地が選ばれており、地歴として最上位に置かれます。" },
    "大名屋敷":   { s: 96, t: "大名の上屋敷跡。江戸で最も条件のよい土地が選定された区画です。" },
    "寺社地":     { s: 86, t: "寺社の境内地。土地神の加護が長く続いた区画とされます。" },
    "町人地":     { s: 62, t: "江戸の町人地。商業の気が蓄積していますが、密集による混雑の気も伴います。" },
    "田畑":       { s: 56, t: "近世まで農地。人の営みが穏やかに続いた土地です。" },
    "河川・水路": { s: 32, t: "旧河道・水路の跡地。埋め立てられた軟弱層が残ります。" },
    "湿地":       { s: 26, t: "旧湿地。近代まで居住に適さなかった土地であり、地歴としては最も弱い分類です。" },
    "海・埋立":   { s: 24, t: "近代以降の埋立地。地の気の蓄積が浅いと判断します。" },
    "工場":       { s: 44, t: "近代の工場用地。土壌履歴の確認が望ましい区画です。" }
  };
  defineModule({
    id: "history.formerUse", category: "history", label: "昔の土地利用", en: "Former Land Use",
    weight: 6, minLevel: "ward", requires: ["history.formerUse"],
    evaluate(s) {
      const u = get(s, "history.formerUse"); const def = FORMER_USE[u]; if (!def) return null;
      return { score: def.s, reason: def.t,
        evidence: [{ label: "近世の土地利用", value: u },
                   { label: "出典", value: "江戸切絵図 ／ 迅速測図 ／ 旧版地形図" }] };
    }
  });

  defineModule({
    id: "history.edoMap", category: "history", label: "江戸切絵図", en: "Edo Map",
    weight: 4, minLevel: "ward", requires: ["history.edo"],
    evaluate(s) {
      const e = get(s, "history.edo"); if (!e) return null;
      return { score: clamp(e.score ?? 50),
        reason: `江戸切絵図では「${e.label}」として描かれています。${e.note || ""}`,
        evidence: [{ label: "切絵図の記載", value: e.label },
                   { label: "出典", value: "尾張屋版江戸切絵図（国立国会図書館デジタルコレクション）" }] };
    }
  });

  defineModule({
    id: "history.meijiMap", category: "history", label: "明治の古地図", en: "Meiji Map",
    weight: 4, minLevel: "town", requires: ["history.meiji"],
    evaluate(s) {
      const m = get(s, "history.meiji"); if (!m) return null;
      return { score: clamp(m.score ?? 50),
        reason: `明治期の地形図では「${m.label}」。${m.note || ""}この時点で市街化していたかどうかが、地盤改変の有無を判断する材料になります。`,
        evidence: [{ label: "明治期の記載", value: m.label },
                   { label: "出典", value: "迅速測図（明治13–19年）／ 参謀本部 5万分1地形図" }] };
    }
  });

  defineModule({
    id: "history.showaMap", category: "history", label: "昭和初期の古地図", en: "Showa Map",
    weight: 3, minLevel: "town", requires: ["history.showa"],
    evaluate(s) {
      const m = get(s, "history.showa"); if (!m) return null;
      return { score: clamp(m.score ?? 50),
        reason: `昭和初期の地形図では「${m.label}」。${m.note || ""}`,
        evidence: [{ label: "昭和初期の記載", value: m.label },
                   { label: "出典", value: "1万分1地形図（昭和初期）" }] };
    }
  });

  defineModule({
    id: "history.aerial", category: "history", label: "旧航空写真", en: "Aerial Photo",
    weight: 3, minLevel: "address", requires: ["history.aerial"],
    evaluate(s) {
      const a = get(s, "history.aerial"); if (!a) return null;
      return { score: clamp(a.score ?? 50),
        reason: `${a.year}年の航空写真では「${a.label}」が確認できます。${a.note || ""}戦災・造成・池の埋立といった改変履歴は、この時期の空中写真でしか追えません。`,
        evidence: [{ label: `${a.year}年 空中写真`, value: a.label },
                   { label: "出典", value: "国土地理院 空中写真アーカイブ（米軍撮影・1947–48ほか）" }] };
    }
  });

  defineModule({
    id: "history.origin", category: "history", label: "土地の由来", en: "Place Name Origin",
    weight: 3, minLevel: "town", requires: ["history.origin"],
    evaluate(s) {
      const o = get(s, "history.origin"); if (!o) return null;
      return { score: clamp(o.score ?? 50),
        reason: `地名の由来：${o.text}`,
        evidence: [{ label: "地名の含意", value: o.implication || "—" },
                   { label: "出典", value: "自治体史 ／ 角川日本地名大辞典" }] };
    }
  });

  /* ══════════════════════════════════════════════════════════
     5. 評価モジュール 。 周辺環境
     ══════════════════════════════════════════════════════════ */
  defineModule({
    id: "environment.shrine", category: "environment", label: "神社仏閣との位置関係", en: "Shrines & Temples",
    weight: 6, minLevel: "ward", requires: ["environment.shrines"],
    evaluate(s) {
      const sh = get(s, "environment.shrines"); if (!sh) return null;
      if (!sh.length) return { score: 46, reason: "半径800m以内に神社仏閣が確認できません。土地神の加護という観点では中立よりやや弱い評価です。",
                               evidence: [{ label: "判定", value: "該当なし" }, { label: "出典", value: "OSM amenity=place_of_worship" }] };
      let score = 50; const notes = [];
      sh.forEach(x => {
        const rank = { 総鎮守: 20, 郷社: 14, 村社: 10, 寺院: 8 }[x.rank] ?? 8;
        const near = x.distance < 300 ? 1 : x.distance < 800 ? .6 : .3;
        score += rank * near;
        notes.push(`${x.name}（${x.distance}m・${x.bearing}）`);
        if (x.type === "墓地" || x.type === "斎場") {
          if (x.distance < 300) { score -= 18; notes.push("ただし墓地・斎場が近接し、独陽殺の減点対象です"); }
        }
      });
      return {
        score: clamp(score),
        reason: `${notes.join("、")}。鎮守社が近いことは地運の安定を示す指標とされます。ただし墓地・斎場は300m以内で減点対象になります。`,
        evidence: sh.map(x => ({ label: x.name, value: `${x.distance}m ／ ${x.bearing} ／ ${x.rank || x.type}` }))
          .concat([{ label: "出典", value: "OSM ／ 神社本庁データ" }])
      };
    }
  });

  defineModule({
    id: "environment.disaster", category: "environment", label: "災害履歴", en: "Disaster History",
    weight: 7, minLevel: "ward", requires: ["environment.hazard"],
    evaluate(s) {
      const h = get(s, "environment.hazard"); if (!h) return null;
      let score = 78;
      const notes = [];
      if (h.floodDepth != null) {
        const adj = h.floodDepth <= 0 ? 10 : h.floodDepth < 0.5 ? -6 : h.floodDepth < 1 ? -16 : h.floodDepth < 3 ? -28 : -38;
        score += adj;
        notes.push(h.floodDepth <= 0 ? "洪水浸水想定区域に含まれません" : `想定浸水深 ${h.floodDepth}m（${adj}点）`);
      }
      if (h.landslide) { score -= 14; notes.push("土砂災害警戒区域に含まれます（−14点）"); }
      if (h.history && h.history.length) {
        h.history.forEach(x => { score -= 6; notes.push(`${x.year}年 ${x.type}の被災記録`); });
      } else if (h.history) notes.push("近代以降の重大な被災記録は確認できません");
      return {
        score: clamp(score),
        reason: notes.join("。") + "。古典が「水の来る土地を避けよ」と説く根拠は、現代のハザードマップとかなりの部分で一致します。",
        evidence: [
          h.floodDepth != null ? { label: "想定浸水深", value: h.floodDepth <= 0 ? "区域外" : h.floodDepth + "m" } : null,
          { label: "土砂災害", value: h.landslide ? "警戒区域内" : "区域外" },
          { label: "出典", value: "重ねるハザードマップ ／ 自治体water災害履歴" }
        ].filter(Boolean)
      };
    }
  });

  defineModule({
    id: "environment.roadFlow", category: "environment", label: "周辺道路の気の流れ", en: "Road Qi Flow",
    weight: 5, minLevel: "address", requires: ["environment.roads"],
    evaluate(s) {
      const r = get(s, "environment.roads"); if (!r) return null;
      let score = 56; const notes = [];
      if (r.frontWidth != null) {
        const adj = r.frontWidth < 4 ? -12 : r.frontWidth <= 12 ? 8 : r.frontWidth <= 25 ? 0 : -10;
        score += adj;
        notes.push(`前面道路幅員 ${r.frontWidth}m（${adj >= 0 ? "+" : ""}${adj}点）。狭すぎれば気が滞り、広すぎれば気が抜けます`);
      }
      if (r.arterialDistance != null) {
        const adj = r.arterialDistance < 30 ? -12 : r.arterialDistance < 80 ? -5 : r.arterialDistance < 200 ? -1 : 4;
        score += adj;
        notes.push(`幹線道路まで ${r.arterialDistance}m（${adj >= 0 ? "+" : ""}${adj}点）`);
      }
      if (r.elevatedDistance != null && r.elevatedDistance < 200) {
        score -= 10; notes.push(`高架構造物が ${r.elevatedDistance}m に近接（−10点）`);
      }
      return { score: clamp(score), reason: notes.join("。") + "。",
        evidence: [
          r.frontWidth != null ? { label: "前面道路幅員", value: r.frontWidth + "m" } : null,
          r.arterialDistance != null ? { label: "幹線道路まで", value: r.arterialDistance + "m" } : null,
          { label: "出典", value: "OSM highway ／ 都市計画道路network" }
        ].filter(Boolean) };
    }
  });

  defineModule({
    id: "environment.tJunction", category: "environment", label: "T字路（路冲）", en: "T-Junction",
    weight: 6, minLevel: "address", requires: ["environment.roads.tJunctions"],
    evaluate(s) {
      const t = get(s, "environment.roads.tJunctions"); if (!t) return null;
      if (!t.length) return { score: 72, reason: "建物正面に突き当たる道路（路冲）はありません。古典が最も強く警戒する形殺に該当しないため加点します。",
                              evidence: [{ label: "判定", value: "該当なし" }, { label: "判定条件", value: "正面±15°・60m以内に終端を持つ道路" }, { label: "出典", value: "OSM highway ジオメトリ解析" }] };
      const worst = t.reduce((a, b) => (a.distance < b.distance ? a : b));
      const score = clamp(48 - (60 - Math.min(worst.distance, 60)) * 0.55 - (worst.width || 6));
      return {
        score,
        reason: `建物正面 ${worst.distance}m に道路が突き当たります（路冲）。幅員 ${worst.width || "?"}m、正面からのずれ ${worst.offsetDeg ?? "?"}°。`
              + "直進してきた気が建物に直撃する形で、形殺のなかでも減点幅が最も大きい項目です。距離が近く道路が広いほど影響が強まります。",
        evidence: t.map(x => ({ label: "突き当たり道路", value: `${x.distance}m ／ 幅員${x.width}m ／ ずれ${x.offsetDeg}°` }))
          .concat([{ label: "出典", value: "OSM highway ジオメトリ解析（ST_Azimuth）" }])
      };
    }
  });

  defineModule({
    id: "environment.reverseBow", category: "environment", label: "反弓路", en: "Reverse Bow",
    weight: 5, minLevel: "address", requires: ["environment.roads.reverseBow"],
    evaluate(s) {
      const rb = get(s, "environment.roads.reverseBow"); if (rb == null) return null;
      if (!rb.present) return { score: 68, reason: "前面道路のカーブ外側（反弓）にはあたりません。道路が土地を抱く側、または直線区間です。",
                                evidence: [{ label: "判定", value: "該当なし" }, { label: "出典", value: "OSM 道路曲率解析" }] };
      const score = clamp(46 - (rb.curvature || 0.5) * 30);
      return {
        score,
        reason: `前面道路がカーブの外側に敷地を置く形（反弓路）です。曲率 ${(rb.curvature ?? 0).toFixed(2)}。`
              + "弓が反り返るように道路が土地から離れていく形で、気が留まらず流れ去るとされます。カーブがきついほど減点が大きくなります。",
        evidence: [{ label: "曲率", value: (rb.curvature ?? 0).toFixed(2) },
                   { label: "判定条件", value: "曲率中心が敷地と反対側" },
                   { label: "出典", value: "OSM 道路曲率解析" }]
      };
    }
  });

  defineModule({
    id: "environment.deadEnd", category: "environment", label: "袋小路", en: "Dead End",
    weight: 3, minLevel: "address", requires: ["environment.roads.deadEnd"],
    evaluate(s) {
      const d = get(s, "environment.roads.deadEnd"); if (d == null) return null;
      if (!d.present) return { score: 60, reason: "袋小路には面していません。気の出入り口が確保されています。",
                               evidence: [{ label: "判定", value: "該当なし" }, { label: "出典", value: "OSM 道路network解析" }] };
      return {
        score: d.depth > 3 ? 30 : 42,
        reason: `袋小路の奥から ${d.depth} 軒目に位置します。行き止まりは気の出口がなく滞留するとされ、奥に入るほど減点が増します。`
              + "一方で通り抜け交通がないため、静穏性という点では利点にもなります。",
        evidence: [{ label: "袋小路の深さ", value: d.depth + "軒目" }, { label: "出典", value: "OSM 道路network解析" }]
      };
    }
  });

  /* ══════════════════════════════════════════════════════════
     6. 評価モジュール 。 建物
     ══════════════════════════════════════════════════════════ */
  const DIR8 = [
    { n: "北", a: 0, el: "水" }, { n: "北東", a: 45, el: "土" },
    { n: "東", a: 90, el: "木" }, { n: "南東", a: 135, el: "木" },
    { n: "南", a: 180, el: "火" }, { n: "南西", a: 225, el: "土" },
    { n: "西", a: 270, el: "金" }, { n: "北西", a: 315, el: "金" }
  ];
  const SANJU = ["子","癸","丑","艮","寅","甲","卯","乙","辰","巽","巳","丙",
                 "午","丁","未","坤","申","庚","酉","辛","戌","乾","亥","壬"];
  const dirOf = deg => DIR8[Math.round(mod360(deg) / 45) % 8];
  const sanjuOf = deg => {
    const i = Math.round(mod360(deg) / 15) % 24;
    const center = i * 15;
    const off = Math.abs(((mod360(deg) - center + 540) % 360) - 180);
    return { name: SANJU[i], center, kengou: off > 4.5 };   // 兼向＝境界付近
  };
  const FACING_BASE = { 南東: 92, 南: 86, 東: 82, 北: 70, 北西: 64, 西: 56, 北東: 42, 南西: 42 };

  defineModule({
    id: "building.facing", category: "building", label: "建物の向き（坐向）", en: "Facing",
    weight: 8, minLevel: "building", requires: ["building.facing"],
    evaluate(s) {
      const f = get(s, "building.facing"); if (f == null) return null;
      const d = dirOf(f), sj = sanjuOf(f), sit = sanjuOf(f + 180);
      let score = FACING_BASE[d.n];
      let extra = "";
      if (d.n === "北東") extra = "表鬼門にあたるため減点が入ります。";
      if (d.n === "南西") extra = "裏鬼門にあたるため減点が入ります。";
      if (sj.kengou) { score = clamp(score - 6); extra += "二十四山の境界（兼向）にかかるため6点減じ、人手による確認対象としています。"; }
      return {
        score,
        reason: `建物の正面方位は ${f}°（${d.n}向き）。二十四山では ${sit.name}山 ${sj.name}向にあたります。`
              + `${d.n}向きは五行の${d.el}に属し、採光と気の入りの両面で${score >= 80 ? "最上位" : score >= 65 ? "中位" : "下位"}の評価です。` + extra,
        evidence: [{ label: "正面方位", value: f + "°（" + d.n + "）" },
                   { label: "二十四山", value: `${sit.name}山 ${sj.name}向` },
                   { label: "兼向判定", value: sj.kengou ? "境界±4.5°以内（要確認）" : "正向" },
                   { label: "出典", value: "建物ポリゴン主軸方位の自動算出（国土地理院 建物データ）" }]
      };
    }
  });

  /** 三元九運：2024年2月4日から九運。
   *  当令＝九紫（離・南）＝旺気／生気＝一白（坎・北）／進気＝二黒（坤・南西）
   *  退気＝八白（艮・北東、前運の余勢）／それ以外は平〜衰。
   */
  const KYUUN = { 南: 96, 北: 82, 南西: 76, 北東: 68, 東: 58, 南東: 56, 西: 50, 北西: 48 };
  const KYUUN_KI = { 南: "旺気", 北: "生気", 南西: "進気", 北東: "退気（前運の余勢）",
                     東: "平気", 南東: "平気", 西: "衰気", 北西: "衰気" };
  defineModule({
    id: "building.era", category: "building", label: "元運適合（九運）", en: "Era Fit",
    weight: 4, minLevel: "building", requires: ["building.facing"],
    evaluate(s) {
      const f = get(s, "building.facing"); if (f == null) return null;
      const d = dirOf(f);
      const built = get(s, "building.builtYear");
      let score = KYUUN[d.n];
      let extra = "";
      if (built != null) {
        if (built >= 2024) { score = clamp(score + 6); extra = `${built}年竣工で九運期に入ってからの建物のため、当運の気を受けます（+6点）。`; }
        else if (built >= 2004) extra = `${built}年竣工＝八運期の建物です。2024年の九運入りで方位の吉凶が入れ替わっており、当時の評価をそのまま当てはめられません。`;
        else extra = `${built}年竣工＝七運以前の建物です。`;
      }
      return {
        score,
        reason: `2024年2月4日から三元九運は九運（2024–2043）に入り、当令は九紫＝離＝南。南が旺気、北が生気、南西が進気にあたる20年間です。${d.n}向きはこの運で${KYUUN_KI[d.n]}にあたります。` + extra,
        evidence: [{ label: "現在の元運", value: "九運（2024–2043）" },
                   { label: "向きの評価", value: d.n + "＝" + KYUUN_KI[d.n] + "／" + score + "点" },
                   built != null ? { label: "竣工年", value: built + "年" } : null].filter(Boolean)
      };
    }
  });

  /* ══════════════════════════════════════════════════════════
     7. 集計
     ══════════════════════════════════════════════════════════ */
  function gradeOf(t) {
    return t >= 90 ? "S" : t >= 84 ? "A+" : t >= 78 ? "A" : t >= 72 ? "B+"
         : t >= 66 ? "B" : t >= 58 ? "C+" : t >= 50 ? "C" : "D";
  }
  function labelOf(t) {
    return t >= 88 ? "非常に良い" : t >= 78 ? "良い" : t >= 70 ? "普通"
         : t >= 60 ? "やや低め" : "低め";
  }

  /**
   * 評価を実行する。
   * @param {object} subject
   * @returns {object} 総合点・カテゴリ別・モジュール別・強み弱み・データ充足率
   */
  function evaluate(subject) {
    const sLevel = levelIdx(subject.level);
    const results = [];

    for (const m of modules) {
      const base = { id: m.id, label: m.label, en: m.en, category: m.category,
                     weight: m.weight, minLevel: m.minLevel };
      if (sLevel < levelIdx(m.minLevel)) {
        results.push(Object.assign({}, base, {
          status: "out_of_scope", score: null,
          reason: `この項目は${LEVEL_JP[m.minLevel]}単位以上でしか判定できません。現在の評価対象は${LEVEL_JP[subject.level]}単位です。`,
          evidence: []
        }));
        continue;
      }
      let r = null;
      try { r = m.evaluate(subject); } catch (e) { r = null; }
      if (!r || r.score == null) {
        results.push(Object.assign({}, base, {
          status: "no_data", score: null,
          reason: "この項目を判定するためのデータが未取得です。取得後に自動で評価に加わります。",
          evidence: []
        }));
        continue;
      }
      results.push(Object.assign({}, base, {
        status: "ok", score: round1(clamp(r.score)),
        reason: r.reason || "", evidence: r.evidence || [], flags: r.flags || []
      }));
    }

    // 。 カテゴリ集計（欠測分の重みは同カテゴリ内で再配分）
    const cats = categories.map(c => {
      const mine = results.filter(r => r.category === c.id);
      const ok = mine.filter(r => r.status === "ok");
      const wSum = ok.reduce((a, r) => a + r.weight, 0);
      const wAll = mine.reduce((a, r) => a + r.weight, 0);
      const score = wSum ? ok.reduce((a, r) => a + r.score * r.weight, 0) / wSum : null;
      ok.forEach(r => { r.effectiveWeight = round1(r.weight / wSum * c.weight); });
      return Object.assign({}, c, {
        score: score == null ? null : round1(score),
        coverage: wAll ? round1(wSum / wAll * 100) / 100 : 0,
        modules: mine
      });
    });

    const liveCats = cats.filter(c => c.score != null);
    const cw = liveCats.reduce((a, c) => a + c.weight, 0);
    const total = cw ? Math.round(liveCats.reduce((a, c) => a + c.score * c.weight, 0) / cw) : null;
    liveCats.forEach(c => { c.contribution = round1(c.score * c.weight / cw); });

    const allW = modules.reduce((a, m) => a + m.weight, 0);
    const okW = results.filter(r => r.status === "ok").reduce((a, r) => a + r.weight, 0);

    // 。 強み・弱み（中立50からの乖離 × 実効重み）
    const scored = results.filter(r => r.status === "ok")
      .map(r => Object.assign({}, r, { impact: round1((r.score - 50) * (r.effectiveWeight || 0) / 10) }));
    const strengths = scored.filter(r => r.impact > 0).sort((a, b) => b.impact - a.impact).slice(0, 4);
    const weaknesses = scored.filter(r => r.impact < 0).sort((a, b) => a.impact - b.impact).slice(0, 4);

    return {
      subject: { id: subject.id, name: subject.name, level: subject.level, levelJP: LEVEL_JP[subject.level] },
      total, grade: total == null ? null : gradeOf(total), label: total == null ? null : labelOf(total),
      coverage: round1(okW / allW * 100) / 100,
      coverageDetail: {
        evaluated: results.filter(r => r.status === "ok").length,
        outOfScope: results.filter(r => r.status === "out_of_scope").length,
        noData: results.filter(r => r.status === "no_data").length,
        total: results.length
      },
      categories: cats, modules: results, strengths, weaknesses,
      version: "2.0.0", evaluatedAt: new Date().toISOString()
    };
  }


  /* ══════════════════════════════════════════════════════════
     7.5 表示用：4運（財運・仕事運・恋愛運・健康運）への写像
     。 内部の22項目を、利用者に馴染みのある4軸へ集約する。
        評価ロジックそのものではなく、あくまで表示のための変換。
     ══════════════════════════════════════════════════════════ */
  const FORTUNE_MAP = [
    { id:"wealth", label:"財運", en:"WEALTH", color:"#8A6E3C", w:{
      "terrain.water":18,"terrain.dragonVein":16,"history.formerUse":14,
      "environment.roadFlow":12,"building.facing":12,"building.era":10,
      "terrain.landform":10,"environment.tJunction":8 } },
    { id:"career", label:"仕事運", en:"CAREER", color:"#3B6BA5", w:{
      "terrain.dragonVein":20,"terrain.elevation":16,"terrain.landform":14,
      "building.facing":16,"building.era":12,"history.edoMap":10,
      "environment.roadFlow":12 } },
    { id:"romance", label:"恋愛運", en:"ROMANCE", color:"#8E4A63", w:{
      "environment.shrine":18,"building.facing":18,"terrain.spring":14,
      "terrain.landform":12,"terrain.water":12,"history.origin":10,
      "terrain.ryuketsu":8,"environment.deadEnd":8 } },
    { id:"vitality", label:"健康運", en:"VITALITY", color:"#2F6B45", w:{
      "environment.disaster":20,"terrain.elevation":18,"terrain.ground":18,
      "terrain.landform":14,"terrain.culvert":12,"environment.roadFlow":10,
      "terrain.spring":8 } }
  ];

  function deriveFortunes(result) {
    const byId = {};
    result.modules.forEach(m => { if (m.status === "ok") byId[m.id] = m.score; });
    return FORTUNE_MAP.map(f => {
      let sw = 0, acc = 0;
      for (const k in f.w) if (byId[k] != null) { sw += f.w[k]; acc += byId[k] * f.w[k]; }
      const score = sw ? Math.round(acc / sw) : null;
      return { id: f.id, label: f.label, en: f.en, color: f.color,
               score, coverage: sw / Object.values(f.w).reduce((a, b) => a + b, 0) };
    });
  }

  /** 複数対象の4運平均（比較用の基準線） */
  function averageFortunes(subjects) {
    const all = subjects.map(s => deriveFortunes(evaluate(s)));
    return FORTUNE_MAP.map((f, i) => {
      const vals = all.map(a => a[i].score).filter(v => v != null);
      return { id: f.id, label: f.label, color: f.color,
               score: vals.length ? Math.round(vals.reduce((a, b) => a + b, 0) / vals.length) : null };
    });
  }

  /* ══════════════════════════════════════════════════════════
     8. 居住者との相性（別レイヤー）
     ══════════════════════════════════════════════════════════ */
  function evaluatePersonal(subject, person) {
    const ky = kyusei(person.birth, person.gender);
    const sc = fourPillars(person.birth, person.time || null, person.lng);
    const facing = get(subject, "building.facing");
    const parts = [];

    // 。 九星気学：本命卦と建物の向き
    let kyScore = 50;
    if (facing != null) {
      const d = dirOf(facing);
      const good = ky.goodDirections.includes(d.n);
      kyScore = good ? 84 : 38;
      parts.push({
        id: "personal.kyusei", label: "九星気学", weight: 50, score: kyScore,
        reason: `${ky.starName}・本命卦は${ky.ka}（${ky.groupJP}）。吉方位は${ky.goodDirections.join("・")}です。`
              + `この建物は${d.n}向きのため、${good ? "吉方位に合致します" : "吉方位から外れます"}。`,
        evidence: [{ label: "本命星", value: ky.starName },
                   { label: "本命卦", value: `${ky.ka}（${ky.groupJP}）` },
                   { label: "立春", value: `${ky.risshun.y}年${ky.risshun.m}月${ky.risshun.d}日 ${String(ky.risshun.h).padStart(2,"0")}:${String(ky.risshun.mi).padStart(2,"0")}` },
                   { label: "年の扱い", value: ky.shifted ? "立春前のため前年で判定" : "暦年と節年が一致" }]
      });
    }

    // 。 四柱推命：用神・忌神と土地／建物の五行
    let scScore = 50;
    const landEl = get(subject, "terrain.element")
      || (facing != null ? dirOf(facing).el : null);
    if (landEl) {
      scScore = sc.yojin.includes(landEl) ? 86 : sc.kijin.includes(landEl) ? 34 : 58;
      parts.push({
        id: "personal.shichu", label: "四柱推命", weight: 50, score: scScore,
        reason: `日主は${sc.dayMaster}（五行の${sc.dayElement}）、命式は${sc.strong ? "身強" : "身弱"}。`
              + `用神は${sc.yojin.join("・")}、忌神は${sc.kijin.join("・")}です。`
              + `この立地の五行は${landEl}であり、${sc.yojin.includes(landEl) ? "用神に一致するため強く加点します"
                : sc.kijin.includes(landEl) ? "忌神に該当するため減点します" : "用神・忌神のいずれでもなく中立です"}。`
              + (sc.hasTime ? `真太陽時補正は経度差 ${sc.trueSolar.lngCorrection}分＋均時差 ${sc.trueSolar.equationOfTime}分＝計 ${sc.trueSolar.totalMinutes}分を適用しています。`
                            : "出生時刻が未入力のため時柱を除いた三柱で判定しています。時刻が分かると精度が上がります。"),
        evidence: [
          { label: "四柱", value: `${sc.pillars.year.stem}${sc.pillars.year.branch} ${sc.pillars.month.stem}${sc.pillars.month.branch} ${sc.pillars.day.stem}${sc.pillars.day.branch}${sc.pillars.hour ? " " + sc.pillars.hour.stem + sc.pillars.hour.branch : ""}` },
          { label: "日主", value: `${sc.dayMaster}（${sc.dayElement}）／${sc.strong ? "身強" : "身弱"}` },
          { label: "五行の数", value: Object.entries(sc.tally).map(([k, v]) => k + v).join(" ") },
          { label: "用神／忌神", value: `${sc.yojin.join("・")} ／ ${sc.kijin.join("・")}` },
          { label: "節入り", value: `${sc.sekki.name}（${sc.sekki.at.m}月${sc.sekki.at.d}日）` }
        ]
      });
    }

    const wSum = parts.reduce((a, p) => a + p.weight, 0);
    const score = wSum ? Math.round(parts.reduce((a, p) => a + p.score * p.weight, 0) / wSum) : null;
    return {
      kyusei: ky, shichu: sc, parts,
      score, grade: score == null ? null : gradeOf(score),
      adjust: score == null ? 0 : (Math.round((score - 60) * 0.2) || 0)   // ±約8点
    };
  }

  /** 物件固有スコアと相性スコアを合成する（表示用。基準スコアは書き換えない） */
  function combine(base, personal) {
    if (!personal || base.total == null) return null;
    const t = clamp(base.total + personal.adjust);
    return { baseTotal: base.total, adjust: personal.adjust,
             personalTotal: Math.round(t), grade: gradeOf(t), label: labelOf(t) };
  }

  /* ══════════════════════════════════════════════════════════
     9. 公開API
     ══════════════════════════════════════════════════════════ */
  global.FengshuiEngine = {
    version: "2.0.0",
    LEVELS, LEVEL_JP,
    categories, modules,
    defineCategory, defineModule,      // 項目の追加・差し替えはここから
    evaluate, evaluatePersonal, combine,
    deriveFortunes, averageFortunes, FORTUNE_MAP,
    gradeOf, labelOf,
    calendar: { fourPillars, kyusei, solarLon, termJD, eqTime, jdToParts },
    helpers: { dirOf, sanjuOf, DIR8, SANJU }
  };
})(typeof window !== "undefined" ? window : globalThis);
