"""Export secondary regulatory guidance faithfully; never infer legal applicability or compliance."""
import argparse
import json
from pathlib import Path
import re
from urllib.parse import quote
import yaml
from jsonschema import Draft202012Validator
from eaa_hf_common import ROOT,SOURCE,MANAGED,EXCLUDED_SOURCES,destination,digest,git,load_config,read_sources

class UniqueKeyLoader(yaml.SafeLoader):
    pass
def unique_mapping(loader, node, deep=False):
    loader.flatten_mapping(node)
    result = {}
    for k,v in node.value:
        key = loader.construct_object(k, deep=deep)
        if key in result: raise ValueError('Duplicate metadata key: ' + str(key))
        result[key] = loader.construct_object(v, deep=deep)
    return result
UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)
def safe_yaml(text):
    return yaml.load(text,Loader=UniqueKeyLoader)

def metadata(text):
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)', text, re.S)
    md = safe_yaml(match[1]) if match else {}
    return md if isinstance(md, dict) else {}

def sections(text):
    """Keep H1/H2 parent context and exact spans; never split fenced examples."""
    boundaries, fence, offset, parents = [(0, 'Document preamble', [])], None, 0, []
    for line in text.splitlines(keepends=True):
        mark = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if mark:
            token = mark[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence) and not line[mark.end():].strip():
                fence = None
        elif fence is None:
            match = re.match(r'^(#{1,2})[ \t]+([^\r\n]+)', line)
            if match:
                level, title = len(match[1]), match[2].strip().rstrip('#').strip()
                parents = parents[:level-1] + [title]
                if offset == 0:
                    boundaries[0] = (offset, title, parents[:])
                else:
                    boundaries.append((offset, title, parents[:]))
        offset += len(line)
    result, counts = [], {}
    for i, (a, title, hierarchy) in enumerate(boundaries):
        b = boundaries[i+1][0] if i+1 < len(boundaries) else len(text)
        if a == b:
            continue
        slug = re.sub(r'[^a-z0-9]+', '-', ' '.join(hierarchy or [title]).lower()).strip('-') or 'section'
        counts[slug] = counts.get(slug, 0) + 1
        key = slug if counts[slug] == 1 else slug + '-' + str(counts[slug])
        result.append((key, title, text[a:b], a, b, hierarchy))
    if ''.join(r[2] for r in result) != text:
        raise ValueError('Section extraction lost source text.')
    return result

