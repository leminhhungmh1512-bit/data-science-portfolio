# Australia and New Zealand Census Analysis

This project compares migration patterns and cultural diversity in Australia and New Zealand using the 2021 Australian Census and the 2023 New Zealand Census. It was completed as a two-person CITS2402 Introduction to Data Science project at The University of Western Australia.

## Research question

How do migration patterns differ between Australia and New Zealand, and how are these patterns related to cultural diversity in the two countries?

The analysis is descriptive. It focuses on overseas-born population shares, major birthplaces, broad settlement cohorts, ethnicity or ancestry, and languages. It also examines how birthplace relates to selected language groups in New Zealand and how parents' birthplace relates to selected ancestry groups in Australia.

## Data sources

- Australian Bureau of Statistics, [2021 Census DataPacks](https://www.abs.gov.au/census/find-census-data/datapacks): General Community Profile tables G08, G09F-G09H, G10C and G13C-G13E for Australia.
- Stats NZ, [Aotearoa Data Explorer](https://explore.data.stats.govt.nz/): 2023 Census tables for birthplace, years since arrival, ethnicity, and language by birthplace at the national level.

The CSV extracts needed to reproduce the notebook are included in this folder. Their filenames are unchanged from the analysis so the notebook can be run without editing paths.

## Analysis workflow

1. Load the supplied CSV extracts with pandas.
2. Select relevant national totals and convert counts to numeric values.
3. Map source category codes to readable labels and exclude totals or residual categories where appropriate.
4. Check expected row counts, missing values and duplicate category codes in the New Zealand extracts.
5. Calculate percentages using stated denominators, then compare birthplace, arrival cohorts, ethnicity or ancestry, and language patterns.
6. Produce Matplotlib bar charts and document the interpretation, assumptions and limitations alongside the code.

The notebook contains the coursework analysis, tables and nine charts. This README explains the data preparation and how to run the analysis. The supplied CSV files and notebook results are unchanged.

## Main findings

- Among people with a stated birthplace, the overseas-born shares were similar: 29.3% in Australia and 28.8% in New Zealand.
- England, India and China appeared among the largest overseas birthplace groups in both countries, while the remaining top groups reflected different regional migration patterns.
- The language and ancestry comparisons showed associations with migration background, but they do not establish causation.

## Reproduce the analysis

Use Python 3.10 or later from this directory:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter notebook census_migration_cultural_diversity.ipynb
```

Run all cells from top to bottom. The notebook reads the CSV files from the same directory and displays the tables and charts inline.

## Limitations

- The Census years differ: Australia uses 2021 data and New Zealand uses 2023 data.
- The arrival-cohort labels are approximate. In particular, the Australian group labelled "Recent (< 5 yrs)" combines arrival years 2016-2021, whereas the New Zealand group combines less than one year through four years. The boundaries are not identical and should be checked before reusing this chart for reporting.
- Australia reports ancestry and language used at home, while New Zealand reports ethnicity and languages spoken. These concepts are related but not directly equivalent.
- Ancestry, ethnicity and language may allow multiple responses, so their percentages should not be summed.
- The analysis uses national totals and does not show variation within each country.
- Birthplace does not describe citizenship, migration category or reason for migration.
- The findings are descriptive associations and do not show that migration causes cultural diversity.

## Authors and academic context

The original coursework was completed collaboratively by Tri Cuong Do and Minh Hung Le. The source notebook contains the academic integrity declaration and detailed attribution. This repository presents the work as an academic portfolio project and preserves the submitted analysis.
