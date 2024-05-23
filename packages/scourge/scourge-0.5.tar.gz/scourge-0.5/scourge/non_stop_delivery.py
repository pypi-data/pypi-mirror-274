from deceit.exceptions import ApiException
from deceit.api_client import ApiClient


class NonStopDeliveryException(ApiException):
    pass


class NonStopDeliveryApi(ApiClient):
    def __init__(self, username=None, password=None):
        super().__init__(
            base_url='https://portal2.hubgroup.com/final-mile',
            exception_class=NonStopDeliveryException)
        self.username = username
        self.password = password
        self.logged_in = False

    def login(self):
        route = 'inc/tm_ajax.msw'
        data = {
            'tm4web_usr': self.username,
            'tm4web_pwd': self.password,
            'remember_password': '1',
            'func': 'SubmitLogin',
        }
        self.log.debug('[nsd] logging in as %s', self.username)
        response = self.post(route, form_data=data, raw=True)
        self.log.debug('[nsd] status code: %s', response.status_code)
        self.logged_in = True

    def is_logged_in(self):
        route = 'inc/tm_ajax.msw?func=isLoggedIn'
        try:
            response = self.get(route)
            return response['MESSAGE'] == 'logged in'
        except (NonStopDeliveryException, KeyError):
            return False

    def get_order_page(self, start_date, end_date=None, page=0, limit=30):
        route = 'trace/trace_class.msw'
        params = {
            'take': f'{limit}',
            'skip': f'{limit * (page - 1)}',
            'page': f'{page}',
            'pageSize': f'{limit}',
            'sort[0][field]': 'BILL_NUMBER',
            'sort[0][dir]': 'asc',
            'sort[1][field]': '',
            'sort[1][dir]': 'asc',
            'include_all_clients': 'false',
            'trace_type': '',
            'search_style': 'starts_with',
            'trace_number': '',
            'TLORDER__DESTNAME_input': '',
            'TLORDER__DESTNAME': '',
            'from_TLORDER__CREATED_TIME': start_date.strftime('%Y-%m-%d'),
            'to_TLORDER__CREATED_TIME':
                '' if not end_date else end_date.strftime('%Y-%m-%d'),
            'TLORDER__CURRENT_STATUS_input': '',
            'TLORDER__CURRENT_STATUS': '',
        }
        self.log.debug('[nsd] page %s of orders from %s', page, start_date)
        return self.get(route, params=params)

    def yield_orders(self, start_date, end_date=None, limit=30):
        n_yielded = 0
        page = 0
        n_total = None
        while n_total is None or n_yielded < n_total:
            page += 1
            result = self.get_order_page(start_date, end_date, page, limit)
            if n_total is None:
                n_total = int(result['totalCount'])
            orders = result['dataResults']
            for order in orders:
                n_yielded += 1
                yield order

    def get_orders(self, start_date, end_date=None, limit=30):
        """
        an order looks like the following:
        {
          "DETAIL_LINE_ID": "1234567",
          "BILL_NUMBER": "12345678",
          "TRACE_TYPE_P": "1234567890",
          "SERVICE_LEVEL": "SOME_SERVICE_LEVEL
          "CURRENT_STATUS": "SOME_STATUS
          "DESTNAME": "DESTINATION",
          "PIECES": "1",
          "WEIGHT": "1.0",
          "CARE_OF_ADDR1": "1234 MAIN ST",
          "CARE_OF_CITY": "OKLAHOMA CITY",
          "CARE_OF_PROV": "OK",
          "CARE_OF_PC": "73129",
          "CREATED_TIME": "2024-01-01 00:00:00.000000",
          "DELIVER_BY": "2024-01-31 00:00:00.000000",
          "DELIVER_BY_END": "2024-01-31 11:59:00.000000",
          "IM_LOADED": "1234567
          "IM_TYPE": "",
          "INTERMODAL": []
        }
        """
        # import json
        rg = list(self.yield_orders(start_date, end_date, limit))
        # order = rg[0]
        # self.log.info('%s', json.dumps(order, indent=2))
        for x in rg:
            x['BILL_NUMBER'] = x['BILL_NUMBER'].strip()
            x['TRACE_TYPE_P'] = x['TRACE_TYPE_P'].strip()
        return rg

    def get_detail(self, detail_line_id):
        """
        detail will look like:
        {
            "TLORDER": {
                "PICK_UP_BY": "2024-01-01 00:00:00.000000",
                "PICK_UP_BY_END": "2024-01-31 00:00:00.000000",
                "DELIVER_BY": "2024-02-25 10:00:00.000000",
                "DELIVER_BY_END": "2024-02-25 14:00:00.000000",
                "DETAIL_LINE_ID": "1234567",
                "BILL_NUMBER": "1234567",
                "CREATED_BY": "12345",
                "CREATED_TIME": "2024-01-01 00:00:00.000000",
                "CALLNAME": "COMPANY",
                "CALLADDR1": "1234 MAIN STREET",
                "CALLADDR2": "",
                "CALLCITY": "OKLAHOMA CITY",
                "CALLPROV": "OK",
                "CALLCOUNTRY": "US",
                "CALLPC": "74239",
                "CALLPHONE": "8005551212",
                "CALLFAX": "",
                "CALLCONTACT": "12345",
                "ORIGNAME": "COMPANY",
                "ORIGADDR1": "1234 MAIN STREET",
                "ORIGADDR2": "",
                "ORIGCITY": "OKLAHOMA CITY",
                "ORIGPROV": "OK",
                "ORIGCOUNTRY": "US",
                "ORIGPC": "74239",
                "ORIGPHONE": "8005551212",
                "ORIGFAX": "",
                "ORIGCONTACT": "",
                "DESTNAME": "CUSTOMER FRIEND",
                "DESTADDR1": "4567 MAIN STREET.",
                "DESTADDR2": "",
                "DESTCITY": "SPRING",
                "DESTPROV": "TX",
                "DESTCOUNTRY": "  ",
                "DESTPC": "77388",
                "DESTPHONE": "2815551212",
                "DESTFAX": "",
                "DESTCONTACT": "",
                "DELIVERY_APPT_MADE": "True ",
                "PICK_UP_APPT_MADE": "False",
                "ORIG_zone_desc": "",
                "DEST_zone_desc": "",
                "PICKUP_AT_zone_desc": ""
            },
            "TLDTL": [
                {
                    "SEQUENCE": "12345678",
                    "ORDER_ID": "1234567",
                    "DESCRIPTION": "THE PRODUCT YOU ORDERED",
                    "WEIGHT": "1.0",
                    "WEIGHT_UNITS": "LB",
                    "PIECES": "1",
                    "PIECES_UNITS": "CTN",
                    "HEIGHT": "0.00000000000000E+000",
                    "WIDTH": "0.00000000000000E+000",
                    "LENGTH_1": "0.00000000000000E+000"
                }
            ],
            "ODRSTAT": [
                {
                    "ORDER_ID": "1234567",
                    "OS_LEG_ID": "",
                    "OS_STATUS_CODE": "DELIVERED",
                    "S_SHORT_DESCRIPTION": "DELIVERED",
                    "OS_SF_REASON_CODE": "",
                    "OS_INS_DATE": "2024-01-25 11:00:00.000000",
                    "OS_CHANGED": "2024-01-25 10:24:00.000000"
                }, ...
            ],
            "TRACE": [
                {
                    "TRACE_TYPE": "P",
                    "TRACE_NUMBER": "123456789",
                    "DESC": "PO #"
                }
            ]
        }
        """
        route = 'trace/bill_details_ajax.msw'
        params = [
            ('func', 'BillDetails',),
            ('dld', detail_line_id,),
        ]
        result = self.get(route, params=params)
        if isinstance(result, dict):
            value = result['TLORDER']['BILL_NUMBER']
            result['TLORDER']['BILL_NUMBER'] = value.strip()
        return result

    def get_images(self, detail_line_id):
        """
        returns an array of dictionaries that look like the following:
        [{
            "DOC_ID": "12345",
            "MICRODEA_DOCID": "Doc12345678",
            "DOCUMENT_TYPE": "document_type",
            "DOC_EXT": "tif",
            "DOC_SIZE": "1234567",
            "MENU_LABEL": "Proof of Delivery"
        }, ...]
        """
        route = 'imaging/imaging.ajax.msw'
        params = {
            'func': 'GetImageList',
            'source': 'trace',
            'source_id': detail_line_id,
            'isViewImagesDLG': 'false',
        }
        return self.get(route, params=params)

    def get_image(self, detail_line_id, image, raw=False):
        """
        returns the bytes of the image, typically as a pdf
        """
        image_id = image['MICRODEA_DOCID']
        route = f'imaging/imaging.ajax.msw/{image_id}'
        params = {
            'func': 'GetImage',
            'source': 'trace',
            'source_id': detail_line_id,
            'image_id': image_id,
            'doc_id': image['DOC_ID'],
            'DOC_SIZE': image['DOC_SIZE'],
            'DOC_EXT': image['DOC_EXT'],
            'MENU_LABEL': image['MENU_LABEL'],
        }
        response = self.get(route, params=params, raw=True)
        if raw:
            return response
        return response.content
