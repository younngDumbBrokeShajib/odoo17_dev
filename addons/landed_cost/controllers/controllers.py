# -*- coding: utf-8 -*-
# from odoo import http


# class LandedCost(http.Controller):
#     @http.route('/landed_cost/landed_cost', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/landed_cost/landed_cost/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('landed_cost.listing', {
#             'root': '/landed_cost/landed_cost',
#             'objects': http.request.env['landed_cost.landed_cost'].search([]),
#         })

#     @http.route('/landed_cost/landed_cost/objects/<model("landed_cost.landed_cost"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('landed_cost.object', {
#             'object': obj
#         })

