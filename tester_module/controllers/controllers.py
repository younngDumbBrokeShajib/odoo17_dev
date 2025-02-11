# -*- coding: utf-8 -*-
# from odoo import http


# class TesterModule(http.Controller):
#     @http.route('/tester_module/tester_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tester_module/tester_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tester_module.listing', {
#             'root': '/tester_module/tester_module',
#             'objects': http.request.env['tester_module.tester_module'].search([]),
#         })

#     @http.route('/tester_module/tester_module/objects/<model("tester_module.tester_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tester_module.object', {
#             'object': obj
#         })

