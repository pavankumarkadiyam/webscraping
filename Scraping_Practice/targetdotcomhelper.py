def get_zone(zones,zone_id):
    if (not zones) or (not zone_id):  return None
    for zone in zones:
        if zone.get('zone_id')==zone_id:
            return zone
    return None
def get_module_group (zone,module_group_id):
    if (not zone) or (not module_group_id): return None
    module_groups = zone.get('module_groups',[])
    for module_group in module_groups:
        if module_group.get('module_group_id') == module_group_id:
            return module_group
    return None
def get_module(module_group,module_type):
    if (not module_group) or (not module_type): return None
    modules = module_group.get('modules',[])
    for module in modules:
        if module.get('module_type')==module_type:
            return module
    return None
def get_product_titles(module):
    if not module: return None
    titles = {}
    products = module.get('module_data',{}).get('data_by_tcin',[])
    for product in products:
        titles[product.get('tcin')]=product.get('title')
    if titles:
        return titles
    else:
        return None

def get_product_prices(products):
    if not products: return None
    prices = {} 
    for product in products:
          prices[product.get('tcin')]=product.get('price',{}).get('current_retail')
    return prices

def get_data_source_module(data_source_modules,module_type):
    if (not data_source_modules) or (not module_type):  return None
    for module in data_source_modules:
        if module.get('module_type')==module_type:
            return module

def get_final_product_set(product_detail_web_datasourcefulfillment_and_variations,product_titles_map,product_price_map):
    if not product_detail_web_datasourcefulfillment_and_variations: return None
    result = []
    for variant in product_detail_web_datasourcefulfillment_and_variations:
        color = variant.get('value')
        result.extend([
            {
                'Id':product.get('tcin'),
                'Title': product_titles_map.get(product.get('tcin'),'Title Not Found'),
                'Color': color,
                'Size': product.get('value'),
                'Price': product_price_map.get(product.get('tcin'),'Price Not Found'),
                'Buying URL':product.get('buy_url'),
                'primary_image_url':product.get('primary_image_url')
            }
            for product in variant.get('variation_hierarchy')
        ])
    return result