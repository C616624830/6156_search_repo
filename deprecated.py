# @app.route('/cats/breeder/<cid>')
# def breeder_of_cat(cid):
#     res = CatResource.get_breeder_id(cid)
#     rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
#
#
# @app.route('/breeders/rating', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def breeder_rating():
#     if request.method == 'GET':
#         breeder_id = request.args.get('bid', default = '1', type = str)
#         res = BreederResource.get_breeder_rating(breeder_id)
#         rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
#         return rsp
#
# @app.route('/comment', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def comment():
#     if request.method == 'GET':
#         template = request.args.to_dict()
#         template = {k: v for k, v in template.items() if
#                     v}  # remove key-value pairs where value is empty such as 'father': ''
#
#         res = db.find_by_template('searchdynamo', template)
#         res = json.dumps(res, indent=4, default=str)
#         print("Result = \n", res)
#         return res
#
#     elif request.method == 'POST':
#         template = request.form.to_dict()
#         template = {k: v for k, v in template.items() if
#                     v}  # remove key-value pairs where value is empty such as 'father': ''
#         tags = template.get('tags')
#         print("tags", tags)
#         comment = template.get('comment')
#         print(comment)
#         email = template.get('email')
#         print(email)
#
#         res = db.add_comment("searchdynamo", email, comment, tags)
#         return res
#
#
#     elif request.method == 'PUT':
#         template = request.form.to_dict()
#         template = {k: v for k, v in template.items() if
#                     v}  # remove key-value pairs where value is empty such as 'father': ''
#         comment_id = template.get('id')
#         print(type(comment_id), comment_id)
#         print("comment_id", comment_id)
#         tags = template.get('tags')
#         print("tags", tags)
#         comment = template.get('comment')
#         print("comment", comment)
#         dt = time.time()
#         dts = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(dt))
#         new_version_id = str(uuid.uuid4())
#
#         original_comment = db.get_item("searchdynamo", {"comment_id": comment_id})
#
#         print(original_comment)
#
#         new_comment = copy.deepcopy(original_comment)
#         new_comment["datetime"] = dts
#         new_comment["comment"] = comment
#         new_comment["tags"] = tags
#         new_comment["version_id"] = new_version_id
#
#         try:
#             res = db.write_comment_if_not_changed("searchdynamo", new_comment, original_comment)
#             print("First write returned: ", res)
#             return res
#         except Exception as e:
#             print("First write exception = ", str(e))
#             return "update exception"
#
#
#
#     elif request.method == 'DELETE':
#         template = request.form.to_dict()
#         template = {k: v for k, v in template.items() if
#                     v}  # remove key-value pairs where value is empty such as 'father': ''
#         comment_id = template.get('id')
#         print("comment_id", comment_id)
#
#         res = db.delete_item('searchdynamo', comment_id)
#         return res
#
#     # res = db.get_item("searchdynamo",
#     #                   {
#     #                       "comment_id": "01cdb10e-6d9b-4b23-98bc-db062ae908ec"
#     #                   })
#     # result = json.dumps(res, indent=4, default=str)
#     # print("Result = \n", result)
#     return None

# @app.route('/test', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def test():
#     return

# @app.route('/')
# def get_index():
#     return render_template('index.html')

# @app.route('/add_cat')
# def add_cat_page():
#     return render_template('add_cat.html')
#
# @app.route('/delete_cat')
# def delete_cat_page():
#     return render_template('delete_cat.html')
#
# @app.route('/search_cat')
# def search_cat_page():
#     return render_template('search_cat.html')
#
# @app.route('/add_breeder')
# def add_breeder_page():
#     return render_template('add_breeder.html')
#
# @app.route('/search_breeder')
# def search_breeder_page():
#     return render_template('search_breeder.html')
#
# @app.route('/view_breeder_rating')
# def view_breeder_rating_page():
#     return render_template('view_breeder_rating.html')