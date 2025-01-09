# -*- coding: utf-8 -*-
# from odoo import http


# class LetterOfCredit(http.Controller):
#     @http.route('/letter_of_credit/letter_of_credit', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/letter_of_credit/letter_of_credit/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('letter_of_credit.listing', {
#             'root': '/letter_of_credit/letter_of_credit',
#             'objects': http.request.env['letter_of_credit.letter_of_credit'].search([]),
#         })

#     @http.route('/letter_of_credit/letter_of_credit/objects/<model("letter_of_credit.letter_of_credit"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('letter_of_credit.object', {
#             'object': obj
#         })

