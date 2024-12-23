from odoo import fields, models, api


class custom_crm(models.Model):
    _inherit = 'crm.lead'
#compute_expected_revenue is writeen at first beacause its onchange! get more resouce on this.

    @api.onchange('x_studio_total_price')
    def _compute_expected_revenue(self):
        for rec in self:
            rec['expected_revenue'] = rec.x_studio_total_price

    @api.depends('x_studio_price', 'x_studio_volumekg', 'x_studio_vat_15')
    def _compute_total_price(self):
        for rec in self:
            if rec.x_studio_vat_15 == True:
                price=(rec.x_studio_volumekg*rec.x_studio_price)+(rec.x_studio_price*rec.x_studio_volumekg*0.15)

            else:
                price = (rec.x_studio_volumekg * rec.x_studio_price)
            rec.x_studio_total_price = price #till here the total price calculation and update works fine