import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app
from validators import clean_amount, validate

GOOD = {"document_type": "rental", "name": "Janani R", "other_party": "Ravi K",
        "purpose": "2BHK flat", "duration": "11 months", "amount": "15000"}


class LegalEaseTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_01_home_page(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_02_valid_rental_preview(self):
        r = self.client.post("/generate", data=GOOD)
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"RENTAL AGREEMENT", r.data)

    def test_03_empty_fields_use_defaults(self):
        data, errors = validate({"document_type": "nda"})
        self.assertFalse(errors)
        self.assertEqual(data["name"], "Sample User")

    def test_04_invalid_amount_rejected(self):
        r = self.client.post("/generate", data={**GOOD, "amount": "abc"})
        self.assertEqual(r.status_code, 400)

    def test_05_negative_amount_rejected(self):
        with self.assertRaises(ValueError):
            clean_amount("-500", "0")

    def test_06_same_party_rejected(self):
        _, errors = validate({**GOOD, "other_party": "janani r"})
        self.assertTrue(errors)

    def test_07_unknown_type_rejected(self):
        r = self.client.post("/generate", data={**GOOD, "document_type": "x"})
        self.assertEqual(r.status_code, 400)

    def test_08_all_types_pdf(self):
        for t in ("rental", "nda", "employment", "leave"):
            r = self.client.post("/download", data={**GOOD, "document_type": t})
            self.assertEqual(r.status_code, 200, t)
            self.assertTrue(r.data.startswith(b"%PDF"), t)

    def test_09_special_characters_pdf(self):
        r = self.client.post("/download", data={**GOOD, "name": "A & B <Ltd>", "purpose": "<b>x"})
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.data.startswith(b"%PDF"))

    def test_10_long_text_truncated(self):
        data, _ = validate({**GOOD, "purpose": "x" * 1000})
        self.assertEqual(len(data["purpose"]), 200)


if __name__ == "__main__":
    unittest.main(verbosity=2)
