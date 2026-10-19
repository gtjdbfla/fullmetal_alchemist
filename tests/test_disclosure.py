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
 def test_author_keeps_exact_v2_source_and_twenty_three_sections(self):
  text=(ROOT/'private/STORY_MASTER_PLAN_v2.1.md').read_text('utf8')
  plan=self.author['masterPlan'];self.assertEqual(plan['fullText'],text);self.assertEqual(len(plan['sections']),23);self.assertEqual(plan['sourceHash'],hashlib.sha256(text.encode()).hexdigest())
  self.assertEqual(self.author['masterVersion'],'2.1')
  self.assertEqual(load(ROOT/'private/archive/master-data-v1.json')['masterPlan']['version'],'1.0')
 def test_reader_payload_has_no_truth_or_future_reveal_fields(self):
  self.assertIsNone(self.public['masterPlan']);self.assertIsNone(self.public['masterAlignment'])
  for row in self.public['disclosureBoard']:
   self.assertIsNone(row['actualSetting']);self.assertIsNone(row['revealPlan']);self.assertNotIn('hypothesisRoadmap',row)
  serialized=json.dumps(self.public,ensure_ascii=False)
  for row in self.author['disclosureBoard']:self.assertNotIn(row['actualSetting']['text'],serialized)
  for secret in ['알은 동쪽에서 서쪽으로 같은 길을 조사해 온다.','이슈발라 = 진리라는 오답을 확신','지역 당사자의 협상과 결정 → 국가의 인정과 지원']:
   self.assertNotIn(secret,serialized)
 def test_knowledge_and_author_truth_are_distinct(self):
  self.assertEqual(len(self.author['disclosureBoard']),11)
  for row in self.author['disclosureBoard']:
   self.assertIsInstance(row['readerKnowledge'],dict);self.assertIsInstance(row['edHypothesis'],dict);self.assertIsInstance(row['actualSetting'],dict)
   self.assertEqual(row['actualSetting']['kind'],'ORIGINAL');self.assertNotEqual(row['edHypothesis']['text'],row['actualSetting']['text'])
  truth=next(r for r in self.author['disclosureBoard'] if r['id']=='reveal-ishvala');self.assertEqual(truth['hypothesisRoadmap'][0]['stage'],'3화');self.assertIn('오답',truth['hypothesisRoadmap'][0]['truthStatus'])
 def test_reader_roadmap_stops_at_submitted_episodes(self):
  self.assertEqual([r['publishedThrough'] for r in self.public['chapterRoadmap']],[1,2])
  parts=[r for r in self.author['chapterRoadmap'] if r['id'].startswith('part-')]
  self.assertEqual(len(parts),5);self.assertTrue(all(r['fixed'] is False for r in parts))
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
 def test_politics_and_unrevealed_resource_titles_are_not_public(self):
  self.assertIsNone(self.public['politicalBoard']);self.assertIsNone(self.public['storyDecisions']);self.assertIsNone(self.public['alTrail'])
  serialized=json.dumps(self.public,ensure_ascii=False)
  for secret in ['적맥석','A부족','B부족','광맥과 땅의 흐름','이슈발의 전략자원','reveal-representation','reveal-resource','reveal-al-trail','al-capital-example']:
   self.assertNotIn(secret,serialized)
  self.assertEqual(len(self.public['disclosureBoard']),8)
 def test_political_unknowns_are_not_fabricated_and_relations_resolve(self):
  parties=self.author['politicalBoard']['parties'];ids={r['id'] for r in parties}
  for r in parties:
   for key in ['wants','fears','concedes','redlines']:
    f=r[key];self.assertIn(f['status'],['명시','예시','미정'])
    if f['status']=='미정':self.assertIsNone(f['text'])
   for relation in r['relations']:self.assertIn(relation['target'],ids)
  ling=next(r for r in parties if r['id']=='pol-ling')
  self.assertEqual(ling['concedes']['status'],'예시');self.assertEqual(ling['redlines']['status'],'예시')
  mining=next(r for r in parties if r['id']=='pol-mining');self.assertIsNone(mining['redlines']['text'])
 def test_resource_examples_and_tentative_hypotheses_stay_tentative(self):
  r=self.author['masterPlan']['resource']
  self.assertIn('가칭',r['nameStatus']);self.assertIn('핵심 용도 확정',r['propertiesStatus']);self.assertIn('미확정',r['hypothesesStatus'])
  self.assertEqual(len(self.author['masterPlan']['arcs']),6)
  self.assertIn('정치적 선택',self.author['masterPlan']['causalChain'][-3]['text'])
 def test_red_stone_observation_does_not_promote_resource_identity(self):
  row=next(r for r in self.public['disclosureBoard'] if r['id']=='reveal-red-stones')
  self.assertIn('물질',row['readerKnowledge']['text']);self.assertIsNone(row['actualSetting'])
  self.assertIsNone(self.public['draftMilestones'])
  self.assertEqual(len(self.public['mysteries']),16)
  self.assertEqual(next(r for r in self.public['mysteries'] if r['id']=='m15')['status'],'CLUE FOUND')
 def test_nine_decisions_are_not_mistaken_for_nine_completed_mysteries(self):
  rows=self.author['storyDecisions'];self.assertEqual([r['number'] for r in rows],list(range(1,10)))
  self.assertEqual(rows[6]['status'],'세부 보류');self.assertEqual(rows[7]['status'],'폐기 완료')
  self.assertEqual(rows[1]['status'],'수정 완료');self.assertEqual(rows[3]['status'],'수정 완료')
  self.assertTrue(all(r['status']!='SOLVED' for r in self.author['mysteries']))
 def test_al_trail_never_invents_dates_or_promotes_candidates(self):
  rows=self.author['alTrail']['entries'];self.assertEqual(sum(r['status']=='원고 제시' for r in rows),1)
  for r in rows:self.assertIsNone(r['sentAt']);self.assertIsNone(r['receivedAt'])
  for r in rows[1:]:self.assertEqual(r['status'],'예시 · 미집필');self.assertEqual(r['evidence'],[])
 def test_brother_hypothesis_matches_revised_prose_and_keeps_final_answer_private(self):
  row=next(r for r in self.public['disclosureBoard'] if r['id']=='reveal-brother')
  self.assertIn('미확정',row['edHypothesis']['status']);self.assertNotIn('단정',row['edHypothesis']['text'])
  self.assertIn('합금',self.author['masterPlan']['resource']['confirmed'][0])
  self.assertIn('동쪽',self.author['timelineLanes'][0][1])
if __name__=='__main__':unittest.main()
