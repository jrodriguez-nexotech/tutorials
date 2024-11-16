from odoo import models, fields
class EstatePropertyTag(models.Model):
        _name = 'estate.property.tag'
        _descripcion = 'Etiquetas de propiedades'

        name = fields.Char(string='Title',required=True)