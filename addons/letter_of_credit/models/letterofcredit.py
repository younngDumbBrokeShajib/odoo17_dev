from odoo import models, fields, api
from odoo.exceptions import UserError

class LetterofCredit(models.Model):
    _name="letter.of.credit"
    product_id = fields.Many2one('product.product', string="Product", required=True)
