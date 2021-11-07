from application_services.BaseApplicationResource import BaseApplicationResource
import database_services.RDBService as d_service


class CatResource(BaseApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_breeder_id(cls, catid):
        res = d_service.select_specific_column("searchbase", "catInfo",
                                      "breeder", 'id', catid)
        return res


    @classmethod
    def get_cats(cls, template, field_list):
        res = d_service.select_by_template("searchbase", "catInfo",
                                         template, None)
        return res

    # add a new cat to database (all not null parameters are needed)
    @classmethod
    def post_cat(cls, template):
        res = d_service.insert_by_template("searchbase", "catInfo",
                                template, None)
        return res

    @classmethod
    def delete_cat(cls, id):
        res = d_service.delete_by_id("searchbase", "catInfo",
                                id, None)
        return res

    @classmethod
    def put_cat(cls, id, template):
        res = d_service.update_by_id_template("searchbase", "catInfo",
                                id, template, None)
        return res

    @classmethod
    def check_cat_id_exist(cls, id):
        res = d_service.select_specific_column("searchbase", "catInfo",
                                      "id", 'id', id)
        return res
