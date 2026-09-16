# CIS Lab 홈페이지

- 사이트: https://hs54kwon.github.io/cislab/
- al-folio (Jekyll) 기반. GitHub Actions가 빌드해서 `gh-pages`로 배포합니다.

`main`에 push하면 2~3분 뒤 자동 반영됩니다.

---

## 어디를 고치나

| 하고 싶은 일 | 파일 |
|---|---|
| 논문 추가 | `_bibliography/papers.bib` |
| 구성원 추가·수정 | `_data/people.yml` |
| 공지 올리기 | `_news/YYYY-MM-DD-이름.md` |
| 홈 소개글 | `_pages/about.md` |
| 연구 주제 | `_pages/research.md` |
| 학회 등급·배지 색 | `_data/venues.yml` |
| 글자 크기·색·여백 | `_sass/_custom.scss` |
| 사이트 주소·제목 | `_config.yml` |

---

## 논문 추가

`_bibliography/papers.bib` 맨 위에 붙이면 됩니다. 정렬·연도 묶기·DOI 버튼은 자동입니다.

```bibtex
@inproceedings{kwon2027example,
  abbr      = {ACM CCS},
  title     = {제목},
  author    = {Kwon, Hyunsoo and Park, Sangkyoung},
  booktitle = {ACM Conference on Computer and Communications Security},
  year      = {2027},
  doi       = {10.1145/...},
  selected  = {true}
}
```

- `abbr`은 `_data/venues.yml`에 같은 키가 있어야 색과 등급 마커가 붙습니다.
- `selected = {true}`는 홈 노출. 4~5편만 유지하세요.
- `%` 주석은 **엔트리 바깥에만**. 중괄호 안에 넣으면 파서가 깨집니다.

## 구성원 추가

`_data/people.yml`의 그룹(`faculty` `phd` `ms` `undergrad` `alumni`) 아래에 추가합니다.

```yaml
  - name: Gildong Hong
    role: M.S. Student
    year: 2027
    email: id@inha.ac.kr
    topic: 연구 주제
    image: gildong.jpg      # assets/img/people/ 에 정사각형 사진
```

- `name` 외에는 전부 선택. **값이 없으면 줄을 지우세요.** 빈 값으로 두면 안 됩니다.
- 여기 이름이 있으면 publications에서 자동으로 파란색 표시됩니다.

## 공지

`_news/`의 파일 하나가 공지 하나입니다.

```yaml
---
layout: post
date: 2026-09-15 10:00:00+0900
inline: true          # true=짧은 한두 문장 / false=긴 글, title 필수
related_posts: false
---

본문
```

- `inline: true` → 홈과 Notice 양쪽에 본문 그대로
- `inline: false` → 홈에는 제목만, Notice에는 전문. 논문·과제 공지에 쓰세요.
- 홈은 최근 5개만 (`_pages/about.md`의 `announcements.limit`)

문장 틀:

- 논문: `Our paper on {짧은 주제} {is accepted to|was presented at|appears in} {VENUE} {year}.`
- 새 구성원: `{이름} joins the lab as {소속}. Welcome, {이름}!`

---

## 관리 도구 (git 없이 업데이트)

`tools/admin.bat` 더블클릭 → 브라우저에 폼이 뜹니다.

| 탭 | 하는 일 |
|---|---|
| 논문 | DOI 넣고 "불러오기" → Crossref에서 제목·저자·학회·연도 자동 입력 → `papers.bib`에 추가 |
| 구성원 | 그룹 고르고 이름/역할/이메일 입력 → `people.yml`에 추가·수정·삭제. 사진은 **파일 선택**하면 EXIF를 지우고 크기를 줄여 자동 저장 |
| 공지 | 날짜·형식 고르고 본문 작성 → `_news/`에 파일 생성 |

아래 **사이트에 반영** 버튼을 누르면 빌드를 먼저 돌려보고, 성공했을 때만 commit + push
합니다. 빌드가 깨지면 push하지 않고 오류를 보여줍니다. 2~3분 뒤 사이트에 나옵니다.

- 127.0.0.1에서만 열리고 외부에서 접속할 수 없습니다.
- 인터넷으로 나가는 건 DOI 조회(Crossref)와 git push뿐입니다. 제3자 서비스에 리포
  권한을 주지 않습니다.
- `people.yml`은 통째로 다시 쓰지 않고 해당 항목만 갈아끼우므로 **주석이 유지됩니다.**
- 저장 전에 YAML을 먼저 파싱해봅니다. 깨지면 파일을 건드리지 않습니다.
- 사진은 비율을 유지한 채 긴 변 980px로 줄이고, **EXIF를 통째로 지웁니다.** 카메라 사진의
  GPS 좌표가 실수로 공개되는 것을 막기 위해서입니다.
- PyYAML과 Pillow가 필요합니다: `pip install pyyaml pillow`

세밀한 수정(연구 주제 글, 디자인, 등급 마커)은 여전히 파일을 직접 고치세요.

## 로컬 미리보기

WSL Ubuntu에 Ruby 환경이 설치돼 있습니다.

```bash
wsl -d Ubuntu -- bash -lc 'cd /mnt/d/codexWorkspace/cislab-site && \
  export PATH="$HOME/.local/share/gem/ruby/3.2.0/bin:$PATH" && \
  bundle exec jekyll serve --host 0.0.0.0'
# http://localhost:4000/cislab/
```

파일을 고치면 자동으로 다시 빌드됩니다.

## push

```bash
cd D:\codexWorkspace\cislab-site
git add -A
git commit -m "메시지"
git push
```

`main`은 보호돼 있습니다. 교수님(admin)은 직접 push할 수 있고, 나머지는 PR을 거칩니다.
PR마다 빌드가 자동 검증되고 실패하면 머지가 막힙니다.

학생은 권한 없이 fork → 수정 → PR 하면 됩니다.
방장 권한: Settings → Collaborators → Add people → `Write`.

---

## 커스텀 도메인 (전산실 승인 후)

요청 내용: 호스트 `cislab.inha.ac.kr` / 종류 **CNAME** / 값 `hs54kwon.github.io`

승인되면 **순서대로** 하세요. `baseurl`을 안 비우면 CSS와 링크가 전부 깨집니다.

1. `nslookup cislab.inha.ac.kr`로 레코드 확인
2. `_config.yml` 수정
   ```yaml
   url: https://cislab.inha.ac.kr
   baseurl:
   ```
3. 리포 루트에 `CNAME` 파일 생성 (내용 한 줄: `cislab.inha.ac.kr`)
4. push 후 Settings → Pages에서 `Enforce HTTPS` 켜기

---

## 주의

- `_pages/research.md`에 **진행 중인 연구의 구체적 내용을 쓰지 마세요.** 수치, 벤더·제품
  이름, 논문 시스템 이름은 double-blind 심사와 책임 공개 일정에 걸립니다.
- 빌드 시 뜨는 `legacy bootstrap-marked content ... bib.liquid:182` 경고는 테마 원본
  코드 때문이며 무해합니다.
- gem에서 복사해 온 파일은 `_layouts/bib.liquid`와 `_includes/footer.liquid` 둘뿐입니다.
  테마를 업그레이드하면 이 둘을 확인하세요.
