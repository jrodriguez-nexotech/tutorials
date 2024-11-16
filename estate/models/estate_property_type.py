from odoo import models, fields
class EstatePropertyType(models.Model):
        _name = 'estate.property.type'
        _descripcion = 'tipos de propiedades'

        name = fields.Char(string='Title',required=True)
        
        _sql_constraints = [
        ("check_name", "UNIQUE(name)", "El nombre debe ser único"),
        ]
