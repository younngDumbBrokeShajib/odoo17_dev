from odoo import models,fields,api

class fieldsforInvoice(models.Model):
    _inherit='account.move'
    buyer_order_no=fields.Char(string="Buyer's Order Number")
    buyer_order_date=fields.Date(string="Buyer's Order Date")
    dispatch_document=fields.Char(string='Dispatch Document',default="Mushok No:637")
    dispatch_through=fields.Char(string="Dispatch Through",default="Covered Van")

