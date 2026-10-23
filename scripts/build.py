#!/usr/bin/env python3
"""Generate the Markdown library, weekly reports and the static dashboard data."""
import json
from pathlib import Path
from radar import CATEGORIES, ROOT
from readme import render_english

PATHWAYS = [
    {'step': 1, 'title': '理解约束与通量', 'description': '从 FBA 的守恒条件、反应边界和目标函数开始，再用 COBRApy 动手。', 'methods': ['FBA','COBRApy','COBRA Toolbox 3.0']},
    {'step': 2, 'title': '读懂一个代谢网络', 'description': '比较酵母、人类和自动重建模型；学习基因、反应与代谢物如何对应。', 'methods': ['Yeast9','Human1','Recon3D','CarveMe','MEMOTE']},
    {'step': 3, 'title': '加入酶容量与动力学', 'description': '理解酶丰度和 kcat 如何约束通量，再研究 AI 参数预测与系统优化。', 'methods': ['GECKO','DLKcat','UniKP','EnzymeTuning']},
    {'step': 4, 'title': '连接数据与机制', 'description': '比较组学到通量的监督学习，以及神经网络和约束优化共同预测表型。', 'methods': ['组学到通量的监督学习','神经网络与机制模型融合']},
    {'step': 5, 'title': '走向细胞状态与实验', 'description': '比较单细胞代谢推断与实测证据，研究推断出的差异能否指导干预。', 'methods': ['scFEA','Compass','METAFlux','SCOOTI']},
]

def build():
    papers = json.loads((ROOT/'data/papers.json').read_text())
    issues = [json.loads(p.read_text()) for p in sorted((ROOT/'data/weeks').glob('*.json'),reverse=True)] if (ROOT/'data/weeks').exists() else []
    (ROOT/'docs').mkdir(exist_ok=True)
    payload = {'title':'Awesome AIVM Papers','updated':max([p['verified_on'] for p in papers]+[i['date'] for i in issues]),
               'categories':CATEGORIES,'pathways':PATHWAYS,'papers':papers,'issues':issues,
               'schedule':{'weekday':'周日','time':'09:00','timezone':'Asia/Shanghai'}}
    (ROOT/'docs/data.json').write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':'))+'\n')
    lines = ['# Awesome AIVM Papers','', '[English](README.md) | **简体中文**','',
             '面向人工智能与虚拟代谢研究的论文、教程和学习入口。持续完善，欢迎通过 Issue 或 Pull Request 补充资料。','',
             '**[浏览学术看板](https://zhang-lecheng.github.io/awesome-aivm-papers/)** · [阅读方法](METHODOLOGY.md) · [贡献文献](CONTRIBUTING.md)','',
             f'已收录 **{len(papers)} 篇**文献。入门库长期维护；近期论文每周日 09:00（Asia/Shanghai）由 DeepSeek Harness 更新，模型为 `westlake/deepseek-flash`。','',
             '本项目覆盖代谢网络重建、酶约束模型、酶动力学预测、组学与通量、机制与机器学习融合，以及单细胞代谢。','',
             '## 建议阅读顺序','']
    for p in PATHWAYS:
        lines += [f'{p["step"]}. **{p["title"]}**：{p["description"]} 入口：'+ '、'.join(p['methods'])+'。']
    lines += ['', '## 本周更新','']
    if issues:
        latest=issues[0]
        lines += [f'最新一期：[{latest["date"]}](weekly/{latest["date"]}.md)。', '',latest['editorial_zh'],'']
    else:
        lines += ['首期正在准备。下面的经典论文可直接作为学习入口。','']
    for key,name in CATEGORIES.items():
        group=[p for p in papers if p['category']==key]
        lines += ['## '+name,'']
        for p in sorted(group,key=lambda p:(p.get('reading_stage',6),-p['year'])):
            lines += [f'- **{p.get("method") or "新收录"}** — [{p["title"]}]({p["url"]})。{p["venue"]}, {p["year"]}。',
                      f'  {p["summary_zh"]}',f'  - 为什么读：{p["why_read"]}',f'  - 阅读时注意：{p["limitation"]}','']
    lines += ['## 历期周报','']+[f'- [{i["date"]}](weekly/{i["date"]}.md)' for i in issues]
    lines += ['', '## 数据与维护','',
              '- `data/papers.json`：文献库及中英文导读。','- `data/weeks/`：每期候选、检索来源和编辑选择的快照。',
              '- `scripts/radar.py`：采集、校验、重建与推送。','- `prompts/weekly.zh-CN.md`：DeepSeek Harness 每周任务指令。','',
              '参考文献的标题、期刊和日期优先核对 DOI 注册信息与 Europe PMC。每篇记录核查日期及证据层级。欢迎提交更正。','']
    (ROOT/'README.zh-CN.md').write_text('\n'.join(lines))
    (ROOT/'README.md').write_text(render_english(papers,issues))
    (ROOT/'weekly').mkdir(exist_ok=True)
    for issue in issues:
        text=[f'# AIVM 每周文献更新｜{issue["date"]}','',f'检索窗口：{issue["since"]} 至 {issue["until"]}。候选 {issue["candidate_count"]} 篇。','',issue['editorial_zh'],'']
        for status,name in [('featured','本周重点'),('watch','观察区')]:
            text += ['## '+name,'']
            group=[p for p in issue['snapshots'] if p['status']==status]
            if not group:
                text += ['本期没有达到该栏标准的新增论文。','']
            for p in group:
                text += [f'### [{p["title"]}]({p["url"]})', '', f'{p["venue"]} · {p["date"]} · 阅读优先分 {p["innovation_score"]}/100', '',
                         p['summary_zh'],'', '**新问题：**'+p['new_question'],'','**为什么读：**'+p['why_read'],'',
                         '**证据与限制：**'+p['limitation'],'',f'证据层级：{p["evidence_level"]}。分项：`{json.dumps(p["scores"],ensure_ascii=False)}`。','',
                         '核查链接：'+ ' · '.join(f'[来源 {n+1}]({url})' for n,url in enumerate(p['evidence_urls'])),'']
        text += ['## 检索来源','']
        for source in issue['sources']:
            text += [f'- {source["source"]}：'+(f'成功，返回 {source["returned"]} 条，命中 {source["total_hits"]} 条'+('（受返回上限影响）' if source.get('truncated') else '') if source['ok'] else '失败，'+source['error'])+'。']
        text += ['','[返回文献库](../README.md) · [打开看板](https://zhang-lecheng.github.io/awesome-aivm-papers/)','']
        (ROOT/'weekly'/f'{issue["date"]}.md').write_text('\n'.join(text))

if __name__=='__main__':
    build()
