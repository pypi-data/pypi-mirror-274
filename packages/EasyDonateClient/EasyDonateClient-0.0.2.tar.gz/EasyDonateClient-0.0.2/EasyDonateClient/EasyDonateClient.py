import requests # Импортируем requests
import json # Импортируем json
from quart import Quart, request, jsonify # Импортируем quart (Для CallBackApi)
class Client():
    def __init__(self, shop_key: str, version: int = 2, user_agent: str = 'EasyDonate, TinyWorld, TinyWorld/version', debug: bool = True):
        self.shop_key = shop_key
        self.version = version
        self.user_agent = user_agent
        self.debug = debug
        if (version not in [2, 3]):
            raise ValueError(version)
        match self.version:
            case 2:
                self.headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'User-Agent': self.user_agent
                }
            case 3:
                self.headers = {
                    'Shop-Key': self.shop_key
                }
        if self.debug == True:
            print(f"[DEBUG] EasyDonateApi Version {self.version}")
    def shop_info(self):
        match self.version:
            case 2:
                response = requests.get(f'https://easydonate.ru/api/v2/shop/{self.shop_key}', headers=self.headers)
                if self.debug == True:
                    print(f"[GET] Shop-Info ({response.status_code})")
                    match response.status_code:
                        case 400:
                            print("[GET] Status-Code: 400. Shop not found.")
                        case 200:
                            print("[GET] Status-Code: 200. Success.")
                return json.loads(response.content)
            case 3:
                response = requests.get(f'https://easydonate.ru/api/v3/shop', headers=self.headers)
                if self.debug == True:
                    print(f"[GET] Shop-Info ({response.status_code})")
                    match response.status_code:
                        case 404:
                            print("[GET] Status-Code: 404. Shop not found.")
                        case 200:
                            print("[GET] Status-Code: 200. Success.")
                return json.loads(response.content)
    def products(self):
        match self.version:
            case 2:
                response = requests.get(f'https://easydonate.ru/api/v2/shop/{self.shop_key}/products', headers=self.headers)
                if self.debug == True:
                    print(f"[GET] Products ({response.status_code})")
                    match response.status_code:
                        case 400:
                            print("[GET] Status-Code: 400. Shop not found / Unknown error.")
                        case 200:
                            print("[GET] Status-Code: 200. Success.")
                return json.loads(response.content)
            case 3:
                response = requests.get(f'https://easydonate.ru/api/v3/shop/products', headers=self.headers)
                if self.debug == True:
                    print(f"[GET] Products ({response.status_code})")
                    match response.status_code:
                        case 404:
                            print("[GET] Status-Code: 404. Shop not found.")
                        case 200:
                            print("[GET] Status-Code: 200. Success.")
                return json.loads(response.content)
    def product_info(self, id):
        match self.version:
            case 2:
                response = requests.get(f'https://easydonate.ru/api/v2/shop/{self.shop_key}/product/{id}', headers=self.headers)
                if self.debug == True:
                    print(f"[GET] Product-Info ({response.status_code})")
                    match response.status_code:
                        case 404:
                            print("[GET] Status-Code: 404. Product not found.")
                        case 200:
                            print("[GET] Status-Code: 200. Success.")
                return json.loads(response.content)
            case 3:
                response = requests.get(f'https://easydonate.ru/api/v3/shop/product/{id}', headers=self.headers)
                if self.debug == True:
                    print(f"[GET] Product-Info ({response.status_code})")
                    match response.status_code:
                        case 404:
                            print("[GET] Status-Code: 404. Product not found.")
                        case 200:
                            print("[GET] Status-Code: 200. Success.")
                return json.loads(response.content)
    def server_list(self):
        match self.version:
            case 2:
                response = requests.get(f'https://easydonate.ru/api/v2/shop/{self.shop_key}/servers', headers=self.headers)
                if self.debug == True:
                    print(f"[GET] Server-List ({response.status_code})")
                    match response.status_code:
                        case 404:
                            print("[GET] Status-Code: 404. Shop not found.")
                        case 200:
                            print("[GET] Status-Code: 200. Success.")
                return json.loads(response.content)
            case 3:
                response = requests.get(f'https://easydonate.ru/api/v3/shop/servers', headers=self.headers)
                if self.debug == True:
                    print(f"[GET] Server-List ({response.status_code})")
                    match response.status_code:
                        case 404:
                            print("[GET] Status-Code: 404. Shop not found.")
                        case 200:
                            print("[GET] Status-Code: 200. Success.")
                return json.loads(response.content)
    def server_info(self, id):
        match self.version:
            case 2:
                response = requests.get(f'https://easydonate.ru/api/v2/shop/{self.shop_key}/server/{id}', headers=self.headers)
                if self.debug == True:
                    print(f"[GET] Server-Info ({response.status_code})")
                    match response.status_code:
                        case 404:
                            print("[GET] Server-Info: 404. Server not found.")
                        case 200:
                            print("[GET] Server-Info: 200. Success.")
                return json.loads(response.content)
            case 3:
                response = requests.get(f'https://easydonate.ru/api/v3/shop/server/{id}', headers=self.headers)
                if self.debug == True:
                    print(f"[GET] Server-Info ({response.status_code})")
                    match response.status_code:
                        case 404:
                            print("[GET] Server-Info: 404. Server not found.")
                        case 200:
                            print("[GET] Server-Info: 200. Success.")
                return json.loads(response.content)
    def success_payments_list(self):
        match self.version:
            case 2:
                response = requests.get(f'https://easydonate.ru/api/v2/shop/{self.shop_key}/payments', headers=self.headers)
                if self.debug == True:
                    print(f"[GET] Payments-List ({response.status_code})")
                    match response.status_code:
                        case 404:
                            print("[GET] Payments-List: 404. Shop not found.")
                        case 200:
                            print("[GET] Payments-List: 200. Success.")
                return json.loads(response.content)
            case 3:
                response = requests.get(f'https://easydonate.ru/api/v3/shop/payments', headers=self.headers)
                if self.debug == True:
                    print(f"[GET] Payments-List ({response.status_code})")
                    match response.status_code:
                        case 404:
                            print("[GET] Payments-List: 404. Shop not found.")
                        case 200:
                            print("[GET] Payments-List: 200. Success.")
                return json.loads(response.content)
    def payment_info(self, id):
        match self.version:
            case 2:
                response = requests.get(f'https://easydonate.ru/api/v2/shop/{self.shop_key}/payment/{id}', headers=self.headers)
                if self.debug == True:
                    print(f"[GET] Payment-Info ({response.status_code})")
                    match response.status_code:
                        case 404:
                            print("[GET] Payment-Info: 404. Payment not found.")
                        case 200:
                            print("[GET] Payment-Info: 200. Success.")
                return json.loads(response.content)
            case 3:
                response = requests.get(f'https://easydonate.ru/api/v3/shop/payment/{id}', headers=self.headers)
                if self.debug == True:
                    print(f"[GET] Payment-Info ({response.status_code})")
                    match response.status_code:
                        case 404:
                            print("[GET] Payment-Info: 404. Payment not found.")
                        case 200:
                            print("[GET] Payment-Info: 200. Success.")
                return json.loads(response.content)
    def create_payment(self, customer : str, server_id: int, products: object, email: str = "None", coupon: str = "None", success_url: str = "None"):
        match self.version:
            case 2:
                if email != "None" or coupon != "None" or success_url != "None":
                    print("[WARNING] Email, Coupon, Success_url don't working in V2.")
                params = {
                    'customer': customer,
                    'server_id': str(server_id),
                    'products': products,
                }
                response = requests.get(f'https://easydonate.ru/api/v2/shop/{self.shop_key}/payment/create', headers=self.headers, params=params)

                if self.debug == True:
                    print(f"[GET] Payment-Create ({response.status_code})")
                    match response.status_code:
                        case 404:
                            print("[GET] Payment-Create: 404. Product not found.")
                        case 200:
                            print("[GET] Payment-Create: 200. Success.")

                return json.loads(response.content)
            case 3:
                path = f"https://easydonate.ru/api/v3/shop/payment/create?customer={customer}&server_id={server_id}&products={products}"
                if email != "None":
                    path = path + f"&email={email}"
                if coupon != "None":
                    path = path + f"&coupon={coupon}"
                if success_url != "None":
                    path = path + f"&coupon={coupon}"
                response = requests.get(path, headers=self.headers)
                if self.debug == True:
                    print(f"[GET] Payment-Create ({response.status_code})")
                    match response.status_code:
                        case 404:
                            print("[GET] Payment-Create: 404. Product not found.")
                        case 200:
                            print("[GET] Payment-Create: 200. Success.")
                return json.loads(response.content)
    def mass_sales(self, where_active: bool = "None"):
        if self.version == 2:
            print("[ERROR] Mass-Sales: Version 2 not supported")
            raise ValueError(2) 
        path = f"https://easydonate.ru/api/v3/shop/massSales"
        if where_active != "None":
            if where_active == False:
                path = path + "?where_active=false"
            else:
                path = path + "?where_active=true"
        response = requests.get(path, headers=self.headers)
        if self.debug == True:
            print(f"[GET] Mass-Sales ({response.status_code})")
            match response.status_code:
                case 404:
                    print("[GET] Mass-Sales: 404. Shop not found.")
                case 200:
                    print("[GET] Mass-Sales: 200. Success.")
        return json.loads(response.content)
    def coupon_list(self, where_active: bool = "None"):
        if self.version == 2:
            print("[ERROR] Coupon-List: Version 2 not supported")
            raise ValueError(2) 
        path = f"https://easydonate.ru/api/v3/shop/coupons"
        if where_active != "None":
            if where_active == False:
                path = path + "?where_active=false"
            else:
                path = path + "?where_active=true"
        response = requests.get(path, headers=self.headers)
        if self.debug == True:
            print(f"[GET] Coupon-List ({response.status_code})")
            match response.status_code:
                case 404:
                    print("[GET] Coupon-List: 404. Shop not found.")
                case 200:
                    print("[GET] Coupon-List: 200. Success.")
        return json.loads(response.content)
class CallBackAPI():
    def __init__(self, port=5000, debug=True):
        self.port = port
        self.on_payment_get_handler = None
        self.debug = debug
        self.app = Quart(__name__)
        self.app.add_url_rule('/payment', 'payment', self.handle_payment, methods=['POST'])
    def on_payment_get(self):
        def decorator(func):
            if self.on_payment_get_handler is not None:
                raise ValueError('on_payment_get_handler is already registered.')
            self.on_payment_get_handler = func
            return func
        return decorator
    async def handle_payment(self):
        data = await request.get_json()
        if self.on_payment_get_handler:
            await self.handle_event(data)
        return jsonify({"status": "success"}), 200
    async def handle_event(self, *args, **kwargs):
        if self.on_payment_get_handler:
            await self.on_payment_get_handler(*args, **kwargs)
        else:
            if self.debug == True:
                print("[DEBUG] No event handler registered for on_payment_get (CallBackApi)")
    async def run(self):
        import hypercorn.asyncio
        import hypercorn.config
        config = hypercorn.config.Config()
        config.bind = ["0.0.0.0:5000"]
        await hypercorn.asyncio.serve(self.app, config)

    
    