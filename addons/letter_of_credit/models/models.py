# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class letter_of_credit(models.Model):
#     _name = 'letter_of_credit.letter_of_credit'
#     _description = 'letter_of_credit.letter_of_credit'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

