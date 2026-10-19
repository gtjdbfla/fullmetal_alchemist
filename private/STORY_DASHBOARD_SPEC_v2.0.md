# FMA 동양편 — STORY DASHBOARD MASTER SPEC
## Version 2.0

# 1. Dashboard Mission

이 대시보드의 목적은 줄거리를 저장하는 것만이 아니다.

본편 집필 과정에서 지속적으로 다음 네 가지를 감시한다.

### CANON

> **기존 《강철의 연금술사》 단행본 설정과 충돌하지 않는가?**

### CHARACTER

> **원작 캐릭터가 후속편의 플롯 때문에 다른 사람이 되지 않는가?**

### CAUSALITY

> **이 작품 내부에서 사건이 충분한 원인과 과정을 거쳐 발생하는가?**

### FORESHADOWING

> **던진 질문·설정·사물·대사가 이후 제대로 회수되는가?**

이 네 축은 편의상 변경하지 않는다.

---

# 2. Story Constitution

모든 새로운 아이디어보다 아래 규칙이 우선한다.

## RULE 1

원작에서 끝난 캐릭터의 성장을 무효화하지 않는다.

## RULE 2

Edward의 alchemy는 절대 돌아오지 않는다.

## RULE 3

Edward는 끝까지 주인공이다.

## RULE 4

새로운 Father급 적이나 더 강한 초월적 존재를 만들지 않는다.

## RULE 5

Ishvala = Truth로 확정하지 않는다.

## RULE 6

정치적 집단을 하나의 인격처럼 표현하지 않는다.

## RULE 7

캐릭터가 주제를 설명하기 위해 작가의 대변인이 되지 않는다.

## RULE 8

사건은 가능한 한 악당의 계획 하나보다 여러 사람의 합리적 행동이 충돌해 발생하도록 한다.

## RULE 9

완벽한 정치적 해결을 만들지 않는다.

## RULE 10

**원작을 존중한다는 것은 원작을 반복한다는 뜻이 아니다.**

본편 경험 때문에 인물들이 이번에는 어떤 다른 선택을 하는지를 보여준다.

---

# 3. Canon Classification

모든 설정은 반드시 다음 중 하나의 상태를 가진다.

### CANON

원작에서 직접 확인.

### CANON_INFERENCE

원작 정보를 통해 비교적 강하게 추론 가능.

### ORIGINAL_COMPATIBLE

본 작품의 창작설정이지만 원작과 알려진 충돌 없음.

### SPECULATIVE

원작의 빈 공간에 적극적인 해석을 넣음.

### FALSE_THEORY

작품 속 인물이 믿지만 실제 설정으로 확정되지 않은 것.

### CANON_RISK

원작과 충돌할 가능성이 있어 검증 필요.

---

# 4. 주요 설정 Canon Registry

| Setting | Status |
|---|---|
| Ed loses ability to transmute | CANON |
| Scar brother studied Amestrian alchemy and Xing alkahestry | CANON |
| Ishvalans worship Ishvala | CANON |
| Bradley participated in Ishval conflict | CANON |
| Graus served as young lieutenant in Ishval | ORIGINAL_COMPATIBLE |
| Bradley personally saved Graus | ORIGINAL_COMPATIBLE |
| Graus later received Bradley decoration | ORIGINAL_COMPATIBLE |
| Ancient Ishval-Xing road | ORIGINAL_COMPATIBLE |
| Karsa | ORIGINAL_COMPATIBLE |
| red mineral / 적맥석 | ORIGINAL_COMPATIBLE |
| ancient Ishval flow interpretation | SPECULATIVE |
| Ishvala = Truth | FALSE_THEORY |
| A/B clans | ORIGINAL_COMPATIBLE |
| Brandt | ORIGINAL_COMPATIBLE |
| Second Ishval War | ORIGINAL_COMPATIBLE |

**FALSE_THEORY를 CANON처럼 서술하면 Critical Warning.**

---

# 5. Character Integrity Registry

## Edward

Must remain:

- impatient
- curious
- proud
- analytical
- direct
- argumentative
- fundamentally compassionate
- funny when irritated

Growth:

> “진리를 봤다.”

→

> **“진리를 봤다고 진리를 다 아는 것은 아니다.”**

→

> **“안다는 것과 어떻게 사용할지는 다르다.”**

Forbidden:

