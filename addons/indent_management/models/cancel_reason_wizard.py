from odoo import fields,api,models
class CancelReasonWizard(models.TransientModel):
    _name = "cancel.reason.wizard"
    _description = "Cancel Reason Wizard"

    reason = fields.Text(string="Reason", required=True)
    cancel_date = fields.Date(string="Cancellation Date", required=True, default=fields.Date.context_today)

    def action_confirm_cancel(self):
        active_id = self.env.context.get('active_id')
        if active_id:
            record = self.env['indent.management'].browse(active_id)
            record.write({
                'stats': 'cancel',
                'reason': self.reason,
                'cancel_date': self.cancel_date,
            })
