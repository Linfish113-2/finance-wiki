#!/usr/bin/env python3
"""Pre-render guard: detect provenance gaps before HTML is generated."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sources=json.loads((ROOT/'data/sources.json').read_text(encoding='utf-8'))
evidence=json.loads((ROOT/'cards/evidence.json').read_text(encoding='utf-8'))
slides=json.loads((ROOT/'data/slides.json').read_text(encoding='utf-8'))
source_ids={s['id'] for s in sources};ev={e['id']:e for e in evidence}
issues=[]
if len(sources)<5:issues.append('Less than five distinct sources')
for e in evidence:
 if not e['sources'] or any(sid not in source_ids for sid in e['sources']):issues.append('Broken evidence '+e['id'])
for slide in slides:
 if not slide['cite'] or any(eid not in ev for eid in slide['cite']):issues.append(f'Slide {slide["num"]}: missing evidence')
 if not slide['title'] or not slide['takeaway']:issues.append(f'Slide {slide["num"]}: missing teaching content')
# Actual correction prompted by first HTML lint failure:
div=next(s for s in slides if s['num']==7)
if '配息不保證' not in (div['takeaway']+div['title']+div['subtitle']):issues.append('Slide 7: missing no-guarantee dividend qualifier')
active=next(s for s in slides if s['num']==4)
if 'E02' not in active['cite']:issues.append('Slide 4: active/passive citation missing')
report={'name':'pre-render content gate','passed':not issues,'source_count':len(sources),'evidence_count':len(evidence),'slide_count':len(slides),'errors':issues}
(ROOT/'reports'/'pre-render-gate.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('CONTENT GATE', 'PASS' if not issues else 'FAIL',report)
sys.exit(0 if not issues else 1)
