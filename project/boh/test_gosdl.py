from django.test import TestCase

from . import gosdl


class TestModule(TestCase):

    def test_str(self):
        """Validates the `__str__` method returns the module title"""
        self.assertEqual('title', str(gosdl.Module('title')))

    def test_tags_when_none_sets_empty_list(self):
        """Validates tags is initialized to an empty list when a `None` argument is provided"""
        self.assertEqual([], gosdl.Module('test').tags)
        self.assertEqual([], gosdl.Module('test', tags=None).tags)

    def test_comma_separated_str_tags(self):
        """Validates comma-separated tags are properly split into a tags list"""
        tags_str = ',  one, two ,   three  ,fo  ur,, ,'
        expected = ['one', 'two', 'three', 'fo  ur']

        tags = gosdl.Module('Test', tags=tags_str).tags

        self.assertEqual(len(tags), len(expected))
        self.assertEqual(sorted(tags), sorted(expected))

    def test_tags_list(self):
        """Validates tags are initialized to the supplied list"""
        expected = ['one', 'two', 'three', 'four']
        tags = gosdl.Module('Test', tags=expected).tags
        self.assertEqual(tags, expected)

    def test_init_submodules(self):
        expected = [gosdl.Module('1'), gosdl.Module('2')]
        actual = gosdl.Module('test', submodules=expected).submodules
        self.assertEqual(actual, expected)

    def test_init_submodules_none_sets_list(self):
        self.assertEqual([], gosdl.Module('Test').submodules)
        self.assertEqual([], gosdl.Module('Test', submodules=None).submodules)


class TestChecklist(TestCase):

    def test_init_title(self):
        self.assertEqual('General', gosdl.Checklist().title)
        self.assertEqual('Test', gosdl.Checklist('Test').title)

    def test_init_questions(self):
        self.assertEqual([], gosdl.Checklist().questions)
        self.assertEqual([], gosdl.Checklist(questions=None).questions)
        self.assertEqual([], gosdl.Checklist(questions=[]).questions)
        # TODO Add expected questions test

    def test_str(self):
        self.assertEqual('title', str(gosdl.Checklist('title')))


class TestQuestion(TestCase):

    def test_init(self):
        from uuid import UUID
        q1 = gosdl.Question('Test')
        self.assertTrue(isinstance(q1.uuid, UUID))
        self.assertEqual(q1.text, 'Test')
        self.assertEqual(q1.description, None)

        q2 = gosdl.Question('Test', description='Description')
        self.assertEqual('Description', q2.description)

    def test_str(self):
        self.assertEqual('Test', str(gosdl.Question('Test')))

