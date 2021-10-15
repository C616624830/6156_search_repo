from application_services.BaseApplicationResource import BaseApplicationResource
import database_services.RDBService as d_service


class BreederResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_by_template(cls, template):
        res = d_service.find_by_template("searchbase", "breederInfo",
                                       template, None)
        return res

    @classmethod
    def get_breeder_rating(cls, breederid):
        res = d_service.get_specifc_column("searchbase", "breederInfo",
                                      "rating", 'id', breederid)
        return res

    # add a new breeder to database (all not null parameters are needed)
    @classmethod
    def post_breeder(cls, bid, name, organization, phone, email, address, website, rating):
        res = d_service.add_breeder("searchbase", "breederInfo",
                                bid, name, organization, phone, email, address, website, rating)
        return res