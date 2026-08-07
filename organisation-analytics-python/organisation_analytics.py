"""Statistical analysis and ranking for organisation records."""

import csv
import json
import sys


REQUIRED_FIELDS = {
    "organisation_id",
    "country",
    "category",
    "number_of_employees",
    "median_salary",
    "profit_2020_million",
    "profit_2021_million",
}


def _normalise_heading(value):
    return "_".join(value.strip().lower().replace("(", " ").replace(")", " ").split())


def _sample_standard_deviation(values):
    if len(values) < 2:
        raise ValueError("At least two observations are required")
    average = sum(values) / len(values)
    variance = sum((value - average) ** 2 for value in values) / (len(values) - 1)
    return variance**0.5


def _minkowski_distance(first, second, order=3):
    return sum(abs(a - b) ** order for a, b in zip(first, second)) ** (1 / order)


def load_records(csv_path):
    """Read valid, unique organisation records from a CSV file."""

    records = []
    seen_ids = set()

    with open(csv_path, newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None:
            raise ValueError("The input file has no header row")

        heading_map = {heading: _normalise_heading(heading) for heading in reader.fieldnames}
        if not REQUIRED_FIELDS.issubset(heading_map.values()):
            missing = sorted(REQUIRED_FIELDS - set(heading_map.values()))
            raise ValueError(f"Missing required columns: {', '.join(missing)}")

        for raw_record in reader:
            record = {heading_map[key]: value.strip() for key, value in raw_record.items()}
            try:
                organisation_id = record["organisation_id"].lower()
                country = record["country"].lower()
                category = record["category"].lower()
                employees = int(record["number_of_employees"])
                median_salary = float(record["median_salary"])
                profit_2020 = float(record["profit_2020_million"])
                profit_2021 = float(record["profit_2021_million"])
            except (KeyError, TypeError, ValueError):
                continue

            if (
                not organisation_id
                or not country
                or not category
                or employees <= 0
                or median_salary <= 0
                or profit_2020 == 0
                or organisation_id in seen_ids
            ):
                continue

            seen_ids.add(organisation_id)
            records.append(
                {
                    "organisation_id": organisation_id,
                    "country": country,
                    "category": category,
                    "employees": employees,
                    "median_salary": median_salary,
                    "profit_2020": profit_2020,
                    "profit_2021": profit_2021,
                }
            )

    return records


def analyse_by_country(records):
    """Calculate profit t-scores and Minkowski distances by country."""

    grouped = {}
    for record in records:
        country = record["country"]
        grouped.setdefault(
            country,
            {"profit_2020": [], "profit_2021": [], "employees": [], "salary": []},
        )
        grouped[country]["profit_2020"].append(record["profit_2020"])
        grouped[country]["profit_2021"].append(record["profit_2021"])
        grouped[country]["employees"].append(record["employees"])
        grouped[country]["salary"].append(record["median_salary"])

    results = {}
    for country, values in grouped.items():
        if len(values["profit_2020"]) < 2:
            continue

        mean_2020 = sum(values["profit_2020"]) / len(values["profit_2020"])
        mean_2021 = sum(values["profit_2021"]) / len(values["profit_2021"])
        standard_error = (
            _sample_standard_deviation(values["profit_2020"]) ** 2
            / len(values["profit_2020"])
            + _sample_standard_deviation(values["profit_2021"]) ** 2
            / len(values["profit_2021"])
        ) ** 0.5

        if standard_error == 0:
            continue

        results[country] = {
            "profit_t_score": round((mean_2020 - mean_2021) / standard_error, 4),
            "employee_salary_minkowski_distance": round(
                _minkowski_distance(values["employees"], values["salary"]), 4
            ),
            "organisation_count": len(values["profit_2020"]),
        }

    return results


def rank_by_category(records):
    """Rank organisations by employees, then absolute profit change."""

    grouped = {}
    for record in records:
        profit_change = abs(record["profit_2021"] - record["profit_2020"])
        profit_change = profit_change / abs(record["profit_2020"]) * 100
        grouped.setdefault(record["category"], []).append(
            {
                "organisation_id": record["organisation_id"],
                "employees": record["employees"],
                "profit_change_percent": round(profit_change, 4),
            }
        )

    rankings = {}
    for category, organisations in grouped.items():
        ordered = sorted(
            organisations,
            key=lambda item: (
                -item["employees"],
                -item["profit_change_percent"],
                item["organisation_id"],
            ),
        )
        rankings[category] = [
            {**organisation, "rank": rank}
            for rank, organisation in enumerate(ordered, start=1)
        ]

    return rankings


def analyse_file(csv_path):
    """Return country statistics and category rankings for a CSV file."""

    records = load_records(csv_path)
    if not records:
        raise ValueError("No valid organisation records were found")
    return {
        "country_statistics": analyse_by_country(records),
        "category_rankings": rank_by_category(records),
    }


def main(arguments=None):
    arguments = sys.argv[1:] if arguments is None else arguments
    if len(arguments) != 1:
        raise SystemExit("Usage: python organisation_analytics.py <csv-file>")
    print(json.dumps(analyse_file(arguments[0]), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
