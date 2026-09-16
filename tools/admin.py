#!/usr/bin/env python3
"""
CIS Lab site admin.

A small local tool so routine updates do not need git. It serves a form on
127.0.0.1, writes the same files a person would edit by hand, and then builds
and pushes. Nothing is sent anywhere except the Crossref lookup and the git
push, and no third party is given access to the repository.

Run:  tools/admin.bat      (or: python tools/admin.py)
"""

import http.server
import json
import os
import re
import socketserver
import subprocess
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML이 필요합니다:  pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
BIB = ROOT / "_bibliography" / "papers.bib"
PEOPLE = ROOT / "_data" / "people.yml"
VENUES = ROOT / "_data" / "venues.yml"
NEWS = ROOT / "_news"
PORT = 8899

GROUPS = [
    ("faculty", "Faculty"),
    ("phd", "Ph.D. / Integrated"),
    ("ms", "M.S."),
    ("undergrad", "Undergraduate"),
    ("alumni", "Alumni"),
]


# ---------------------------------------------------------------- helpers


def run(cmd, cwd=ROOT, timeout=900):
    p = subprocess.run(
        cmd, cwd=str(cwd), capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=timeout, shell=isinstance(cmd, str),
    )
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def jekyll_build():
    """Build through WSL, which is where the Ruby toolchain lives."""
    wsl_root = "/mnt/" + str(ROOT).replace("\\", "/").replace(":", "").lower()[0] \
               + str(ROOT).replace("\\", "/")[2:]
    cmd = (
        'wsl -d Ubuntu -- bash -lc "cd {} && '
        'export PATH=\\"$HOME/.local/share/gem/ruby/3.2.0/bin:$PATH\\" && '
        'JEKYLL_ENV=production bundle exec jekyll build"'
    ).format(wsl_root)
    return run(cmd)


def load_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def slugify(s):
    s = re.sub(r"[^\w\s-]", "", s.lower())
    return re.sub(r"[\s_]+", "-", s).strip("-")[:48] or "notice"


# ------------------------------------------------------------ bib writing


def bib_keys():
    txt = BIB.read_text(encoding="utf-8")
    return set(re.findall(r"^@(?!string)\w+\{([^,]+),", txt, re.M))


def make_key(authors, year, title):
    last = "lab"
    if authors:
        last = re.split(r"[,\s]+", authors.split(" and ")[0].strip())[0]
    word = next((w for w in re.sub(r"[^\w\s]", " ", title).split()
                 if len(w) > 4 and w.lower() not in
                 {"towards", "toward", "study", "analysis", "empirical"}), "paper")
    base = f"{last.lower()}{year}{word.lower()}"
    key, n = base, 2
    existing = bib_keys()
    while key in existing:
        key, n = f"{base}{n}", n + 1
    return key


def append_paper(d):
    """Insert a new entry directly above the first existing one."""
    fields = [("abbr", d["abbr"]), ("title", d["title"]), ("author", d["author"])]
    entry_type = "inproceedings" if d["kind"] == "conference" else "article"
    if d["kind"] == "conference":
        fields.append(("booktitle", d["venue"]))
    else:
        fields.append(("journal", d["venue"]))
        for f in ("volume", "number", "pages"):
            if d.get(f):
                fields.append((f, d[f]))
    fields.append(("year", d["year"]))
    if d.get("doi"):
        fields.append(("doi", d["doi"]))
    if d.get("note"):
        fields.append(("note", d["note"]))
    if d.get("selected"):
        fields.append(("selected", "true"))

    key = make_key(d["author"], d["year"], d["title"])
    width = max(len(k) for k, _ in fields)
    body = ",\n".join(f"  {k.ljust(width)} = {{{v}}}" for k, v in fields)
    block = f"@{entry_type}{{{key},\n{body}\n}}\n\n"

    txt = BIB.read_text(encoding="utf-8")
    m = re.search(r"^% -+ \d{4} -+$", txt, re.M)
    at = m.start() if m else txt.index("@", txt.index("---", 3))
    BIB.write_text(txt[:at] + block + txt[at:], encoding="utf-8")
    return key


