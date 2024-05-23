"""Higher-level api for searching for papers, uses an object interface
with overridden magic methods for syntactic sugar
"""
from typing import Union

from sxolar.api import arxiv
from sxolar.api.arxiv import LogicalOperator, SearchField


class Query:
    """Represents a query clause for the arxiv API

    Attributes:
        value (str): The value to search for
        operator (str): The operator to use
    """

    def __init__(self, value: str):
        """Creates a new query

        Args:
            value:
                str, the value to search for
        """
        self.value = value

    def __str__(self):
        """Returns the string representation of the query"""
        return self.value

    def __and__(self, other):
        """Overloads the and operator to create a new query"""
        return self.and_(other)

    def __or__(self, other):
        """Overloads the or operator to create a new query"""
        return self.or_(other)

    def __sub__(self, other):
        """Overloads the subtraction operator to create a new query"""
        return self.and_not(other)

    def and_(self, other: Union[str, 'Query']):
        """Join two queries with the AND operator

        Args:
            other:
                str, the other query to join with

        Returns:
            Query: A new query object
        """
        return Query(f'{self}{LogicalOperator.AND}{other}')

    def and_not(self, other):
        """Join two queries with the AND NOT operator

        Args:
            other:
                str, the other query to join with

        Returns:
            Query: A new query object
        """
        return Query(f'{self}{LogicalOperator.AND_NOT}{other}')

    def or_(self, other):
        """Join two queries with the OR operator

        Args:
            other:
                str, the other query to join with

        Returns:
            Query: A new query object
        """
        return Query(f'{self}{LogicalOperator.OR}{other}')

    def wrap(self):
        """Wrap the query in parenthesis

        Returns:
            Query: A new query object
        """
        return Query(f'({self})')

    def search(self, start: int = 0, max_results: int = 10):
        """Searches the arxiv API with the query

        Args:
            start:
                int, optional, The starting index of the results
            max_results:
                int, optional, The maximum number of results to return

        Returns:
            list: A list of dictionaries representing the search results
        """
        return arxiv._query(self.value, id_list=None, start=start, max_results=max_results)


class Author(Query):
    """Represents an author query for the arxiv API
    """

    def __init__(self, name: str):
        """Creates a new author query

        Args:
            name:
                str, the name of the author, "First Last"
        """
        if not name.startswith(SearchField.AUTHOR):
            name = f'{SearchField.AUTHOR}:{name}'
        super().__init__(name)


class Title(Query):
    """Represents a title query for the arxiv API
    """

    def __init__(self, title: str):
        """Creates a new title query

        Args:
            title:
                str, the title of the paper
        """
        if not title.startswith(SearchField.TITLE):
            title = f'{SearchField.TITLE}:{title}'
        super().__init__(title)


class Abstract(Query):
    """Represents an abstract query for the arxiv API
    """

    def __init__(self, abstract: str):
        """Creates a new abstract query

        Args:
            abstract:
                str, the abstract of the paper
        """
        if not abstract.startswith(SearchField.ABSTRACT):
            abstract = f'{SearchField.ABSTRACT}:{abstract}'
        super().__init__(abstract)


class All(Query):
    """Represents an all query for the arxiv API
    """

    def __init__(self, all_: str):
        """Creates a new all query

        Args:
            all_:
                str, the value to search for
        """
        if not all_.startswith(SearchField.ALL):
            all_ = f'{SearchField.ALL}:{all_}'
        super().__init__(all_)


class JournalRef(Query):
    """Represents a journal reference query for the arxiv API
    """

    def __init__(self, journal_ref: str):
        """Creates a new journal reference query

        Args:
            journal_ref:
                str, the journal reference
        """
        if not journal_ref.startswith(SearchField.JOURNAL_REFERENCE):
            journal_ref = f'{SearchField.JOURNAL_REFERENCE}:{journal_ref}'
        super().__init__(journal_ref)


class Category(Query):
    """Represents a category query for the arxiv API
    """

    def __init__(self, category: str):
        """Creates a new category query

        Args:
            category:
        """
        if not category.startswith(SearchField.CATEGORY):
            category = f'{SearchField.CATEGORY}:{category}'
        super().__init__(category)
