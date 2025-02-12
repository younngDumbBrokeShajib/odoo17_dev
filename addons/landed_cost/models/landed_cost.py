from odoo import fields,models,api
from odoo.exceptions import UserError


class LandedCost(models.Model):
    _name="dev.landed.cost" #by (.dot) it will create a table name as landed_cost in database
    product_id=fields.Many2one('product.product','Product')
    # use product.product for the actual product variant used in transactions like sales and purchases
    product_id_template=fields.Many2one('product.template','product_template')
    #product.template is used to get all other information saved in template
    #then we use this product.template saved in another varr to get name, hs_code or anyother inforamtion to use
    product_name=fields.Char('Product Name',related='product_id_template.name',store=True)
    custom_hs_code=fields.Char("BD Custom HS Code",related='product_id_template.hs_code',store=True)
    x_empty_field=fields.Char(string='N/A')
    hs_code=fields.Char(string='BD Custom H.S Code')
    #------------for journal entries------------
    journal_entry_created = fields.Selection([
        ('not_created', 'Not Created'),
        ('created', 'Journal Entry Created')
    ], string="Journal Entry Status", default="not_created", readonly=True) #this is for status bar

    #--------------------for PO information------------
    import_qty=fields.Float(string="Quantity Imported(KG)")
    vendor_id = fields.Many2one('res.partner', string="Vendor", domain=[('supplier_rank', '>', 0)], required=True)
    vendor_name = fields.Char('Vendor Name', related='vendor_id.name', store=True)
    po_id = fields.Many2one('purchase.order', string="Purchase Order", readonly=True)
    lc_reference = fields.Char(string="LC Reference")
    lc_margin_percent = fields.Float(string="LC Margin (%)")

    inv_value=fields.Float(string="Commercial Invoice Value(CPT) in US $",store=True)
    inv_value_pkg=fields.Float(string="Commercial Invoice Value(CPT) per Kg in $", store=True,compute="_compute_com_value_us")
    cob=fields.Float(string="Carriage on Board (Quality wise allocated) BDT",store=True)
    #addition_inv_with_cob=fields.Float(string='addition of the price with the carriage on board',compute='_compute_add_cob_inv',store=True)
    crf_val_psi=fields.Float(string="CRF Value by PSI Company per Kg in US $")
    inv_value_BDT=fields.Float(string="Commercial Invoice Value In BDT",compute="_compute_convert_bdt_to_usd",store=True)
    currency_id = fields.Many2one('res.currency', string="Currency", required=True,default=lambda self: self.env.user.company_id.currency_id)
    con_rate=fields.Float(string="Convertion Rate")
    inv_value_BDT_pkg=fields.Float(string="Commercial Invoice Value in BDT per KG",store=True,compute="_compute_BDT_pkg")
    insurance_premium_bdt=fields.Float(string="Insurance Premium BDT")
    insurance_premium_precent=fields.Float(string="% of Actual Invoice")
    cif_value_imported_cost=fields.Float(string="CIF value of imported cost",store=True,compute="_compute_cif_imported_cost")
    custom_assessable_value_bdt=fields.Float(string="Custom assessable value in BDT as per Bill of Entry")

    custom_assessable_value_percent=fields.Float(string="% of actual Invoice Value")
    custom_duty=fields.Float(string="Custom Duty (CD)")
    cd = fields.Float(string='CD', related='product_id.cd', store=True)
    cd_landed=fields.Float(string='Custom Duty (CD)',store=True,compute='_compute_cd')
    sd = fields.Float(string='Supplementary Duty', related='product_id.sd', store=True)
    sd_landed=fields.Float(string="Supplimentary Duty",store=True,compute='_compute_cd')
    rd = fields.Float(string='Regulatory Duty', related='product_id.rd', store=True)
    rd_landed=fields.Float(string='Regulatory Duty',store=True,compute='_compute_cd')
    landed_vat = fields.Float(string='Value Added Tax', related='product_id.landed_vat', store=True)
    vat_landed=fields.Float(string='Value Added Tax',store=True,compute='_compute_vat_landed')
    ait = fields.Float(string='Advance Income Tax', related='product_id.ait', store=True)
    ait_landed=fields.Float(string='Advance Income Tax',store=True,compute='_compute_ait_landed')
    at = fields.Float(string='Advance Tax', related='product_id.at', store=True)
    at_landed=fields.Float(string='Advance Tax',store=True,compute='_compute_at_landed')
    DSC=fields.Float(string='Development Subcharges')
    atv=fields.Float(string='Advance Trade Tax')
    duties_taxes=fields.Float(string='Duties and Taxes',store=True,compute='_compute_duties_taxes')
    #dutiestaxes=fields.Float(string='Duties & Taxes',store=True,compute='')

    #0 - S
    doc_pros_fee=fields.Float(string='Document Processing Fee')
    VAT_c_f_agents=fields.Float(string='VAT on C & F Agent')
    fine_penalties=fields.Float(string="Fine and Pelanties")  #added on 8/9/24
    others=fields.Float(string='Others')
    lcl_charges=fields.Float(string='LCL Charges')
    income_tax_c_f_comm=fields.Float(string='Income Tax on C & F agents')
    tax_for_c_f_agent_jobs=fields.Float(string='Add. Taxes for C & F agent jobs',store=True,compute='_compute_c_f_agent_jobs')
    total_duties_taxes=fields.Float(string='Total Duties and Taxes',store=True,compute='_compute_total_duties_taxes')

    #T - V
    air_way_bill=fields.Float(string='Delivery Order Charges/Airway Bill collection')
    noc_charges=fields.Float(string='NOC and Demirrage Charges')
    shipping_charges=fields.Float(string='Shipping Charges',store=True,compute='_compute_shipping_charges')


    #W - AA
    import_handling_fee=fields.Float(string='Import handling Fee')
    lift_charge=fields.Float(string='Fork Lift Charges')
    storage_charge=fields.Float(string='Storage Charge (Shipping Port)')
    dg_charge=fields.Float(string='DG Charges')
    port_dues_charge=fields.Float(string="Port Dues and Charges",store=True, compute='_compute_port_dues')

    #AB - AF
    ass_examination_expenses=fields.Float(string='Assessment/Examination Expenses')
    labour_expenses=fields.Float(string='Delivery Expenses/Labour Expenses')
    chemical_test_avoid=fields.Float(string='Chemical Test Avoidance')
    c_f_agent_comm=fields.Float(string='C F Agent Commission')
    local_transport_charge=fields.Float(string='Local Transport Charge To Warehouse')
    clear_forwar_exp=fields.Float(string='Clearing and Forwarding Expenses',store=True,compute='_compute_clr_ford_exp')

    #AG - AM
    lc_related_charges=fields.Float(string='L/C Commission & L/C Related Charges')
    vat_lc_comm=fields.Float(string='Vat on L/C comm')
    bank_process_fee=fields.Float(string='Bank Gurantee/ Processing Fee')
    cable_charges =fields.Float(string='Cable Charges (Office+Swift+VAT)')
    insurance_payorder_charge=fields.Float(string='Insurance Payorder Charge')
    misc_charges=fields.Float(string='Misc Charges')
    stamp_charges=fields.Float(string='Stamp Charges and other Charges')
    credit_report_charges =fields.Float(string='Credit Report Collection Charges')
    final_doc_procc_fee =fields.Float(string='Final Documents Fee')

    bank_service_fee=fields.Float(string='Bank Service Fee',store=True,compute='_compute_bank_service_charges')
    total_inland_cost=fields.Float(string='Total Inland Cost incl. Insurance',store=True,compute='_compute_bank_service_charges')

    gross_cost_to_warehouse=fields.Float(string='Total Gross Landed Cost upto Warehouse',store=True,compute='_compute_gross_cost_to_warehouse')
    vat_tobe_adjust=fields.Float(string='Vat to be adjusted with output Vat on Scale',store=True,compute='_compute_vat_ait_adjusted')
    ait_tobe_adjust=fields.Float(string='AIT to be adjusted with Corporate Income Tax',store=True,compute='_compute_vat_ait_adjusted')
    net_cost_to_warehouse=fields.Float(string='Total Net Landed Cost up to Warehouse',store=True,compute='_compute_net_cost_to_warehouse')
    net_cost_per_kg=fields.Float(string='Total Net Landed Cost Per KG',store=True,compute='_compute_net_cost_per_kg')
    gross_cost_per_kg=fields.Float(string='Total Gross Landed Cost Per KG',store=True,compute='_compute_gross_cost_per_kg')
    pur_mushok1_vat_price_dec=fields.Float(string='Purchase Price for Mushok 1 Vat Price Decleration',compute='_compute_mushok_vat_price',store=True)
    vat_tobe_adjust_output_per_kg=fields.Float(string='VAT to be adjusted with Output VAT on Sale per KG',store=True,compute='_compute_output_vat_sale_perkg')

    floor_price_without_vat=fields.Float(string='Floor Price for sale without VAT')
    min_price_cover_import_vat=fields.Float(string='Minimum Price withouy VAT to cover the import VAT',compute='_compute_min_to_cover_vat',store=True)

    custom_duty_percent=fields.Float(string="% of actual Invoice Value")


    #---------------------- Creating PO---------------------

    def action_create_po(self):
        for record in self:
            if not record.product_id or not record.vendor_id:
                raise UserError("Please select a Product and Vendor to create a Purchase Order.")

            # Create PO Line
            po_line_vals = {
                'product_id': record.product_id.id,
                'product_qty': record.import_qty,
                'price_unit': record.inv_value_pkg,
                'name': record.product_id.name,
                'date_planned': fields.Date.today(),
            }

            # Create PO
            po_vals = {
                'partner_id': record.vendor_id.id,
                'date_order': fields.Datetime.now(),
                'currency_id':record.currency_id.id,
                'order_line': [(0, 0, po_line_vals)],
            }
            po = self.env['purchase.order'].create(po_vals)

            # Link the PO to the Landed Cost record
            record.po_id = po.id

    # -------------------- Journal Entry------------------

    def action_create_journal_entry(self):
        for record in self:
            # Validate required fields
            if not record.lc_margin_percent:
                raise ValueError("Please enter LC Margin (%)")

            # Calculate margin amount
            margin_amount = record.inv_value_BDT * (record.lc_margin_percent / 100)

            # Create journal entry
            journal_entry = self.env['account.move'].create({
                'journal_id': self.env.ref('account.1_general').id,
                # Replace with your Miscellaneous journal's external ID
                'date': fields.Date.today(),
                'ref': record.lc_reference,
                'line_ids': [
                    (0, 0, {
                        'account_id': self.env['account.account'].search([('code', '=', '122101')], limit=1).id,
                        # LC Margin Account
                        'debit': margin_amount,
                        'credit': 0.0,
                        'name': 'LC Margin Amount',
                    }),
                    (0, 0, {
                        'account_id': self.env['account.account'].search([('code', '=', '128203')], limit=1).id,
                        # Bank Account
                        'debit': 0.0,
                        'credit': margin_amount,
                        'name': 'LC Margin Amount',
                    }),
                ]
            })
            self.journal_entry_created = 'created' #changing the Journal entry staus from not-created to created
            #if we call this then the entries will be posted.
            #so to keep the entry as draft stage do not call the below method .action.post()
            #journal_entry.action_post()












    @api.depends('pur_mushok1_vat_price_dec','cd_landed','sd_landed','rd_landed','custom_assessable_value_bdt','import_qty')
    def _compute_mushok_vat_price(self):
        for rec in self:
            if rec.import_qty:
                rec['pur_mushok1_vat_price_dec'] =(rec.custom_assessable_value_bdt + rec.cd_landed + rec.sd_landed + rec.rd_landed) / rec.import_qty

    @api.depends('vat_tobe_adjust_output_per_kg')
    def _compute_min_to_cover_vat(self):
        for rec in self:
            rec['min_price_cover_import_vat']=rec.vat_tobe_adjust_output_per_kg/0.15

    @api.depends('net_cost_to_warehouse','import_qty','vat_tobe_adjust')
    def _compute_output_vat_sale_perkg(self):
        for rec in self:
            if rec.import_qty:
                rec['vat_tobe_adjust_output_per_kg']=rec.vat_tobe_adjust/rec.import_qty


    @api.depends('vat_landed','atv','ait_landed')
    def _compute_vat_ait_adjusted(self):
        for rec in self:
            rec['vat_tobe_adjust']=rec.vat_landed+rec.atv+rec.at_landed
            rec['ait_tobe_adjust']=rec.ait_landed #here for every cd,sd,at,ait,vat calculation we use ait_landed type of varr.

    @api.depends('cd','custom_assessable_value_bdt','sd','rd')
    def _compute_cd(self):
        for rec in self:
            rec['cd_landed']=rec.custom_assessable_value_bdt*(rec.cd/100)
            rec['sd_landed']=(rec.custom_assessable_value_bdt+rec.cd)*(rec.sd/100)
            rec['rd_landed']=rec.custom_assessable_value_bdt*(rec.rd/100)

    #@api.depends('sd', 'custom_assessable_value_bdt')
    #def _compute_sd(self):
        #for rec in self:
            #rec['sd_landed'] = rec.custom_assessable_value_bdt * (rec.sd / 100)

    #@api.depends('rd', 'custom_assessable_value_bdt')
    #def _compute_rd(self):
        #for rec in self:
            #rec['rd_landed'] = rec.custom_assessable_value_bdt * (rec.rd / 100)

    @api.depends('landed_vat', 'custom_assessable_value_bdt','cd_landed','sd_landed')
    def _compute_vat_landed(self):
        for rec in self:
            rec['vat_landed'] = (rec.custom_assessable_value_bdt+rec.cd_landed+rec.sd_landed) * (rec.landed_vat/ 100)

    @api.depends('ait_landed', 'custom_assessable_value_bdt')
    def _compute_ait_landed(self):
        for rec in self:
            rec['ait_landed'] = rec.custom_assessable_value_bdt * (rec.ait/ 100)

    @api.depends('at_landed', 'custom_assessable_value_bdt','cd_landed')
    def _compute_at_landed(self):
        for rec in self:
            rec['at_landed'] = (rec.custom_assessable_value_bdt+rec.cd_landed) * (rec.at / 100)





    @api.depends('cd_landed','sd_landed','vat_landed','ait_landed','DSC','atv','at_landed')
    def _compute_duties_taxes(self):
        for rec in self:
            rec['duties_taxes']=rec.cd_landed+rec.sd_landed+rec.vat_landed+rec.ait_landed+rec.DSC+rec.atv+rec.at_landed



    @api.depends('doc_pros_fee','VAT_c_f_agents','others','lcl_charges','income_tax_c_f_comm','duties_taxes','fine_penalties')
    def _compute_c_f_agent_jobs(self):
        for rec in self:
            rec['tax_for_c_f_agent_jobs'] =rec.doc_pros_fee+rec.VAT_c_f_agents+rec.others+rec.lcl_charges+rec.income_tax_c_f_comm+rec.fine_penalties

    @api.depends('duties_taxes','tax_for_c_f_agent_jobs')
    def _compute_total_duties_taxes(self):
        for rec in self:
            rec['total_duties_taxes']=rec.duties_taxes+rec.tax_for_c_f_agent_jobs

    @api.depends('air_way_bill','noc_charges')
    def _compute_shipping_charges(self):
        for rec in self:
            rec['shipping_charges']=rec.air_way_bill+rec.noc_charges


    @api.depends('import_handling_fee','lift_charge','storage_charge','dg_charge')
    def _compute_port_dues(self):
        for rec in self:
            rec['port_dues_charge']=rec.import_handling_fee+rec.lift_charge+rec.storage_charge+rec.dg_charge


    @api.depends('ass_examination_expenses','labour_expenses','chemical_test_avoid','c_f_agent_comm','local_transport_charge')
    def _compute_clr_ford_exp(self):
        for rec in self:
            rec['clear_forwar_exp'] =rec.ass_examination_expenses+rec.labour_expenses+rec.chemical_test_avoid+rec.c_f_agent_comm+rec.local_transport_charge



    @api.depends('lc_related_charges','vat_lc_comm','bank_process_fee','cable_charges','insurance_payorder_charge','misc_charges','stamp_charges','credit_report_charges','final_doc_procc_fee')
    def _compute_bank_service_charges(self):
        for rec in self:
            rec['bank_service_fee']=rec.lc_related_charges+rec.vat_lc_comm+rec.bank_process_fee+rec.cable_charges+rec.insurance_payorder_charge+rec.misc_charges+rec.credit_report_charges+rec.final_doc_procc_fee+rec.stamp_charges
            rec['total_inland_cost']=rec.bank_service_fee+ rec.clear_forwar_exp+rec.port_dues_charge+rec.shipping_charges+rec.total_duties_taxes+rec.insurance_premium_bdt

    @api.depends('inv_value_BDT','total_inland_cost')
    def _compute_gross_cost_to_warehouse(self):
        for rec in self:
            rec['gross_cost_to_warehouse'] =rec.inv_value_BDT+rec.total_inland_cost


    @api.depends('ait_tobe_adjust','vat_tobe_adjust','gross_cost_to_warehouse','import_qty')
    def _compute_net_cost_to_warehouse(self):
        for rec in self:
            rec['net_cost_to_warehouse']=rec.gross_cost_to_warehouse-rec.vat_tobe_adjust-rec.ait_tobe_adjust


    @api.depends('ait_tobe_adjust', 'vat_tobe_adjust', 'gross_cost_to_warehouse', 'import_qty','net_cost_to_warehouse')
    def _compute_gross_cost_per_kg(self):
        for rec in self:
            if rec.import_qty:
                rec['gross_cost_per_kg']=rec.gross_cost_to_warehouse/rec.import_qty

    @api.depends('ait_tobe_adjust', 'vat_tobe_adjust', 'gross_cost_to_warehouse', 'import_qty', 'net_cost_to_warehouse','floor_price_without_vat')
    def _compute_net_cost_per_kg(self):
        for rec in self:
            if rec.import_qty:
                rec['net_cost_per_kg']=rec.net_cost_to_warehouse/rec.import_qty
            if rec.product_id:
                rec.product_id.standard_price=rec.net_cost_per_kg
                rec.product_id.list_price=rec.floor_price_without_vat


    #@api.depends('con_rate','inv_value','inv_value_BDT')
    @api.depends('con_rate','inv_value','inv_value_BDT')
    def _compute_convert_bdt_to_usd(self):
        for rec in self:
            if rec.con_rate:
                rec['inv_value_BDT']=rec.con_rate*(rec.cob+rec.inv_value)


    @api.depends('inv_value','import_qty')
    def _compute_com_value_us(self):
        for rec in self:
            if rec.import_qty:  # Check to prevent division by zero
                rec['inv_value_pkg'] = rec.inv_value/rec.import_qty
            else:
                rec['inv_value_pkg'] = 0.0  # Set to 0 if import_qty is 0


    @api.depends('import_qty','inv_value_BDT')
    def _compute_BDT_pkg(self):
        for rec in self:
            if rec.import_qty:
                rec['inv_value_BDT_pkg'] = rec.inv_value_BDT / rec.import_qty


    @api.depends('insurance_premium_precent','inv_value_BDT') #ommit the calculation.
    def _compute_insurance_premium(self):
        for rec in self:
            x=rec.inv_value*(rec.insurance_premium_precent/100)
            rec['insurance_premium_bdt']=rec.inv_value_BDT*(rec.insurance_premium_precent/100)

    @api.depends('insurance_premium_bdt','inv_value_BDT')
    def _compute_cif_imported_cost(self):
        for rec in self:
            rec['cif_value_imported_cost']=rec.inv_value_BDT+rec.insurance_premium_bdt


    @api.depends('inv_value_BDT','custom_assessable_value_percent')
    def _compute_custom_assessable_value(self):
        for rec in self:
            rec['custom_assessable_value_bdt']=rec.inv_value_BDT*(rec.custom_assessable_value_percent/100)



