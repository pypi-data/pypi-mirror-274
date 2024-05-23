"""Arxiv API wrappers for sxolar, low-level functions for querying the Arxiv API.
For more user-friendly functions, see the `sxolar.api.query` module.

References:
    [1] API Basics: https://info.arxiv.org/help/api/basics.html
    [2] Rate Limits: https://info.arxiv.org/help/api/tou.html
    [3] Search Query Language: https://info.arxiv.org/help/api/user-manual.html#query_details
    [4] Entry output format: https://info.arxiv.org/help/api/user-manual.html#_entry_metadata
"""
import collections
from typing import List, Union
from urllib import parse
from defusedxml import ElementTree as SecureElementTree
from xml.etree import ElementTree

from requests_ratelimiter import LimiterSession

# Impose the public ratelimit by default [2]
SESSION = LimiterSession(per_minute=20)

# Define the base URL for the Arxiv API [1]
URL_BASE = 'http://export.arxiv.org/api/'
URL_QUERY = URL_BASE + 'query'

# Define XML tags for the Arxiv API [4]
TAG_PREFIX = '{http://www.w3.org/2005/Atom}'
TAG_ENTRY = 'entry'
TAG_TITLE = 'title'
TAG_ID = 'id'
TAG_PUBLISHED = 'published'
TAG_UPDATED = 'updated'
TAG_SUMMARY = 'summary'
TAG_AUTHOR = 'author'
TAG_NAME = 'name'
TAG_AFFILIATION = 'affiliation'
TAG_CATEGORY = 'category'
TAG_TERM = 'term'
TAG_SCHEME = 'scheme'

# Define the Entry output formats for the Arxiv API [4]
Entry = collections.namedtuple('Entry', 'title id published updated summary author category')
Author = collections.namedtuple('Author', 'name affiliation')
Category = collections.namedtuple('Category', 'term scheme')


class SearchField:
    """Enumeration of search fields for the Arxiv API [3]
    """
    TITLE = 'ti'
    AUTHOR = 'au'
    ABSTRACT = 'abs'
    COMMENT = 'co'
    JOURNAL_REFERENCE = 'jr'
    CATEGORY = 'cat'
    REPORT_NUMBER = 'rn'
    ID = 'id'
    ALL = 'all'


class LogicalOperator:
    """Enumeration of logical operators for the Arxiv API [3]
    """
    AND = ' AND '
    OR = ' OR '
    AND_NOT = ' ANDNOT '


def find(entry: ElementTree.Element, tag: str, find_all: bool = False) -> Union[str, List[str]]:
    """Find the tag in the entry and return the text.

    Args:
        entry (ElementTree.Element): The entry to search.
        tag (str): The tag to search for.

    Returns:
        str: The text of the tag.
    """
    if not tag.startswith(TAG_PREFIX):
        tag = TAG_PREFIX + tag

    if find_all:
        return entry.findall(tag)

    res = entry.find(tag)
    if res is not None:
        return res.text


def parse_entry(entry: ElementTree.Element) -> Entry:
    """Parse an entry from the Arxiv API response.

    Args:
        entry (ElementTree.Element): The entry to parse.

    Returns:
        Entry: The parsed entry.
    """
    # Parse the authors
    authors = [Author(name=find(author, TAG_NAME),
                      affiliation=find(author, TAG_AFFILIATION)) for author in find(entry, TAG_AUTHOR, find_all=True)]

    # Parse the categories
    categories = [Category(term=category.attrib[TAG_TERM],
                           scheme=category.attrib[TAG_SCHEME]) for category in find(entry, TAG_CATEGORY, find_all=True)]

    # Return the parsed entry
    return Entry(title=find(entry, TAG_TITLE),
                 id=find(entry, TAG_ID),
                 published=find(entry, TAG_PUBLISHED),
                 updated=find(entry, TAG_UPDATED),
                 summary=find(entry, TAG_SUMMARY),
                 author=authors,
                 category=categories)


def get_and_parse(url: str, params: dict) -> List[Entry]:
    """Get and parse the response from the Arxiv API, the payloads
    are encoded using the Atom 1 XML format.

    Args:
        url (str): The endpoint to query
        params (dict): The parameters to pass to the query

    Returns:
        dict: The parsed response
    """
    # Get the response
    response = SESSION.get(url, params=params)

    # Parse the response securely into ElementTree
    root = SecureElementTree.fromstring(response.text)

    # TODO finish parsing response into a list of named tuples if no errors, otherwise raise the error
    if len(root) == 1 and root[0].tag == 'error':
        raise ValueError(f'No results found. Error: {root[0].text}')

    entries = [parse_entry(entry) for entry in find(root, TAG_ENTRY, find_all=True)]

    # Return the parsed response
    return entries


def _extend_query(query: str, field: SearchField, value: Union[str, List[str]],
                  how: LogicalOperator = LogicalOperator.AND, how_list: LogicalOperator = LogicalOperator.OR) -> str:
    """Extend the query with the given field and value.

    Args:
        query:
            str, The current query string.
        field:
            SearchField, The field to search in.
        value:
            Union[str, List[str]], The value to search for.
        how:
            LogicalOperator, The logical operator to use when adding the field.
        how_list:
            LogicalOperator, The logical operator to use when adding a list of values.

    Returns:
        str: The extended query string.
    """
    # Check if query exists, if so then extend with cross-field logical operator
    if query:
        query += how

    # Check if value is scalar or list, then extend query
    if isinstance(value, str):
        query += f'{field}:{value}'
    elif isinstance(value, list):
        query += f'({field}:{how_list.join(value)})'

    return query


