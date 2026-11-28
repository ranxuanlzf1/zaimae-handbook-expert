---
name: zaimae-live-check
description: "Controlled live verification layer for the ZaiMei v2/v3 handbook. Load when the school is not in the handbook's 607-school tables, when a city is outside the 532-city index, when handbook data must be checked against the current academic year, or when the user asks for an official page / current policy. Governs WebSearch and WebFetch use, official-domain whitelists, source labelling and conflict handling. Never writes results back into handbook references."
---

# 在美 · 实时核对层（Live Check）

## 这一层是什么，不是什么

手册 `references/` 是**版本三 · 2026-11-28 的静态快照**。本 Skill 是它之外的第五层：当快照答不了或可能过期时，用宿主自带的 `WebSearch` / `WebFetch` 去**官方页面**核对当期口径。

- 工具由系统统一分配，专家包不声明也不需要声明 `tools`；专家模式原生提供 `WebSearch`、`WebFetch`。
- **实时层不是手册内容**：不署名「在美手册」，不写进 `references/`，不覆盖快照数值，不冒充手册已收录。
- 它只回答两件事：**手册没收录的本校层**、**快照是否已被当期官方页改动**。手册原生数据层仍是**三层（通用 → 城市 → 学校）**，`LAYER` 规则为「上层没写落回通用」；答疑时拆出的「州」是城市层里的州级字段，**不是手册的独立一层**，回答时不要说「手册州层」。

## 什么时候触发

| 触发 | 做法 |
|---|---|
| 学校不在 `03` 分表 / `01` 的 `SCHOOLS` 里 | 四层降级后，联网补本校层 |
| 城市在 `04.CITY`（532 城）与 `01.PLACES`（15 城补充）里都没有 | 联网补城市层（气候、交通、安全、税） |
| 涉及签约、付款、申报、豁免、理赔、申诉 | 即使手册有数据，也联网核当期截止/金额 |
| 用户问「现在还是这样吗」「今年截止是哪天」「给我官方链接」 | 联网核并给原页 URL |
| 手册数据带「新闻源 / 线索 / 非资助规定页」标记 | 只给线索，联网找官方规定页；找不到就明说 |
| 用户明确说「不用查，按手册答」 | 不联网，只给快照并标采集时间 |

**不触发**：通用机制类问题（五条线、147 检查点、一学期五节点）用 `00-手册正文.md` 直接答，不联网。

## 四层降级（答疑组织顺序，先做完再决定要不要联网）

> 这是**为未收录学校设计的作答顺序**，不是手册的数据层。手册本体只有通用 → 城市 → 学校三层；「州」只是城市层里的州级字段（`04.STATE` 便于检索）。

1. **通用层**：`00-手册正文.md` + `02-通用规则.json`，不依赖学校，永远可答。手册 `data` 层缺键会保留默认文案、不空白，别把「没写」当成「不适用」。
2. **州级字段**：从用户给的州名/缩写直接查 `04-城市与州.json` 的 `STATE[abbr]`（51 州与特区，含州税 / DMV / 领区）。**不需要 schoolId**，标注时写「城市层·州级字段｜手册 04 · TX」，不要写「手册州层」。
3. **城市层**：用 `01.CITY_EN[英文城市名小写]` 换出 `cityKey`，**先查 `04.CITY[cityKey]`（532 城，含税/DMV/领区），再查 `01.PLACES[cityKey]`（15 城补充：香槟-厄巴纳、安娜堡、亚特兰大、西拉法叶、哥伦布、麦迪逊等）**；中文名按两处 `name` 字段精确或包含匹配，禁止对整份 JSON 全文搜索（说明文字里的地名会串到别的城市）。两处都没有才算城市层缺。
   - 有 `schoolId` 时也可走 `SCHOOL[schoolId].cityKey` 换算，**但 schoolId 不是入口前提**。
4. **本校层**：`03`–`11` 按 ID 检索。缺了就留白，**用联网核对补**，不要拿别校数据套。
   - 手册「覆盖范围」页自带「搜不到自己的学校？补录一所」入口：可提示用户自行回手册补录，**专家不代提交、不把联网结果写成手册数据**。

各层来源不要写进正文，统一收进末尾「参考索引」，索引里写「城市层·州级字段｜手册 04 · TX」「联网｜Rice 注册处官网」这样的短行即可。

## 联网操作 SOP

1. **先定主题页**：按下方「主题 → 官方页」表确定要找的部门页，不要漫无目的搜校名。
2. **WebSearch 找入口**：用 `site:<官方域名> <主题关键词> <学年/学期>` 限定域名。示例：
   - `site:ga.rice.edu academic probation GPA undergraduate`
   - `site:registrar.rice.edu Fall 2026 add drop deadline`
   - `site:irs.gov 1040-NR 8843 nonresident alien`
3. **WebFetch 打开原页核正文**：凡涉及金额、截止日、GPA 阈值、电话号码、条款编号，**必须打开原页确认**；搜索摘要只算线索。
4. **学年与状态对齐**：确认页面标注的学年/学期与用户所问一致；不一致就明说「查到的是 X 学年，非所问学期」，并给校历入口。**费率要标学年，拟定稿与正式稿分开说**，不把「拟定 / proposed / draft」写成已生效。
5. **交叉验证**：至少一条依据来自校方或政府官网。校方新闻稿、活动日历、学生手册 PDF 可作补充，但要标明文档类型与版本年份；第三方转载单独标注为未逐条自行核验，不作一手依据。
6. **摘要与正文不符时，以 WebFetch 打开的原页正文为准**；动态日历抓不到就如实说「该页日历为动态加载，本次未能取到具体日期」，给入口链接让用户自己核，绝不从摘要硬凑。**核不到就标「未核」**，不推测填补。

