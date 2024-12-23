# -*- coding: utf-8 -*-
# from odoo import http


# class CustomLotDate(http.Controller):
#     @http.route('/custom_lot_date/custom_lot_date', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_lot_date/custom_lot_date/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_lot_date.listing', {
#             'root': '/custom_lot_date/custom_lot_date',
#             'objects': http.request.env['custom_lot_date.custom_lot_date'].search([]),
#         })

#     @http.route('/custom_lot_date/custom_lot_date/objects/<model("custom_lot_date.custom_lot_date"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_lot_date.object', {
#             'object': obj
#         })

