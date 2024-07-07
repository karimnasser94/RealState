from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    property_id = fields.Many2one('property')

    def action_confirm(self):
        res = super().action_confirm()
        print("Hello inside action_confirm method")
        return res



