"""Tests for the arxiv module.
"""
from sxolar.api import arxiv


class TestArxivAPI:
    """Test the arxiv API"""

    def test_get_and_parse(self):
        """Test the get_and_parse function"""


    def test_query(self):
        """Test the query function,

        This test mimicks the behavior of the API documentation, which gives "3" results
            Docs Test Query: "http://export.arxiv.org/api/query?search_query=au:del_maestro+ANDNOT+%28ti:checkerboard+OR+ti:Pyrochlore%29"
        """
        res = arxiv.query(author='del maestro')
        assert len(res) == 10
