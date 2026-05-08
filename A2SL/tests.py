"""
Unit tests for the Voice2Sign NLP pipeline.

Run with:  python manage.py test A2SL
"""

from django.test import TestCase

from A2SL import nlp_utils, nlp_pipeline


class AssetRegistryTests(TestCase):
    def test_registry_populated(self):
        reg = nlp_utils.get_asset_registry()
        self.assertIn("hello", reg)
        self.assertEqual(reg["hello"], "Hello")

    def test_multi_word_assets(self):
        multi = nlp_utils.get_multi_word_assets()
        stems = [stem for _, stem in multi]
        self.assertIn("Thank You", stems)

    def test_has_video_hit(self):
        self.assertEqual(nlp_utils.has_video("Hello"), "Hello")
        self.assertEqual(nlp_utils.has_video("hello"), "Hello")

    def test_has_video_miss(self):
        self.assertIsNone(nlp_utils.has_video("xylophone"))


class StopwordTests(TestCase):
    def test_negation_preserved(self):
        sw = nlp_utils.get_stopwords()
        for word in ("not", "no", "never", "cannot"):
            self.assertNotIn(word, sw)

    def test_articles_removed(self):
        sw = nlp_utils.get_stopwords()
        for word in ("a", "an", "the"):
            self.assertIn(word, sw)


class SynonymTests(TestCase):
    def test_glad_maps_to_happy(self):
        hit = nlp_utils.find_synonym_with_video("glad")
        self.assertEqual(hit, "Happy")

    def test_unknown_word_returns_none(self):
        self.assertIsNone(nlp_utils.find_synonym_with_video("xylophone"))


class PipelineTests(TestCase):
    def test_empty_input_raises(self):
        with self.assertRaises(ValueError):
            nlp_pipeline.process_text("")

    def test_whitespace_only_raises(self):
        with self.assertRaises(ValueError):
            nlp_pipeline.process_text("   ")

    def test_hello_passthrough(self):
        result = nlp_pipeline.process_text("Hello")
        self.assertIn("Hello", result)

    def test_i_maps_to_me(self):
        result = nlp_pipeline.process_text("I am happy")
        self.assertTrue("Me" in result or "ME" in result)

    def test_past_tense_marker(self):
        result = nlp_pipeline.process_text("She walked to college")
        self.assertIn("Before", result)

    def test_synonym_expansion(self):
        result = nlp_pipeline.process_text("I am glad")
        self.assertIn("Happy", result)

    def test_fingerspelling_fallback(self):
        result = nlp_pipeline.process_text("xylophone")
        self.assertTrue(any(len(tok) == 1 and tok.isalpha() for tok in result))

    def test_thank_you_phrase(self):
        result = nlp_pipeline.process_text("thank you for your help")
        self.assertIn("Thank You", result)

    def test_output_all_strings(self):
        result = nlp_pipeline.process_text("I want to learn sign language")
        self.assertTrue(all(isinstance(tok, str) for tok in result))
