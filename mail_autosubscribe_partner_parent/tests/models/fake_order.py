from odoo import fields, models


class FakeOrder(models.Model):
    _name = "fake.order"
    _inherit = "mail.thread"
    _description = "Fake sale.order like model"

    partner_id = fields.Many2one("res.partner", required=True)