# ------------------------------------------------------------- API handler


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, obj, code=200):
        raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        if self.path.startswith("/api/state"):
            people = load_yaml(PEOPLE)
            venues = load_yaml(VENUES)
            rc, out = run(["git", "status", "--porcelain"])
            news = sorted((p.name for p in NEWS.glob("*.md")), reverse=True)
            return self._send({
                "groups": GROUPS,
                "people": {g: (people.get(g) or []) for g, _ in GROUPS},
                "venues": sorted(venues.keys()),
                "papers": len(bib_keys()),
                "news": news,
                "dirty": [l for l in out.splitlines() if l.strip()],
                "today": date.today().isoformat(),
            })
        raw = HTML.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        d = json.loads(self.rfile.read(n) or b"{}")
        try:
            return self._send(self.dispatch(self.path, d))
        except Exception as e:
            return self._send({"ok": False, "msg": f"{type(e).__name__}: {e}"}, 200)

    def dispatch(self, path, d):
        if path == "/api/doi":
            return self.api_doi(d)
        if path == "/api/paper":
            key = append_paper(d)
            return {"ok": True, "msg": f"papers.bib에 추가했습니다 (key: {key})"}
        if path == "/api/member":
            return self.api_member(d)
        if path == "/api/news":
            return self.api_news(d)
        if path == "/api/build":
            rc, out = jekyll_build()
            bad = [l for l in out.splitlines()
                   if re.search(r"\b(error|fatal|Liquid Exception)\b", l, re.I)]
            return {"ok": rc == 0 and not bad,
                    "msg": "빌드 성공" if rc == 0 and not bad else "빌드 실패",
                    "log": "\n".join(bad) or out[-1500:]}
        if path == "/api/publish":
            return self.api_publish(d)
        return {"ok": False, "msg": "알 수 없는 요청"}

    def api_doi(self, d):
        doi = (d.get("doi") or "").strip()
        doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi)
        if not doi:
            return {"ok": False, "msg": "DOI를 입력하세요"}
        req = urllib.request.Request(
            "https://api.crossref.org/works/" + urllib.parse.quote(doi),
            headers={"User-Agent": "cislab-admin/1.0 (mailto:hskwon@inha.ac.kr)"})
        try:
            m = json.load(urllib.request.urlopen(req, timeout=25))["message"]
        except urllib.error.HTTPError:
            return {"ok": False, "msg": "Crossref에 해당 DOI가 없습니다"}
        auth = " and ".join(
            f"{a.get('family','')}, {a.get('given','')}".strip(", ")
            for a in m.get("author", []))
        parts = (m.get("published") or m.get("issued") or {}).get("date-parts", [[None]])[0]
        return {"ok": True, "msg": "Crossref에서 불러왔습니다", "data": {
            "title": (m.get("title") or [""])[0],
            "author": auth,
            "venue": (m.get("container-title") or [""])[0],
            "year": str(parts[0] or ""),
            "volume": str(m.get("volume") or ""),
            "number": str(m.get("issue") or ""),
            "pages": (m.get("page") or "").replace("-", "--"),
            "doi": m.get("DOI", doi),
            "kind": "journal" if m.get("type", "").startswith("journal") else "conference",
        }}

    def api_member(self, d):
        """Edit people.yml as text.

        A yaml round-trip would drop every comment in the file, and those
        comments carry the romanization status and the instructions students
        follow. So the entry is spliced in and out by hand instead.
        """
        raw = PEOPLE.read_text(encoding="utf-8")
        lines = raw.splitlines(keepends=True)
        group, name = d["group"], d["name"].strip()

        # span of this group: its key line to the next top-level key
        try:
            gi = next(i for i, l in enumerate(lines) if l.startswith(group + ":"))
        except StopIteration:
            return {"ok": False, "msg": f"people.yml에 {group} 그룹이 없습니다"}
        gj = next((i for i in range(gi + 1, len(lines))
                   if re.match(r"^[A-Za-z_]+:", lines[i])), len(lines))

        # An empty group is written `ms: []`. List items cannot follow that, so
        # the inline marker has to go before anything is added under it.
        if not d.get("remove") and re.match(r"^" + re.escape(group) + r":\s*\[\s*\]",
                                            lines[gi]):
            lines[gi] = group + ":\n"

        # drop an existing entry with the same name
        removed = False
        i = gi + 1
        while i < gj:
            if re.match(r"^\s*-\s+name:\s*" + re.escape(name) + r"\s*(#.*)?$", lines[i]):
                j = i + 1
                while j < gj and not re.match(r"^\s*-\s", lines[j])                         and not re.match(r"^[A-Za-z_]+:", lines[j])                         and lines[j].strip() != "":
                    j += 1
                del lines[i:j]
                gj -= (j - i)
                removed = True
                continue
            i += 1

        if d.get("remove"):
            if not removed:
                return {"ok": False, "msg": f"{name} 을(를) 찾지 못했습니다"}
            out = "".join(lines)
            try:
                yaml.safe_load(out)
            except yaml.YAMLError as e:
                return {"ok": False, "msg": "YAML이 깨져서 저장하지 않았습니다",
                        "log": str(e)[:600]}
            PEOPLE.write_text(out, encoding="utf-8")
            return {"ok": True, "msg": f"{name} 삭제"}

        fields = [("name", name)]
        for f in ("role", "year", "email", "topic", "degree", "now",
                  "homepage", "scholar", "github", "image"):
            if d.get(f):
                fields.append((f, str(d[f]).strip()))
        nl = "\n"
        block = f"  - name: {name}{nl}" + "".join(
            f"    {k}: {v}{nl}" for k, v in fields[1:])

        # insert at the end of the group, before any trailing blank lines
        at = gj
        while at > gi + 1 and lines[at - 1].strip() == "":
            at -= 1
        lines.insert(at, block)
        out = "".join(lines)
        # Parse before writing. Writing first and validating after leaves a
        # broken file on disk when anything goes wrong.
        try:
            yaml.safe_load(out)
        except yaml.YAMLError as e:
            return {"ok": False, "msg": "YAML이 깨져서 저장하지 않았습니다",
                    "log": str(e)[:600]}
        PEOPLE.write_text(out, encoding="utf-8")
        return {"ok": True, "msg": ("수정" if removed else "추가") + f": {name}"}

    def api_news(self, d):
        when = d.get("date") or date.today().isoformat()
        inline = bool(d.get("inline"))
        title = (d.get("title") or "").strip()
        if not inline and not title:
            return {"ok": False, "msg": "긴 공지는 제목이 필요합니다"}
        slug = slugify(title or d.get("body", "")[:40])
        fm = [f"date: {when} 10:00:00+0900"]
        if not inline:
            fm.insert(0, f"title: {title}")
        path = NEWS / f"{when}-{slug}.md"
        path.write_text(
            "---\nlayout: post\n" + "\n".join(fm)
            + f"\ninline: {'true' if inline else 'false'}\nrelated_posts: false\n---\n\n"
            + d.get("body", "").strip() + "\n", encoding="utf-8")
        return {"ok": True, "msg": f"{path.name} 생성"}

    def api_publish(self, d):
        msg = (d.get("message") or "Update site content").strip()
        rc, out = run(["git", "add", "-A"])
        rc, out = run(["git", "commit", "-m", msg])
        if rc != 0 and "nothing to commit" in out:
            return {"ok": False, "msg": "변경된 내용이 없습니다"}
        if rc != 0:
            return {"ok": False, "msg": "commit 실패", "log": out[-1200:]}
        rc, out2 = run(["git", "push", "origin", "main"])
        if rc != 0:
            return {"ok": False, "msg": "push 실패", "log": out2[-1200:]}
        return {"ok": True,
                "msg": "push 완료. 2~3분 뒤 사이트에 반영됩니다.",
                "log": out2[-600:]}


