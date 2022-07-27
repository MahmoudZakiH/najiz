# -*- coding: utf-8 -*-
# from odoo import http


# class EditPaymentMethodSales(http.Controller):
#     @http.route('/edit_payment_method_sales/edit_payment_method_sales', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/edit_payment_method_sales/edit_payment_method_sales/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('edit_payment_method_sales.listing', {
#             'root': '/edit_payment_method_sales/edit_payment_method_sales',
#             'objects': http.request.env['edit_payment_method_sales.edit_payment_method_sales'].search([]),
#         })

#     @http.route('/edit_payment_method_sales/edit_payment_method_sales/objects/<model("edit_payment_method_sales.edit_payment_method_sales"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('edit_payment_method_sales.object', {
#             'object': obj
#         })
