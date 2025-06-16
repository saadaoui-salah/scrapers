#from data.models import Item
#import json
#from django.utils.timezone import now
#
#with open('2.json') as f:
#    data = json.load(f)
#
#
#for i, d in enumerate(data):
#    if not Item.objects.filter(site_id=d['site_id']): 
#        Item.objects.create(spider_id=2, site_id=d['site_id'], data=d, last_seen=now())
#        print(i)
#