- alchemy restoration
- philosopher-like omniscience
- solving all politics
- chosen-one status

---

## Scar

Must remain:

- terse
- serious
- religious
- morally complicated
- unwilling to erase past

Growth:

> dead brother's revenge

→

> **dead brother's future**

Forbidden:

- complete forgiveness of Amestris
- sudden pacifism
- verbose philosophical lecturer
- sole representative of Ishval

---

## Mustang

Must remain:

- ambitious
- politically intelligent
- pragmatic
- responsible for his past
- capable of humor
- willing to use power

Growth:

> “좋은 지도자가 되겠다.”

→

> **“좋은 지도자가 필요해야만 하는 체제가 문제다.”**

Forbidden:

- guilt-only character
- instant democrat
- incompetent politician
- Messiah of Ishval

---

## Ling

Must remain:

- playful
- hungry
- politically sharp
- loyal
- willing to take risks

Growth:

> “황제가 되어 부족을 지킨다.”

→

> **“왜 부족을 지키기 위해 황제가 되어야 하지?”**

Forbidden:

- solemn generic emperor
- instant abolition of Xing
- personally deciding every region's future

---

## Al

No POV for now.

Must remain independent of Ed.

Research style:

**collaborative / listening / comparative.**

Al may reach conceptual insight earlier than Ed, but not because “Al is simply smarter.”

---

## Hawkeye

Must retain independent moral agency.

Bark killing must not be triumphant.

Her action means:

> **한 사람을 죽여 전쟁의 확대를 막는다.**

It does not erase her past.

---

# 6. Causality Engine

Every major plot event must have:

**CAUSE**

↓

**MOTIVATION**

↓

**DECISION**

↓

**ACTION**

↓

**IMMEDIATE CONSEQUENCE**

↓

**LONG-TERM CONSEQUENCE**

If two adjacent steps are missing, flag:

`CAUSALITY_GAP`

---

# 7. Example — Red Mineral Chain

Ancient Ishval cultural use

↓

Ed discovers red mineral

↓

identified as already-known rare mineral

↓

large Ishval deposits suspected

↓

Ed carries sample east for research

↓

Ed reaches western Xing trade city

↓

researchers recognize mineral

↓

Ed casually reveals Ishval quantity

↓

Ed reveals ancient route

↓

merchants connect mineral + transport cost + route

↓

route exits through A territory

↓

middleman realizes information value

↓

sells information to B

↓

B verifies information

↓

B fears A's future rise

↓

Kairan pressured

↓

Xing conflict.

Separate chain:

large deposits

↓

Amestrian industrial research accelerates

↓

existing alloy research expands

↓

experimental rifle

↓

field testing with Graus unit

↓

Bark uses rifle

↓

Ishvalan killed.

This entire chain must remain visible on dashboard.

---

# 8. Graus Causality Chain

Young lieutenant in Ishval

↓

unit nearly destroyed

↓

Bradley personally saves him

↓

Bradley later decorates him

↓

Bradley becomes personal ideal

↓

Promised Day occurs

↓

Graus lacks hidden truth

↓

interprets Mustang/Armstrong as forces that destroyed Bradley regime

↓

Mustang eventually gains supreme power

↓

Mustang supports Ishval

↓

Brandt contacts Graus

↓

normal investigation

↓

tension management

↓

selective neglect

↓

report exaggeration

↓

Mustang repeatedly resolves crisis

↓

Graus radicalizes

↓

studies original Ishval War

↓

“one bullet”

↓

plans controlled ignition

↓

Bark exceeds order

↓

actual war

↓

Graus loses control

↓

orders Bark to stop

↓

arrest/trial.

If Graus jumps directly from Brandt contact to war plan:

`CHARACTER_CAUSALITY_ERROR`.

---

# 9. Brandt Causality Chain

Hates military dictatorship

↓

accepts Mustang is better leader

↓

still rejects concentrated power

↓

fails to restrain Mustang through weak civilian institutions

↓

uses Graus to create political evidence

↓

underestimates Graus

↓

discovers war plan

↓

alerts Mustang side

↓

Mustang already in Ishval

↓

Brandt remains in Central

↓

worsening reports

↓

internal guilt/conflict

↓

drives toward Ishval

↓

sees consequences physically

↓

protects young soldier

↓

shot

↓

stops retaliatory fire

↓

death

↓

