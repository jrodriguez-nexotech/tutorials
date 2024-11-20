from odoo import models, fields
class EstatePropertyTag(models.Model):
        _name = 'estate.property.tag'
        _descripcion = 'Etiquetas de propiedades'
        _order = 'name'
        name = fields.Char(string='Title',required=True)
        _sql_constraints = [
        ("check_name", "UNIQUE(name)", "El nombre debe ser único"),
        ]
        color = fields.Integer('Color')