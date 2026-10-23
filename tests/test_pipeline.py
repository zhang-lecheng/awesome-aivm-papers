"""Exercise publication boundaries and reproducible generation without network access."""
import argparse
import contextlib
import copy
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import radar
import build

class PipelineTests(unittest.TestCase):
    def sample(self):
        candidate={'id':'arxiv:2610.12345','arxiv_id':'2610.12345','version':'2610.12345v1','title':'A metabolic model','date':'2026-10-22','year':2026,'url':'https://arxiv.org/abs/2610.12345','venue':'arXiv','source':'arXiv','authors':'A. Researcher'}
        manifest={'date':'2026-10-23','since':'2026-10-09','until':'2026-10-23','sources':[{'source':'test','ok':True,'returned':1,'total_hits':1}],'candidates':[candidate],'candidate_count':1}
        p={'id':candidate['id'],'category':'hybrid','status':'watch','summary_zh':'论文把代谢网络与学习方法结合，并讨论预测代谢通量的验证方法。','why_read':'了解学习模型需要哪些输入与真实标签。','limitation':'目前只核对摘要，尚未核对全文的独立验证。','new_question':'从网络约束出发，哪些代谢响应可以预测？','scores':dict(question=20,decision=10,information=10,evaluation=10,evidence=5,nontriviality=3),'innovation_score':58,'evidence_level':'abstract','evidence_urls':[candidate['url']]}
        decision={'date':manifest['date'],'editorial_zh':'本周候选讨论代谢模型的预测与验证，只有摘要的工作暂列观察区。','papers':[p]}
        return manifest,decision

    def test_canonical_arxiv_removes_version(self):
        self.assertEqual(radar.identity({'arxiv_id':'2610.12345v3'}),'arxiv:2610.12345')

    def test_metadata_does_not_come_from_model(self):
        m,d=self.sample();d['papers'][0]['title']='fabricated title'
        self.assertEqual(radar.validate(d,m)[0]['title'],'A metabolic model')

    def test_abstract_cannot_enter_featured(self):
        m,d=self.sample();d['papers'][0]['status']='featured'
        with self.assertRaises(ValueError):radar.validate(d,m)

    def test_bad_score_and_unknown_candidate_rejected(self):
        m,d=self.sample();d['papers'][0]['innovation_score']=99
        with self.assertRaises(ValueError):radar.validate(d,m)
        m,d=self.sample();d['papers'][0]['id']='arxiv:0000.00000'
        with self.assertRaises(ValueError):radar.validate(d,m)

    def test_rerun_is_idempotent_and_failure_does_not_advance(self):
        m,d=self.sample()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);runtime=root/'.runtime';runtime.mkdir();(root/'data').mkdir();(root/'docs').mkdir()
            radar.write(root/'data/papers.json',[]);radar.write(runtime/'input.json',m);radar.write(runtime/'decision.json',d)
            a=argparse.Namespace(candidates=str(runtime/'input.json'),decisions=str(runtime/'decision.json'),dry_run=False,publish=True)
            with patch.object(radar,'ROOT',root),patch.object(radar,'RUNTIME',runtime),patch.object(build,'ROOT',root),contextlib.redirect_stdout(io.StringIO()):
                with patch.object(radar,'publish_repo',side_effect=RuntimeError('push failed')):
                    with self.assertRaises(RuntimeError):radar.apply(a)
                self.assertFalse((runtime/'state.json').exists())
                with patch.object(radar,'publish_repo',return_value='test-commit'):
                    radar.apply(a)
                    first=(root/'docs/data.json').read_bytes()
                    radar.apply(a)
                self.assertEqual(first,(root/'docs/data.json').read_bytes())
                self.assertEqual(len(radar.read(root/'data/papers.json')),1)
                self.assertEqual(radar.read(runtime/'state.json')['last_successful_run'],'2026-10-23')

    def test_empty_week_keeps_existing_library(self):
        m,d=self.sample();d['papers']=[]
        self.assertEqual(radar.validate(d,m),[])

if __name__=='__main__':unittest.main()
