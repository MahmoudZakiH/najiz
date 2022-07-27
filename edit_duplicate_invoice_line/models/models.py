# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    def delete_duplicate_lines(self):
        for rec in self:
            products = []
            new_lines = []
            for line in rec.invoice_line_ids:
                if line.product_id.id not in products:
                    products.append(line.product_id.id)
                    new_lines.append([0, 0, {
                        'product_id': line.product_id.id,
                        'analytic_account_id': line.analytic_account_id.id,
                        'name': line.name,
                        'quantity': line.quantity,
                        'product_uom_id': line.product_uom_id.id,
                        'price_unit': line.price_unit,
                        'tax_ids': line.tax_ids.mapped('id'),
                    }])
                else:

                    for x in new_lines:
                        if int(x[2]['product_id']) == line.product_id.id:
                            x[2]['quantity'] = x[2]['quantity'] + line.quantity
            rec.invoice_line_ids = False

            rec.invoice_line_ids = new_lines
