from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    bank_code = fields.Char(string="Bank Code")
    account_number = fields.Char(string="Account Number")
    print_format = fields.Selection([
        ('print.png', 'Print'),
        ('compact.png', 'Compact'),
        ('compact2.png', 'Compact2'),
        ('qr_only.png', 'QR Only')
    ], string="Print Format", default="print.png")
    account_name = fields.Char(string="Account Name")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        bank_code = self.env['ir.config_parameter'].sudo().get_param('bank_code') or ''
        account_number = self.env['ir.config_parameter'].sudo().get_param('account_number') or ''
        print_format = self.env['ir.config_parameter'].sudo().get_param('print_format') or ''
        account_name = self.env['ir.config_parameter'].sudo().get_param('account_name') or ''
        res.update({
            'bank_code': bank_code,
            'account_number': account_number,
            'print_format': print_format,
            'account_name': account_name,
        })
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('bank_code', self.bank_code or '')
        self.env['ir.config_parameter'].sudo().set_param('account_number', self.account_number or '')
        self.env['ir.config_parameter'].sudo().set_param('print_format', self.print_format or '')
        self.env['ir.config_parameter'].sudo().set_param('account_name', self.account_name or '')

