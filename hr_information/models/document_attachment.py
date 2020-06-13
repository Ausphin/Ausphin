# -*- coding: utf-8 -*-

from datetime import datetime, date, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import Warning


class HrEmployeeDocument(models.Model):
    _name = 'hr.employee.document'
    _description = 'HR Employee Documents'


    name = fields.Char(string='Document Number', required=True, copy=False)
    document_name = fields.Many2one('employee.checklist', string='Document', required=True)
    description = fields.Text(string='Description', copy=False)
    employee_ref = fields.Many2one('hr.employee', copy=False)
    doc_attachment_id = fields.Many2many('ir.attachment', 'doc_attach_rel', 'doc_id', 'attach_id3', string="Attachment",
                                         help='You can attach the copy of your document', copy=False)
    

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def _document_count(self):
        for each in self:
            document_ids = self.env['hr.employee.document'].search([('employee_ref', '=', each.id)])
            each.document_count = len(document_ids)

    @api.multi
    def document_view(self):
        self.ensure_one()
        domain = [
            ('employee_ref', '=', self.id)]
        return {
            'name': _('Documents'),
            'domain': domain,
            'res_model': 'hr.employee.document',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                           Click to Create for New Documents
                        </p>'''),
            'limit': 80,
            'context': "{'default_employee_ref': '%s'}" % self.id
        }

    document_count = fields.Integer(compute='_document_count', string='# Documents')


class HrEmployeeAttachment(models.Model):
    _inherit = 'ir.attachment'

    doc_attach_rel = fields.Many2many('hr.employee.document', 'doc_attachment_id', 'attach_id3', 'doc_id',
                                      string="Attachment", invisible=1)


class EmployeeEntryDocuments(models.Model):
    _name = 'employee.checklist'
    _inherit = 'mail.thread'
    _description = "Employee Documents"

    name = fields.Char(string='Document Name', copy=False, required=1)
    document_type = fields.Selection([('entry', 'Entry Process'),
                                      ('exit', 'Exit Process'),
                                      ('other', 'Other')], string='Checklist Type', required=1)