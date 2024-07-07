from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    _description = 'Karim Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=1, default='New', size=20, translate=True)
    ref = fields.Char(default='New', readonly=1)
    description = fields.Text()
    postcode = fields.Char(required=1)
    date_availability = fields.Date(tracking=1)
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute="_compute_diff")
    bedrooms = fields.Integer(tracking=1)
    living_area = fields.Integer()
    garage = fields.Boolean(groups="app_one.prop_manager_group")
    garden = fields.Boolean()
    garden_area = fields.Integer()
    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')
    owner_phone = fields.Char(related='owner_id.phone', readonly=0)
    owner_address = fields.Char(related='owner_id.address')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('east', 'East'),
        ('west', 'West'),
        ('south', 'South'),
    ], default='north')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ], default='draft')

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name already exist')
    ]
    line_ids = fields.One2many('property.line', 'property_id')
    active = fields.Boolean(default=True)


    def check_expected_selling_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            print(rec)
            if rec.expected_selling_date and rec.expected_selling_date < fields.Date.today():
                rec.is_late = True

    @api.depends('expected_price', 'selling_price', 'owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            print("inside method _compute_diff")
            rec.diff = rec.expected_price - rec.selling_price

    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            print(rec)
            print("inside method _onchange_expected_price")
            return {
                'warning': {
                    'title': "Warning",
                    'message': "negative value",
                    'type': "notification"
                }
            }

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms < 1:
                raise ValidationError('please add valid number of bedrooms')

    @api.model
    def create(self, vals):
        res = super().create(vals)
        print("Hello Karim")
        return res

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        res = super()._search(args, offset=0, limit=None, order=None, count=False, access_rights_uid=None)
        print("Searching")
        return res

    def write(self, vals):
        res = super().write(vals)
        print("Hello inside write function")
        return res

    def unlink(self):
        res = super().unlink()
        print("Hello inside unlink function")
        return res

    def action_draft(self):
        for rec in self:
            rec.create_history_record(rec.state, 'draft')
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state, 'pending')
            rec.write({
                'state': 'pending',
            })

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state, 'sold')
            rec.state = 'sold'

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')
            rec.state = 'closed'

    def action_zein(self):
        for rec in self:
            print("inside action zein")

    def action(self):
        print(self.env['property'].search([('name', '=', 'property 2')]))

    @api.model
    def create(self, vals):
        res = super(Property, self).create(vals)
        if res.ref == "New":
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return res

    def create_history_record(self, old_state, new_state, reason=""):
        for rec in self:
            rec.env['property.history'].create({
                'user_id': rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or "",
                'line_ids': [(0, 0, {'description': line.description, 'area': line.area}) for line in rec.line_ids],
            })

    def action_open_change_state_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.property_change_state_server_action')
        action['context'] = {'default_property_id': self.id}
        return action


class PropertyLine(models.Model):
    _name = 'property.line'

    property_id = fields.Many2one('property')
    area = fields.Float()
    description = fields.Char()
