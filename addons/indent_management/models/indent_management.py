# -*- coding: utf-8 -*-

from odoo import models, fields, api



class indent_management(models.Model):

    _name = 'indent.management'
    _description = 'indent_management'

    serial_number = fields.Integer(string="Serial Number", compute="_compute_serial_number")
    name = fields.Char()
    indent_type=fields.Selection([('exe','Exepients'),('api','API'),('neu','Neutra'),('own','Own Imports')],string='Indent Type',required=True)
    supplier_id=fields.Many2one('res.partner','Supplier')
    customer_id=fields.Many2one('res.partner','Customer')
    product_lines = fields.One2many('indent.product.line', 'indent_id', string="Products")
    purchase_order_id=fields.Many2one('purchase.order','Purchase Order Ref') #this OLD
    purchase_order_no=fields.Char(string='Purchase Order Number',readonly=True,copy=False)
    purchase_order_date=fields.Date(string='Purchase order Date')

    #purchase_order_id_created=fields.Char(string='Purchase Order Id',compute='_generate_pruchase_order_id',store=True)
    po_status=fields.Char('Purchase order Status',readonly=True)
    total_qty=fields.Float(string='Total quantity',compute='_compute_totalqty',store=True) #used to find total commission later on
    subtotal=fields.Float(string='Subtotal',compute='_compute_subtotal',store=True)
    total_amount=fields.Float(string='PI Value',compute='_compute_totalamount',store=True)
    currency_id=fields.Selection([('usd','USD'),('bdt','BDT'),('euro','Euro')],string='Currency')
    pi_no=fields.Char(string='Proforma Invoice No:')
    pi_date=fields.Date(string='Proforma Invoice date')
    sales_num=fields.Char(string='Sales Order Number')
    sales_person=fields.Many2one('hr.employee','Salesperson')

    lc_tt_cad_sel=fields.Selection([('lc','LC'),('tt','TT'),('cad','CAD')],string='Import Document',default='lc')
    lc_tt_cad=fields.Char(string='LC/TT/CAD NO:')
    #for showing lc_tt_cad field to compute the boolean
    lc_date=fields.Date(string='LC/TT/CAD Date') #make it dropdown
    shipment_plan=fields.Selection([('air','Air'),('sea','Sea')],string='Shipment Type') #not added
    etd=fields.Date(string='ETD')
    eta=fields.Date(string='ETA')
    inv_month=fields.Date(string='Invoice Month')
    com_inv_date=fields.Date(string='Commercial Invoice Date')
    com_inv_no=fields.Char(string='Commercial Invoice Number')
    stats=fields.Selection([('draft','Draft'),('confirmed','Confirmed'),('ongoing','Ongoing'),('ececuted','Executed'),('cancel','Cancel')],default='draft')
    #commission calculation fields
    type_comm=fields.Selection([('quantity','Volume'),('percent','Percent'),('manual','Manual')],string='Type of Commission')
    val_com_inv=fields.Float(string='Value of Comm Invoice')
    base_val=fields.Float(string="Base Value")
    percent_comm=fields.Float(string='Percentage of commission')
    total_comm=fields.Float(string='Total Commission',compute='_compute_comm',store=True)
    comm_input=fields.Float(string='Commission Value to Register') #this field is required to for manual type of commission


    #quantity_cal=fields.Boolean(string='Select The calculation type',compute="_compute_comm2")

    #calculating Purchase Order Number which is auto generated
    def create(self,vals):
        if 'indent_type' in vals and not vals.get('purchase_order_no'):
            indent_type = vals['indent_type']
            sequence_prefix = {
                'exe': 'Exe',
                'api': 'API',
                'neu': 'Neu',
                'own': 'Own'
            }.get(indent_type, 'PO')  # Default prefix if none is found
            # Generate the purchase order number using a sequence
            sequence_name = f"indent.{indent_type}"
            sequence = self.env['ir.sequence'].next_by_code(sequence_name) or '0001'
            sequence_number = self.env['ir.sequence'].next_by_code(sequence_name) or '0001'
            vals['purchase_order_no'] = f"{sequence_prefix}/{fields.Date.today().year}/{sequence_number}"
        return super(indent_management,self).create(vals)

    @api.depends('base_val','percent_comm','type_comm','total_qty')
    def _compute_comm(self):
        for record in self:
            if record.type_comm is not None:
                if record.type_comm=='quantity':
                    record['total_comm']=record.total_qty*record.base_val
                elif record.type_comm=='percent':
                    record['total_comm']=record.total_amount*(record.percent_comm/100)
                else:
                    record['total_comm']=record.comm_input
            #record['total_comm']=record.base_val*(record.percent_comm/100)


    @api.depends('product_lines.pro_quantity', 'product_lines.pro_unit_price')
    def _compute_subtotal(self):
        for record in self:
            subtotal = sum(line.pro_quantity * line.pro_unit_price for line in record.product_lines)
            record.subtotal = subtotal
    #tester
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)

    #_compute_totalqty function finds the total quantity added in the product line
    #total_qty will be used to calculate the total commission later on
    @api.depends('product_lines.pro_quantity')
    def _compute_totalqty(self):
        for record in self:
            totalqty=sum(line.pro_quantity for line in record.product_lines)
        record.total_qty=totalqty




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



#15/Jan/2025
#move value of comm inv value below the comm inv no
