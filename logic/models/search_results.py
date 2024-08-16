class SearchResults:

    def __init__(self, keyword, first_filter, second_filter, third_filter):
        self._keyword = keyword
        self._first_filter = first_filter
        self._second_filter = second_filter
        self._third_filter = third_filter

    def to_dict(self):
        """
        Converts the SearchResults instance to a dictionary.
        """
        return {
            "keyword": self._keyword,
            "sortBy": self._first_filter,
            "datePosted": self._second_filter,
            "start": self._third_filter
        }
