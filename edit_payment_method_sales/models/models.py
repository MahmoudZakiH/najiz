# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EditSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    analytic_account_id = fields.Many2one('account.analytic.account', string='Driver Name')


    def _prepare_invoice_line(self, **optional_values):
        invoice_line = super(EditSaleOrderLine, self)._prepare_invoice_line(**optional_values)
        invoice_line['analytic_account_id'] = self.analytic_account_id.id
        return invoice_line



class EditSaleOrder(models.Model):
    _inherit = 'sale.order'


    payment_type_method = fields.Selection(string="Order Type", selection=[('cod', 'COD'), ('cc', 'CC'), ], required=False, )
    cod_amount = fields.Float(string="Cod Amount", required=False,compute='get_cod_amount' )
    payment_state = fields.Selection(string="State", selection=[('delivered', 'Delivered'), ('returned', 'Returned'), ], required=True, )
    is_cash = fields.Boolean(string="Cash",)
    cash_amount = fields.Float(string="Cash Amount", required=False, )
    is_visa = fields.Boolean(string="Visa",)
    visa_commission = fields.Float(string="Visa Amount",  required=False, )
    is_mada = fields.Boolean(string="Mada",)
    mada_commission = fields.Float(string="Mada Amount",  required=False, )
    analytic_account_id = fields.Many2one('account.analytic.account', string='Driver Name')
    awb_no = fields.Char(string="AWB NO", required=False, )
    origin = fields.Char(string="ORIGIN", required=False, )
    description = fields.Char(string="DESTINATION", required=False, )
    receiver_phone = fields.Char(string="RECEIVER PHONE", required=False, )
    receiver_name = fields.Char(string="RECEIVER Name", required=False, )
    receiver_address = fields.Char(string="RECEIVER ADDRESS", required=False, )
    receiver_date = fields.Date(string="DELIVER DATE", required=False, )
    on_pieces = fields.Char(string="ON PIECES", required=False, )
    cod_cc_amount = fields.Float(string="Cod/Cc Amount",  required=False, )



    @api.depends('cash_amount','visa_commission','mada_commission')
    def get_cod_amount(self):
        for rec in self:
            rec.cod_amount=rec.cash_amount+rec.visa_commission+rec.mada_commission



    def compute_payment_method(self):
        for rec in self:
            print('hellooooooooooooooooooooooooooooooo')
            cc_list=[]
            cod_cash=[]
            cod_mada=[]
            cod_visa=[]
            return_list=[]
            product_return_sitting = self.env['product.product'].search(
                [('id', '=', int(self.env['ir.config_parameter'].sudo().get_param('product_return_id', )))])
            product_delivery_sitting = self.env['product.product'].search(
                [('id', '=', int(self.env['ir.config_parameter'].sudo().get_param('product_delivery_id', )))])
            collect_on_delivery_sitting = self.env['product.product'].search([('id', '=', int(self.env['ir.config_parameter'].sudo().get_param('collect_on_delivery_id', )))])
            product_mada_sitting = self.env['product.product'].search([('id', '=', int(self.env['ir.config_parameter'].sudo().get_param('product_mada_id', )))])
            mada_commission_percent_sitting = float(self.env['ir.config_parameter'].sudo().get_param('mada_commission_percent', ))
            product_visa_sitting = self.env['product.product'].search(
                [('id', '=', int(self.env['ir.config_parameter'].sudo().get_param('product_visa_id', )))])
            visa_commission_percent_sitting = float(self.env['ir.config_parameter'].sudo().get_param('visa_commission_percent', ))
            rec.order_line = False
            if rec.payment_state == 'delivered':
                if rec.payment_type_method == 'cc':
                    print('rec.payment_type_method', rec.payment_type_method)
                    cc_list.append([0, 0, {
                        'product_id': product_delivery_sitting.id,
                        'name': product_delivery_sitting.name,
                        'analytic_account_id': rec.analytic_account_id.id,
                        'product_uom_qty': 1,
                        'price_unit': 14,
                    }])
                    rec.order_line = cc_list
                elif rec.payment_type_method == 'cod':

                    if rec.is_cash:
                        print('is_cashis_cashis_cash')
                        cod_cash.append([0, 0, {
                            'product_id': product_delivery_sitting.id,
                            'name': product_delivery_sitting.name,
                            'analytic_account_id': rec.analytic_account_id.id,
                            'product_uom_qty': 1,
                            'price_unit': 14,
                        }])
                        cod_cash.append([0, 0, {
                            'product_id': collect_on_delivery_sitting.id,
                            'name': collect_on_delivery_sitting.name,
                            'analytic_account_id': rec.analytic_account_id.id,
                            'product_uom_qty': 1,
                            'price_unit': 4,
                        }])
                        print('cod_cashcod_cash', cod_cash)
                        rec.order_line = cod_cash
                    if rec.is_mada :
                        cod_mada.append([0, 0, {
                            'product_id': product_mada_sitting.id,
                            'name': product_mada_sitting.name,
                            'analytic_account_id': rec.analytic_account_id.id,
                            'product_uom_qty': 1,
                            'price_unit': mada_commission_percent_sitting / 100 * rec.mada_commission,
                        }])
                        if not rec.is_cash:
                            cod_mada.append([0, 0, {
                                'product_id': product_delivery_sitting.id,
                                'name': product_delivery_sitting.name,
                                'analytic_account_id': rec.analytic_account_id.id,
                                'product_uom_qty': 1,
                                'price_unit': 14,
                            }])
                        rec.order_line = cod_mada
                    if rec.is_visa:
                        print('tttttttttttttttt mada')
                        cod_visa.append([0, 0, {
                            'product_id': product_visa_sitting.id,
                            'name': product_visa_sitting.name,
                            'analytic_account_id': rec.analytic_account_id.id,
                            'product_uom_qty': 1,
                            'price_unit': visa_commission_percent_sitting / 100 * rec.visa_commission,
                        }])
                        print('cod_visa', cod_visa)
                        if not rec.is_cash:
                            cod_visa.append([0, 0, {
                                'product_id': product_delivery_sitting.id,
                                'name': product_delivery_sitting.name,
                                'analytic_account_id': rec.analytic_account_id.id,
                                'product_uom_qty': 1,
                                'price_unit': 14,
                            }])
                        rec.order_line = cod_visa
            elif rec.payment_state == 'returned':
                return_list.append([0, 0, {
                    'product_id': product_return_sitting.id,
                    'name': product_return_sitting.name,
                    'analytic_account_id': rec.analytic_account_id.id,
                    'product_uom_qty': 1,
                    'price_unit': product_return_sitting.list_price,
                }])
                print('return_listreturn_list',return_list)
                rec.order_line = return_list
            rec.action_confirm()








