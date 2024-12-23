from odoo import models,fields,api

class deliveryNoteFields(models.Model):
    _inherit = 'stock.picking'
    buyer_order_no=fields.Char(string='Buyer Order Number')
    buyer_order_date=fields.Date(string='Buyers Order Date')
    dispatch_doc=fields.Char(string='Dispatch Document',default='Mushok 6.3')
    dispatch_through=fields.Char(string='Dispacth Through')
