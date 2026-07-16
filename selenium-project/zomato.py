import requests
import time
import json
session = requests.Session()
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.zomato.com',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36'
}

r = session.get("https://www.zomato.com/Bengaluru", headers=headers)
cookies = session.cookies.get_dict()
print(cookies)

new_headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.zomato.com',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
    'x-zomato-csrft': f"{cookies.get("csrf")}"
}
json_data = {
    # 'context': 'nightlife',
    'addressId': 0,
    'entityId': 6,
    'entityType': 'city',
    'locationType': '',
    # 'isOrderLocation': 1,
    'cityId': 4,
    # 'latitude': '12.9716060000000000',
    # 'longitude': '77.5943760000000000',
    # 'userDefinedLatitude': 12.971606,
    # 'userDefinedLongitude': 77.594376,
    # 'entityName': 'Bengaluru',
    # 'orderLocationName': 'Bengaluru',
    'cityName': 'Bengaluru',
    'countryId': 1,
    'countryName': 'India',
    # 'displayTitle': 'Bengaluru',
    'o2Serviceable': True,
    'placeId': '3655',
    'cellId': '4300399395616063488',
    # 'deliverySubzoneId': 9419,
    'placeType': 'DSZ',
    # 'placeName': 'Bengaluru',
    'isO2City': True,
    'fetchFromGoogle': False,
    # 'fetchedFromCookie': True,
    # 'isO2OnlyCity': False,
    # 'address_template': [],
    # 'otherRestaurantsUrl': '',
}

def create_filter(searchMetadata):
    postbackParams = json.loads(searchMetaData.get('postbackParams'))
    postbackParams['search_id'] = None
    searchMetaData['postbackParams'] = json.dumps(postbackParams)
    print(searchMetaData)
    return {
        'searchMetadata':searchMetadata,
        'dineoutAdsMetaData':{},
        'appliedFilter':[
            # {
            #     'filterType':'category_sheet',
            #     'filterValue':'go_out_home',
            #     'isHidden':True,
            #     'isApplied':True,
            #     # 'postKey':json.dumps({'category_context':'go_out_home'})
            # },
            # {
            #     'filterType':'context',
            #     'filterValue':'nightlife_home',
            #     'isHidden':True,
            #     'isApplied':True,
            #     # 'postKey':json.dumps({'context':'nightlife_home'})
            # }
        ],
        'urlParamsForAds':{}
    }

def generate_json_data_filters(solr_offset,page,total_restaurants_shown,total_results_shown):
    return {
        'solr_offset' : solr_offset,
        'page': page,
        'total':total_restaurants_shown,
        'total_results_shown': total_results_shown
    }

results = []
count = 0
response = session.post('https://www.zomato.com/webroutes/search/home', cookies=cookies, headers=new_headers, json=json_data)
json_response = response.json()
while json_response.get('sections').get('SECTION_SEARCH_META_INFO').get('searchMetaData').get('hasMore'):
    count += 1
    if response.status_code == 200:
        SECTION_SEARCH_RESULT = json_response.get('sections').get('SECTION_SEARCH_RESULT')
        results.extend([
            {
                'Type': result.get('type','N/A'),
                'resId':result.get('info').get('resId'),
                'Name':result.get('info').get('name')


            }
            for result in SECTION_SEARCH_RESULT
        ])
        searchMetaData = json_response.get('sections',{}).get('SECTION_SEARCH_META_INFO',{}).get('searchMetaData')
        postbackParams = json.loads(searchMetaData.get('postbackParams'))
        print(
            f"page: {postbackParams.get('page','NR')} || "
            f"Total Restaurants shown: {postbackParams.get('total_restaurants_shown','NR')} || "
            f"Total Restaurants Scraped: {len(results)}"
        )
        json_data['filters'] = json.dumps(create_filter(searchMetaData))
        if count%20 == 0:
            session.close()
            session= requests.Session()
            r = session.get("https://www.zomato.com/Bengaluru", headers=headers)
            cookies = session.cookies.get_dict()
            if(new_headers['x-zomato-csrft'] == cookies.get('csrf')):
                print(True)
            else:
                print(False)
            new_headers['x-zomato-csrft'] = cookies.get('csrf')
            # break
            

        response = session.post('https://www.zomato.com/webroutes/search/home', cookies=cookies, headers=new_headers, json=json_data)
        json_response = response.json()
        time.sleep(2)
        if len(results) >= 1000:
            break
import pandas as pd
pd.DataFrame(results).to_csv('results_.csv',index=False)