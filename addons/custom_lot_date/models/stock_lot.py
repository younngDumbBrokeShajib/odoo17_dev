from odoo import models,fields,api

class stocklotdate(models.Model):
    _inherit='stock.lot'
    mfgdate=fields.Date(string="Manufacturing Date")


