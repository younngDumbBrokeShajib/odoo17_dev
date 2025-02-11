from odoo import fields,api,models

class ProductTemplateIndent(models.Model):

    _inherit = 'product.template'

    #new fields for Indent
    principle = fields.Many2one('res.partner', string='Principle Company')