class sale_payment_config_settings(models.TransientModel):
    _inherit = 'res.config.settings'

    product_delivery_id = fields.Many2one(comodel_name="product.product", string="Delivery 14", required=False, )
    collect_on_delivery_id = fields.Many2one(comodel_name="product.product", string="Collect on delivery ", required=False, )
    product_mada_id = fields.Many2one(comodel_name="product.product", string="Product Mada Commission", required=False, )
    mada_commission_percent = fields.Float(string="Mada Commission Percent %",  required=False, digits=(16, 4))
    product_visa_id = fields.Many2one(comodel_name="product.product", string="Product Visa Commission", required=False, )
    visa_commission_percent = fields.Float(string="Visa Commission Percent %",  required=False, digits=(16, 4))
    product_return_id = fields.Many2one(comodel_name="product.product", string="Product Return", required=False, )



    #
    # portal_allow_api_keys = fields.Boolean(
    #     string='Customer API Keys',
    #     # compute='_compute_portal_allow_api_keys',
    #     # inverse='_inverse_portal_allow_api_keys',
    # )

    @api.model
    def get_values(self):
        res = super(sale_payment_config_settings, self).get_values()
        res.update(
            product_delivery_id=int(self.env['ir.config_parameter'].sudo().get_param('product_delivery_id', )),
            collect_on_delivery_id=int(self.env['ir.config_parameter'].sudo().get_param('collect_on_delivery_id', )),
            product_mada_id=int(self.env['ir.config_parameter'].sudo().get_param('product_mada_id',)),
            mada_commission_percent=(self.env['ir.config_parameter'].sudo().get_param('mada_commission_percent', )),
            product_visa_id=int(self.env['ir.config_parameter'].sudo().get_param('product_visa_id', )),
            visa_commission_percent=(self.env['ir.config_parameter'].sudo().get_param('visa_commission_percent', )),
            product_return_id=int(self.env['ir.config_parameter'].sudo().get_param('product_return_id', ))
        )
        return res

    def set_values(self):
        super(sale_payment_config_settings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('product_delivery_id', self.product_delivery_id.id)
        self.env['ir.config_parameter'].sudo().set_param('collect_on_delivery_id', self.collect_on_delivery_id.id)
        self.env['ir.config_parameter'].sudo().set_param('product_mada_id', self.product_mada_id.id)
        self.env['ir.config_parameter'].sudo().set_param('mada_commission_percent', self.mada_commission_percent)
        self.env['ir.config_parameter'].sudo().set_param('product_visa_id', self.product_visa_id.id)
        self.env['ir.config_parameter'].sudo().set_param('visa_commission_percent', self.visa_commission_percent)
        self.env['ir.config_parameter'].sudo().set_param('product_return_id', self.product_return_id.id)

