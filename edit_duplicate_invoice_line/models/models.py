# -*- coding: utf-8 -*-

from odoo import models, fields, api

class InvoiceLine(models.Model):
    _name = 'invoice.line'
    _rec_name = 'name'
    _description = 'Invoice Line'

    product_id = fields.Many2one(comodel_name="product.product", string="Product", required=False, )
    name = fields.Char(string="Name", required=False,related='product_id.name' )
    quantity = fields.Float(string="Quantity",  required=False, )
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure', ondelete="restrict")
    price_unit = fields.Float(string="Price Unit",  required=False, )
    discount = fields.Float(string="Discount",  required=False, )
    tax_ids = fields.Many2many(comodel_name="account.tax",  string="Taxes", )
    price_total = fields.Float(string="total",  required=False, )
    price_subtotal = fields.Float(string="Subtotal",  required=False, )
    invoice_line_id = fields.Many2one(comodel_name="account.move", string="", required=False, )
    partner_id = fields.Many2one(comodel_name="res.partner", string="", required=False, )
    company_id = fields.Many2one(comodel_name='res.company', string='Company',
                                 store=True, readonly=True,
                                 compute='_compute_company_id')
    currency_id = fields.Many2one(string='Company Currency', readonly=True,
                                          related='company_id.currency_id')
    display_type = fields.Selection([
        ('line_section', 'Section'),
        ('line_note', 'Note'),
    ], default=False, help="Technical field for UX purpose.")


    def get_price_subtotal(self):
        self.price_subtotal = self._get_price_total_and_subtotal_model()['price_subtotal']
        self.price_total = self._get_price_total_and_subtotal_model()['price_total']

    @api.depends('product_id')
    def _compute_company_id(self):
        for move in self:
            move.company_id =  self.env.company.id

    @api.model
    def _get_price_total_and_subtotal_model(self):
        price_unit = self.price_unit
        quantity = self.quantity
        discount = self.discount
        currency = self.currency_id
        product = self.product_id
        partner = self.partner_id
        taxes = self.tax_ids
        move_type = self.invoice_line_id.move_type

        res = {}

        # Compute 'price_subtotal'.
        line_discount_price_unit = price_unit * (1 - (discount / 100.0))
        print('line_discount_price_unit', line_discount_price_unit)
        subtotal = quantity * line_discount_price_unit

        # Compute 'price_total'.
        if taxes:
            taxes_res = taxes._origin.with_context(force_sign=1).compute_all(line_discount_price_unit,
                                                                             quantity=quantity, currency=currency,
                                                                             product=product, partner=partner,
                                                                             is_refund=move_type in (
                                                                                 'out_refund', 'in_refund'))
            print('taxestaxes', taxes)
            res['price_subtotal'] = taxes_res['total_excluded']
            res['price_total'] = taxes_res['total_included']
        else:
            res['price_total'] = res['price_subtotal'] = subtotal
        # In case of multi currency, round before it's use for computing debit credit
        # if currency:
        #     res = {k: currency.round(v) for k, v in res.items()}
        return res


class AccountMove(models.Model):
    _inherit = 'account.move'


    new_invoice_line_ids = fields.One2many(comodel_name="invoice.line", inverse_name="invoice_line_id", string="Invoice Line", required=False, )

    def delete_duplicate_lines(self):
        for rec in self:
            products = []
            new_lines = []
            for line in rec.invoice_line_ids:
                if line.product_id.id not in products:
                    products.append(line.product_id.id)
                    new_lines.append([0, 0, {
                        'product_id': line.product_id.id,
                        # 'analytic_account_id': line.analytic_account_id.id,
                        'name': line.name,
                        'quantity': line.quantity,
                        'product_uom_id': line.product_uom_id.id,
                        'price_unit': line.price_unit,
                        # 'price_subtotal': line.price_subtotal,
                        'tax_ids': line.tax_ids.mapped('id'),
                    }])
                else:

                    for x in new_lines:
                        if int(x[2]['product_id']) == line.product_id.id:
                            x[2]['quantity'] = x[2]['quantity'] + line.quantity
            rec.new_invoice_line_ids = False

            rec.new_invoice_line_ids = new_lines
            for new_line in rec.new_invoice_line_ids:
                new_line.get_price_subtotal()
