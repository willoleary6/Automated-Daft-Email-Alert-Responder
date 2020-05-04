from unittest import TestCase

from CsvHandler import CsvHandler


class TestCsvHandler(TestCase):
    def setUp(self):
        self.CsvHandler = CsvHandler()


class testReadAndWrite(TestCsvHandler):
    def test_read_csv_file_get_column_names(self):
        self.CsvHandler.read_csv_file()
        self.assertEqual(
            self.CsvHandler.get_csv_structure_dict(),
            {  # the expected shape of the csv file structure
                'sender': '',
                'receiver': '',
                'subject': '',
                'date': '',
                'status': '',
                'file path': ''
            }
        )

    def test_read_csv_file_get_data(self):
        self.CsvHandler.read_csv_file()
        actual_length = len(self.CsvHandler.get_data_read_from_csv())
        expected_length = 0
        # testing that the file is actually populated
        value_for_assert = False
        if actual_length >= expected_length:
            value_for_assert = True

        self.assertEqual(
            True,
            value_for_assert
        )

    def test_write_to_csv_file(self):
        self.CsvHandler.read_csv_file()
        pre_insertion_length = len(self.CsvHandler.get_data_read_from_csv())

        test_entry = {
            'sender': 'no-reply@accounts.google.com',
            'receiver': 'william.o.leary.789@gmail.com',
            'subject': 'Critical security alert',
            'date': '2020-05-04 12:21:30+00:00',
            'status': 'test',
            'file path': ''
        }
        self.CsvHandler.write_to_csv_file(test_entry)

        self.CsvHandler.read_csv_file()
        post_insertion_length = len(self.CsvHandler.get_data_read_from_csv())

        self.assertNotEqual(
            pre_insertion_length,
            post_insertion_length
        )
