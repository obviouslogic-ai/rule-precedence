import json
import unittest
from pathlib import Path

from precedence import Weakening, check, merge


def layer(name, **rules):
    return {"name": name, "rules": rules}


class PrecedenceTest(unittest.TestCase):
    def test_lower_layer_can_add(self):
        eff = check([layer("org"), layer("team", log=dict(type="flag", value=True))])
        self.assertTrue(eff["log"]["value"])

    def test_lower_layer_can_tighten(self):
        eff = check([layer("org", spend=dict(type="max", value=500)),
                     layer("team", spend=dict(type="max", value=100))])
        self.assertEqual(eff["spend"]["value"], 100)

    def test_cannot_raise_limit(self):
        with self.assertRaises(Weakening):
            check([layer("org", spend=dict(type="max", value=100)),
                   layer("team", spend=dict(type="max", value=900))])

    def test_cannot_turn_off_flag(self):
        with self.assertRaises(Weakening):
            check([layer("org", review=dict(type="flag", value=True)),
                   layer("team", review=dict(type="flag", value=False))])

    def test_cannot_widen_allow_list(self):
        with self.assertRaises(Weakening):
            check([layer("org", tools=dict(type="allow", value=["read"])),
                   layer("team", tools=dict(type="allow", value=["read", "delete"]))])

    def test_rejected_rule_keeps_stricter_value(self):
        eff, bad = merge([layer("org", spend=dict(type="max", value=100)),
                          layer("team", spend=dict(type="max", value=900))])
        self.assertEqual(eff["spend"]["value"], 100)
        self.assertEqual(len(bad), 1)

    def test_example_file(self):
        eff, bad = merge(json.loads(Path("example.json").read_text()))
        self.assertEqual(eff["max_spend"]["value"], 100)
        self.assertTrue(eff["require_review"]["value"])
        self.assertEqual(len(bad), 2)


if __name__ == "__main__":
    unittest.main()
