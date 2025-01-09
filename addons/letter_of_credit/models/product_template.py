from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = "product.template"

    # New float fields
    hs_code=fields.Char(string='Custom HS Code')
    sd = fields.Float(string='SD')
    cd = fields.Float(string='CD')
    rd = fields.Float(string='RD')
    landed_vat = fields.Float(string='Landed VAT')
    ait = fields.Float(string='Advance Income Tax')
    at = fields.Float(string='Advance Tax')
