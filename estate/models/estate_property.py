from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
from odoo.tools import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order='id desc'
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
    total_area=fields.Float(compute="_area_total", string="Total área")
    best_price =fields.Float(compute="_mejor_price", string="Mejor precio",  help="Best offer received")

    _sql_constraints = [
        ('check_expected_price','CHECK(expected_price>0)','El precio esperado deber ser positivo'),
        ('check_selling_price','CHECK(selling_price>=0)','El precio de venta deber ser positivo')
    ]

    @api.depends('living_area', 'garden_area')
    def _area_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_id.price')
    def _mejor_price(self):
        for record in self:
            if record.offer_id:
                record.best_price = max(record.offer_id.mapped('price'))
            else:
                record.best_price = 0.0
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains("expected_price", "selling_price")
    def _check_price_difference(self):
        for prop in self:
            if (
                not float_is_zero(prop.selling_price, precision_rounding=0.01)
                and float_compare(prop.selling_price, prop.expected_price * 90.0 / 100.0, precision_rounding=0.01) < 0
            ):
                raise ValidationError(
                    "¡El precio de venta debe ser al menos el 90% del precio esperado! "
                    + "Debes reducir el precio esperado si quieres aceptar esta oferta."
                )


    def action_sold(self):
        if "cancelado" in self.mapped("state"):
            raise UserError("Las propiedades canceladas no se pueden vender.")
        return self.write({"state": "vendido"})

    def action_cancel(self):
        if "vendido" in self.mapped("state"):
            raise UserError("Las propiedades vendidas no se pueden cancelar.")
        return self.write({"state": "canceled"})
    
    @api.ondelete(at_uninstall=False)  
    def _unlink_if_not_new_or_cancelled(self):
        if any(property.state  in ['nuevo', 'cancelado'] for property in self):
            raise UserError("No se puede eliminar la propiedad porque su estado no es 'Nueva' o 'Cancelada'.")

  
