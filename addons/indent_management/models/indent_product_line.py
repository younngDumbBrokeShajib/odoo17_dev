from odoo import models, fields, api

class IndentProductLine(models.Model):
    _name='indent.product.line'
    _description = "Indent Product Line"

    product_id=fields.Many2one('product.product','Product',required=True)
    pro_quantity=fields.Float(string='Quantity',required=True,default=0.0)
    pro_unit_price=fields.Float(string='Unit Price',required=True)
    pro_subtotal=fields.Float(string='Subtotal',compute='_compute_subtotal',store=True)
    #unit of measure. Get to explain this code
    uom_id = fields.Many2one(
        'uom.uom',
        string='Unit of Measure',
        required=True,
        domain="[('category_id', '=', product_uom_category_id)]"
    )
    product_uom_category_id = fields.Many2one(
        'uom.category',
        string='UoM Category',
        related='product_id.uom_id.category_id',
        #store=True,
        #readonly=True
    )


    indent_id=fields.Many2one('indent.management','Indent Reference',ondelete='cascade')
    pi_value_compute=fields.Float(string='Total Compute',compute='_compute_subtotal')
    pi_value_final=fields.Float(string='Pi Value',compute='_compute_pivalue')
    @api.depends('pro_quantity','pro_unit_price')
    def _compute_subtotal(self):
        for record in self:
            record['pro_subtotal']=record.pro_unit_price*record.pro_quantity
            record.pi_value_compute=record.pi_value_compute+record.pro_subtotal

