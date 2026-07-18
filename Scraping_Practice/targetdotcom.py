import requests
import json
import pandas as pd
import targetdotcomhelper
cookies = {
    'x-digital-context': 'eNpFkF1LwzAYhf9KeK82KG262q95tQ-rsA1FHRNESuyyGZomocnmpvjffVtFyVWenJPDOZ9g9aGtOIzBsXbPnV_pBjyo3phSXCLeXE3xzowpj7y1QitkoU99inTLj6L3brmtnTaIhCqt0y3CHZOWe6BtuWONkGeULYU6nKBn_5-tVa30u0J8FFagtxRbxDTMi5TO85gWOR1RmiXZJKJXRTadTdKEFqg_WN6WbM-VQ_1KfwgpWRD7lAyewvCS9GnklCVlcjEkE2Mk3_DXhXBBHKV-lJDB4uZxtfSIFDUn17yq9ZDM3lrd8CCMqd8f8sB2rBW_Fgw1GAjjT5zrpJVuulqmxy1ruMNWMH6GPB6FNIsiePHAnU030d397Xw9e-wm6uoFJvgTfXnQnH9m67uP0iT14EOYstJb9MYJpYkHkmHPcOTn-Ci12sM4Tf009sA65rqIxQS-vgFzN4ph',
    'accessToken': 'eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI5ZTg3ZjliZS1mY2Q2LTQ0ZGYtYWI5Zi1hYWVjMjg0YmIxZWIiLCJpc3MiOiJNSTYiLCJleHAiOjE3ODQzOTExMTgsImlhdCI6MTc4NDMwNDcxOCwianRpIjoiVEdULjNjZDk5OTk1YmM5NDRhNDQ5YmQ3YTFmZTQ2MjNiOTFlLWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6IjA1ZTdmMWZjZjdhZDA4MTY0ZTg5MjUwYjA5ZmUyY2I5MTg4ZTE4YjhkMWQyMThiYjJhOTZmMjkyODQzMjQ0Y2MiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.iqEP_r3a4m-fc7d9QPGO87Mbd0vU2ZI8uH-FYt-_ZB3XTJQJW7BIh_H4v3U17k_wOd_q2CPXoz5wZm4a50rgNjMqzc7V55JbETC0GFJYKEoHqwriC3nPsAA-Pm1VbL-au6GVED0sjtlvuMn4ZQwPv2fXjO2xEB-_KVaIWtKoc37r3SEALbobSt2g-Ed318sTMwjBxbPXvqFbMbO6Wu2ZKz0sSfBzEQqQxg42ckU2vOkhwhxKIq5akl6iMNMQg6IRjARurZ6gG_3oUei2U0s2IMVIsPc8MBB2U3b5eos--_4_49z3gHSFi7p53_SqCDsr4rFYlc5L_6WfAH4RmeF-Rw',
    'refreshToken': 'rofrwl8ou-H_PG18SDea3cVZRQZlAaCZh6ntcRSrVX9hOBrc6il4HsNW929Pqo3eACo_jGql-4Ij_zhsuh9ckg',
    'adScriptData': 'KA',
    'TealeafAkaSid': '7XMrEgQb0c0YFHP_k86XRBqgCIG2BufC',
    'sapphire': '1',
    'onboardingGuest': 'timestamp=1784304718725',
    'visitorId': '019F70D950F90200868A30EF8BCA760F',
    'idToken': 'eyJhbGciOiJub25lIn0.eyJzdWIiOiI5ZTg3ZjliZS1mY2Q2LTQ0ZGYtYWI5Zi1hYWVjMjg0YmIxZWIiLCJpc3MiOiJNSTYiLCJleHAiOjE3ODQzOTExMTgsImlhdCI6MTc4NDMwNDcxOCwiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZm51IjpudWxsLCJlbSI6bnVsbCwicGgiOmZhbHNlLCJsZWQiOm51bGwsImx0eSI6ZmFsc2UsInN0IjoiS0EiLCJzbiI6bnVsbH19.',
    'egsSessionId': '9a010d66-9402-45dc-91da-dc7fc3e4732b',
    'UserLocation': '56006|12.970|77.750|KA|IN',
    'ffsession': '{%22sessionHash%22:%221ab81ac3cf21d81784304720187%22}',
    '_pxvid': '3d93a805-81fa-11f1-9cda-c203e7f0051f',
    'AMCVS_99DD1CFE5329660B0A490D45%40AdobeOrg': '1',
    'AMCV_99DD1CFE5329660B0A490D45%40AdobeOrg': '179643557%7CMCIDTS%7C20652%7CMCMID%7C84286559077801175921856730194531091717%7CMCAAMLH-1784909521%7C12%7CMCAAMB-1784909521%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1784311921s%7CNONE%7CvVersion%7C5.5.0',
    'fiatsCookie': 'DSI_2767|DSN_Oakland-Emeryville|DSZ_94608',
    '__attentive_id': '6d4ab70d719142bdae0f9f12071dffda',
    '__attentive_session_id': '403f0fd37ad34d8381488058d4a3cd03',
    '_attn_': 'eyJ1Ijoie1wiY29cIjoxNzg0MzA0NzIxNzQ1LFwidW9cIjoxNzg0MzA0NzIxNzQ1LFwibWFcIjoyMTkwMCxcImluXCI6ZmFsc2UsXCJ2YWxcIjpcIjZkNGFiNzBkNzE5MTQyYmRhZTBmOWYxMjA3MWRmZmRhXCJ9In0=',
    '__attentive_cco': '1784304721747',
    '__attentive_ss_referrer': 'ORGANIC',
    '__attentive_dv': '1',
    '_fs_dwell_passed': '305fda23-f075-4c2c-9a8a-ef010e0f1077',
    '__gads': 'ID=a17f2409c431e40d:T=1784304721:RT=1784305025:S=ALNI_MYLqRV_ua6YdKscw88pNz-s-LxwlA',
    '__gpi': 'UID=000014c59aef247c:T=1784304721:RT=1784305025:S=ALNI_MbnQosej1iR2jgwC9TqbEqHYuZZsw',
    '__eoi': 'ID=ac0056b1c132620f:T=1784304721:RT=1784305025:S=AA-AfjYXUH_E_88l7hymSh8g0Hbq',
    'fs_lua': '1.1784305311554',
    'fs_uid': '#o-221JN4-na1#25427057-a4dd-4cd2-8078-8f581804d34e:305fda23-f075-4c2c-9a8a-ef010e0f1077:1784304721872::6####/1815840733',
    '__attentive_pv': '23',
    '_px3': '39e2ec2a3eb9f980ead1df1563f0ac61153d5034490e452000cf16a220d161f7:9oY4A5O6/z2W311J7L+EW3dd7G406WEBCC7nUn3Y/DUEE14Q7HpVnBCDezXMLBZCbYYNUU1e4N/VdLUMWpKdbw==:1000:qapWFIuxJHvLH61o9zaAZdILNz1Ew3DBPtzCqYSFbXOEaDzfeGA1FbuSP3rtq1vunruXnJ19HCqWLPyfhRxf2blUyFtpcXoy4VH/d7RasQjEmoSHBzEql91mfASOrACklcUiiQStiaHZ99cjBxUObGiS4doLGxATUhZ8v4kAPNpwjfZVxl0NDRNRc7cVxmLQLuhNvlfJt8XQHLTAiPDdJ3phXn+bkzjEmW8ziVj3J6NySRDP7u/jJQwy7YASKzQEhTxV8IPzc30gBctzoLuKe26L0TxM155i2l/oHqmSWnao6JAd5TPCqNcWIwvoMdDrZUIaf0RAUqOLhdgBK1ApwzkShPQdgHdzMPye8KicJfKAm8vDa3gYd9bD2OphQ9Ydld7n3WWwwgHat6zNr2B1MkVN9Ybc4ngUgbx8O99ic1QATQ05MoTqnymywEhvyQjWJQsDYKDaQ0lChSeGywx076tcfqoQMTk1hQUZG68ebMs=',
    '_px2': 'eyJ1IjoiOWJhM2JlNTAtODFmYi0xMWYxLTkzNjYtMzU1ZDU4YTYxMjljIiwidiI6IjNkOTNhODA1LTgxZmEtMTFmMS05Y2RhLWMyMDNlN2YwMDUxZiIsInQiOjE3ODQzMDU2MzM0NzYsImgiOiIxNjk3NzczZWU2OWEyMmI0YWI1YTE0NzhiZmE0OWM0ZjE3MjhlNjY0MTJiZmQ2ZjBkY2FmMjE0YmI3OTRjOTBhIn0=',
    'pxcts': 'h71pFDSd0o2jPnI-nprEkjdEJsg1JONDUJkuOycPk1A=:KxptKesnKi1X5iZPWhWYFqhkqAkMV1iTE4fr8qb-ynY3OptdWShWtnm3C8FFFSb/1RLLfCwjJ9FNgPWQatMgdm1vhaJnREsRPmDk2pqSgPB0wfIXA51owo4ZhOqxQzV-Tlul1g2qaXuBG/er1e7hlllrMpRlJTx6Z8KJSdea5YfVOoJUqi0oODjSbrX/WzxJ',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7,te;q=0.6',
    'dnt': '1',
    'origin': 'https://www.target.com',
    'priority': 'u=1, i',
    'referer': 'https://www.target.com/p/women-s-tie-front-midi-dress-a-new-day/-/A-95210833?preselect=95193995',
    'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
    # 'cookie': 'x-digital-context=eNpFkF1LwzAYhf9KeK82KG262q95tQ-rsA1FHRNESuyyGZomocnmpvjffVtFyVWenJPDOZ9g9aGtOIzBsXbPnV_pBjyo3phSXCLeXE3xzowpj7y1QitkoU99inTLj6L3brmtnTaIhCqt0y3CHZOWe6BtuWONkGeULYU6nKBn_5-tVa30u0J8FFagtxRbxDTMi5TO85gWOR1RmiXZJKJXRTadTdKEFqg_WN6WbM-VQ_1KfwgpWRD7lAyewvCS9GnklCVlcjEkE2Mk3_DXhXBBHKV-lJDB4uZxtfSIFDUn17yq9ZDM3lrd8CCMqd8f8sB2rBW_Fgw1GAjjT5zrpJVuulqmxy1ruMNWMH6GPB6FNIsiePHAnU030d397Xw9e-wm6uoFJvgTfXnQnH9m67uP0iT14EOYstJb9MYJpYkHkmHPcOTn-Ci12sM4Tf009sA65rqIxQS-vgFzN4ph; accessToken=eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI5ZTg3ZjliZS1mY2Q2LTQ0ZGYtYWI5Zi1hYWVjMjg0YmIxZWIiLCJpc3MiOiJNSTYiLCJleHAiOjE3ODQzOTExMTgsImlhdCI6MTc4NDMwNDcxOCwianRpIjoiVEdULjNjZDk5OTk1YmM5NDRhNDQ5YmQ3YTFmZTQ2MjNiOTFlLWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6IjA1ZTdmMWZjZjdhZDA4MTY0ZTg5MjUwYjA5ZmUyY2I5MTg4ZTE4YjhkMWQyMThiYjJhOTZmMjkyODQzMjQ0Y2MiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.iqEP_r3a4m-fc7d9QPGO87Mbd0vU2ZI8uH-FYt-_ZB3XTJQJW7BIh_H4v3U17k_wOd_q2CPXoz5wZm4a50rgNjMqzc7V55JbETC0GFJYKEoHqwriC3nPsAA-Pm1VbL-au6GVED0sjtlvuMn4ZQwPv2fXjO2xEB-_KVaIWtKoc37r3SEALbobSt2g-Ed318sTMwjBxbPXvqFbMbO6Wu2ZKz0sSfBzEQqQxg42ckU2vOkhwhxKIq5akl6iMNMQg6IRjARurZ6gG_3oUei2U0s2IMVIsPc8MBB2U3b5eos--_4_49z3gHSFi7p53_SqCDsr4rFYlc5L_6WfAH4RmeF-Rw; refreshToken=rofrwl8ou-H_PG18SDea3cVZRQZlAaCZh6ntcRSrVX9hOBrc6il4HsNW929Pqo3eACo_jGql-4Ij_zhsuh9ckg; adScriptData=KA; TealeafAkaSid=7XMrEgQb0c0YFHP_k86XRBqgCIG2BufC; sapphire=1; onboardingGuest=timestamp=1784304718725; visitorId=019F70D950F90200868A30EF8BCA760F; idToken=eyJhbGciOiJub25lIn0.eyJzdWIiOiI5ZTg3ZjliZS1mY2Q2LTQ0ZGYtYWI5Zi1hYWVjMjg0YmIxZWIiLCJpc3MiOiJNSTYiLCJleHAiOjE3ODQzOTExMTgsImlhdCI6MTc4NDMwNDcxOCwiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZm51IjpudWxsLCJlbSI6bnVsbCwicGgiOmZhbHNlLCJsZWQiOm51bGwsImx0eSI6ZmFsc2UsInN0IjoiS0EiLCJzbiI6bnVsbH19.; egsSessionId=9a010d66-9402-45dc-91da-dc7fc3e4732b; UserLocation=56006|12.970|77.750|KA|IN; ffsession={%22sessionHash%22:%221ab81ac3cf21d81784304720187%22}; _pxvid=3d93a805-81fa-11f1-9cda-c203e7f0051f; AMCVS_99DD1CFE5329660B0A490D45%40AdobeOrg=1; AMCV_99DD1CFE5329660B0A490D45%40AdobeOrg=179643557%7CMCIDTS%7C20652%7CMCMID%7C84286559077801175921856730194531091717%7CMCAAMLH-1784909521%7C12%7CMCAAMB-1784909521%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1784311921s%7CNONE%7CvVersion%7C5.5.0; fiatsCookie=DSI_2767|DSN_Oakland-Emeryville|DSZ_94608; __attentive_id=6d4ab70d719142bdae0f9f12071dffda; __attentive_session_id=403f0fd37ad34d8381488058d4a3cd03; _attn_=eyJ1Ijoie1wiY29cIjoxNzg0MzA0NzIxNzQ1LFwidW9cIjoxNzg0MzA0NzIxNzQ1LFwibWFcIjoyMTkwMCxcImluXCI6ZmFsc2UsXCJ2YWxcIjpcIjZkNGFiNzBkNzE5MTQyYmRhZTBmOWYxMjA3MWRmZmRhXCJ9In0=; __attentive_cco=1784304721747; __attentive_ss_referrer=ORGANIC; __attentive_dv=1; _fs_dwell_passed=305fda23-f075-4c2c-9a8a-ef010e0f1077; __gads=ID=a17f2409c431e40d:T=1784304721:RT=1784305025:S=ALNI_MYLqRV_ua6YdKscw88pNz-s-LxwlA; __gpi=UID=000014c59aef247c:T=1784304721:RT=1784305025:S=ALNI_MbnQosej1iR2jgwC9TqbEqHYuZZsw; __eoi=ID=ac0056b1c132620f:T=1784304721:RT=1784305025:S=AA-AfjYXUH_E_88l7hymSh8g0Hbq; fs_lua=1.1784305311554; fs_uid=#o-221JN4-na1#25427057-a4dd-4cd2-8078-8f581804d34e:305fda23-f075-4c2c-9a8a-ef010e0f1077:1784304721872::6####/1815840733; __attentive_pv=23; _px3=39e2ec2a3eb9f980ead1df1563f0ac61153d5034490e452000cf16a220d161f7:9oY4A5O6/z2W311J7L+EW3dd7G406WEBCC7nUn3Y/DUEE14Q7HpVnBCDezXMLBZCbYYNUU1e4N/VdLUMWpKdbw==:1000:qapWFIuxJHvLH61o9zaAZdILNz1Ew3DBPtzCqYSFbXOEaDzfeGA1FbuSP3rtq1vunruXnJ19HCqWLPyfhRxf2blUyFtpcXoy4VH/d7RasQjEmoSHBzEql91mfASOrACklcUiiQStiaHZ99cjBxUObGiS4doLGxATUhZ8v4kAPNpwjfZVxl0NDRNRc7cVxmLQLuhNvlfJt8XQHLTAiPDdJ3phXn+bkzjEmW8ziVj3J6NySRDP7u/jJQwy7YASKzQEhTxV8IPzc30gBctzoLuKe26L0TxM155i2l/oHqmSWnao6JAd5TPCqNcWIwvoMdDrZUIaf0RAUqOLhdgBK1ApwzkShPQdgHdzMPye8KicJfKAm8vDa3gYd9bD2OphQ9Ydld7n3WWwwgHat6zNr2B1MkVN9Ybc4ngUgbx8O99ic1QATQ05MoTqnymywEhvyQjWJQsDYKDaQ0lChSeGywx076tcfqoQMTk1hQUZG68ebMs=; _px2=eyJ1IjoiOWJhM2JlNTAtODFmYi0xMWYxLTkzNjYtMzU1ZDU4YTYxMjljIiwidiI6IjNkOTNhODA1LTgxZmEtMTFmMS05Y2RhLWMyMDNlN2YwMDUxZiIsInQiOjE3ODQzMDU2MzM0NzYsImgiOiIxNjk3NzczZWU2OWEyMmI0YWI1YTE0NzhiZmE0OWM0ZjE3MjhlNjY0MTJiZmQ2ZjBkY2FmMjE0YmI3OTRjOTBhIn0=; pxcts=h71pFDSd0o2jPnI-nprEkjdEJsg1JONDUJkuOycPk1A=:KxptKesnKi1X5iZPWhWYFqhkqAkMV1iTE4fr8qb-ynY3OptdWShWtnm3C8FFFSb/1RLLfCwjJ9FNgPWQatMgdm1vhaJnREsRPmDk2pqSgPB0wfIXA51owo4ZhOqxQzV-Tlul1g2qaXuBG/er1e7hlllrMpRlJTx6Z8KJSdea5YfVOoJUqi0oODjSbrX/WzxJ',
}

