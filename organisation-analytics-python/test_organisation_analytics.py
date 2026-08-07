"""Tests for organisation analytics."""

import os
import tempfile
import unittest

from organisation_analytics import analyse_file, load_records


SAMPLE_DATA = os.path.join(os.path.dirname(__file__), "data", "sample_organisations.csv")


class TestOrganisationAnalytics(unittest.TestCase):
    def test_sample_analysis(self):
        result = analyse_file(SAMPLE_DATA)

        self.assertEqual(set(result["country_statistics"]), {"australia", "germany", "japan"})
        self.assertEqual(result["country_statistics"]["australia"]["organisation_count"], 4)
        self.assertEqual(result["category_rankings"]["energy"][0]["organisation_id"], "au-energy-01")
        self.assertEqual(result["category_rankings"]["transport"][0]["rank"], 1)

    def test_invalid_and_duplicate_rows_are_skipped(self):
        content = """organisation_id,country,category,number_of_employees,median_salary,profit_2020_million,profit_2021_million
valid-1,Australia,Energy,100,80000,10,12
valid-1,Australia,Energy,200,90000,12,15
bad-employees,Australia,Energy,-5,70000,8,9
,Australia,Energy,50,60000,5,6
"""
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as temporary:
            temporary.write(content)
            path = temporary.name

        try:
            records = load_records(path)
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["organisation_id"], "valid-1")
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
