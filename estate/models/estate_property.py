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
  
