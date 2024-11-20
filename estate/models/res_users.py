from odoo import models, fields

class EstateProperty(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        'estate.property', 'comprador_id', string='Properties',domain=[("state", "in", ["nuevo", "ofertaR"])]
    )