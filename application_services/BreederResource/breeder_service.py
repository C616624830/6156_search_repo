from application_services.BaseApplicationResource import BaseApplicationResource
import database_services.RDBService as d_service


class BreederResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_breeders(cls, template, field_list):
        res = d_service.select_by_template("searchbase", "breederInfo",
                                       template, field_list)
        return res

    # add a new breeder to database (all not null parameters are needed)
    @classmethod
    def post_breeder(cls, template):
        res = d_service.insert_by_template("searchbase", "breederInfo",
                                template, None)
        return res

    @classmethod
    def delete_breeder(cls, id):
        res = d_service.delete_by_id("searchbase", "breederInfo",
                                     id, None)
        return res

    @classmethod
    def put_breeder(cls, id, template):
        res = d_service.update_by_id_template("searchbase", "breederInfo",
                                              id, template, None)
        return res

    @classmethod
    def check_breeder_id_exist(cls, id):
        res = d_service.select_specific_column("searchbase", "breederInfo",
                                           "id", 'id', id)
        return res

    @classmethod
    def get_breeder_rating(cls, breederid):
        res = d_service.select_specific_column("searchbase", "breederInfo",
                                               "rating", 'id', breederid)
        return res


