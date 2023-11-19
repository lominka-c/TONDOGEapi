import requests, hashlib, os

class API():
	def __init__(self, user_login, api_key):
		self.user_login = user_login
		self.api_key = api_key
	
	def get_api_signature(self, request, api_key):
	   sorted_keys = sorted(request)
	   elements = []
	   for k in sorted_keys:
	       v = request[k].strip()
	       if v != "" and k != "sign":
	       	elements.append(v)
	       	sign = ":".join(elements) + ":" + api_key
	   return hashlib.sha256(sign.encode()).hexdigest()
    
    
    
	def all_coins(self):
		url = 'https://cabot.pro/?show=api&act=allcoins'
		params = {
			"login": self.user_login,
		}
		params['sign'] = self.get_api_signature(params, self.api_key)
		r = requests.post(url, data=params)
		return r.json()
	
	def balance(self, coin=None):
		
		url="https://cabot.pro/?show=api&act=balans"
		params = {'login': self.user_login}
		params['sign'] = self.get_api_signature(params, self.api_key)
		r = requests.post(url, data=params)
		if coin is not None:
			r = r.json().get("balans")
			for i in r:
				if i['coin'] == coin:
					return i
		return r.json()
	
	def price(self, coin=None, amount=1):
		if coin is None: raise (TypeError("The name of the coin has not been transmitted"))
		n = self.all_coins().get("allcoins")
		result = 0
		for i in n:
			if coin == i["name"]:
				result = 1
		if result == 0: raise (KeyError(f"Coin '{coin}' is not in the list of coins"))
		url = "https://cabot.pro/?show=api&act=coin"
		params = {'login': self.user_login, "coin_name": coin}
		params['sign'] = self.get_api_signature(params, self.api_key)
		r = requests.post(url, data=params)
		r = r.json()
		p = r['coin']["rate"] * amount
		return p
	def send(self, to_id, coin, amount):
		
		url="https://cabot.pro/?show=api&act=transfer"
		params = {'login': self.user_login, "user2_id": to_id, "coin_name": coin, "amount": amount}
		params['sign'] = self.get_api_signature(params, self.api_key)
		r = requests.post(url, data=params)
		r = r.json()
		try:
			r = r.get("transfer").get("status")
		except:
			pass
		return r
	def getPayments(self, coin, amount):
		#raise (TypeError("Unknown Error"))
		url='https://cabot.pro/?show=api&act=getpayment'
		try:
			n = open(f"id{self.user_login}.txt", "r")
			u = n.readline()
			n.close()
		except:
			n = open(f"id{self.user_login}.txt", "w")
			n.write("1")
			n.close()
			n = open(f"id{self.user_login}.txt", "r")
			u = n.readline()
			n.close()
		
		params = {
    'login': self.user_login,
    'coin_name': coin,
    'amount': str(amount),
    'order_id': str(u),
    'product_name': 'SuperTop',
    'success_url': 'https://t.me/sun_company_bot',
    'failed_url': 'https://mysite.com/payment-failed',
    'notification_url': 'https://mysite.com/payment-notification'
}
		params['sign'] = self.get_api_signature(params, self.api_key)
		r = requests.post(url, data=params)
		n = open(f"id{self.user_login}.txt", "w")
		o = u
		n.write(str(int(u) + 1))
		n.close()
		return r.json()
		