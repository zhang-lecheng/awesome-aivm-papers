"""Render the English repository overview from the bilingual source records."""

CATEGORIES_EN = {
    'perspectives': 'Perspectives and reviews',
    'foundations': 'FBA and constraint-based modeling',
    'gem': 'Genome-scale metabolic models and reconstruction',
    'enzyme': 'Enzyme constraints and kinetic parameters',
    'hybrid': 'Machine learning and mechanistic models',
    'single-cell': 'Single-cell and spatial metabolism',
    'validation': 'Experimental data and model validation',
}

PATHWAYS_EN = [
    ('Understand constraints and fluxes', 'Start with FBA mass balance, reaction bounds, and objective functions; then try COBRApy.', 'FBA, COBRApy, COBRA Toolbox 3.0'),
    ('Read a metabolic network', 'Compare yeast, human, and automatically reconstructed models; learn how genes, reactions, and metabolites connect.', 'Yeast9, Human1, Recon3D, CarveMe, MEMOTE'),
    ('Add enzyme capacity and kinetics', 'Learn how enzyme abundance and kcat constrain flux, then study AI parameter prediction and systems-level optimization.', 'GECKO, DLKcat, UniKP, EnzymeTuning'),
    ('Connect data and mechanisms', 'Compare supervised omics-to-flux learning with approaches that combine neural networks and constraint-based optimization.', 'Omics-to-flux supervised learning; neural-mechanistic hybrid models'),
    ('Study cell states and experiments', 'Compare single-cell metabolic inference with measured evidence and ask whether inferred differences can guide interventions.', 'scFEA, Compass, METAFlux, SCOOTI'),
]


def render_english(papers, issues):
    lines = ['# Awesome AIVM Papers', '', '**English** | [简体中文](README.zh-CN.md)', '',
             'A curated collection of papers, tutorials, and learning resources for AI and virtual metabolism. This collection is a work in progress; readers are welcome to suggest resources through Issues or Pull Requests.', '',
             '**[Explore the research dashboard](https://zhang-lecheng.github.io/awesome-aivm-papers/)** · [Selection methodology (Chinese)](METHODOLOGY.md) · [Contribution guide (Chinese)](CONTRIBUTING.md)', '',
             f'The library currently contains **{len(papers)} papers**. Foundational resources are maintained over time; recent literature is updated every **Sunday at 09:00, Asia/Shanghai**, by DeepSeek Harness using `westlake/deepseek-flash`.', '',
             'Topics include metabolic network reconstruction, enzyme-constrained models, enzyme kinetic prediction, omics-to-flux inference, neural-mechanistic integration, and single-cell metabolism. AIVM is used here as an organizing theme; individual papers may use different terminology.', '',
             '## Suggested reading path', '']
    for i,(title,description,methods) in enumerate(PATHWAYS_EN,1):
        lines += [f'{i}. **{title}.** {description} Start with: {methods}.']
    lines += ['', '## This week', '']
    if issues:
        latest = issues[0]
        lines += [f'Latest issue: [{latest["date"]}](weekly/{latest["date"]}.md) (Chinese).', '',
                  latest.get('editorial_en') or 'See the linked issue for the latest findings and evidence review. An English editorial is pending.', '']
    else:
        lines += ['The first issue is being prepared. The foundational papers below are ready to explore.', '']
    for key,name in CATEGORIES_EN.items():
        lines += ['## '+name, '']
        group = [p for p in papers if p['category'] == key]
        for p in sorted(group, key=lambda p:(p.get('reading_stage',6),-p['year'])):
            lines += [f'- **{p.get("method_en") or "New addition"}** — [{p["title"]}]({p["url"]}). {p["venue"]}, {p["year"]}.',
                      '  '+(p.get('summary_en') or 'English annotation pending; see the Chinese README for the current entry.'),
                      '  - Why read: '+(p.get('why_read_en') or 'See the Chinese entry.'),
                      '  - Reading note: '+(p.get('limitation_en') or 'See the Chinese entry for evidence limitations.'), '']
    lines += ['## Weekly archive', ''] + [f'- [{i["date"]}](weekly/{i["date"]}.md) (Chinese)' for i in issues]
    lines += ['', '## Data and maintenance', '',
              '- `data/papers.json`: paper records and bilingual reading annotations.',
              '- `data/weeks/`: weekly snapshots, retrieval sources, and editorial selections.',
              '- `scripts/radar.py`: collection, validation, rebuilding, and publishing.',
              '- `prompts/weekly.zh-CN.md`: instructions for the weekly DeepSeek Harness task.', '',
              'The build generates both `README.md` (English, the default GitHub landing page) and `README.zh-CN.md` (Simplified Chinese). Use the language links at the top to switch. Weekly reports and the dashboard remain in Chinese.', '',
              'Titles, venues, and dates are checked against DOI registration metadata and Europe PMC where available. Records retain their verification date and evidence level. Corrections and additional references are welcome.', '']
    return '\n'.join(lines)
