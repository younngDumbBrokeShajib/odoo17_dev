# -*- coding: utf-8 -*-

from odoo import models, fields, api



class indent_management(models.Model):

    _name = 'indent.management'
    _description = 'indent_management'

    serial_number = fields.Integer(string="Serial Number", compute="_compute_serial_number")
    name = fields.Char()
    supplier_id=fields.Many2one('res.partner','Supplier')
    customer_id=fields.Many2one('res.partner','Customer')
    product_lines = fields.One2many('indent.product.line', 'indent_id', string="Products")
    purchase_order_id=fields.Many2one('purchase.order','Purchase Order Ref')
    #purchase_order_id_created=fields.Char(string='Purchase Order Id',compute='_generate_pruchase_order_id',store=True)
    po_status=fields.Char('Purchase order Status',readonly=True)
    subtotal=fields.Float(string='Subtotal',compute='_compute_subtotal',store=True)
    total_amount=fields.Float(string='PI Value',compute='_compute_totalamount',store=True)
    currency_id=fields.Selection([('usd','USD'),('bdt','BDT'),('euro','Euro')])
    pi_date=fields.Date(string='Pi date')
    sales_num=fields.Char(string='Sales Order Number')
    sales_person=fields.Many2one('hr.employee','Salesperson')
    lc_no=fields.Char(string='LC No:')
    lc_date=fields.Date(string='LC Date')
    shipment_plan=fields.Char(string='Shipment Plan')
    etd=fields.Date(string='ETD')
    eta=fields.Date(string='ETA')
    inv_month=fields.Date(string='Invoice Month')
    com_inv_date=fields.Date(string='Commercial Invoice Date')
    com_inv_no=fields.Char(string='Commercial Invoice Number')
    stats=fields.Selection([('draft','Draft'),('confirmed','Confirmed'),('ongoing','Ongoing'),('ececuted','Executed'),('cancel','Cancel')],default='draft')
    val_com_inv=fields.Float(string='Value of Comm Invoice')
    base_val=fields.Float(string="Base Value")
    percent_comm=fields.Float(string='Percentage of commission')
    total_comm=fields.Float(string='Total Commission',compute='_compute_comm')

    @api.depends('base_val','percent_comm')
    def _compute_comm(self):
        for record in self:
            record['total_comm']=record.base_val*(record.percent_comm/100)

    @api.depends('product_lines.pro_quantity', 'product_lines.pro_unit_price')
    def _compute_subtotal(self):
        for record in self:
            subtotal = sum(line.pro_quantity * line.pro_unit_price for line in record.product_lines)
            record.subtotal = subtotal
    #tester
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)

    @api.depends('product_lines.pro_subtotal')
    def _compute_totalamount(self):
        for record in self:
            total= sum(line.pro_subtotal for line in record.product_lines)
        record.total_amount=total

    # @api.depends('purchase_order_id')
    # def _updatePoState(self):
    #     for record in self:
    #         if record.purchase_order_id:
    #             record['po_status']=record.purchase_order_id.state


    def _compute_serial_number(self):
        for idx, record in enumerate(self, start=self._context.get('offset', 0) + 1):
            record.serial_number = idx


    #----------------Button Actions---------------

    def action_create_po(self):
        purchase_order = self.env['purchase.order'].create({
            'partner_id': self.supplier_id.id,
            'order_line': [(0, 0, {
                'product_id': line.product_id.id,
                'product_qty': line.pro_quantity,
                'price_unit': line.pro_unit_price,
                'price_subtotal':line.pro_subtotal,
            }) for line in self.product_lines]
        })
        self.purchase_order_id = purchase_order.id

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'res_id': purchase_order.id,
            'view_mode': 'form',
            'target': 'current',
        }


#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100