Mustang concludes system itself must change.

---

# 10. Knowledge Ledger

Every major character has a knowledge state.

Characters cannot know information without a transmission event.

Example:

## Ed early

KNOWS:
- own Truth experience
- Amestrian alchemy
- Al's question

DOES_NOT_KNOW:
- Karsa
- red mineral economic importance
- A/B politics
- Graus plot
- Ishvala answer

## Graus

KNOWS:
- Ishval War
- Bradley as soldier/leader
- Scar's violence
- visible Promised Day events
- Mustang's rise
- Ishval reconstruction

DOES_NOT_KNOW:
- Father's complete plan
- full Homunculus truth
- metaphysical Truth event
- symbolic significance of red-mineral rifle
- Ed's discovery chain

## Ling

Knowledge must update only through Xing channels or direct Ed contact.

## Al

Must not magically know Ed's journey.

---

# 11. Timeline Ledger

Every chapter stores:

`DATE`

`DAY_INDEX`

`LOCATION`

`POV`

`CHARACTERS_PRESENT`

`TRAVEL_STARTED`

`TRAVEL_COMPLETED`

`INFORMATION_RECEIVED`

`TIME_SINCE_PREVIOUS_EVENT`

Critical routes:

- Ed: Ishval → desert → Karsa → western Xing
- Scar: Karsa → Ishval
- Ling: capital → western territory
- Brandt: Central → Ishval
- commercial information: western city → B
- Al: Xing capital

If impossible:

`TIMELINE_ERROR`.

---

# 12. Foreshadowing State Machine

Every important clue receives one status:

`PLANNED`

→ `PLANTED`

→ `REINFORCED`

→ `PARTIAL_PAYOFF`

→ `PAYOFF`

Alternative final states:

`OPEN_MYSTERY`

`REMOVED`

`ABANDONED_ERROR`

No important clue may end in `ABANDONED_ERROR`.

---

# 13. Core Foreshadowing Ledger

| Foreshadow | Plant | Payoff |
|---|---|---|
| How Scar brother knew alkahestry | Ch1 | Karsa/Xing |
| Ishvala | Ch2 | late thematic resolution |
| Karsa source mark | Ch2 | Ch10 |
| red stones | Ch2 | Ch5 |
| Ishvala=Truth | Ch3 | Ch12 false-theory collapse |
| Adin | Ch6 | Ishval development debate |
| Zahir | Ch6 | Second Ishval War |
| young soldier | Ch6 | Ch31 |
| Brandt anti-dictatorship | Ch7 | Ch35 |
| old eastern route | Ch8 | Karsa/Xing trade |
| Karsa isolation | Ch9–12 | Ch38 |
| brother's view of Scar | Ch11 | Scar arc |
| Nadir road warning | Ch12 | Ch22/38 |
| red mineral sample east | Ch15 | Xing politics |
| trade-city conversation | Ch15 | B intelligence |
| information middleman | Ch16 | B reaction |
| Bradley saved Graus | Ch18 | Graus radicalization + Ch30 self-recognition |
| Kairan succession request | Ch20 | rebellion/reform |
| Al's alternate research question | early letters | Epilogue |
| experimental rifle | Ch23 or earlier | Ch28 |
| “one bullet” | Ch25 | Ch28 |
| Brandt guilt | Ch26–27 | Ch31–32 |
| Bark utilitarian cruelty | multiple | Ch28/30 |
| Hawkeye Ishval history | before Ch30 | Bark death |
| Karsa refuses road | Karsa arc | Ch38 |
| Winry letters | throughout | Epilogue |

---

# 14. Political Faction Registry

Never use `Ishval thinks...`.

Use:

### Ishval
- Development faction
- Preservation/religious faction
- Autonomy faction
- Independence faction
- violent hardliners

### A Clan
- Seiran / development
- Hazan / preservation
- undecided population

### B Clan
- Kairan
- elders
- hardliners
- ordinary population

### Amestris
- Mustang reformers
- civilian reformers
- old-regime military
- younger military
- bureaucracy
- business interests

This prevents political monoculture.

---

# 15. Information Propagation Rule

Important information must move through **people and institutions**, not narrative teleportation.

Example:

Ed tells western Xing researchers/merchants.

↓

middleman hears.

↓

middleman sells information.

↓

B receives.

↓

B verifies.

↓

Kairan receives report.