## 域名白名单 / 黑名单

**可用（按可信度排序）**
1. 学校官方域 `*.edu` 及子域：`registrar.*`、`ga.*`（General Announcements / Catalog）、`*health*`、`isss.*` / `international.*`、`housing.*`、`financialaid.*`、`police.*` / `publicsafety.*`、`counseling.*`。须确认域名确实属于该学校。
2. 政府域 `*.gov`：`irs.gov`、`uscis.gov`、`studentaid.gov`、`ssa.gov`、`travel.state.gov`、州 DMV / 州税务局 / `weather.gov`。
3. 使领馆：`us.china-embassy.gov.cn`、`*.mfa.gov.cn`。
4. 承保方、官方基金会等机构官网：可用但须标注「商业/机构方页面，非校方规定」。

**禁用为依据**：论坛与问答社区（Reddit、知乎、一亩三分地等）、留学中介与代写站、个人博客、新闻聚合与二手汇总、微信公众号文章、AI 摘要站、内容农场。可作为「有人这么说过」的线索提及，但不能当成规则或阈值报给用户。

## 主题 → 该查哪一页

| 主题 | 官方页 |
|---|---|
| 校历、加退选、退课记 W、late registration | Office of the Registrar / Academic Calendar |
| GPA 红线、学术警告、停学、申诉 | General Announcements / Academic Regulations / Academic Standing / Dean of Undergraduates |
| 保险计划、豁免窗口、疫苗、理赔 | Student Health Center / University Health Services / Insurance & Waiver |
| 宿舍、费率、签约、续租 | Housing & Residence Life / Off-Campus Housing |
| 国际生身份、OPT/CPT、full-time 定义 | ISSS / International Students & Scholars / DSO |
| 专业申报、学分、学位要求 | College / Department Advising + Course Catalog |
| 奖学金与资助 | Financial Aid Office / 项目官网 / `studentaid.gov` / 官方基金会 |
| SSN | `ssa.gov` + 学校 ISSS 指引 |
| 报税 1040-NR / 8843 | `irs.gov` + 州税务局（`STATE[abbr].tax` 可作手册侧对照） |
| 驾照、车辆登记 | 州 DMV / RMV / BMV 官网 |
| 校园应急号码、夜间护送 | Campus Police / Public Safety 官网 |
| 心理支持 | Counseling Center / CAPS |
| 领区与领事保护 | 中国驻美使领馆官网 + 外交部 12308 |

## 结果标注模板（强制 · 收进末尾「参考索引」）

联网得到的每一条结论，**只在回复最下面的「参考索引」里**单独成组；正文只给答案，不出现这个模板，也不出现「实时核对层」「非手册数据」这类内部字样。索引里写这样的短行：

```
参考索引（联网核对 · 非手册内容）
- 结论：……
- 来源：<完整 URL>（<页面标题 / 文档名>）
- 来源类型：校方规定页 / 校方拟定草案 / 政府页 / 机构方页面 / 第三方转载（未逐条自行核验）
- 抓取时间：YYYY-MM-DD（以用户本地时区为准）
- 适用学年/学期：……（费率类必须标学年；拟定与正式分开）
- 与手册快照的关系：手册未收录 / 手册 2026-11 记为 X，当期官方页为 Y（以官方页为准）
```

手册来源与联网来源在「参考索引」里用行首前缀分开写、不混排——这一条不因为换了位置而放松。

- **冲突处理**：官方当期页与手册快照不一致时，在参考索引里两条并列，明确「以官方当期页为准」，并说明手册是 2026-11-28 采集的历史快照。不改口说「手册写错了」也不硬替手册辩护。
- **查不到就明说**：在参考索引里写「本次未能实时核到」或标「未核」；正文照样给能答的答案，别让对话卡住。**不推测、不编造、不套用邻校数值。**
- **不得写回**：禁止用 Write/Edit 修改 `references/` 下任何文件来「顺便补上」新学校。要把新校固化进手册，走正规流程：更新飞书手册 → 重新导出生成 references → 重新打包专家包。

## 合规红线（与手册一致）

- 联网只用于**核对规则与找入口**，不因此变成代办服务；仍然不代办申请、不代写作业、不代填表格、不代发邮件。
- **沿用手册内容口径四条**：只写官网原文、核不到标「未核」；每条带复核日期与抓取时间；费率标学年、拟定与正式分开；第三方口径单独标注、不与官网原文混排。
- 不构成法律、税务、签证、医疗或心理意见；身份、报税、理赔、申诉指向国际办、注册办、承保方与领馆。
- 生命危险先打 **911**，优先于一切检索。
- 不把外部来源内容混入手册引用；「手册 v3 · 版本三 · 2026-11-28 采集」与联网来源、抓取时间都写在末尾「参考索引」，两类来源分行标明、不混排。
- 用户提供的个人信息只用于当次核对，不写入任何文件。
