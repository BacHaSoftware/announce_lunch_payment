from urllib.parse import urlencode
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class BHSLunchCronMail(models.Model):
    _inherit = 'lunch.order'

    @api.model
    def send_email_announce_lunch_payment(self, user_ids=[], start_date=None, end_date=None):
        orders = self._get_lunch_orders(user_ids, start_date, end_date)
        user_orders = self._get_dict_user_orders(orders)

        settings = self.env['res.config.settings'].get_values()
        url = {
            'bank_code': settings.get('bank_code', ''),
            'account_number': settings.get('account_number', ''),
            'print': settings.get('print_format', ''),
            'accountName': settings.get('account_name', '')
        }

        for user_id, data in user_orders.items():
            order = {
                'user_name': user_id.name,
                'total_price': data['total_price'],
                'email': user_id.email,
                'lang': user_id.lang,
                'start_date': start_date,
                'end_date': end_date
            }
            email_orders = [{
                'product': item,
                'price': data['order_lines_price'][index],
                'quantity': data['quantity'][index],
                'date': data['date_order_lines'][index],

            } for index, item in enumerate(data['order_lines'])]

            url['amount'] = data['total_price']
            url['addInfo'] = f"{order.get('user_name')} thanh toan tien an trua"
            dynamic_url = "https://img.vietqr.io/image/{}?{}".format(url['bank_code'] + '-' + url['account_number'] + '-' + url['print'], urlencode(url))

            # send mail
            self.env.ref('bhs_announce_lunch_payment.email_template_bhs_lunch_cron').with_context(
                order=order, email_orders=email_orders, dynamic_url=dynamic_url).send_mail(self.id, force_send=True)

    @api.model
    def _get_lunch_orders(self, user_ids, start_date, end_date):
        domain = [('state', '!=', 'cancelled')]
        if user_ids:
            domain.append(('user_id', 'in', user_ids))

        if (start_date or end_date) and not (start_date and end_date):
            raise UserError(_("Please input both start_date and end_date or leave both parameters blank."))
        if start_date and end_date:
            domain.extend([
                ('date', '>=', start_date),
                ('date', '<=', end_date)
            ])
        else:
            # if not start_date and end_date:
            # start_date = first day of previous month
            # end_date = last day of previous month
            end_date = fields.Date.today().replace(day=1) - relativedelta(days=1)
            start_date = end_date.replace(day=1)
            domain.extend([
                ('date', '>=', start_date),
                ('date', '<=', end_date)
            ])
        orders = self.env['lunch.order'].search(domain)
        return orders

    def _get_dict_user_orders(self, orders):
        user_orders = {}

        for order in orders:
            if order.user_id in user_orders:
                user_orders[order.user_id]['total_price'] += order.price
                user_orders[order.user_id]['order_lines'].append(order.product_id.name)
                user_orders[order.user_id]['order_lines_price'].append(order.price)
                user_orders[order.user_id]['date_order_lines'].append(order.date)
                user_orders[order.user_id]['quantity'].append(order.quantity)
            else:
                user_orders[order.user_id] = {
                    'total_price': order.price,
                    'order_lines': [order.product_id.name],
                    'order_lines_price': [order.price],
                    'date_order_lines': [order.date],
                    'quantity': [order.quantity]
                }

        return user_orders
