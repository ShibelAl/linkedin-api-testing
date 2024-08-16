class CompanyJobs:

    def __init__(self, company_id, page):
        self._company_id = company_id
        self._page = page

    def to_dict(self):
        """
        Converts the CompanyJobs instance to a dictionary.
        """
        return {
            "companyIds": self._company_id,
            "page": self._page
        }
