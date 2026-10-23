#!/usr/bin/env python3
"""Collect verified candidates, validate editorial decisions and publish reproducibly."""
from __future__ import annotations
import argparse
import concurrent.futures
import datetime as dt
import fcntl
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / '.runtime'
REPO = 'zhang-lecheng/awesome-aivm-papers'
CATEGORIES = {
    'perspectives': '前瞻与综述', 'foundations': 'FBA 与约束建模',
    'gem': 'GEM 与模型重建', 'enzyme': '酶约束与动力学',
    'hybrid': '机器学习与机制融合', 'single-cell': '单细胞与空间代谢',
    'validation': '实验数据与模型验证',
}
LIMITS = {'question': 30, 'decision': 20, 'information': 15, 'evaluation': 15, 'evidence': 15, 'nontriviality': 5}

def today():
    return dt.datetime.now(ZoneInfo('Asia/Shanghai')).date().isoformat()

def read(path, default=None):
    return json.loads(path.read_text()) if path.exists() else default

def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    tmp.replace(path)

def plain(value):
    import html
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', str(value or '')))).strip()

def identity(p):
    doi = str(p.get('doi', '')).lower().strip().removeprefix('https://doi.org/').rstrip('.')
    if doi:
        return 'doi:' + doi
    aid = re.sub(r'v\d+$', '', str(p.get('arxiv_id', '')).strip().split('/abs/')[-1])
    if aid:
        return 'arxiv:' + aid
    if p.get('pmcid'):
        return 'pmc:' + p['pmcid']
    if p.get('pmid'):
        return 'pmid:' + p['pmid']
    raise ValueError('Every record needs a DOI, arXiv, PMC or PubMed identifier')

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Awesome-AIVM-Papers/1.0 (public literature index)'})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)

def epmc(query):
    url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?' + urllib.parse.urlencode({
        'query': query, 'format': 'json', 'resultType': 'core', 'pageSize': 30, 'sort': 'FIRST_PDATE_D desc'})
    payload = fetch_json(url)
    records = []
    for p in payload['resultList']['result']:
        if not (p.get('doi') or p.get('pmcid') or p.get('source') == 'MED'):
            continue
        doi = p.get('doi','').lower()
        date = p.get('firstPublicationDate', '')
        record = {
            'doi': doi, 'pmid': p['id'] if p.get('source')=='MED' else '', 'title': plain(p.get('title')),
            'date': date, 'year': int(p.get('pubYear') or date[:4] or 0),
            'venue': p.get('journalInfo', {}).get('journal', {}).get('title', '') or ('预印本' if 'PPR' == p.get('source') else '未标注期刊'),
            'authors': plain(p.get('authorString')), 'abstract': plain(p.get('abstractText')),
            'url': 'https://doi.org/' + doi if doi else 'https://europepmc.org/article/'+p['source']+'/'+p['id'], 'pmcid': p.get('pmcid', ''),
            'metadata_url': url, 'source': 'Europe PMC', 'kind': 'preprint' if p.get('source') == 'PPR' else 'article',
        }
        record['id'] = identity(record)
        records.append(record)
    return records, int(payload.get('hitCount', len(records)))

def arxiv(since, until):
    # lastUpdatedDate includes revised preprints. The canonical ID omits version suffixes.
    terms = '(all:"metabolic flux" OR all:"enzyme kinetics" OR all:"genome-scale metabolic" OR all:"metabolic pathway reconstruction")'
    query = terms + f' AND lastUpdatedDate:[{since.replace("-", "")}0000 TO {until.replace("-", "")}2359]'
    url = 'https://export.arxiv.org/api/query?' + urllib.parse.urlencode({'search_query': query, 'max_results': 35, 'sortBy': 'lastUpdatedDate', 'sortOrder': 'descending'})
    req = urllib.request.Request(url, headers={'User-Agent': 'Awesome-AIVM-Papers/1.0'})
    with urllib.request.urlopen(req, timeout=40) as r:
        xml = ET.fromstring(r.read())
    ns = {'a': 'http://www.w3.org/2005/Atom'}
    records = []
    for e in xml.findall('a:entry', ns):
        get = lambda key: plain(e.findtext('a:' + key, default='', namespaces=ns))
        aid = get('id').split('/abs/')[-1]
        p = {'arxiv_id': re.sub(r'v\d+$', '', aid), 'version': aid, 'title': get('title'), 'abstract': get('summary'),
             'date': get('published')[:10], 'updated': get('updated')[:10], 'year': int(get('published')[:4]),
             'venue': 'arXiv', 'url': get('id').replace('http:', 'https:'), 'source': 'arXiv', 'metadata_url': url,
             'kind': 'preprint', 'authors': ', '.join(plain(a.findtext('a:name', '', ns)) for a in e.findall('a:author', ns))}
        p['id'] = identity(p)
        records.append(p)
    return records, len(records)

