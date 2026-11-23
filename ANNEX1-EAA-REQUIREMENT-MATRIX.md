# EAA Annex I requirement support matrix

## Purpose and authority

This matrix routes Annex I requirements to relevant public Double-FW guidance and evidence workflows. It is a planning aid, not a complete legal interpretation, technical test catalogue, applicability decision, or conformity statement.

Use the [official Directive (EU) 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882/oj), especially Articles 2 and 4 and Annex I, as the legal source. Confirm the service or product scope, responsible economic operator, applicable national transposition, exemptions, exceptions and any permitted alternative route with the authorised reviewer. The Directive’s requirements depend on the subject and route; do not assume that every Annex I section applies to every product or service.

The linked [EAA Annex I training dataset in Inclusive and Effective Design](https://github.com/Double-FW/Inclusive_and_Effective_Design/blob/main/EAA%20Annex%201%20%E2%80%94%20Training%20Dataset%20%28Websites%20%26%20Online%20Applications%29.md) is explicitly marked **superseded**. It is a migration notice, not current guidance or a source for extracting legal requirements. Use the repository’s current [Inclusive Digital Service Outcome Dataset](https://github.com/Double-FW/Inclusive_and_Effective_Design/blob/main/Inclusive_Digital_Service_Outcome_Dataset.md) for the Double-FW Layer 2 outcome model.

## Legal routing through Annex I

Article 4 determines which Annex I sections apply, subject to the Directive’s scope and qualifications. In broad terms, products route to Sections I and, except self-service terminals, II. Services route to Section III except urban, suburban and regional transport services, and services route to Section IV; Article 4(5) provides a service-provider microenterprise exemption from the requirements referred to in Article 4(3). Answering 112 emergency communications has the specific Section V route. Apply all qualifications and national implementation provisions. Section VII contains functional performance criteria with its own conditions. This summary is a navigation aid; use the Directive and applicable national law for the actual decision.

| Internal reference | Annex I location | Requirement area | Routing note |
| --- | --- | --- | --- |
| A1-I | Section I | General requirements for products | Apply to products within Article 2(1), subject to the Directive. |
| A1-II | Section II | Additional product requirements | Apply to products other than self-service terminals, subject to the Directive. |
| A1-III-a | Section III(a) | Accessibility of products used to provide a service | Assess relevant products under Section I and, where applicable, Section II. |
| A1-III-b | Section III(b)(i–vii) | Information about the service, related products, accessibility characteristics and interoperability | Assess the required information channels, format, understandability, perception, text availability, typography, non-text alternatives and POUR properties in context. |
| A1-III-c | Section III(c) | Websites, related online applications and mobile-device-based services | Assess the in-scope web and mobile service consistently against the legal wording and selected technical assessment profile. |
| A1-III-d | Section III(d) | Available support services | Assess accessible communication modes and information about service accessibility and assistive-technology compatibility where support services are available. |
| A1-IV-a | Section IV(a) | Electronic communications services, including specified emergency communications | Check real-time text, total conversation where video accompanies voice, and required synchronisation and routing. |
| A1-IV-b | Section IV(b) | Services providing access to audiovisual media services | Check EPG accessibility and accessibility-component transmission, quality, synchronisation and user control. EAA coverage of access services does not make this a general media-production or AVMSD assessment. |
| A1-IV-c | Section IV(c) | Specified air, bus, rail and waterborne passenger transport services | Check accessibility, assistance, ticketing, real-time travel and other service information. The stated urban, suburban and regional transport exclusions matter. |
| A1-IV-d | Section IV(d) | Urban, suburban and regional transport services | The specified requirement concerns accessibility of self-service terminals under Section I. Do not generalise it to all digital transport interfaces. |
| A1-IV-e | Section IV(e) | Consumer banking services | Check accessible identification, electronic signatures, security and payment, and the specific information-complexity condition. |
| A1-IV-f | Section IV(f) | E-books | Check synchronised text/audio where present, AT operation, content and navigation access, structure, presentation choice, alternative renditions, discoverability metadata and DRM effects. |
| A1-IV-g | Section IV(g) | E-commerce services | Check accessibility information where supplied by the responsible operator and accessible identification, security, signature and payment functions as specified. |
| A1-V | Section V | Answering 112 emergency communications | Apply the specific Section V requirements through the national emergency-system organisation and competent authority. |
| A1-VII | Section VII | Functional performance criteria | Use only under the conditions in Section VII. It is not a general substitute checklist or an automatic alternative to a specific technical requirement. |

Annex III built-environment requirements are a separate route: Article 4(4) allows Member States to decide whether specified built environments used by clients of covered services must meet them. Annex II contains indicative, non-binding examples of possible solutions; it is not itself a list of binding requirements.

## Section VII functional performance criteria

Section VII addresses functions not covered by Sections I–VI and also sets conditions for using a functional performance criterion as an alternative to a specific technical requirement. Do not invoke it to waive a requirement by assertion. Record the exact function, clause, legal route, evidence and authorised decision; demonstrate the result required by the Directive for foreseeable use.

The criteria address: use without vision; use with limited vision; use without perception of colour; use without hearing; use with limited hearing; use without vocal capability; use with limited manipulation or strength; use with limited reach; minimising photosensitive seizure risk; use with limited cognition; and privacy.

These are criteria in the Directive, not a complete taxonomy of disability or a set of Double-FW personas. For research or design planning, use voluntary, task-relevant needs questions and preserve the limits described in the EAA repository’s [customer outcomes and research guide](guides/04-customer-outcomes-and-research.md).

## Double-FW outcome and terminology alignment

The Double-FW [Inclusive Digital Service Outcome Dataset (IDSO)](https://github.com/Double-FW/Inclusive_and_Effective_Design/blob/main/Inclusive_Digital_Service_Outcome_Dataset.md) is an organisational design and research framework, not legislation or a technical standard. Use relevant IDSO outcomes to plan and interpret functional, task and experience evidence; do not relabel them as EAA clauses or treat a positive outcome as proof of legal conformity.

| Annex I route | Relevant Double-FW guidance | Use and boundary |
| --- | --- | --- |
| Sections I–IV and VII: identify needs, tasks and outcomes | [Inclusive Digital Service Outcome Dataset](https://github.com/Double-FW/Inclusive_and_Effective_Design/blob/main/Inclusive_Digital_Service_Outcome_Dataset.md) | Select material outcomes with rationale. Preserve outcome IDs, context, population, method, limitations and uncertainty. |
| Section III(b–d), IV and VII: communication, modality, structure and cognition | [Inclusive Multimodal UX](https://github.com/Double-FW/Inclusive-Multimodal-UX) · [Cognitive UX Design](https://github.com/Double-FW/Cognitive-UX-Design) | Inform design and evaluation. Guidance does not itself establish that a service meets a clause. |
| Section IV(b): media access services and connected controls | [Inclusive Media Interfaces](https://github.com/Double-FW/Inclusive-Media-Interfaces) · [AVMSD delivery and evidence repository](https://github.com/Double-FW/The-Audiovisual-Media-Services-Directive-AVMSD-) | Use media-interface guidance for discovery and control; use the AVMSD source for its separate regulatory route. Do not conflate the two legal regimes. |
| Technical requirements, test planning and evidence | [QA Accessibility Testing](https://github.com/Double-FW/QA_Accessibility_Testing) | Use its canonical sources and selected standards mappings. A mapping, automated result or test count alone does not establish full legal coverage. |
| Terminology and interpretation status | [Double-FW Terminology and Principles](https://github.com/Double-FW/Terminology-and-Principles), starting with [Start Here](https://github.com/Double-FW/Terminology-and-Principles/blob/main/START_HERE.md) | Preserve originating authority and entry status. Proposed or unresolved terms are not automatically adopted definitions. |

All Double-FW destinations listed above were checked as public repositories during this update. Follow each repository’s own source hierarchy and authority notes.

## Technical mapping is a separate layer

The previous version used WCAG-style topic numbers (1.1–4.1) as if they were Annex I clause numbers. That was inaccurate and has been corrected. The topic labels below are useful technical-assessment routes only; they are not Annex I references and do not establish one-to-one equivalence with an Annex I requirement.

| Technical topic family | Possible Annex I relationship | Required qualification |
| --- | --- | --- |
| Text alternatives; time-based media | Section III(b), III(c), and where applicable IV(b), IV(f) | Identify the actual information, service function and applicable specific-service clause. |
| Adaptable and distinguishable content | Section III(b–c), and relevant product clauses | Map the chosen technical baseline and assessed functions; do not treat a WCAG topic number as the legal clause. |
| Keyboard access; timing and pauses; seizure and physical-reaction risks; navigation; input modalities | Section III(c), relevant Sections I–II or IV, and potentially VII | Confirm the service or product, user task, technical baseline, specialist scope and evidence. |
| Readable language; predictable operation; input assistance | Section III(b–c), relevant Sections I–II or IV, and potentially VII | Check the actual legal wording and any specific conditions, including banking information complexity where applicable. |
| Compatibility with assistive technologies and systems | Section III(a–d), relevant Sections I–II or IV | Assess the applicable product, information, interface, support and interoperability requirements; do not infer compatibility from code quality alone. |

A WCAG criterion or EN 301 549 provision may support assessment of an Annex I requirement when the relationship is established for the applicable scope and baseline. Record the exact source/version, clause, relationship type, coverage limits, assessment method and evidence. Do not assume that shared terminology or numbering proves equivalence. The [requirements and assessment guide](guides/02-requirements-and-assessment.md) gives the repository’s mapping and baseline rules.

## Evidence and use workflow

1. **Establish scope first.** Use [scope and applicability](guides/01-scope-and-applicability.md) to record the product or service, operator, jurisdiction, relevant dates, facts and authorised applicability decision.
2. **Select applicable Annex I clauses.** Keep the legal text and its interpretation separate. Record the exact clause, source version, applicability rationale and unresolved questions.
3. **Choose the assessment profile.** Record adopted standards, versions, contractual baselines, other technical requirements and specialist methods. Do not imply WCAG 2.2 A/AA is named directly by the Directive.
4. **Map without overstating.** Use exact clause-level relationships such as supports, partially supports, contradicts or assesses. One requirement may need multiple tests; one test may inform multiple requirements.
5. **Use outcomes as complementary evidence.** Select relevant IDSO outcomes; distinguish technical conformance, functional access, task outcomes and experience findings.
6. **Evaluate and preserve limits.** Record test setup, task/state, release, method, sample, observation, failures, uncertainty, accessibility barriers and what the evidence cannot establish.
7. **Route decisions to the right authority.** QA prepares assessment; authorised legal/compliance reviewers determine legal meaning and claims. Follow [evidence, conformity and claims](guides/05-evidence-conformity-and-claims.md). Do not turn a positive user outcome, standards mapping or automated pass into an EAA conformity conclusion.

## Reusable agent prompts

**Requirement routing**

> For the identified product or service and approved jurisdictional scope, retrieve the relevant text of Directive (EU) 2019/882, including the exact Annex I clause and Article 4 route. Separate legal text from interpretation. Record applicability, source/version, technical mappings, their relationship and limits, selected methods, evidence needs and unresolved issues. Use Double-FW outcome guidance only as complementary design or research guidance. Do not decide legal applicability or approve a conformity claim.

**Outcome and evidence planning**

> For each applicable Annex I clause, identify the user tasks and contexts that could be affected. Select relevant IDSO outcomes with a rationale, then propose complementary technical, manual, assistive-technology, service and user-research evidence as appropriate. Keep statutory requirements, standards mappings, observed outcomes, hypotheses and recommendations distinct. State missing evidence and route legal or conformity decisions to the authorised human reviewer.

## References and maintenance

- [Directive (EU) 2019/882, EUR-Lex](https://eur-lex.europa.eu/eli/dir/2019/882/oj) — authoritative legal text.
- [Inclusive Digital Service Outcome Dataset](https://github.com/Double-FW/Inclusive_and_Effective_Design/blob/main/Inclusive_Digital_Service_Outcome_Dataset.md) — current Double-FW Layer 2 outcome framework.
- [Superseded Annex I training dataset migration notice](https://github.com/Double-FW/Inclusive_and_Effective_Design/blob/main/EAA%20Annex%201%20%E2%80%94%20Training%20Dataset%20%28Websites%20%26%20Online%20Applications%29.md) — do not use as current requirements or legal interpretation.
- Repository-local [source register](SOURCE-REGISTER.md), [standards status](control/standards-status.yaml), scope, assessment and evidence guides determine source status and workflow.

Update this matrix when the legal text, relevant national provisions, approved technical profile or linked canonical Double-FW sources change. Record the reviewed source revision and date in the change history; do not silently convert a proposed mapping into an approved legal interpretation.
