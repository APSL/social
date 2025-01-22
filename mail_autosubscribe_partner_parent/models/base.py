from odoo import api, models


class BaseModel(models.AbstractModel):
    _inherit = "base"

    @api.model
    def _message_get_autosubscribe_followers(self, partners):
        res = super()._message_get_autosubscribe_followers(partners)
        return res + (res.mapped("parent_id"))
