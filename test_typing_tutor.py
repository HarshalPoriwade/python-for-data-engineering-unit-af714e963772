import io
import unittest
from unittest import mock

import typing_tutor


class CleanTextTests(unittest.TestCase):
    def test_lowercases_and_removes_punctuation(self):
        self.assertEqual(typing_tutor.clean_text("Hello, World!"), ["hello", "world"])

    def test_extra_spaces_are_ignored(self):
        self.assertEqual(typing_tutor.clean_text("  hello    world "), ["hello", "world"])


class CountCorrectTests(unittest.TestCase):
    def test_task_example_counts_ten_correct(self):
        self.assertEqual(typing_tutor.count_correct("Hello, World!", "hello world"), 10)

    def test_task_example_is_one_hundred_percent(self):
        self.assertEqual(typing_tutor.accuracy("Hello, World!", "hello world"), 100.0)

    def test_one_wrong_letter(self):
        self.assertEqual(typing_tutor.count_correct("Hello, World!", "hello wurld"), 9)
        self.assertEqual(typing_tutor.accuracy("Hello, World!", "hello wurld"), 90.0)

    def test_missing_word_scores_zero_for_it(self):
        self.assertEqual(typing_tutor.count_correct("Hello, World!", "hello"), 5)
        self.assertEqual(typing_tutor.accuracy("Hello, World!", "hello"), 50.0)

    def test_extra_letters_at_end_of_word_do_not_add_points(self):
        self.assertEqual(typing_tutor.count_correct("Hello, World!", "hello worlds"), 10)

    def test_typing_only_first_letters_scores_only_those(self):
        self.assertEqual(typing_tutor.count_correct("Hello, World!", "h w"), 2)

    def test_empty_input_scores_zero(self):
        self.assertEqual(typing_tutor.count_correct("Hello, World!", ""), 0)
        self.assertEqual(typing_tutor.accuracy("Hello, World!", ""), 0.0)

    def test_sentence_with_no_letters(self):
        self.assertEqual(typing_tutor.accuracy("!!!", "anything"), 0.0)


class RecordTests(unittest.TestCase):
    def test_record_has_the_four_keys(self):
        record = typing_tutor.check_attempt("Hello, World!", "hello world", 3.456)
        self.assertEqual(
            record,
            {"sentence": "Hello, World!", "typed": "hello world",
             "accuracy": 100.0, "time": 3.46},
        )

    def test_average_accuracy(self):
        records = [{"accuracy": 100.0}, {"accuracy": 50.0}, {"accuracy": 90.0}]
        self.assertEqual(typing_tutor.average_accuracy(records), 80.0)

    def test_average_of_no_records_is_zero(self):
        self.assertEqual(typing_tutor.average_accuracy([]), 0.0)


class RunTutorTests(unittest.TestCase):
    def test_full_session_with_fake_typing_and_clock(self):
        sentences = ["Hello, World!", "Practice makes perfect!"]
        answers = ["hello world", "practise makes perfect"]
        clock = [10.0, 12.5, 20.0, 24.0]
        output = io.StringIO()
        with mock.patch("builtins.input", side_effect=answers), \
                mock.patch("typing_tutor.time.time", side_effect=clock), \
                mock.patch("sys.stdout", output):
            records = typing_tutor.run_tutor(sentences)
            typing_tutor.print_summary(records)

        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["time"], 2.5)
        self.assertEqual(records[0]["accuracy"], 100.0)
        self.assertEqual(records[1]["typed"], "practise makes perfect")
        self.assertEqual(records[1]["time"], 4.0)
        # "practise" vs "practice": 7 of 8 letters, total 20 letters -> 19/20
        self.assertEqual(records[1]["accuracy"], 95.0)
        text = output.getvalue()
        self.assertIn("Correct characters: 10 of 10", text)
        self.assertIn("Accuracy: 95.0%", text)
        self.assertIn("Time taken: 2.5 seconds", text)
        self.assertIn("Average accuracy: 97.5%", text)


if __name__ == "__main__":
    unittest.main()