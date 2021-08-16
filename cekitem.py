import json
import re
import requests

h = {
        'Host': 'mall.shopee.co.id',
        'user-agent': 'Android app Shopee appver=26308 app_type=1',
        'x-api-source': 'rn',
        'accept': 'application/json',
        'x-shopee-language': 'id',
        'if-none-match-': '55b03-4f8abf870572e2887118fb97f99b463b',
        'content-type': 'application/json',
        'origin': 'https://mall.shopee.co.id',
        'referer': 'https://mall.shopee.co.id/checkout',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,id;q=0.8',
        
        }

print('-' * 50)
link = input('Input Link: ')
print('-' * 50)
if '/product/' in link:
    if '?' in link:
        shopid = re.findall('product/(.*?)/', link)[0]
        itemid = re.findall(shopid + '/(.*?)\?', link)[0]
    else:
        shopid = re.findall('product/(.*?)/', link)[0]
        itemid = re.findall(shopid + '/(.*)', link)[0].replace('/', '')
else:
    shopid = re.findall('-i\.(.*?)\.', link)[0]
    itemid = re.findall(shopid + '\.(.*)', link)[0]

r = requests.get('https://shopee.co.id/api/v2/item/get?itemid=' + itemid + '&shopid=' + shopid, headers=h)
name = json.loads(r.text).get('item').get('name')
if '"modelid"' in r.text:
    models = json.loads(r.text).get('item').get('models')
    if '"modelids":[' in r.text:
        modelids = json.loads(r.text).get('item').get('upcoming_flash_sale').get('modelids')
        print('Ditemukan ' + str(len(modelids)) + ' dari total ' + str(len(models)) + ' varian flash sale:')
        i = 0
        while i <= (len(models) - 1):
            name = json.loads(r.text).get('item').get('models')[i].get('name')
            price = json.loads(r.text).get('item').get('models')[i].get('price')
            modelid = json.loads(r.text).get('item').get('models')[i].get('modelid')
            if modelid in modelids:
                print(str(name) + ' - Rp{:0,.0f}'.format(int(price / 100000)) + ' - ' + str(modelid))
            i += 1
    else:
        print('Produk ini mempunyai ' + str(len(models)) + ' varian:')
        i = 0
        while i <= (len(models) - 1):
            name = json.loads(r.text).get('item').get('models')[i].get('name')
            price = json.loads(r.text).get('item').get('models')[i].get('price')
            modelid = json.loads(r.text).get('item').get('models')[i].get('modelid')
            print(str(name) + ' - Rp{:0,.0f}'.format(int(price / 100000)) + ' - ' + str(modelid))
            i += 1
    print('-' * 50)