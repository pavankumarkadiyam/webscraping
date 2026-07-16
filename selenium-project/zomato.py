import requests
import time
import json
import pandas as pd
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

r = session.get("https://www.zomato.com/hyderabad", headers=headers)
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
    'cityName': 'Hyderabad',
    'countryId': 1,
    'countryName': 'India',
    # 'displayTitle': 'Bengaluru',
    'o2Serviceable': True,
    'placeId': '9419',
    'cellId': '4308704762854899712',
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
response = session.post('https://www.zomato.com/webroutes/search/home', cookies=cookies, headers=new_headers, json=json_data)
json_response = response.json()

if response.status_code == 200:
    while True:
        response = session.post('https://www.zomato.com/webroutes/search/home', cookies=cookies, headers=new_headers, json=json_data)
        json_response = response.json()
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            SECTION_SEARCH_RESULT = json_response.get('sections').get('SECTION_SEARCH_RESULT')
            print(f'Section Result Length: {len(SECTION_SEARCH_RESULT)}')

            results.extend([
                {
                    'Type': result.get('type','N/A'),
                    'resId':result.get('info',{}).get('resId'),
                    'Name':result.get('info',{}).get('name'),
                    'Address': result.get('info',{}).get('locality',{}).get('address',"No Address found"),
                    'Has fake reviews': result.get('info',{}).get('rating',{}).get('has_fake_reviews',0),
                    'Rating':result.get('info',{}).get('rating',{}).get('aggregate_rating',0),
                    'Votes':result.get('info',{}).get('rating',{}).get('votes',0),
                    'Has Bulk Offers': result.get('bulkOffers',[])

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
            time.sleep(1)
            if len(SECTION_SEARCH_RESULT) == 0:
                print(f"{len(results)} restaurants were scraped.")
                break
        pd.DataFrame(results).to_csv('results_.csv',index=False)
else:
    print(response.status_code)