Not:

> “Soon all Xing knew.”

Every major information jump requires `TRANSMISSION_EVENT`.

---

# 16. Convenience Detector

Automatically flag scenes containing these structural problems:

### COINCIDENCE
Needed character happens to be present.

### SUDDEN_CHANGE
Political/character position changes without preparation.

### WHY_HERE
Character lacks reason to be at location.

### TOO_FAST
Technology, information, politics or travel moves unrealistically quickly.

### PROTAGONIST_PRIVILEGE
Ed knows or solves something only because he is protagonist.

### VILLAIN_PRIVILEGE
Antagonist succeeds because everyone else becomes stupid.

### SPEECHIFYING
Character suddenly delivers author's thesis rather than speaking naturally.

---

# 17. Mystery Management

Separate:

`QUESTION`

`CURRENT_HYPOTHESIS`

`EVIDENCE_FOR`

`EVIDENCE_AGAINST`

`FINAL_STATUS`

Example:

### ISHVALA

Question:
What did ancient Ishvalans mean by Ishvala?

Hypothesis 1:
Creator deity.

Hypothesis 2:
Truth/Gate entity.

Hypothesis 3:
religious interpretation of world/life flow.

Final status:

**Not yet locked.**

The dashboard must NEVER silently convert a hypothesis into fact.

---

# 18. Power-System Guardrails

No:

- Ed alchemy restoration
- superior Philosopher's Stone
- new God enemy
- “true alchemy” stronger than canon
- Karsa supermagic
- Ishvala combat power
- new Gate superpower

Karsa's techniques must be explainable as:

**prepared structures + accumulated knowledge + terrain.**

The sequel escalates **complexity**, not power level.

---

# 19. Chapter Card Schema

Every actual manuscript chapter must have:

```text
CHAPTER:
TITLE:

PRIMARY POV:
SECONDARY POV:

LOCATION:
DAY/TIME:

MAIN EVENT:

CHARACTER GOAL:
CHARACTER DECISION:
CHARACTER CHANGE:

NEW INFORMATION:

CANON REFERENCES:

NEW ORIGINAL LORE:

FORESHADOWING PLANTED:

FORESHADOWING REINFORCED:

PAYOFFS:

INFORMATION TRANSMISSIONS:

CAUSALITY FROM PREVIOUS CHAPTER:

CAUSALITY TO NEXT CHAPTER:

UNRESOLVED QUESTIONS:

CANON RISKS:

CHARACTER RISKS:

TIMELINE RISKS:

NOTES:
```

---

# 20. Manuscript Review Score

Each completed chapter scores 0–2.

| Category | Test |
|---|---|
| Canon | 원작과 충돌 없는가 |
| Character | 캐릭터다운가 |
| Motivation | 행동 이유가 있는가 |
| Causality | 사건이 자연스럽게 이어지는가 |
| Knowledge | 알 수 없는 정보를 아는가 |
| Timeline | 이동/시간이 맞는가 |
| Foreshadowing | 필요한 복선을 심었는가 |
| Payoff | 이전 떡밥을 회수했는가 |
| Theme | 전체 이야기와 연결되는가 |
| Entertainment | 실제로 재미있는가 |

20점.

18–20: PASS  
15–17: MINOR_REVISION  
12–14: MAJOR_REVISION  
0–11: HOLD

점수보다 감점 이유를 반드시 저장.

---

# 21. Dashboard Critical Alerts

### 🔴 CANON CONFLICT
원작과 직접 충돌.

### 🟠 CHARACTER DRIFT
캐릭터 정체성 훼손.

### 🟡 CAUSALITY GAP
사건 사이 원인 부족.

### 🔵 UNPAID FORESHADOWING
장기간 방치된 중요 떡밥.

### 🟣 KNOWLEDGE ERROR
알 수 없는 정보 사용.

### 🟤 TIMELINE ERROR
시간/이동 불가능.

### ⚫ THEME OVERRIDE
캐릭터가 작가의 철학을 말하기 위해 행동함.

### 🟧 WORLD REACTION GAP
엄청난 사건이 발생했는데 사회·경제·정치적 반응이 없음.

이 마지막 경고도 추가하는 게 좋다.

적맥석, Second Ishval War, Mustang의 정치개혁 정도의 사건은 반드시 주변 세계에 파장이 있어야 한다.

---

