from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_id = fields.Many2one('property')
    price = fields.Float(related='property_id.expected_price')
    price_selling = fields.Float(compute='_compute_price')

    def _compute_price(self):
        for rec in self:
            rec.price_selling = rec.property_id.selling_price
