import unittest
import multi_replace

class TestMultiReplace(unittest.TestCase):
    def verify(self, from_to, text, want):
        config = {'from_to': []}
        for from_regex, to in from_to:
            config['from_to'].append({
                'from': from_regex,
                'to': to,
            })
        sub = multi_replace.MultiReplace(config)
        self.assertEqual(want, sub.sub(text))

    def test_multi(self):
        text = 'Larry Wall is the creator of Perl'
        want = 'Guido van Rossum is the Benevolent Dictator for Life of Python'
        config = [
            (r'L.+ W.l+', 'Guido van Rossum'),
            ('creator', 'Benevolent Dictator for Life'),
            ('Perl', 'Python'),
        ]
        self.verify(config, text, want)

    def test_order_matters(self):
        text = 'XXX XX X X XX XXX'
        want = 'AAA BB C C BB AAA'
        config = [
            ('XXX', 'AAA'),
            ('XX', 'BB'),
            ('X', 'C'),
        ]
        self.verify(config, text, want)

    def test_backref(self):
        self.verify([(r'(\w+)=(\w+)', r'\2=\1')], 'left=right', 'right=left')

    def test_func(self):
        self.verify([(r'\w+', str.lower)], 'TOlOWER', 'tolower')

    def test_func_with_one_group(self):
        self.verify([(r'(\w+)', str.lower)], 'TOlOWER', 'tolower')


if __name__ == '__main__':
    unittest.main()