def collect(args):
    RUNTIME.mkdir(exist_ok=True)
    state = read(RUNTIME / 'state.json', {})
    previous = state.get('last_successful_run')
    # A three-day overlap catches delayed indexing; existing canonical IDs are excluded downstream.
    since = args.since or ((dt.date.fromisoformat(previous) - dt.timedelta(days=3)).isoformat() if previous else (dt.date.fromisoformat(args.date) - dt.timedelta(days=14)).isoformat())
    terms = [
        '("genome-scale metabolic" OR "enzyme-constrained" OR "metabolic pathway reconstruction") AND ("machine learning" OR "deep learning" OR "artificial intelligence")',
        '("metabolic flux" OR "fluxomics" OR "enzyme kinetic") AND ("prediction" OR "learning" OR "benchmark")',
        '("single-cell" OR "spatial") AND ("metabolic flux" OR "metabolic modeling" OR "metabolic modelling")',
    ]
    tasks = [('Europe PMC · ' + str(i+1), lambda q=q: epmc(q + f' AND FIRST_PDATE:[{since} TO {args.date}]')) for i,q in enumerate(terms)]
    tasks.append(('arXiv', lambda: arxiv(since, args.date)))
    sources, candidates = [], {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(fn): name for name,fn in tasks}
        for future in concurrent.futures.as_completed(futures):
            name = futures[future]
            try:
                records, total = future.result()
                sources.append({'source': name, 'ok': True, 'returned': len(records), 'total_hits': total, 'truncated': total > len(records)})
                for p in records:
                    p['id'] = identity(p)
                    candidates[p['id']] = p
            except Exception as e:
                sources.append({'source': name, 'ok': False, 'error': str(e)})
    if not any(s['ok'] for s in sources):
        raise RuntimeError('All literature sources failed; do not publish a no-news issue')
    known = {p['id']: p for p in read(ROOT / 'data/papers.json', [])}
    fresh = []
    for p in candidates.values():
        existing = known.get(p['id'])
        if existing:
            if p.get('version') and p.get('version') != existing.get('version'):
                p['existing_record'] = existing
                p['change_type'] = 'revision'
            else:
                continue
        else:
            p['change_type'] = 'new'
        fresh.append(p)
    output = {'date': args.date, 'since': since, 'until': args.date, 'sources': sorted(sources, key=lambda s:s['source']),
              'candidates': sorted(fresh, key=lambda p:p.get('updated',p.get('date','')), reverse=True)[:60],
              'candidate_count': len(fresh), 'review_limit': 12}
    path = RUNTIME / f'candidates-{args.date}.json'
    write(path, output)
    print(json.dumps({'input': str(path), 'since': since, 'candidates': len(output['candidates']), 'sources': output['sources']}, ensure_ascii=False))

def validate(decision, manifest):
    if decision.get('date') != manifest['date']:
        raise ValueError('Decision date must match collection date')
    if not isinstance(decision.get('editorial_zh'), str) or len(decision['editorial_zh']) < 15:
        raise ValueError('A concrete Chinese weekly editorial is required')
    candidates = {p['id']: p for p in manifest['candidates']}
    papers = decision.get('papers')
    if not isinstance(papers, list) or len(papers) > 12:
        raise ValueError('Review 0–12 papers per issue')
    seen, clean = set(), []
    for p in papers:
        if p.get('id') not in candidates or p['id'] in seen:
            raise ValueError('A selected paper must match a unique collected candidate')
        seen.add(p['id'])
        if p.get('category') not in CATEGORIES or p.get('status') not in ('featured', 'watch'):
            raise ValueError('Unknown category or status')
        if p.get('evidence_level') not in ('abstract', 'fulltext', 'reproduced'):
            raise ValueError('evidence_level must be abstract/fulltext/reproduced')
        if p['status'] == 'featured' and p['evidence_level'] == 'abstract':
            raise ValueError('Abstract-only records belong to watch, not featured')
        for key in ('summary_zh', 'why_read', 'limitation', 'new_question'):
            if not isinstance(p.get(key),str) or len(p[key]) < 12:
                raise ValueError('Missing substantive Chinese field: ' + key)
        scores = p.get('scores', {})
        if set(scores) != set(LIMITS) or any(type(scores[k]) is not int or not 0 <= scores[k] <= v for k,v in LIMITS.items()):
            raise ValueError('Invalid six-part score')
        if sum(scores.values()) != p.get('innovation_score'):
            raise ValueError('Score breakdown does not sum to total')
        if not p.get('evidence_urls') or any(not str(u).startswith('https://') for u in p['evidence_urls']):
            raise ValueError('At least one direct HTTPS evidence link is required')
        original = candidates[p['id']]
        # Bibliographic metadata always comes from retrieval, never from the language model.
        record = {k:v for k,v in original.items() if k not in ('abstract','existing_record','metadata_url')}
        record.update({k:p[k] for k in ('category','status','summary_zh','why_read','limitation','new_question','scores','innovation_score','evidence_level','evidence_urls')})
        record['verified_on'] = manifest['date']
        clean.append(record)
    return sorted(clean, key=lambda p:-p['innovation_score'])

