from odoo import models, fields
from dateutil.relativedelta import relativedelta
class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description', copy=False)
    postcode = fields.Char(string='Postal Code')
    date_availability = fields.Date(string='Availability Date', copy=False,default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string='Garden Orientation'
    )
    state = fields.Selection(
        [
            ('nuevo','Nuevo'),
            ('ofertaR','Oferta recibida'),
            ('ofertaA','Oferta aceptada'),
            ('vendido','Vendido'),
            ('cancelado','Cancelado')
        ],
        string="state", required=True, copy=False, default='nuevo'
    )
    active = fields.Boolean(string='Active', default=True)
    tipo_propiedad_id =fields.Many2one("estate.property.type",string="Tipo Propiedad")
    comprador_id =fields.Many2one("res.users",string="Comprador", copy=False, default=lambda self: self.env.user)
    vendedor_id =fields.Many2one("res.partner",string="Vendedor", copy=False)
    tag_ids= fields.Many2many("estate.property.tag", string="Tags")
    offer_id= fields.One2many("estate.property.offer","property_id",string="Offers")
    total_area=fields.Float(compute="_area_total")

    def _area_total(self):
        total_Area = self.living_area + self.garden_area
        return total_Area
     
  
