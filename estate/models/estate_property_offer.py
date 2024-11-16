from odoo import models, fields
class EstatePropertyOffer(models.Model):
        _name = 'estate.property.offer'
        _descripcion = 'Oferta de propiedades'

        price = fields.Float(String='Price')
        status = fields.Selection([
                
                ('accepted','Acceptado'),
                ('refused','Rechazado')],
                copy=False, String='Estado'
        )
        partner_id = fields.Many2one("res.partner", String='Comprador',required=True)
        property_id = fields.Many2one("estate.property",String='Propiedad',required=True)
