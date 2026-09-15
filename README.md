# CIS Lab 홈페이지

인하대학교 컴퓨터공학과 Computer & Intelligence Security Lab 홈페이지 소스입니다.
[al-folio](https://github.com/alshedivat/al-folio) (Jekyll) 기반이며 GitHub Pages로 배포됩니다.

기존 Google Sites(`sites.google.com/inha.ac.kr/cislab`)를 대체하기 위한 초안입니다.
**아직 공개 전이며, 아래 "공개 전 체크리스트"를 먼저 처리해야 합니다.**

---

## 어디를 고치면 되나

| 하고 싶은 일 | 고칠 파일 |
|---|---|
| 논문 추가 | `_bibliography/papers.bib` |
| 랩 구성원 추가·수정 | `_data/people.yml` |
| 공지 올리기 | `_news/YYYY-MM-DD-제목.md` 새로 만들기 |
| 연구 주제 | `_pages/research.md` |
| 홈 소개글 | `_pages/about.md` |
| 연구 주제 설명 | `_pages/research.md` |
| 학생 모집 안내 | `_pages/join.md` |
| 사이트 제목·주소·푸터 | `_config.yml` |
| 학회 배지 색 | `_data/venues.yml` |

| 디자인·글자 크기·색 | `_sass/_custom.scss` |
| 학회 등급 표시 | `_data/venues.yml` |

레이아웃은 al-folio gem 안에 있습니다. 예외는 `_layouts/bib.liquid` 하나뿐입니다 (아래 참고).

### 논문 한 편 추가하기

`_bibliography/papers.bib` 맨 위에 한 덩어리 붙이면 끝입니다. 정렬·연도 묶기·링크 생성은 자동입니다.

```bibtex
@inproceedings{kwon2027example,
  abbr        = {ACM CCS},
  title       = {제목},
  author      = {Kwon, Hyunsoo and Park, Sangkyoung},
  booktitle   = {ACM Conference on Computer and Communications Security (ACM CCS)},
  year        = {2027},
  doi         = {10.1145/...},
  selected    = {true},
  bibtex_show = {true}
}
```

- `abbr` 값은 `_data/venues.yml`에 같은 키가 있어야 색이 붙습니다. 없으면 회색으로 나옵니다.
- `selected = {true}`는 홈 화면 노출입니다. 4~5편만 유지하세요.
- PDF·코드·슬라이드를 걸려면 `pdf = {파일명.pdf}`(→`assets/pdf/`), `code = {https://...}`, `slides = {...}`를 추가합니다.
- **`%` 주석은 엔트리 바깥에만 쓰세요.** 중괄호 안에 넣으면 파서가 깨집니다.

### 학생이 자기 프로필 올리기

이게 이 사이트로 옮기는 주된 이유입니다. 교수님이 전부 쓰지 않아도 됩니다.

1. 리포를 fork 하거나 브랜치를 팝니다.
2. `_data/people.yml`에서 자기 그룹(`phd`/`ms`/`undergrad`) 아래에 블록을 추가합니다.
3. 정사각형 사진을 `assets/img/people/`에 넣습니다. (없어도 됩니다)
4. PR을 올립니다. CI가 자동으로 빌드를 돌려 깨지지 않는지 확인해줍니다.

`name` 외의 필드는 전부 선택입니다. **값이 없으면 줄 자체를 지우세요.**
빈 값으로 남기면 예전 Google Sites처럼 `E-mail:` 라벨만 덩그러니 나오는 게 아니라,
아예 렌더링되지 않도록 템플릿을 짜두었습니다.

---

## 공개 전 체크리스트

### 반드시 확인이 필요한 것 (내용 정확성)

- [ ] **`_data/people.yml`의 학생 이메일·입학연도** — 소속 구분은 확정했습니다(이지용: 석박사통합, 박상경: 학부연구생). 이메일과 입학연도가 아직 비어 있습니다.
- [ ] **`papers.bib`의 `TODO(doi)` 12곳** — 기존 사이트에 DOI가 없던 항목입니다. 지어내지 않고 비워뒀습니다. `TODO(doi)` 로 grep 하면 나옵니다.
- [ ] **`kim2022darkweb`의 페이지 범위** — 기존 사이트에 `pp. 70078-10091`로 적혀 있어 `70078--70091`로 고쳤습니다. 원문 확인 부탁드립니다.
- [ ] **`_news/`의 `[TODO]` 2건** — S&P 2027 accept 날짜, 과제 공식 명칭/과제번호/시작일.
- [ ] **`_pages/join.md` 맨 아래** — 현재 모집 상태와 대학원 입시 일정.

`TODO` 로 전체 grep 하면 남은 항목이 전부 나옵니다.

```bash
grep -rn "TODO" _bibliography _data _pages _news
```

### 저자명 표기 통일 (이미 반영함)

기존 사이트에서 같은 사람이 다르게 적혀 있던 것을 아래로 통일했습니다. 틀린 쪽이 있으면 알려주세요.

| 기존 표기 | 통일한 표기 | 근거 |
|---|---|---|
| Daeyeong / Daeyoung Kim | **Daeyoung Kim** | 5회 대 1회 |
| Jongmin Jung / Jongmin Jeong | **Jongmin Jeong** | 국내논문 저자 `정종민` |
| Dongyoug / Dongyoung Koo | **Dongyoung Koo** | 오타 |
| Hyungjun / Hyungjune Shin | **Hyungjune Shin** | 국내논문 저자 `신형준` |
| Jeju Isalnd | **Jeju Island** | 오타, 2곳 |

### 학회/저널 등급 표시

배지 아래에 마커가 최대 두 개 붙습니다. `_data/venues.yml`에서 **학회당 한 번만** 지정하며
논문마다 손댈 필요가 없습니다.

| 필드 | 역할 | 값 예시 |
|---|---|---|
| `tier` | 진한 마커 | 학회 `Top-tier` / 저널 `Q1` |
| `rank` | 흐린 마커 | 학회 `BK 4` / 저널 `Top 10%` |

현재 값 (2026-09-15 확인):

| 학회·저널 | tier | rank |
|---|---|---|
| IEEE S&P, ACM CCS | Top-tier | BK 4 |
| USENIX Security | Top-tier | BK 3 (현재 포스터뿐이라 화면에는 안 보임) |
| IEEE CLOUD | (없음) | BK 1 |
| ACM CSUR | Q1 | Top 1% |
| IEEE TDSC, TIFS, TSC, IoT-J | Q1 | Top 10% |
| IJIS | Q1 | (퍼센타일 없음) |

- **배지 색은 종류만 나타냅니다** — 파랑 `#00539b`는 학회, 슬레이트 `#5a6b7a`는 저널.
  등급은 아래 마커가 담당하므로 색을 여러 개 쓸 이유가 없습니다.
- 포스터 2건은 `tier = {none}`으로 **두 마커 모두** 자동 제외됩니다.
- 값이 없는 학회는 마커가 안 붙습니다. 확인 안 된 값을 채우지 마세요.
- USENIX Security는 현재 포스터 1건뿐이라 마커가 안 보입니다. BK 3은 나중에 정식 논문이
  실릴 때 자동으로 붙도록 미리 적어둔 값입니다.

### Impact Factor 표기는 전부 제거했습니다

기존 사이트의 IF 값은 2019~2021년 기준이라 현재 수치와 맞지 않고(TSC 11.019는 지금 5점대),
`BK IF`는 국내 지표라 해외 방문자에게 의미가 전달되지 않습니다.
위의 Q1/퍼센타일 마커가 그 역할을 대신합니다.

### 검색 기능은 꺼져 있습니다

`search_enabled: false`, `bib_search: false`. Ctrl+K 오버레이와 논문 목록 위의
"Type to filter" 입력창이 여기서 나오던 것입니다. 사이트가 작아 굳이 필요하지 않습니다.
다시 켜려면 `_config.yml`에서 둘 다 `true`로 바꾸면 됩니다.

### 연구실 학생 표시

publications에서 **`_data/people.yml`에 이름이 있는 사람은 자동으로 볼드** 처리됩니다.
교수님 이름은 기존대로 밑줄(jekyll-scholar의 `author_is_self`)이라 구분됩니다.

학생을 명단에 추가하면 그 학생의 논문이 전부 자동으로 표시되므로, 따로 관리할 목록이
없습니다. 졸업생을 `alumni`에 남겨두면 그들의 논문도 계속 표시됩니다.

### Notice와 News의 관계

둘은 같은 `_news/` 폴더를 씁니다. 파일의 `inline:` 값이 차이를 만듭니다.

| `inline` | 길이 | Home | Notice |
|---|---|---|---|
| `true` | 한두 문장 | 최근 5개만 표시 | 전부, 본문 그대로 |
| `false` | 길어도 됨 (`title:` 필수) | 제목만 | 제목 링크 → 별도 페이지 |

길게 쓸 공지는 `inline: false`에 `title:`을 주면 자체 페이지가 생깁니다.
Home의 5개 제한은 `_pages/about.md`의 `announcements.limit`입니다.

### 미공개 연구를 research 페이지에 쓸 때

진행 중인 연구는 **주제 수준으로만** 적어뒀습니다. 수치, 대상 벤더 이름, 시스템/도구 이름,
구체적 공격 절차는 전부 뺐습니다. 이유는 아래 "공개 전 주의" 항목을 보세요.

### news 작성 규칙

논문 제목을 그대로 쓰면 너무 길어집니다. 아래 틀을 쓰세요.

> **Our {paper|survey} on {짧은 주제} {is accepted to|was presented at|appears in} {VENUE} {year}.**

- 주제는 3~5단어로. `package attestation`, `certificate revocation`,
  `certificate validation in in-app browsers` 정도.
- 전체 제목은 publications 페이지가 담당합니다.
- 주어는 항상 `Our`로 통일. (`Our work` / `Our paper` 혼용 금지)
- 학생 이름은 축하 문장에서만.

### 디자인 커스터마이징

`_sass/_custom.scss` 한 파일에 모여 있고, `assets/css/main.scss`에서 **맨 마지막에**
로드되므로 gem을 건드리지 않고 테마를 덮어씁니다.

- **강조색**: 인하대 블루 `#00539B` (다크모드는 대비 확보를 위해 `#5AA2DD`).
  al-folio 기본값은 형광 마젠타 `#b509ac`였습니다.
- **글자 크기**: 페이지 제목이 Bootstrap 기본값으로 데스크톱에서 ~50px까지 커지던 것을
  clamp로 고정했고, 본문은 0.95rem / line-height 1.7로 조정했습니다.
- **소셜 아이콘**: 테마 기본이 `font-size: 4rem`(64px)이라 홈 하단을 점령하고 있었습니다.
- **본문 색**: 논문 뒤 학회명·연월은 기본 텍스트 색입니다. 회색은 연도 구분선에만 씁니다.
- **위로가기 버튼**: 푸터가 Bootstrap `.fixed-bottom`(z-index 1030)이라 버튼(z-index 10,
  bottom 30px)을 덮고 있었습니다. `bottom: 70px` / `z-index: 1031`로 띄웠습니다.
- 되돌리려면 `_sass/_custom.scss`에서 해당 블록만 지우면 됩니다. 각 블록에 왜 넣었는지
  주석이 달려 있습니다.

빌드할 때 `legacy bootstrap-marked content detected ... _layouts/bib.liquid:182` 경고가
뜹니다. gem 원본 코드의 Bootstrap 4 잔재(annotation 팝오버)이며, 우리가 그 파일을 복사해
왔기 때문에 우리 쪽 줄번호로 표시될 뿐입니다. 해당 기능을 쓰지 않으므로 무해합니다.

gem에서 복사해 온 오버라이드 파일은 **두 개뿐**입니다 (al_folio_core 1.0.15 기준).
gem을 올릴 때 이 둘이 낡지 않았는지 확인하세요. 추가·수정한 부분은 전부 주석으로
표시해뒀습니다.

- `_layouts/bib.liquid` — 등급 마커, 연구실 학생 볼드 처리
- `_includes/footer.liquid` — 저작권에서 개인 이름 제거, last updated를 별도 줄로 분리

---

## ⚠ 공개 전 주의: 미공개 연구 노출

`_pages/research.md`에 진행 중인 연구 4건(코딩 에이전트, OAuth 2.1/DPoP, 모바일 포렌식,
GPU 부채널)을 넣었습니다. **주제 수준으로만 쓰고 아래는 의도적으로 제외했습니다.**

- 성공률 등 모든 수치
- 대상 벤더·제품 이름 (Anthropic, OpenAI, Auth0, 모델명 등)
- 논문에서 붙인 시스템 이름 (double-blind 심사에서 신원 노출 위험)
- 공격 절차의 구체적 내용

**공개 전에 확인하세요.**

1. **Double-blind 심사** — S&P, CCS, USENIX 등은 이중맹검입니다. 랩 페이지에 주제를
   자세히 적으면 심사위원이 검색으로 저자를 특정할 수 있습니다. 투고 중인 주제는
   심사가 끝날 때까지 빼두는 것도 방법입니다.
2. **책임 공개 일정** — 벤더에 통보한 취약점은 공개 합의 기간이 끝나기 전에 웹사이트에
   올리면 안 됩니다. 코딩 에이전트 건과 Auth0 가용성 영향 건이 여기 해당합니다.
3. **암호화 트래픽 연구** — 아직 공개 불가라고 하셔서 "deep learning을 도구로 쓴
   네트워크 트래픽 보안 분석" 수준으로만 적었습니다.

문단을 통째로 빼려면 `_pages/research.md`에서 해당 `##` 절만 지우면 됩니다.

## 배포

### 1. GitHub organization 만들기

개인 계정 말고 **organization**으로 만드세요. 나중에 학생에게 권한을 주거나 후임에게 넘길 때 훨씬 간단합니다.

- 예: `inha-cislab`
- 리포 이름: `inha-cislab.github.io` (조직 페이지 → 루트 주소로 서빙)

### 2. 올리기

```bash
git remote add origin https://github.com/inha-cislab/inha-cislab.github.io.git
git push -u origin main
```

Settings → Pages → Source를 **Deploy from a branch → `gh-pages` / `(root)`** 로 지정합니다.
(`.github/workflows/deploy.yml`이 빌드해서 `gh-pages` 브랜치로 밀어줍니다.)

첫 빌드는 3~5분 걸립니다. Actions 탭에서 결과를 확인하세요.

### 3. 도메인

`_config.yml`의 `url`이 현재 `https://inha-cislab.github.io` 로 되어 있습니다.

교내 전산실에 **`cislab.inha.ac.kr` CNAME**을 요청해두시면 좋습니다.
승인되면 `inha.ac.kr` 도메인을 유지한 채 GitHub Pages로 서빙할 수 있어서, 주소 변경 충격이 거의 없어집니다.

- 요청 내용: `cislab.inha.ac.kr` → `inha-cislab.github.io` (CNAME 레코드)
- 승인 후: 리포 루트에 `CNAME` 파일 생성(내용 한 줄 `cislab.inha.ac.kr`), `_config.yml`의 `url`도 같이 수정

### 4. 기존 Google Sites 처리

Google Sites는 301 리다이렉트를 걸 수 없습니다. 지우지 마시고 **안내 페이지 한 장으로 남기세요.**

- 본문을 전부 지우고 "CIS Lab has moved to <새 주소>" 한 줄 + 링크만 남깁니다
- 하위 페이지(About/People/Publications/Notice)는 삭제하거나 같은 안내로 교체
- 논문에 기존 주소를 적어 보내신 적이 있다면 최소 1~2년은 유지하는 게 안전합니다

---

## 로컬 미리보기

이 PC는 **WSL Ubuntu 24.04 + Ruby 3.2.3**으로 이미 세팅해뒀습니다.
gem은 `vendor/bundle/`(D드라이브, git 추적 제외)에 들어 있습니다. sudo 없이 동작합니다.

```bash
wsl -d Ubuntu -- bash -lc 'cd /mnt/d/codexWorkspace/cislab-site &&   export PATH="$HOME/.local/share/gem/ruby/3.2.0/bin:$PATH" &&   bundle exec jekyll serve --host 0.0.0.0'
# http://localhost:4000
```

`--watch`가 기본이라 파일을 고치면 자동으로 다시 빌드됩니다. 빌드는 약 1.6초.

한 번만 빌드하려면 `bundle exec jekyll build` (결과물은 `_site/`).

### ImageMagick 경고

로컬 빌드에서 `convert: not found` 경고가 납니다. 이미지의 webp 축소본을 만드는
단계인데, 설치에 sudo가 필요해서 생략했습니다. **빌드는 정상 완료되고**, GitHub
Actions에는 ImageMagick이 설치되므로 실제 배포본에는 영향이 없습니다.
없애고 싶으면 `sudo apt install imagemagick` 한 번 하시면 됩니다.

---

## 이 초안에서 al-folio 원본과 달라진 점

- 데모 콘텐츠 제거: `_posts`(33개 예시 글), `_projects`, `_books`, `_teachings`, Einstein 관련 페이지, 예시 이미지
- 워크플로 22개 → `deploy.yml` 1개만 유지 (나머지는 템플릿 자체 유지보수용이라 이 리포에서는 실패하거나 Actions 시간만 소모)
- `_pages/profiles.md`(1인용 프로필 레이아웃)를 **`_pages/people.md`로 교체** — `_data/people.yml`에서 렌더링하는 랩 명단 형태
- `_pages/research.md`, `_pages/join.md` 신규 작성
- 논문 배지에서 Altmetric / Dimensions / InspireHEP 비활성화, Google Scholar만 유지
- `external_sources` 비활성화 — 원본 설정이 al-folio의 Medium 피드와 Google AI 블로그 글을
  우리 사이트로 끌어오고 있었습니다 (첫 빌드에서 실제로 `blog/2024/google-gemini-...` 페이지가 생성됨)
- `max_author_limit` 해제 — 3명에서 잘려서 7인 공저 논문(KICS 2017)에서 교수님 이름이
  "and 4 more authors"에 가려졌습니다

업스트림 al-folio 업데이트를 가져오고 싶으면:

```bash
git remote add upstream https://github.com/alshedivat/al-folio.git
git fetch upstream && git merge upstream/main
```

`_pages/`, `_data/`, `_bibliography/`는 우리가 새로 쓴 파일이라 충돌이 거의 없습니다.
