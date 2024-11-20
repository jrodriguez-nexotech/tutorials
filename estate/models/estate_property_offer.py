from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from odoo.tools import float_compare
class EstatePropertyOffer(models.Model):
        _name = 'estate.property.offer'
        _descripcion = 'Oferta de propiedades'
        _order = 'price desc'
        price = fields.Float(String='Price')
        status = fields.Selection([
                
                ('accepted','Acceptado'),
                ('refused','Rechazado')],
                copy=False, String='Estado'
        )
        partner_id = fields.Many2one("res.partner", String='Comprador',required=True)
        property_id = fields.Many2one("estate.property",String='Propiedad',required=True)
        property_type_id = fields.Many2one("estate.property.type", related="property_id.tipo_propiedad_id", string="Property Type", store=True)
        validity = fields.Integer(default=7)
        date_deadline = fields.Date(compute='_compute_date_deadline',inverse='_inverse_date_deadline',store=True)
        _sql_constraints = [
                ('check_price','CHECK(price>0)','El precio de oferta deber ser positivo')
        ]
        @api.depends('create_date', 'validity')
        def _compute_date_deadline(self):
                for offer in self:
                        create_date = offer.create_date or datetime.now()
                        offer.date_deadline = create_date + timedelta(days=offer.validity)

        def _inverse_date_deadline(self):
                for offer in self:
                        date = offer.create_date.date() if offer.create_date else fields.Date.today()
                        offer.validity = (offer.date_deadline - date).days
        
        def action_accept(self):
                if self.property_id.offer_id.filtered(lambda offer: offer.status == 'accepted'):
                        raise UserError('Ya existe una oferta aceptada para esta propiedad.')

                self.property_id.write({
                'selling_price': self.price,  
                'vendedor_id': self.partner_id.id,    
                })
                self.write({'status': 'accepted'})
                self.property_id.write({'state': 'ofertaA'})
                
                return True

        def action_refuse(self):
                self.write({'status': 'refused'})
                return True
        @api.model
        def create(self, vals):
                if vals.get("property_id") and vals.get("price"):
                        prop = self.env["estate.property"].browse(vals["property_id"])
                
                if prop.offer_id:
                        max_offer = max(prop.mapped("offer_id.price"))
                        if float_compare(vals["price"], max_offer, precision_rounding=0.01) <= 0:
                                raise UserError("The offer must be higher than %.2f" % max_offer)
                prop.state = "ofertaR"
                return super().create(vals)
        