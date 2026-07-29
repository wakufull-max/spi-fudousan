# -*- coding: utf-8 -*-
"""475件をエンジンで評価し、スコア入りのデータを作る"""
import json, subprocess
props = json.load(open("props.json"))

script = """
require('/mnt/user-data/outputs/fengshui-engine.js');
require('/mnt/user-data/outputs/subjects.js');
const E=FengshuiEngine;
const props=JSON.parse(require('fs').readFileSync('/home/claude/build/props.json','utf8'));
const out=props.map(p=>{
  const w = p.wardId ? Subjects.byId(p.wardId) : null;
  // 区の地相を土台に、建物固有の値を載せる
  const s = {
    id:p.id, name:p.name, level:"building",
    town:p.ward, ward:(p.pref==="東京都"?p.ward:p.city+p.ward),
    price:p.price,
    terrain: w ? JSON.parse(JSON.stringify(w.terrain)) : {},
    history: w ? JSON.parse(JSON.stringify(w.history)) : {},
    environment: w ? JSON.parse(JSON.stringify(w.environment)) : {},
    building: { facing:p.deg, builtYear:p.built }
  };
  const r = E.evaluate(s);
  const f = E.deriveFortunes(r);
  return Object.assign({}, p, {
    total:r.total, grade:r.grade, label:r.label,
    cov: r.coverage!=null ? Math.round(r.coverage*100) : null,
    f: f.map(x=>({id:x.id,l:x.label,s:x.score})),
    era: (r.modules.find(m=>m.id==="building.era")||{}).score,
    dir: E.helpers.dirOf(p.deg).n,
    sanju: E.helpers.sanjuOf(p.deg).name
  });
});
console.log(JSON.stringify(out));
"""
res = subprocess.run(["node","-e",script], capture_output=True, text=True)
if res.returncode: print(res.stderr[:1500]); raise SystemExit(1)
data = json.loads(res.stdout)
json.dump(data, open("props_scored.json","w"), ensure_ascii=False)

tk = [d for d in data if d["pref"]=="東京都"]
ot = [d for d in data if d["pref"]!="東京都"]
print(f"評価完了 {len(data)} 件")
print(f"  東京23区  平均 {sum(d['total'] for d in tk)/len(tk):.1f}点  データ充足率 {tk[0]['cov']}%")
print(f"  その他都市 平均 {sum(d['total'] for d in ot)/len(ot):.1f}点  データ充足率 {ot[0]['cov']}%")
print()
print("■ 東京23区 上位10件")
for d in sorted(tk, key=lambda x:-x["total"])[:10]:
    print(f"  {d['grade']:>2s} {d['total']:3d}  {d['name'][:24]:26s} {d['ward']:5s} {d['price']:>11s} {d['dir']}向き")
print()
print("■ 方角ごとの平均点（九運の反映を確認）")
import collections
g=collections.defaultdict(list)
for d in tk: g[d["dir"]].append(d["total"])
for k in ["南","北","南西","北東","東","南東","西","北西"]:
    if g[k]: print(f"  {k:3s} {sum(g[k])/len(g[k]):5.1f}点  ({len(g[k])}件)")
