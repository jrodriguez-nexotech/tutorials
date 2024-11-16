from odoo import models, fields
class EstatePropertyType(models.Model):
        _name = 'estate.property.type'
        _descripcion = 'tipos de propiedades'

        name = fields.Char(string='Title',required=True)