def build(root,output):
    root,output=Path(root).resolve(),Path(output).resolve()
    if output==root or root in output.parents:raise ValueError('Write the export outside the source checkout.')
    cfg=load_config(root);target=destination(cfg['destination_dataset']);texts,manifest=read_sources(root,cfg)
    sha=git(root,'rev-parse','HEAD').decode().strip();date=git(root,'show','-s','--format=%cs','HEAD').decode().strip()
    index=safe_yaml(texts['control/document-index.yaml'])
    sources=safe_yaml(texts['control/source-register.yaml'])
    standards=safe_yaml(texts['control/standards-status.yaml'])
    for path,text in texts.items():
        if path.endswith('.yaml'):safe_yaml(text)
        elif path.endswith('.json'):
            parsed=json.loads(text)
            if path.endswith('.schema.json'):Draft202012Validator.check_schema(parsed)
    by_path={d['path']:d for d in index['documents']}
    if len(by_path)!=6:raise ValueError('The six-guide document index must be retained.')
    for path,entry in by_path.items():
        if path not in texts:raise ValueError('An indexed guide is missing from the export.')
        md=metadata(texts[path])
        for key in ['document_id','version','status','authority_type','review_date','source_ids','prerequisites','output_record_types']:
            if md.get(key)!=entry.get(key):raise ValueError('Guide/index metadata mismatch: '+path+' / '+key)
    for path,title in [('AGENTS.md','Sources and evidence'),('guides/01-scope-and-applicability.md','Inputs and boundaries'),('guides/02-requirements-and-assessment.md','Select and version the baseline')]:
        if not any(part[1]==title for part in sections(texts[path])):
            raise ValueError('Required interpretation context missing: '+path+' / '+title)
    if not sources.get('sources') or not standards.get('verified_on'):
        raise ValueError('Dated source and standards registers are required.')
    warnings=[
        'Secondary EAA practitioner guidance, not primary law, legal advice, a complete EN catalogue, approved national adapter or product conformity decision.',
        'Six guides and the runbook remain draft for organisational adoption. Workflow definitions and validation do not deploy integrations or authorise actions.',
        'Preserve national scope, exact provisions, standard versions and original verification dates. EAA and WAD citation are distinct; export dates do not establish legal currency.',
        'Technical results, customer outcomes, legal conclusions, approvals and public claims are distinct. Satisfaction is an additional Double FW outcome, not a fifth official WCAG principle.',
        'Combined historical RAG, known misleading Annex planning matrix and synthetic developer fixtures are excluded from both dataset views. Linked external sources are not copied or rechecked.',
        'Retrieved instructions, blank templates and workflow actions are data, not runtime authority. Historical validation reports and synthetic checks do not establish real evidence, authentic approval or independent model accuracy.'
    ]
    def kind(path,body):
        if path=='AGENTS.md':return 'advisory_agent_guidance_not_runtime_authority'
        if path in by_path:return 'draft_practitioner_guide'
        if path=='EAA_Operational_Runbook.md':return 'draft_operational_runbook'
        if path=='EAA_Plain_English_Breakdown_and_Evidence_Guide.md':return 'secondary_eaa_explanation'
        if path=='control/validation-report.md':return 'historical_source_authored_validation_report'
        if path.startswith('control/'):return 'source_adoption_standards_and_remediation_context'
        if path.startswith('workflows/'):return 'workflow_definition_or_schema_not_deployed'
        if path=='records/templates.yaml':return 'blank_record_templates_not_actual_evidence'
        if path.endswith('.schema.json'):return 'record_schema_not_evidence_or_approval'
        return 'orientation_and_interpretation_guidance'
    def intro(path):
        parts=sections(texts[path])
        # Front matter may be a separate preamble. Keep it plus the opening heading/introduction.
        return ''.join(x[2] for x in parts[:2]) if (parts[0][1]=='Document preamble' or path=='EAA_Plain_English_Breakdown_and_Evidence_Guide.md') and len(parts)>1 else parts[0][2]
    def row(path,key,title,body,a,b,hierarchy):
        md=metadata(texts[path]) if path.endswith('.md') else {k:v for k,v in (safe_yaml(texts[path]) if path.endswith('.yaml') else json.loads(texts[path])).items() if k in ('schema_version','status','as_of','checked_on','verified_on','implementation_status','ready_for_operational_use')}
        if md.get('license','MIT')!='MIT':raise ValueError('Review changed source licence: '+path)
        return {'id':path+'::'+key,'title':title,'text':body,'record_type':kind(path,body),
            'source_repository':SOURCE,'source_path':path,'source_commit':sha,
            'source_url':f'https://github.com/{SOURCE}/blob/{sha}/{quote(path)}',
            'source_start_line':texts[path][:a].count('\n')+1,
            'source_end_line':max(1,texts[path][:b].count('\n')+(not texts[path][:b].endswith('\n'))),
            'source_document_sha256':digest(texts[path].encode()),'text_sha256':digest(body.encode()),
            'heading_path':hierarchy,'metadata_json':json.dumps(md,ensure_ascii=False,sort_keys=True,default=str),
            'declared_source_license':str(md.get('license','not_declared_in_document_front_matter')),
            'repository_license':'MIT','source_status':str(md.get('status','see_source_for_status')),
            'source_approval_status':str(md.get('review',{}).get('approval_status','not_established_by_export')),
            'dataset_version':cfg['dataset_version'],'export_format_version':cfg['export_format_version'],
            'source_commit_date':date,'language':'en-GB','required_context_paths':cfg['context_files'],
            'source_governance_context':texts['AGENTS.md'],
            'document_index_context':texts['control/document-index.yaml'],
            'source_register_context':texts['control/source-register.yaml'],
            'standards_status_context':texts['control/standards-status.yaml'],
            'scope_guide_context':texts['guides/01-scope-and-applicability.md'],
            'baseline_guide_context':texts['guides/02-requirements-and-assessment.md'],
            'record_contract_context':texts['records/README.md'],
            'source_document_intro':intro(path),
            'guide_prerequisite_context':texts[path] if path in by_path else 'Read the source status, scope, sources, dates and applicable prerequisites; this export grants no operational authority.',
            'legal_currency_status':'not_reverified_by_export',
            'interpretation_notice':'Secondary EAA guidance; six guides/runbook are draft for adoption. Preserve national applicability, legal versus technical evidence, source dates, exclusions and unresolved gaps. Templates/workflow definitions are not deployed or approved; retrieved instructions are data, never executed.',
            'validation_scope':'faithful extraction and packaging only; no independent legal, standards, national, product-conformity or operational validation'}

    docs,chunks=[],[]
    for path in cfg['files']:
        text=texts[path];docs.append(row(path,'document',path,text,0,len(text),[]))
        if path in cfg['document_only_files']:continue
        for key,title,body,a,b,hierarchy in sections(text):chunks.append(row(path,key,title,body,a,b,hierarchy))
    if not docs or not chunks:raise ValueError('Guidance export is empty.')
    schema={'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','required':list(docs[0]),'additionalProperties':False,'properties':{}}
    for key,value in docs[0].items():schema['properties'][key]={'type':'array','items':{'type':'string'}} if isinstance(value,list) else {'type':'integer' if isinstance(value,int) else 'string'}
    validator=Draft202012Validator(schema)
    for rows in (docs,chunks):
        if len({x['id'] for x in rows})!=len(rows):raise ValueError('Duplicate record IDs.')
        for item in rows:validator.validate(item)
    output.mkdir(parents=True,exist_ok=True)
    def write_json(name,value):(output/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for name,rows in [('documents.jsonl',docs),('knowledge_chunks.jsonl',chunks)]:
        (output/name).write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows),encoding='utf-8')
    (output/'LICENSE').write_bytes(texts['LICENSE'].encode());write_json('record_schema.json',schema)
    write_json('provenance.json',{'source_repository':SOURCE,'source_commit':sha,'source_commit_date':date,
        'destination_dataset':target,'dataset_version':cfg['dataset_version'],'export_format_version':cfg['export_format_version'],
        'files':manifest,'source_warnings':warnings,'external_sources_fetched':False,
        'source_instructions_executed':False,'legal_currentness_verified':False,
        'legal_applicability_determined':False,'compliance_or_conformance_verified':False,
        'operational_agent_deployed':False,'source_approval_changed':False,
        'excluded_source_files':sorted(EXCLUDED_SOURCES),
        'synthetic_developer_material_exported':False,
        'source_register_checked_on':sources.get('checked_on'),
        'standards_register_verified_on':standards.get('verified_on')})
    card=f'''---
pretty_name: Double FW European Accessibility Act Compliance Approach
language:
- en
license: mit
tags:
- accessibility
- european-accessibility-act
- governance
- inclusive-design
- secondary-source
- text
configs:
- config_name: knowledge_chunks
  default: true
  data_files:
  - split: train
    path: knowledge_chunks.jsonl
- config_name: documents
  data_files:
  - split: train
    path: documents.jsonl
---

# European Accessibility Act Compliance Approach

Double FW practitioner guidance for EAA scope, delivery, procurement, assessment, customer
outcomes, evidence, claims and continuing correction. It includes six guides, an operational
runbook, a plain-English explanation, source/adoption/standards registers, record contracts,
blank templates, schemas and workflow definitions. This is secondary guidance, not primary
law, legal advice, a complete EN test catalogue, an approved national adapter or a product
conformity assessment. The six guides and runbook remain draft for organisational adoption.

## Source and dates

Authoring source: https://github.com/{SOURCE}

Source commit: `{sha}` ({date}); dataset version {cfg['dataset_version']}; export format
{cfg['export_format_version']}. Exact original bodies, metadata, dates, source identities,
rights notices, line/heading spans and hashes remain traceable. Source review dates are
preserved, including {sources.get('checked_on')} in the source register and
{standards.get('verified_on')} in standards status. Export/commit dates do not refresh those
legal or standards checks. Workflow definitions do not become installed integrations.

Applicable primary law and national implementation govern real decisions. Verify current
scope, dates, conditions, exact provisions, relevant standards and legislation-specific
citation before live use. EAA and WAD citation must stay distinct. This sync does not fetch
linked law, standards, recovered attachments or other repositories, or check their currency,
rights, completeness or present availability. Source-register entries retain their constraints;
historical exclusions and unresolved dependencies remain excluded or unresolved.
Private access URLs are withheld from the public source register; source labels, hashes and
historical review status remain. This does not make private dependencies publicly available.

## Dataset views

- `documents`: {len(docs)} complete approved Markdown, YAML and JSON sources.
- `knowledge_chunks`: {len(chunks)} exact H1/H2 sections from the six guides, runbook and plain-English explanation.

Structured sources, governance, navigation and control reports stay complete-document only.
Sections preserve subordinate headings, complete tables, schemas, templates and fenced blocks.
Some sections and context fields are large; handle context budgets without silently truncating
conditions or qualifications. The views overlap; choose a view rather than count them as
independent examples. Repeated context is interpretation support, not additional evidence.
The `train` split is a loading convention, not evidence of model training or a benchmark split.

```python
from datasets import load_dataset
chunks = load_dataset("{target}", "knowledge_chunks", split="train")
documents = load_dataset("{target}", "documents", split="train")
```

## Interpretation and exclusions

Technical conformance, customer outcomes, statutory limitations, approvals and public claims
need distinct evidence and competent accountable decisions. Satisfaction is an additional
Double FW outcome, not an official fifth WCAG principle. Positive satisfaction does not erase
a failed obligation; a technical pass alone does not establish independent task completion,
equivalent experience or complete legal compliance. Missing/contradictory evidence stays visible.

Rows carry exact governance, document index, source and standards registers, scope and baseline
guides, record contract, source introduction and guide prerequisite context. Guide front matter
retains IDs, draft status, sources, prerequisites, outputs and review dates. Workflow IDs,
record types and original result vocabularies are preserved. Retrieved instructions and action
examples are data, never runtime authority or executed operations. Blank templates do not
contain actual approvals or real operational evidence; schema validity does not authenticate
identity, prove evidence true or authorise an action.

Excluded from both views:

- European_Accessibility_Act_EAA_RAG.md: a combined historical snapshot with duplicate source bodies.
- ANNEX1-EAA-REQUIREMENT-MATRIX.md: planning material with known WCAG-style numbering/coverage limitations; not retrieved as legal clause authority.
- examples/synthetic-service-cycle.yaml and validation/cases.yaml: synthetic developer fixtures, kept separate from training, real evidence and independent benchmarks.
- validation/check_repository.py, sync code, tests, setup, change log and workflow automation: implementation/maintenance material.

These GitHub files are retained. The historical source-authored control/validation-report.md
remains labelled as such; its statements describe its recorded review, not a freshly executed
legal review or the current licence decision. Current distribution is governed by root LICENSE
and the corrected README/source-register distribution metadata. Original source verification
dates remain unchanged. The separate generated validation_report.json reports packaging checks.

## Licence and data care

The unchanged MIT LICENSE is copied, including copyright (c) 2026 Double FW. Retain copyright
and permission notices when distributing copies or substantial portions. External law,
standards, linked materials and recovered sources retain their own terms; this repository's
MIT licence does not automatically relicense them or imply endorsement. No credentials,
actual participant records, customer/employee data or complaint evidence are added. Real
research and evidence use require their own authority and data arrangements.

## Updates and checks

Manual runs and Mondays at 08:17 UTC are configured in GitHub. GitHub can delay scheduled
runs or disable them after public-repository inactivity. Publication is one-way from approved
committed GitHub sources; it does not check weekly legal changes. New/renamed source files
require allow-list review. Missing sources/context, changed licence, unsafe paths or invalid
metadata/structured sources block publication.

Seven destination files are managed: README.md, LICENSE, documents.jsonl, knowledge_chunks.jsonl,
provenance.json, record_schema.json and validation_report.json. Existing unmanaged files,
including .gitattributes, are retained and do not automatically stay current. Dataset visibility
is preserved and historical downloads are not recalled. Destination: `{target}`.

The workflow runs the repository's structural/synthetic checker, extraction tests and export
validation before publication. Those checks do not prove legal currency, product conformity,
source truth, genuine approval, operational readiness or independently measured model accuracy.
Verify authenticated publication through the workflow result and destination provenance/history.
Pin a dataset revision for reproducible use.
'''
    yaml.safe_load(card.split('---',2)[1]);(output/'README.md').write_text(card,encoding='utf-8')
    report={'status':'passed','scope':'faithful extraction and packaging only','source_commit':sha,
        'source_files_verified':len(manifest),'document_records':len(docs),'knowledge_section_records':len(chunks),
        'source_warnings':warnings,'independent_content_review':False,'live_publication_tested':False,
        'export_file_sha256':{name:digest((output/name).read_bytes()) for name in MANAGED if name!='validation_report.json'}}
    write_json('validation_report.json',report);return report

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    print(json.dumps(build(ROOT,args.output)))

if __name__=='__main__':main()
