/**
 * render.js — 評価結果の描画コンポーネント
 *
 * エンジンが返す result オブジェクトだけを入力に取る。
 * ページ側は「どこに描くか」を指定するだけでよい。
 */
(function (global) {
  "use strict";
  const esc = s => String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const bar = (v, cls) =>
    `<span class="bar ${cls || ""}"><i style="width:${Math.max(0, Math.min(100, v))}%"></i></span>`;

  /* 。 総合スコアのヘッダー 。 */
  function scoreHeader(r, opts) {
    opts = opts || {};
    const cov = Math.round(r.coverage * 100);
    const warn = cov < 55
      ? `<div class="cov-warn">データ充足率が ${cov}％です。この階層では判定できない項目が
         ${r.coverageDetail.outOfScope} 件あり、総合点は評価済みの項目のみで算出しています。
         より細かい階層（町丁目・建物）ほど精度が上がります。</div>` : "";
    return `
    <div class="sc-head">
      <div class="sc-main">
        <div class="sc-g">${r.grade}</div>
        <div class="sc-n">${r.total}<small>点</small></div>
        <div class="sc-meta">
          <span class="sc-lab">${r.label}</span>
          <span class="sc-lv">${esc(r.subject.name)}／${r.subject.levelJP}単位の評価</span>
        </div>
      </div>
      <div class="sc-cov">
        <div class="cov-row"><span>データ充足率</span><b>${cov}%</b></div>
        ${bar(cov, "gold")}
        <div class="cov-detail">
          評価済 ${r.coverageDetail.evaluated}
          ／ 階層対象外 ${r.coverageDetail.outOfScope}
          ／ 未取得 ${r.coverageDetail.noData}
          （全 ${r.coverageDetail.total} 項目）
        </div>
      </div>
      ${warn}
    </div>`;
  }

  /* 。 カテゴリ別 。 */
  function categories(r) {
    const rows = r.categories.map(c => {
      if (c.score == null) return `
        <div class="cat off">
          <div class="cat-h"><span class="cat-n">${c.label}<em>${c.en}</em></span>
            <span class="cat-s">判定対象外</span></div>
          ${bar(0)}
          <div class="cat-f">この階層では評価できません</div>
        </div>`;
      return `
        <div class="cat">
          <div class="cat-h"><span class="cat-n">${c.label}<em>${c.en}</em></span>
            <span class="cat-s">${c.score}</span></div>
          ${bar(c.score, c.score >= 70 ? "up" : c.score < 50 ? "down" : "")}
          <div class="cat-f">配点 ${c.weight}%　／　総合への寄与 ${c.contribution ?? "—"} 点
            ${c.coverage < 1 ? `　／　この分類の充足率 ${Math.round(c.coverage * 100)}%` : ""}</div>
        </div>`;
    }).join("");
    return `<div class="cats">${rows}</div>`;
  }

  /* 。 強み・弱み 。 */
  function highlights(r) {
    const item = (x, dir) => `
      <li class="${dir}">
        <span class="hl-l">${esc(x.label)}</span>
        <span class="hl-s">${x.score}</span>
        <span class="hl-i">${x.impact > 0 ? "+" : ""}${x.impact}</span>
      </li>`;
    return `
    <div class="hl">
      <div class="hl-col">
        <h4 class="hl-h up">強み<em>Strengths</em></h4>
        <ul>${r.strengths.length ? r.strengths.map(x => item(x, "up")).join("")
          : '<li class="none">中立を上回る項目がありません</li>'}</ul>
      </div>
      <div class="hl-col">
        <h4 class="hl-h down">弱み<em>Weaknesses</em></h4>
        <ul>${r.weaknesses.length ? r.weaknesses.map(x => item(x, "down")).join("")
          : '<li class="none">中立を下回る項目はありません</li>'}</ul>
      </div>
    </div>
    <p class="hl-note">数値は「中立50からの乖離 × 実効重み」で算出した総合点への影響度です。
      点数の高低ではなく、総合点をどれだけ押し上げ／押し下げているかを示します。</p>`;
  }

  /* 。 全項目（理由と根拠つき） 。 */
  function modules(r, opts) {
    opts = opts || {};
    const byCat = r.categories.map(c => {
      const items = c.modules.map(m => {
        const off = m.status !== "ok";
        const badge = m.status === "ok" ? `<span class="m-s">${m.score}</span>`
          : m.status === "out_of_scope"
            ? `<span class="m-s off">階層対象外</span>`
            : `<span class="m-s off">未取得</span>`;
        const ev = (m.evidence || []).map(e =>
          `<tr><th>${esc(e.label)}</th><td>${esc(e.value)}</td></tr>`).join("");
        return `
        <details class="m ${off ? "off" : ""}">
          <summary>
            <span class="m-n">${esc(m.label)}<em>${esc(m.en || "")}</em></span>
            ${off ? "" : bar(m.score, m.score >= 70 ? "up" : m.score < 50 ? "down" : "")}
            ${badge}
            <span class="m-w">重み ${m.weight}${m.effectiveWeight ? `／実効 ${m.effectiveWeight}` : ""}</span>
          </summary>
          <div class="m-body">
            <p class="m-why"><b>なぜこの評価か</b>${esc(m.reason)}</p>
            ${ev ? `<table class="m-ev"><caption>根拠データ</caption>${ev}</table>` : ""}
            <div class="m-lv">判定可能な最小階層：${FengshuiEngine.LEVEL_JP[m.minLevel]}</div>
          </div>
        </details>`;
      }).join("");
      return `<section class="mgroup"><h4>${c.label}<em>${c.en}</em>
        <span class="mg-w">配点 ${c.weight}%</span></h4>${items}</section>`;
    }).join("");
    return `<div class="mods">${byCat}</div>`;
  }

  /* 。 相性レイヤー 。 */
  function personal(p, comb) {
    if (!p) return "";
    const parts = p.parts.map(x => `
      <details class="m">
        <summary>
          <span class="m-n">${esc(x.label)}</span>
          ${bar(x.score, x.score >= 70 ? "up" : x.score < 50 ? "down" : "")}
          <span class="m-s">${x.score}</span>
          <span class="m-w">重み ${x.weight}</span>
        </summary>
        <div class="m-body">
          <p class="m-why"><b>なぜこの評価か</b>${esc(x.reason)}</p>
          <table class="m-ev"><caption>根拠データ</caption>
            ${x.evidence.map(e => `<tr><th>${esc(e.label)}</th><td>${esc(e.value)}</td></tr>`).join("")}
          </table>
        </div>
      </details>`).join("");
    const c = comb ? `
      <div class="comb">
        <span>物件固有 <b>${comb.baseTotal}</b></span>
        <span class="op">${comb.adjust >= 0 ? "+" : ""}${comb.adjust}</span>
        <span>あなたの総合 <b class="big">${comb.personalTotal}</b> <em>${comb.grade}</em></span>
      </div>
      <p class="hl-note">相性は物件固有スコアには合算していません。物件そのものの評価は誰が見ても同じ値であるべきだからです。
        上の合成値は表示専用で、基準スコアは書き換えません。</p>` : "";
    return `<div class="pers">${c}${parts}</div>`;
  }


  /* 。 運気バランス（4軸ダイヤ） 。 */
  function fortuneRadar(f, avg, grade, label) {
    const CX = 210, CY = 188, R = 108;
    const v = id => (f.find(x => x.id === id) || {}).score || 0;
    const a = id => (avg ? (avg.find(x => x.id === id) || {}).score || 0 : 0);
    const poly = (w, c, r2, v2) =>
      `${CX},${(CY - R * w / 100).toFixed(1)} ${(CX + R * c / 100).toFixed(1)},${CY} ` +
      `${CX},${(CY + R * r2 / 100).toFixed(1)} ${(CX - R * v2 / 100).toFixed(1)},${CY}`;
    let grid = "";
    [25, 50, 75, 100].forEach(k => { grid += `<polygon points="${poly(k,k,k,k)}" fill="none" stroke="#E6E3DC"/>`; });
    const dots = [[CX, CY - R * v("wealth") / 100], [CX + R * v("career") / 100, CY],
                  [CX, CY + R * v("romance") / 100], [CX - R * v("vitality") / 100, CY]]
      .map(([x, y]) => `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="4.2" fill="#fff" stroke="#1D1C1A" stroke-width="1.6"/>`).join("");
    const lab = (id, x, y, anchor) => {
      const o = f.find(z => z.id === id) || {};
      return `<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="12.5" fill="#5C5852">${o.label}</text>
              <text x="${x}" y="${y + 21}" text-anchor="${anchor}" font-family="Shippori Mincho B1,serif"
                    font-size="19" font-weight="700" fill="#1D1C1A">${o.score ?? "—"}</text>`;
    };
    return `<div class="balance">
      <div class="p-k">FORTUNE BALANCE</div>
      <h3 class="p-t">運気バランス</h3>
      <svg viewBox="0 0 420 372" class="bal-svg" role="img" aria-label="運気バランス">
        ${grid}
        <line x1="${CX}" y1="${CY-R}" x2="${CX}" y2="${CY+R}" stroke="#F0EEE9"/>
        <line x1="${CX-R}" y1="${CY}" x2="${CX+R}" y2="${CY}" stroke="#F0EEE9"/>
        ${avg ? `<polygon points="${poly(a("wealth"),a("career"),a("romance"),a("vitality"))}"
                 fill="none" stroke="#928D85" stroke-width="1.3" stroke-dasharray="5 4"/>` : ""}
        <polygon points="${poly(v("wealth"),v("career"),v("romance"),v("vitality"))}"
                 fill="rgba(29,28,26,.07)" stroke="#1D1C1A" stroke-width="2"/>
        ${dots}
        <circle cx="${CX}" cy="${CY}" r="45" fill="#FAF9F7" stroke="#EDEAE3"/>
        <text x="${CX}" y="${CY+5}" text-anchor="middle" font-family="Shippori Mincho B1,serif"
              font-size="27" font-weight="700" fill="#A8905F">${grade}</text>
        <text x="${CX}" y="${CY+24}" text-anchor="middle" font-size="10" fill="#928D85">${label}</text>
        ${lab("wealth", CX, 22, "middle")}
        ${lab("career", 410, 182, "end")}
        ${lab("romance", CX, 338, "middle")}
        ${lab("vitality", 10, 182, "start")}
      </svg>
      ${avg ? `<div class="legend"><span><i></i>この対象</span><span><i class="d"></i>23区平均</span></div>` : ""}
    </div>`;
  }

  /* 。 4運の内訳（グラデーションバー＋23区平均マーカー） 。 */
  function fortuneRows(f, avg) {
    const lab = n => n >= 88 ? "非常に良い" : n >= 78 ? "好調" : n >= 70 ? "普通" : n >= 60 ? "やや低め" : "低め";
    const hex2rgb = h => [parseInt(h.slice(1,3),16), parseInt(h.slice(3,5),16), parseInt(h.slice(5,7),16)];
    return `<div class="brk">${f.map(x => {
      const v = x.score || 0;
      const a = avg ? ((avg.find(z => z.id === x.id) || {}).score || 0) : null;
      const [r,g,b] = hex2rgb(x.color);
      return `<div class="brow">
        <div class="brow-h">
          <span class="bn">${x.label}<em>${x.en}</em></span>
          <span class="bv">${x.score ?? "—"}</span>
          <span class="btag">${x.score == null ? "—" : lab(v)}</span>
        </div>
        <div class="gbar">
          <i style="width:${v}%;background:linear-gradient(90deg,
             rgba(${r},${g},${b},.22) 0%, rgba(${r},${g},${b},.55) 55%, rgba(${r},${g},${b},.95) 100%)"></i>
          ${a ? `<span class="avg" style="left:${a}%"></span>` : ""}
        </div>
      </div>`; }).join("")}
      <p class="brk-note">※ 0〜100 の目安値／縦線＝23区平均</p></div>`;
  }

  /* 。 3カラムの評価パネル 。 */
  function fortunePanel(r, f, avg, desc, ctaHref) {
    return `<div class="panel">
      <section class="p-col">
        <div class="p-k">OVERALL FORTUNE</div>
        <div class="ov-main">
          <span class="ov-g">${r.grade}</span>
          <span class="ov-n">${r.total}<small>/100</small></span>
        </div>
        <span class="ov-pill">${r.label}</span>
        <p class="ov-d">${esc(desc)}</p>
        <a class="ov-cta" href="${ctaHref || "#"}">無料で相性を診断する　→</a>
      </section>
      <section class="p-col">
        ${fortuneRadar(f, avg, r.grade, r.label)}
      </section>
      <section class="p-col">
        <div class="p-k">BREAKDOWN</div>
        <h3 class="p-t">4つの運気</h3>
        ${fortuneRows(f, avg)}
      </section>
    </div>`;
  }

  /* 。 公開用サマリー（配点や根拠データは出さない） 。 */
  function publicSummary(r) {
    const li = (x, d) => `<li class="${d}"><span class="hl-l">${esc(x.label)}</span></li>`;
    return `<div class="hl">
      <div class="hl-col"><h4 class="hl-h up">この土地の強み<em>Strengths</em></h4>
        <ul>${r.strengths.length ? r.strengths.map(x => li(x, "up")).join("") : '<li class="none">—</li>'}</ul></div>
      <div class="hl-col"><h4 class="hl-h down">注意したい点<em>Points to note</em></h4>
        <ul>${r.weaknesses.length ? r.weaknesses.map(x => li(x, "down")).join("")
          : '<li class="none">大きな減点要因はありません</li>'}</ul></div>
    </div>`;
  }

  /* 。 Googleマップ埋め込み 。 */
  function gmap(query, label) {
    const q = encodeURIComponent(query);
    return `<div class="gmap">
      <iframe src="https://maps.google.com/maps?q=${q}&output=embed&hl=ja&z=16"
        loading="lazy" referrerpolicy="no-referrer-when-downgrade"
        title="${esc(label || query)}の地図"></iframe>
    </div><div class="gmap-c">所在地：${esc(query)}</div>`;
  }

  global.FengshuiRender = { scoreHeader, categories, highlights, modules, personal,
    fortuneRadar, fortuneRows, fortunePanel, publicSummary, gmap, bar, esc };
})(typeof window !== "undefined" ? window : globalThis);
