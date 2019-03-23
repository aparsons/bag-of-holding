"""

"""

import json, uuid
from typing import List, Union


class Module(object):
    """
    Attributes:
        title (str): The name of the module
        category (str):
        description (str, optional):
        tags (list(str), optional):
        questions (list(Checklist), optional):
        submodules (list(Module), optional):
    """

    def __init__(self, title: str, category: str = 'General', description: str = None,
                 tags: Union[str, List[str]] = None, questions: List['Checklist'] = None,
                 submodules: List['Module'] = None):
        self.title = title
        self.category = category
        self.description = description

        if tags is None:
            tags = []
        if isinstance(tags, str):
            # Split out comma-separated string and strip whitespace
            self.tags = list(filter(None, [tag.strip() for tag in tags.split(',') if tag]))
        elif isinstance(tags, list):
            self.tags = tags

        if questions is None:
            questions = []
        self.questions = questions

        if submodules is None:
            submodules = []
        self.submodules = submodules

    def __str__(self):
        return self.title


class Checklist(object):
    def __init__(self, title: str = 'General', questions: List['Question'] = None):
        self.title = title
        if questions is None:
            questions = []
        self.questions = questions

    def __str__(self):
        return self.title


class Question(object):
    """A specific question

    Attributes:
        uuid (UUID):
        text (str): The text of the question
        description (str, optional): A description of the question
    """

    def __init__(self, text: str, description: str = None):
        self.uuid = uuid.uuid4()
        self.text = text
        self.description = description

    def __str__(self):
        return self.text


class GoSDL(object):  # TODO REMOVE?
    """
    Attributes:
        title (str):
        description (str, optional):
    """

    def __init__(self, title, description=None):
        self.title = title
        self.description = description

    def __str__(self):
        return self.title

    @classmethod
    def from_json(cls, value):
        return GoSDL('as', 'as')

    class Category(object):
        pass
