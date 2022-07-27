# -*- coding: utf-8 -*-
# from odoo import http


# class EditDuplicateInvoiceLine(http.Controller):
#     @http.route('/edit_duplicate_invoice_line/edit_duplicate_invoice_line/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/edit_duplicate_invoice_line/edit_duplicate_invoice_line/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('edit_duplicate_invoice_line.listing', {
#             'root': '/edit_duplicate_invoice_line/edit_duplicate_invoice_line',
#             'objects': http.request.env['edit_duplicate_invoice_line.edit_duplicate_invoice_line'].search([]),
#         })

#     @http.route('/edit_duplicate_invoice_line/edit_duplicate_invoice_line/objects/<model("edit_duplicate_invoice_line.edit_duplicate_invoice_line"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('edit_duplicate_invoice_line.object', {
#             'object': obj
#         })
