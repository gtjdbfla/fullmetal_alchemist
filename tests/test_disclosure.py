import json,hashlib,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_views import projections

def load(path):return json.loads(path.read_text('utf8'))
class DisclosureTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.public=load(ROOT/'site/data/project.json');cls.author=load(ROOT/'author-site/data/project.json');cls.master=load(ROOT/'private/master-data.json')
 def test_author_keeps_exact_master_source_and_thirteen_sections(self):
  text=(ROOT/'private/STORY_MASTER_PLAN_v1.md').read_text('utf8')
  plan=self.author['masterPlan'];self.assertEqual(plan['fullText'],text);self.assertEqual(len(plan['sections']),13);self.assertEqual(plan['sourceHash'],hashlib.sha256(text.encode()).hexdigest())
 def test_reader_payload_has_no_truth_or_future_reveal_fields(self):
  self.assertIsNone(self.public['masterPlan']);self.assertIsNone(self.public['masterAlignment'])
  for row in self.public['disclosureBoard']:
   self.assertIsNone(row['actualSetting']);self.assertIsNone(row['revealPlan']);self.assertNotIn('hypothesisRoadmap',row)
  serialized=json.dumps(self.public,ensure_ascii=False)
  for row in self.author['disclosureBoard']:self.assertNotIn(row['actualSetting']['text'],serialized)
  for secret in ['알은 동쪽에서 서쪽으로 같은 길을 조사해 온다.','이슈발라 = 진리라는 오답을 확신','지역 당사자의 협상과 결정 → 국가의 인정과 지원']:
   self.assertNotIn(secret,serialized)
 def test_knowledge_and_author_truth_are_distinct(self):
  self.assertEqual(len(self.author['disclosureBoard']),6)
  for row in self.author['disclosureBoard']:
   self.assertIsInstance(row['readerKnowledge'],dict);self.assertIsInstance(row['edHypothesis'],dict);self.assertIsInstance(row['actualSetting'],dict)
   self.assertEqual(row['actualSetting']['kind'],'ORIGINAL');self.assertNotEqual(row['edHypothesis']['text'],row['actualSetting']['text'])
  truth=next(r for r in self.author['disclosureBoard'] if r['id']=='reveal-ishvala');self.assertEqual(truth['hypothesisRoadmap'][0]['stage'],'3화');self.assertIn('오답',truth['hypothesisRoadmap'][0]['truthStatus'])
 def test_reader_roadmap_stops_at_submitted_episodes(self):
  self.assertEqual([r['publishedThrough'] for r in self.public['chapterRoadmap']],[1,2]);self.assertEqual(len(self.author['chapterRoadmap']),8)
 def test_all_evidence_quotes_exist(self):
  data=self.author;documents={m['id']:m['text'] for m in data['manuscripts']}
  evidence=[]
  for r in data['disclosureBoard']:evidence+=r['readerKnowledge']['evidence']+r['edHypothesis']['evidence']
  for r in data['masterAlignment']['findings']+data['masterAlignment']['checks']:evidence+=r['evidence']
  for e in evidence:self.assertIn(e['quote'],documents[e['manuscript']])
 def test_build_is_repeatable_without_promoting_future_information(self):
  public,author=projections(self.public,load(ROOT/'private/archive/pre-master-project.json'),self.master)
  self.assertEqual(public,self.public);self.assertEqual(author,self.author)
 def test_public_assets_do_not_contain_master_manuscript_or_private_data(self):
  for path in (ROOT/'site').rglob('*'):
   if path.is_file():
    self.assertNotIn('private',path.relative_to(ROOT/'site').parts)
    text=path.read_text('utf8')
    self.assertNotIn('알은 동쪽에서 서쪽으로 같은 길을 조사해 온다.',text)
if __name__=='__main__':unittest.main()
