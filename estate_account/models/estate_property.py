from odoo import models,api, Command, fields
class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        res = super().action_sold()
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        for prop in self:
            self.env["account.move"].create(
                {
                    "partner_id": prop.vendedor_id.id,
                    "move_type": "out_invoice",
                    "journal_id": journal.id,
                    "invoice_line_ids": [
                        (
                            0,
                            0,
                            {
                                "name": prop.name,
                                "quantity": 1.0,
                                "price_unit": prop.selling_price * 6.0 / 100.0,
                            },
                        ),
                        (
                            0,
                            0,
                            {
                                "name": "Administrative fees",
                                "quantity": 1.0,
                                "price_unit": 100.0,
                            },
                        ),
                    ],
                }
            )
        return res

    