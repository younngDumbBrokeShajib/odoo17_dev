# -*- coding: utf-8 -*-
# from odoo import http


# class IndentManagement(http.Controller):
#     @http.route('/indent_management/indent_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/indent_management/indent_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('indent_management.listing', {
#             'root': '/indent_management/indent_management',
#             'objects': http.request.env['indent_management.indent_management'].search([]),
#         })

#     @http.route('/indent_management/indent_management/objects/<model("indent_management.indent_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('indent_management.object', {
#             'object': obj
#         })

