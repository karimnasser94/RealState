import json
from odoo import http
from odoo.http import request


class PropertyApi(http.Controller):

    # @http.route("/v1/property", methods=["POST"], type="http", auth="none", csrf=False)
    # def post_property(self):
    #     args = request.httprequest.data.decode()
    #     vals = json.loads(args)
    # Try:
    #     res = request.env['property'].sudo().create(vals)
        # if res:
        #     return request.make_json_response({
        #         "message": "Property has been created successfully from API",
        #          "id": res.id,
        #          "name": res.name
        #     }, status=200)
    # except Exception as error:
    #     return request.make_json_response({
    #         "message": error
    #     }, status=400)

    @http.route("/v1/property/json", methods=["POST"], type="json", auth="none", csrf=False)
    def post_property_json(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['property'].sudo().create(vals)
        if res:
            return {
                "message": "Property has been created successfully from API Json"
            }