def format_search_query(title: Union[str, List[str]] = None, author: Union[str, List[str]] = None, abstract: Union[str, List[str]] = None, comment: Union[str, List[str]] = None,
                        journal_reference: Union[str, List[str]] = None, category: Union[str, List[str]] = None, report_number: Union[str, List[str]] = None, id_list: List[str] = None,
                        all_: Union[str, List[str]] = None, how: LogicalOperator = LogicalOperator.AND, how_list: LogicalOperator = LogicalOperator.OR) -> Union[str, None]:
    """Format the search query for the Arxiv API.

    Args:
        title:
            Union[str, List[str]], optional, The title to search for. Defaults to None.
        author:
            Union[str, List[str]], optional, The author to search for. Defaults to None.
        abstract:
            Union[str, List[str]], optional, The abstract to search for. Defaults to None.
        comment:
            Union[str, List[str]], optional, The comment to search for. Defaults to None.
        journal_reference:
            Union[str, List[str]], optional, The journal reference to search for. Defaults to None.
        category:
            Union[str, List[str]], optional, The category to search for. Defaults to None.
        report_number:
            Union[str, List[str]], optional, The report number to search for. Defaults to None.
        id_list:
            List[str], optional, The list of Arxiv IDs to search for. Defaults to None.
        all_:
            Union[str, List[str]], optional, The all field to search for. Defaults to None.

    Returns:
        str or None: The formatted query string, or None if no fields are provided.
    """
    # Short-circuit if no fields are provided
    if all(v is None for v in (title, author, abstract, comment, journal_reference, category, report_number, id_list, all_)):
        return None

    query = ''

    for field, value in zip(
            (SearchField.TITLE, SearchField.AUTHOR, SearchField.ABSTRACT, SearchField.COMMENT, SearchField.JOURNAL_REFERENCE, SearchField.CATEGORY, SearchField.REPORT_NUMBER, SearchField.ID, SearchField.ALL),
            (title, author, abstract, comment, journal_reference, category, report_number, id_list, all_)
    ):
        if value is not None:
            query = _extend_query(query, field, value, how=how, how_list=how_list)

    return parse.quote(query, safe='/:&=')


def _query(search_query: str = None, id_list: List[str] = None, start: int = 0, max_results: int = 10) -> dict:
    """Query the Arxiv API with the given parameters.

    Args:
        search_query:
            str, optional, The query string to search for. Defaults to None.
        id_list:
            List[str], optional, A list of Arxiv IDs to search for. Defaults to None.
        start:
            int, optional, The index to start the search from. Defaults to 0.
        max_results:
            int, optional, The maximum number of results to return. Defaults to 10.

    Returns:
        dict: The parsed response from the API
    """
    # Define the parameters for the query
    params = {
        'search_query': search_query,
        'id_list': id_list,
        'start': start,
        'max_results': max_results
    }

    # Filter out the None values
    params = {k: v for k, v in params.items() if v is not None}

    # Get and parse the response
    return get_and_parse(URL_QUERY, params)


def query(title: Union[str, List[str]] = None, author: Union[str, List[str]] = None, abstract: Union[str, List[str]] = None, comment: Union[str, List[str]] = None,
          journal_reference: Union[str, List[str]] = None, category: Union[str, List[str]] = None, report_number: Union[str, List[str]] = None, id_list: List[str] = None,
          all_: Union[str, List[str]] = None, how: LogicalOperator = LogicalOperator.AND, how_list: LogicalOperator = LogicalOperator.OR, start: int = 0, max_results: int = 10) -> dict:
    """Query the Arxiv API with the given parameters.

    Args:
        title:
            Union[str, List[str]], optional, The title to search for. Defaults to None.
        author:
            Union[str, List[str]], optional, The author to search for. Defaults to None.
        abstract:
            Union[str, List[str]], optional, The abstract to search for. Defaults to None.
        comment:
            Union[str, List[str]], optional, The comment to search for. Defaults to None.
        journal_reference:
            Union[str, List[str]], optional, The journal reference to search for. Defaults to None.
        category:
            Union[str, List[str]], optional, The category to search for. Defaults to None.
        report_number:
            Union[str, List[str]], optional, The report number to search for. Defaults to None.
        id_list:
            List[str], optional, The list of Arxiv IDs to search for. Defaults to None.
        all_:
            Union[str, List[str]], optional, The all field to search for. Defaults to None.
        how:
            LogicalOperator, optional, The logical operator to use when adding the field. Defaults to LogicalOperator.AND.
        how_list:
            LogicalOperator, optional, The logical operator to use when adding a list of values. Defaults to LogicalOperator.OR.
        start:
            int, optional, The index to start the search from. Defaults to 0.
        max_results:
            int, optional, The maximum number of results to return. Defaults to 10.
    """
    # Format the search query
    search_query = format_search_query(title, author, abstract, comment, journal_reference, category, report_number, id_list, all_, how, how_list)

    # Short-circuit if no search query is provided
    if search_query is None and id_list is None:
        raise ValueError('No search query provided; cannot query the entire Arxiv.')

    # Query the API
    return _query(search_query, id_list, start, max_results)