params = {
    'key': '9f36aeafbe60771e321a7cc95a78140772ab3e96',
    'platform': 'WEB',
    'sapphire_channel': 'WEB',
    'sapphire_page': '/p/A-95210833',#f'/p/A-{tcin}'
    'visitor_id': '019F70D950F90200868A30EF8BCA760F',
    'tcin': '95193995',
    'is_seo_bot': 'false',
    'include_data_source_modules': 'true',
}

response = requests.get(
    'https://cdui-orchestrations.target.com/cdui_orchestrations/v1/pages/pdp',
    params=params,
    cookies=cookies,
    headers=headers,
)
product_titles_map = {}
product_price_map = {}
product_variants_result=[] 
if response.status_code == 200:
    json_response = response.json()
    zones = json_response.get('layout',{}).get('zones',[])
    product_titles_map = {}
    if zones:
        zone = targetdotcomhelper.get_zone(zones=zones,zone_id='ProductDetailAboveTheFoldRight')
        if zone:
            module_group = targetdotcomhelper.get_module_group(zone=zone,module_group_id='ProductDetailAboveTheFoldRight')
            if module_group:
                module = targetdotcomhelper.get_module(module_group=module_group,module_type='ProductDetailTitle')
                if module:
                    product_titles_map = targetdotcomhelper.get_product_titles(module=module)
    
    if product_titles_map:           
        data_source_modules = json_response.get('data_source_modules')
        product_detail_web_datasource_with_store = []
        product_detail_web_datasourcefulfillment_and_variations=[]
        if data_source_modules:
            module_web_store = targetdotcomhelper.get_data_source_module(data_source_modules=data_source_modules,module_type='ProductDetailWebDatasourceWithStore')
            module_with_variants = targetdotcomhelper.get_data_source_module(data_source_modules=data_source_modules,module_type='ProductDetailWebDatasourceFulfillmentAndVariations')
            if module_web_store:
                product_detail_web_datasource_with_store = module_web_store.get('module_data',{}).get('data',{}).get('product',{}).get('children',[])
                product_price_map =  targetdotcomhelper.get_product_prices(product_detail_web_datasource_with_store)
            if module_with_variants:
                product_detail_web_datasourcefulfillment_and_variations = module_with_variants.get('module_data',{}).get('data',{}).get('product',{}).get('variation_hierarchy',[])
                product_variants_result=targetdotcomhelper.get_final_product_set(product_detail_web_datasourcefulfillment_and_variations=product_detail_web_datasourcefulfillment_and_variations,product_titles_map=product_titles_map,product_price_map=product_price_map)
                
print(len(product_titles_map))
print(len(product_price_map))
print(len(product_variants_result))
df = pd.DataFrame(product_variants_result)
df.to_csv('product_variants_result.csv',index=False)