# 22. Final Arc Validation

최종부에 들어가기 전에 다음을 검사한다.

### Edward

- Ishvala=Truth 가설 붕괴 완료?
- 지식의 결과 경험?
- 자기비난이 아니라 책임의식으로 성장?
- alchemy 여전히 없음?

### Scar

- brother knowledge → brother future 전환?
- Ishval 내부 다양성 인정?
- revenge logic에서 벗어나되 과거를 잊지 않음?

### Mustang

- benevolent paternalism 경험?
- Second Ishval War?
- Brandt death?
- good dictator → system reform 인과 충분?

### Ling

- Kairan mirror 충분?
- A/B 갈등 충분?
- emperor-system question 충분?
- reform이 갑작스럽지 않음?

### Graus

- Bradley relationship planted?
- Mustang resentment understandable?
- gradual radicalization?
- Bark stopping believable?

### Brandt

- democratic ideals?
- own contradiction?
- Graus mistake?
- hesitation?
- voluntary trip?
- death not absolution?

---

# 23. Ending State Matrix

## CLOSED

- Scar brother's alkahestry route
- Karsa connection
- red-mineral information chain
- B conspiracy
- Graus conspiracy
- Bark
- Second Ishval War
- Brandt arc
- Mustang's core political conclusion
- Ling's core political conclusion

## TRANSITIONING

- Amestrian democracy
- Ishval autonomy/status
- Xing decentralization
- red-mineral governance
- new trade corridor

## OPEN BY DESIGN

- exact metaphysical identity of Ishvala
- precise relationship between Truth / flow / Dragon's Pulse
- Ed and Al's future research

Rule:

> **미스터리는 남겨도 된다. 플롯은 버리면 안 된다.**

---

# 24. Central Thematic Matrix

대시보드에서 이 네 줄은 항상 보이게 한다.

**Edward**

> **모든 것을 알 필요는 없다.**

**Scar**

> **과거를 잊지 않는 것과 과거를 반복하는 것은 다르다.**

**Ling**

> **모든 것을 다스릴 필요는 없다.**

**Mustang**

> **모든 것을 결정할 필요는 없다.**

그리고 작품 전체:

> **힘을 가졌다는 것은 다른 사람을 대신해 결정할 권리를 얻었다는 뜻이 아니다.**

한 단계 더 정확한 최종형:

> **그러나 결정하지 않는 것 역시 책임회피가 될 수 있다.**

따라서 좋은 지도자의 역할은:

> **정답을 대신 선택하는 것이 아니라, 누가 결정해야 하는지를 정당하게 결정할 수 있는 구조를 만드는 것.**

---

# 25. Dashboard Top-Level Workflow

실제 집필은 항상 다음 순서로 진행한다.

**MASTER STORYLINE**

↓

**현재 Chapter Beat 확인**

↓

**Canon 필요한 부분 확인**

↓

**Character State 확인**

↓

**Knowledge State 확인**

↓

**Timeline 확인**

↓

**필요한 Foreshadowing 확인**

↓

**본편 작성**

↓

**Canon Review**

↓

**Character Review**

↓

**Causality Review**

↓

**Knowledge/Timeline Review**

↓

**Foreshadowing Ledger 업데이트**

↓

**Character State 업데이트**

↓

**World State 업데이트**

↓

**다음 Chapter 준비**

---

## 최종적으로 대시보드 구조는 이렇게 잡으면 돼

```text
FMA EASTERN ARC
│
├── STORY CONSTITUTION
│
├── MASTER STORYLINE
│
├── CHAPTERS
│
├── CHARACTERS
│   ├── Edward
│   ├── Scar
│   ├── Mustang
│   ├── Ling
│   ├── Alphonse
│   ├── Hawkeye
│   ├── Brandt
│   ├── Graus
│   ├── Bark
│   └── ...
│
├── CANON REGISTRY
│
├── LORE REGISTRY
│
│   ├── Ishvala
│   ├── Karsa
│   ├── Red Mineral
│   └── Ancient Road
│
├── FACTIONS
│
├── TIMELINE
│
├── LOCATIONS
│
├── KNOWLEDGE LEDGER
│
├── FORESHADOWING LEDGER
│
├── CAUSALITY GRAPH
│
├── MYSTERY TRACKER
│
├── WORLD STATE
│
└── REVIEW / ALERTS
```
