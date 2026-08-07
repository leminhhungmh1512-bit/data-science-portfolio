# Organisation Analytics in Python

## Overview

This project analyses organisation records by country and industry category. It demonstrates data validation, grouping, statistical calculation and multi-key ranking using only Python's standard library.

The portfolio version uses a small synthetic dataset so the original coursework data and submission are not published.

## Questions Answered

- How different were average organisation profits between 2020 and 2021 within each country?
- How far apart were employee counts and median salaries using third-order Minkowski distance?
- Which organisations ranked highest in each category by employee count, with profit growth as a tie-breaker?

## Data Processing

The program:

- normalises headings and text fields;
- rejects missing, malformed and non-positive values;
- removes duplicate organisation IDs;
- calculates a two-sample t-score by country;
- calculates Minkowski distance by country; and
- ranks organisations within each category.

## Files

```text
organisation-analytics-python/
├── data/sample_organisations.csv
├── organisation_analytics.py
└── test_organisation_analytics.py
```

## Run the Analysis

```bash
python organisation_analytics.py data/sample_organisations.csv
```

## Run the Tests

```bash
python -m unittest -v
```

No third-party packages are required.
