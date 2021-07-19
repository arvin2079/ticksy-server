from django.test import TestCase
from ..validators import *


class TestValidators(TestCase):

    def test_validate_email_contain_at_sign(self):
        sample_email = 'example.com'
        self.assertFalse(validate_email(sample_email))

    def test_validate_email_multiple_at_sign(self):
        sample_email = 'A@b@c@domain.com'
        self.assertFalse(validate_email(sample_email))

    def test_validate_email_no_special_char_in_local_part(self):
        sample_email = 'a”b(c)d,e:f;gi[j\k]l@domain.com'
        self.assertFalse(validate_email(sample_email))

    def test_validate_email_quoted_strings(self):
        sample_email = 'abc”test”email@domain.com'
        self.assertFalse(validate_email(sample_email))

    def test_validate_email_spaces_quotes_and_backslashes(self):
        sample_email = 'abc is”not\\valid@domain.com'
        self.assertFalse(validate_email(sample_email))

    def test_validate_email_quotes_after_backslash(self):
        sample_email = 'abc\is\”not\\valid@domain.com'
        self.assertFalse(validate_email(sample_email))

    def test_validate_email_double_dot_before(self):
        sample_email = '.test@domain.com'
        self.assertFalse(validate_email(sample_email))

    def test_validate_email_double_dot_befor_domain(self):
        sample_email = 'test@domain..com'
        self.assertFalse(validate_email(sample_email))

    def test_validate_email_leading_space(self):
        sample_email = 'test@domain.com    '
        self.assertFalse(validate_email(sample_email))

    def test_validate_email_trailing_space(self):
        sample_email = '    test@domain.com'
        self.assertFalse(validate_email(sample_email))

    def test_validate_email_valid_form(self):
        sample_email = 'test@domain.com'
        self.assertTrue(validate_email(sample_email))

    def test_is_persian_leading_invalid_char(self):
        sample_quote = 's' + 'مثال'
        self.assertFalse(is_persian(sample_quote))

    def test_is_persian_trailing_invalid_char(self):
        sample_quote = 'مثال' + 's'
        self.assertFalse(is_persian(sample_quote))

    def test_is_persian_within_invalid_char(self):
        sample_quote = 'مثال' + 'k' + 'مثال'
        self.assertFalse(is_persian(sample_quote))

    def test_is_persian_all_invalid_char(self):
        sample_quote = 'example'
        self.assertFalse(is_persian(sample_quote))

    def test_is_persian_all_valid(self):
        sample_quote = 'کگوئدذرزطظژؤآإأءًٌٍَُِّ۱۲۳۴۵۶۷۸۹۰'
        self.assertTrue(is_persian(sample_quote))


    def test_is_english_leading_invalid_char(self):
        sample_quote = 'exmaple' + 'مثال'
        self.assertFalse(is_english(sample_quote))

    def test_is_english_trailing_invalid_char(self):
        sample_quote = 'مثال' + 'example'
        self.assertFalse(is_english(sample_quote))

    def test_is_english_within_invalid_char(self):
        sample_quote = 'sample' + 'مثال' + 'sample'
        self.assertFalse(is_english(sample_quote))

    def test_is_english_all_invalid_char(self):
        sample_quote = 'مثال'
        self.assertFalse(is_english(sample_quote))

    def test_is_english_all_valid(self):
        sample_quote = 'sdkflkjlk lsdk s'
        self.assertTrue(is_english(sample_quote))