HTML = r"""<!doctype html>
<meta charset="utf-8"><title>CIS Lab 사이트 관리</title>
<style>
 :root{--bd:#d8dbe0;--mut:#6b7280;--accent:#00539b;--bg:#fff;--fg:#1f2328}
 @media(prefers-color-scheme:dark){:root{--bd:#33373d;--mut:#9aa1aa;--accent:#5aa2dd;--bg:#16181b;--fg:#e6e8ea}}
 *{box-sizing:border-box}
 body{font:15px/1.6 system-ui,'Malgun Gothic',sans-serif;margin:0;background:var(--bg);color:var(--fg)}
 header{padding:18px 26px;border-bottom:1px solid var(--bd);display:flex;align-items:baseline;gap:14px}
 h1{font-size:17px;margin:0}
 .sub{color:var(--mut);font-size:13px}
 nav{display:flex;gap:6px;padding:14px 26px 0}
 nav button{font:inherit;padding:8px 16px;border:1px solid var(--bd);border-bottom:none;
   background:transparent;color:var(--mut);border-radius:6px 6px 0 0;cursor:pointer}
 nav button.on{color:var(--fg);border-color:var(--bd);background:var(--bg);font-weight:600;
   box-shadow:inset 0 2px 0 var(--accent)}
 main{border-top:1px solid var(--bd);padding:22px 26px 90px;max-width:820px}
 section{display:none} section.on{display:block}
 label{display:block;margin:12px 0 4px;font-size:13px;color:var(--mut)}
 input,select,textarea{font:inherit;width:100%;padding:8px 10px;border:1px solid var(--bd);
   border-radius:6px;background:var(--bg);color:var(--fg)}
 textarea{min-height:110px;resize:vertical}
 .row{display:flex;gap:12px}.row>*{flex:1}
 .chk{display:flex;align-items:center;gap:8px;margin-top:14px}
 .chk input{width:auto}
 button.go{font:inherit;margin-top:18px;padding:9px 18px;border:0;border-radius:6px;
   background:var(--accent);color:#fff;cursor:pointer;font-weight:600}
 button.ghost{background:transparent;color:var(--accent);border:1px solid var(--accent)}
 button:disabled{opacity:.5;cursor:default}
 .bar{position:fixed;left:0;right:0;bottom:0;background:var(--bg);border-top:1px solid var(--bd);
   padding:12px 26px;display:flex;gap:10px;align-items:center}
 .bar input{flex:1}
 #msg{padding:10px 14px;border-radius:6px;margin-top:16px;display:none;white-space:pre-wrap;font-size:14px}
 #msg.ok{display:block;background:#e7f4ea;color:#14532d}
 #msg.err{display:block;background:#fdecec;color:#7f1d1d}
 pre{background:rgba(127,127,127,.12);padding:10px;border-radius:6px;overflow:auto;font-size:12px;max-height:220px}
 .list{border:1px solid var(--bd);border-radius:6px;margin-top:10px}
 .list div{padding:7px 12px;border-bottom:1px solid var(--bd);display:flex;justify-content:space-between;gap:10px}
 .list div:last-child{border:0}
 .list small{color:var(--mut)}
 .hint{color:var(--mut);font-size:12px;margin-top:4px}
</style>
<header><h1>CIS Lab 사이트 관리</h1><span class="sub" id="stat"></span></header>
<nav>
 <button class="on" data-t="paper">논문</button>
 <button data-t="member">구성원</button>
 <button data-t="news">공지</button>
</nav>
<main>
 <section id="paper" class="on">
  <label>DOI 로 불러오기</label>
  <div class="row"><input id="doi" placeholder="10.1145/3719027.3765215">
   <button class="go ghost" style="flex:0 0 120px;margin:0" onclick="fetchDoi()">불러오기</button></div>
  <div class="hint">제목·저자·학회·연도·페이지를 Crossref에서 채웁니다. DOI가 없으면 직접 입력하세요.</div>
  <label>제목</label><input id="p_title">
  <label>저자 <span class="hint">Family, Given and Family, Given</span></label><input id="p_author">
  <div class="row">
   <div><label>종류</label><select id="p_kind"><option value="conference">학회</option><option value="journal">저널</option></select></div>
   <div><label>배지 (venues.yml)</label><select id="p_abbr"></select></div>
   <div><label>연도</label><input id="p_year"></div>
  </div>
  <label>학회/저널 정식명</label><input id="p_venue">
  <div class="row">
   <div><label>Volume</label><input id="p_volume"></div>
   <div><label>Number</label><input id="p_number"></div>
   <div><label>Pages</label><input id="p_pages"></div>
  </div>
  <div class="row">
   <div><label>DOI</label><input id="p_doi"></div>
   <div><label>Note (예: To appear, Poster)</label><input id="p_note"></div>
  </div>
  <div class="chk"><input type="checkbox" id="p_sel"><label style="margin:0">홈 화면에 표시 (selected)</label></div>
  <button class="go" onclick="addPaper()">papers.bib에 추가</button>
 </section>

 <section id="member">
  <div class="row">
   <div><label>그룹</label><select id="m_group" onchange="renderPeople()"></select></div>
   <div><label>이름 (영문)</label><input id="m_name"></div>
  </div>
  <div class="row">
   <div><label>role</label><input id="m_role" placeholder="Undergraduate Student"></div>
   <div><label>year</label><input id="m_year"></div>
  </div>
  <div class="row">
   <div><label>email</label><input id="m_email"></div>
   <div><label>image <span class="hint">assets/img/people/</span></label><input id="m_image"></div>
  </div>
  <label>topic</label><input id="m_topic">
  <div class="row" id="alumni_only" style="display:none">
   <div><label>degree <span class="hint">M.S. 2025</span></label><input id="m_degree"></div>
   <div><label>now <span class="hint">Samsung Research</span></label><input id="m_now"></div>
  </div>
  <button class="go" onclick="saveMember(0)">저장</button>
  <button class="go ghost" onclick="saveMember(1)">이 이름 삭제</button>
  <div class="hint">같은 이름이 있으면 덮어씁니다. 파일의 주석은 그대로 유지됩니다.</div>
  <div class="list" id="m_list"></div>
 </section>

 <section id="news">
  <div class="row">
   <div><label>날짜</label><input id="n_date" type="date"></div>
   <div><label>형식</label><select id="n_inline" onchange="toggleNews()">
     <option value="1">짧은 공지 (홈에 본문 그대로)</option>
     <option value="0">긴 공지 (홈엔 제목만, Notice에 전문)</option></select></div>
  </div>
  <div id="n_title_wrap" style="display:none"><label>제목</label><input id="n_title"></div>
  <label>본문</label><textarea id="n_body" placeholder="Our paper on ... is accepted to ..."></textarea>
  <div class="hint">논문: Our paper on {주제} {is accepted to|was presented at|appears in} {VENUE} {year}.<br>
   새 구성원: {이름} joins the lab as {소속}. Welcome, {이름}!</div>
  <button class="go" onclick="addNews()">공지 만들기</button>
  <div class="list" id="n_list"></div>
 </section>

 <div id="msg"></div>
 <div id="log"></div>
</main>
<div class="bar">
 <button class="go ghost" style="margin:0" onclick="doBuild()">빌드 확인</button>
 <input id="cmsg" placeholder="커밋 메시지">
 <button class="go" style="margin:0" id="pub" onclick="doPublish()">사이트에 반영</button>
</div>
<script>
let S={};
const $=id=>document.getElementById(id);
document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{
  document.querySelectorAll('nav button').forEach(x=>x.classList.toggle('on',x===b));
  document.querySelectorAll('section').forEach(s=>s.classList.toggle('on',s.id===b.dataset.t));
});
function say(ok,m,log){const e=$('msg');e.className=ok?'ok':'err';e.textContent=m;
  $('log').innerHTML=log?'<pre>'+log.replace(/[<&]/g,c=>c=='<'?'&lt;':'&amp;')+'</pre>':'';}
async function api(p,d){const r=await fetch(p,{method:'POST',body:JSON.stringify(d||{})});return r.json();}
async function load(){
  S=await (await fetch('/api/state')).json();
  $('stat').textContent=`논문 ${S.papers}편 · 공지 ${S.news.length}건`+(S.dirty.length?` · 미반영 변경 ${S.dirty.length}건`:'');
  $('p_abbr').innerHTML=S.venues.map(v=>`<option>${v}</option>`).join('');
  $('m_group').innerHTML=S.groups.map(g=>`<option value="${g[0]}">${g[1]}</option>`).join('');
  $('n_date').value=S.today;
  renderPeople();
  $('n_list').innerHTML=S.news.slice(0,8).map(n=>`<div><span>${n}</span></div>`).join('');
}
function renderPeople(){
  const g=$('m_group').value;
  $('alumni_only').style.display=g==='alumni'?'flex':'none';
  $('m_list').innerHTML=(S.people[g]||[]).map(m=>
    `<div><span>${m.name}</span><small>${m.role||m.degree||''}</small></div>`).join('')
    ||'<div><small>비어 있음</small></div>';
}
function toggleNews(){$('n_title_wrap').style.display=$('n_inline').value==='0'?'block':'none';}
async function fetchDoi(){
  const r=await api('/api/doi',{doi:$('doi').value});
  if(!r.ok)return say(0,r.msg);
  for(const[k,v]of Object.entries(r.data)){
    if(k==='kind')$('p_kind').value=v; else if($('p_'+k))$('p_'+k).value=v;}
  say(1,r.msg);
}
async function addPaper(){
  const d={kind:$('p_kind').value,abbr:$('p_abbr').value,title:$('p_title').value,
    author:$('p_author').value,venue:$('p_venue').value,year:$('p_year').value,
    volume:$('p_volume').value,number:$('p_number').value,pages:$('p_pages').value,
    doi:$('p_doi').value,note:$('p_note').value,selected:$('p_sel').checked};
  if(!d.title||!d.author||!d.year)return say(0,'제목·저자·연도는 필수입니다');
  const r=await api('/api/paper',d); say(r.ok,r.msg); if(r.ok)load();
}
async function saveMember(rm){
  const d={group:$('m_group').value,name:$('m_name').value,role:$('m_role').value,
    year:$('m_year').value,email:$('m_email').value,image:$('m_image').value,
    topic:$('m_topic').value,degree:$('m_degree').value,now:$('m_now').value,remove:!!rm};
  if(!d.name)return say(0,'이름을 입력하세요');
  const r=await api('/api/member',d); say(r.ok,r.msg); if(r.ok)load();
}
async function addNews(){
  const r=await api('/api/news',{date:$('n_date').value,inline:$('n_inline').value==='1',
    title:$('n_title').value,body:$('n_body').value});
  say(r.ok,r.msg); if(r.ok){$('n_body').value='';$('n_title').value='';load();}
}
async function doBuild(){say(1,'빌드 중...');const r=await api('/api/build',{});say(r.ok,r.msg,r.log);}
async function doPublish(){
  $('pub').disabled=true; say(1,'빌드 확인 중...');
  const b=await api('/api/build',{});
  if(!b.ok){$('pub').disabled=false;return say(0,'빌드가 실패해서 반영하지 않았습니다',b.log);}
  say(1,'push 중...');
  const r=await api('/api/publish',{message:$('cmsg').value||'Update site content'});
  say(r.ok,r.msg,r.log); $('pub').disabled=false; load();
}
load();
</script>
"""


def main():
    os.chdir(ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as srv:
        url = f"http://127.0.0.1:{PORT}/"
        print(f"CIS Lab 사이트 관리 도구\n  {url}\n  종료: 이 창에서 Ctrl+C")
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            print("\n종료")


if __name__ == "__main__":
    main()
