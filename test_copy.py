import unittest

import lint_copy


def _phrase(*parts):
    return "".join(parts)


class CopyLintTest(unittest.TestCase):
    def test_repo_copy_matches_verified_wording(self):
        self.assertEqual(lint_copy.check_repo(), [])

    def test_guard_rejects_savings_figures_and_numbers(self):
        errors = lint_copy.check_digits("Defaults include " + "1" + "00 runs.")
        self.assertTrue(errors)
        errors = lint_copy.check_claims("The gap is " + "$" + "11000 a month.")
        self.assertTrue(errors)
        errors = lint_copy.check_claims("Modelled " + "overspend" + " stays on the page.")
        self.assertTrue(errors)
        errors = lint_copy.check_claims("Quoted " + "savings" + " stay off the page.")
        self.assertTrue(errors)

    def test_guard_rejects_every_attempt_claim(self):
        sample = _phrase("Every ", "attempt is ", "reported.")
        self.assertTrue(lint_copy.check_claims(sample))
        sample = _phrase("Any ", "attempt to loosen one is ", "reported.")
        self.assertTrue(lint_copy.check_claims(sample))

    def test_guard_rejects_each_spelled_number(self):
        for word in lint_copy.SPELLED_NUMBERS:
            with self.subTest(word=word):
                self.assertTrue(lint_copy.check_spelled_numbers("Count " + word + " items."))

    def test_guard_rejects_every_single_attempt(self):
        sample = _phrase("Every ", "single ", "attempt gets a line.")
        self.assertTrue(lint_copy.check_claims(sample))

    def test_guard_rejects_write_once(self):
        self.assertTrue(lint_copy.check_claims(_phrase("write", "-once")))

    def test_guard_rejects_cannot_be_altered(self):
        self.assertTrue(lint_copy.check_claims(_phrase("cannot ", "be ", "altered")))

    def test_guard_rejects_integrity_claims(self):
        for sample in (
            _phrase("hash", "-chain"),
            _phrase("hash", " chain"),
            _phrase("tamper", "-proof"),
            _phrase("tamper", " proof"),
            _phrase("tamper", "-evident"),
            _phrase("tamper", " evident"),
            _phrase("immutab", "ility"),
            _phrase("immutab", "le ledger"),
        ):
            self.assertTrue(lint_copy.check_claims(sample), sample)

    def test_guard_rejects_real_person_names(self):
        sample = _phrase("Dan", " ", "De", "Zago")
        self.assertTrue(lint_copy.check_names(sample))
        self.assertTrue(lint_copy.check_names("Written by " + "Dan" + "."))

    def test_guard_rejects_single_and_lowercase_names(self):
        self.assertTrue(lint_copy.check_names("see " + "dan"))
        self.assertTrue(lint_copy.check_names("see " + "dezago"))
        self.assertTrue(lint_copy.check_names("dan" + " " + "dezago"))

    def test_layer_and_role_words_are_not_names(self):
        sample = " ".join(lint_copy.LAYERS) + " operator department charter agent client"
        self.assertEqual(lint_copy.check_names(sample), [])

    def test_layers_must_stay_in_order(self):
        good = " ".join(
            (
                lint_copy.LEAD,
                lint_copy.SENTENCE,
                lint_copy.RATIFY,
                "Charter, Agent code, Operator (build work only), Department, and Client adjustment.",
            )
        )
        self.assertEqual(lint_copy.require_story(good), [])
        bad = " ".join(
            (
                lint_copy.LEAD,
                lint_copy.SENTENCE,
                lint_copy.RATIFY,
                "Client adjustment, then Charter, Agent code, Operator (build work only), Department.",
            )
        )
        self.assertTrue(lint_copy.require_story(bad))


if __name__ == "__main__":
    unittest.main()