def build_site():
    from build import build
    build()

def git(*args, **kwargs):
    return subprocess.run(['git', *args], cwd=ROOT, check=True, **kwargs)

def publish_repo():
    env = os.environ.copy()
    if not env.get('GITHUB_TOKEN'):
        # Load an explicitly configured, owner-only local credential file without printing it.
        secret = Path(os.environ.get('AIVM_CREDENTIAL_FILE', '/home/lc/.config/aivc-radar/github.env'))
        if not secret.exists() or secret.stat().st_mode & 0o077:
            raise RuntimeError('GitHub credential file missing or not owner-only')
        env.update(line.split('=',1) for line in secret.read_text().splitlines() if '=' in line and not line.startswith('#'))
    if not env.get('GITHUB_TOKEN'):
        raise RuntimeError('GitHub credential not configured')
    env.update(GIT_TERMINAL_PROMPT='0', GIT_ASKPASS=str(ROOT / 'scripts/git-askpass.sh'))
    git('add', 'README.md', 'docs', 'data', 'weekly', 'scripts', 'prompts', 'CONTRIBUTING.md', 'METHODOLOGY.md', '.gitignore', 'tests')
    changed = subprocess.run(['git','diff','--cached','--quiet'],cwd=ROOT).returncode
    if changed:
        git('commit','-m',f'weekly AIVM library: {today()}')
    git('-c','credential.helper=','push','origin','HEAD',env=env)
    return subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()

def apply(args):
    RUNTIME.mkdir(exist_ok=True)
    with (RUNTIME / 'run.lock').open('w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        manifest = read(Path(args.candidates))
        decision = read(Path(args.decisions))
        records = validate(decision, manifest)
        issue_path = ROOT / 'data/weeks' / f'{manifest["date"]}.json'
        digest = hashlib.sha256(json.dumps(decision,sort_keys=True).encode()).hexdigest()
        existing_issue = read(issue_path, {})
        if existing_issue and existing_issue.get('decision_hash') != digest:
            raise ValueError('An issue already exists for this date; use a new issue date instead of silently overwriting it')
        if args.dry_run:
            print(json.dumps({'validated':True,'papers':len(records),'featured':sum(p['status']=='featured' for p in records)},ensure_ascii=False));return
        existing = {p['id']:p for p in read(ROOT / 'data/papers.json', [])}
        for p in records:
            old = existing.get(p['id'], {})
            p['added_on'] = old.get('added_on',manifest['date'])
            p['updated_on'] = manifest['date']
            p['essential'] = old.get('essential',False)
            if old.get('version') and old.get('version') != p.get('version'):
                p['versions'] = old.get('versions',[]) + [{'version':old['version'],'url':old['url']}]
            existing[p['id']] = {**old,**p}
        write(ROOT / 'data/papers.json',list(existing.values()))
        write(issue_path,{'date':manifest['date'],'since':manifest['since'],'until':manifest['until'],
                         'editorial_zh':decision['editorial_zh'],'paper_ids':[p['id'] for p in records],
                         'snapshots':records,'sources':manifest['sources'],'candidate_count':manifest['candidate_count'],
                         'decision_hash':digest})
        build_site()
        commit = None
        if args.publish:
            commit = publish_repo()
            write(RUNTIME/'state.json',{'last_successful_run':manifest['date'],'commit':commit,'decision_hash':digest})
        print(json.dumps({'published':bool(args.publish),'date':manifest['date'],'papers':len(records),'commit':commit},ensure_ascii=False))

def main():
    parser=argparse.ArgumentParser()
    sub=parser.add_subparsers(dest='command',required=True)
    c=sub.add_parser('collect');c.add_argument('--since');c.add_argument('--date',default=today());c.set_defaults(fn=collect)
    a=sub.add_parser('apply');a.add_argument('--candidates',required=True);a.add_argument('--decisions',required=True);a.add_argument('--dry-run',action='store_true');a.add_argument('--publish',action='store_true');a.set_defaults(fn=apply)
    b=sub.add_parser('build');b.set_defaults(fn=lambda a:build_site())
    p=sub.add_parser('publish');p.set_defaults(fn=lambda a:print(json.dumps({'commit':publish_repo()})))
    args=parser.parse_args();args.fn(args)

if __name__=='__main__':
    main()
