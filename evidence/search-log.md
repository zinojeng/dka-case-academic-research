# Evidence search log (evidence-librarian)

Compiled 2026-10-28 (research date, not a case date). Source IDs refer to `evidence/source-register.json`. Raw files and parse outputs are in the git-ignored `fulltext/` and `parsed/`.

## Tools used
- paper-search MCP: `get_crossref_paper_by_doi`, `search_pubmed`, `search_europepmc`, `search_unpaywall`, `download_with_fallback`
- research_hub MCP: `download_paper` (1 call, failed with 403)
- scihub MCP: `download_pdf` (8 calls: 3 succeeded, 5 failed)
- llamaparse MCP: `parse_pdf_to_markdown` (3 calls, all succeeded)
- NCBI E-utilities (esummary/efetch), Europe PMC REST, curl to publisher/PMC/EMA/DailyMed, WebFetch (ADA 2026 page and DailyMed; quotes then re-verified against raw HTML)

## Queries and outcomes
| # | Query / lookup | Tool | Result |
|---|---|---|---|
| 1 | DOI 10.2337/dci24-0032 | Crossref | Found: Diabetes Care 47(8):1257-1275 (S01) |
| 2 | DOI 10.2337/dc26-S016 | Crossref | Found: Diabetes Care 49(Suppl 1):S339-S355 (S03) |
| 3 | DOI 10.2337/dci24-0032 | Unpaywall | Empty result |
| 4 | DOI:"10.2337/dci24-0032" | Europe PMC | PMID 39052901, PMC11272983, isOpenAccess false |
| 5 | balanced crystalloids saline diabetic ketoacidosis randomized | PubMed | 10 hits: Self 2020, Alghamdi 2022, BRISK-ED 2024, Liu 2024, Szabo 2024, Soliman 2026, Agarwal 2025 (paediatric), paediatric MA 2026, protocols |
| 6 | Plasma-Lyte saline DKA SCOPE-DKA | PubMed | 0 hits |
| 7 | Ramanan Plasma-Lyte 148 vs saline DKA ICU | PubMed | Attokaran 2023 nested cohort; BEST-DKA protocol 2025 (S07) |
| 8 | BEST-DKA results (sorted by date) | PubMed | Protocol only; no results paper found |
| 9 | PMID 34609547 (SCOPE-DKA) | E-utilities | Verified Intensive Care Med 47:1248-1257 (S05); abstract read |
| 10 | phosphate therapy DKA randomized Fisher Kitabchi | PubMed | PMID 6406531 (S09) |
| 11 | Katz hyperglycemia-induced hyponatremia | PubMed / Crossref | PMID 4763428; NEJM 289:843-844 (S10) |
| 12 | Hillier correction factor (3 query variants) | PubMed MCP | 0 hits; resolved by Crossref DOI and E-utilities PMID 10225241 (S11) |
| 13 | Roscoe 1975 metabolic factor | PubMed | PMID 1111894 (S12) |
| 14 | pseudohyponatremia TG direct indirect ISE | PubMed | PMID 42729988 (S15) |
| 15 | pseudohyponatremia lipemia blood gas analyzer | PubMed | Vera 2022 (S13), Evenepoel 2022 (S14) |
| 16 | pseudohyponatremia review electrolyte exclusion | PubMed | 0 hits (no narrative methods review registered) |
| 17 | Toujeo / NovoRapid labels | EMA EPAR PDFs; DailyMed | S16, S17, S18 retrieved |

## Full-text retrieval
- Successes: S02 XML (Europe PMC), S03 HTML (PMC), S04/S09/S11 PDFs (Sci-Hub), S16/S18 PDFs (EMA), S17 HTML (DailyMed).
- Failures: see `fulltext-manifest.json > failed_attempts`. Every HTML challenge page saved under a .pdf name was deleted and is **not** counted as a download.
- Abstract-only: S05 SCOPE-DKA, S06 BRISK-ED, S07, S08, S12-S15. Metadata-only: S01 (content via S02), S10 Katz, S19 (2009 consensus).

## Peer-supplied locators
Received two peer messages: electrolyte-specialist (Diabetologia XML, Fig 4 discrepancy) and fluid-insulin-specialist (locators; Toujeo US set 257ca17b). These were incorporated as noted in the register. Peer-reported items that I did not verify myself are labelled as such.

## Accuracy review notes
- The 2024 consensus statements were checked against the Diabetologia XML text. Figures were not read.
- The ADA 2026 quotes were re-verified against raw PMC HTML, because the WebFetch summary is paraphrastic.
- The LlamaParse output for figure-only content (Fisher Fig 1-2, Hillier Fig 1-3) is unreliable and is flagged in the manifest.
- Discrepancies D1-D7 are listed in the register.
