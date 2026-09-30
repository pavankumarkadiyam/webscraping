from curl_cffi import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def parse_postings_from_html(html_content, initial_date=None):
    """Extract structured posting details from calendar table HTML."""
    soup = BeautifulSoup(html_content, 'lxml')
    table = soup.select_one('#eventScreener') or soup.select_one('table')
    if not table:
        return []

    postings = []
    current_date = initial_date
    
    for tr in table.select('tbody tr'):
        # Check if row is a date header
        if 'sticky-second' in tr.get('class', []):
            current_date = tr.get('data-date') or tr.text.strip().replace('\n', ' ')
            continue
            
        tds = tr.select('td')
        if len(tds) < 3:
            continue
            
        # Filter out non-company rows (like table control header)
        company_elem = tr.select_one('td a[href*="/kurs/"]') or tr.select_one('td div span a')
        if not company_elem:
            continue
            
        company_name = company_elem.text.strip()
        company_url = company_elem.get('href', '')
        if company_url and company_url.startswith('/'):
            company_url = f"https://se.marketscreener.com{company_url}"
            
        # Event type (e.g. quarterly report), period, and time
        event_type = tds[2].text.strip().replace('\n', ' ') if len(tds) > 2 else ''
        period = tds[3].text.strip().replace('\n', ' ') if len(tds) > 3 else ''
        event_time = tds[4].text.strip().replace('\n', ' ') if len(tds) > 4 else 'All day'
        
        postings.append({
            'date': current_date,
            'company': company_name,
            'event': event_type,
            'period': period,
            'time': event_time,
            'url': company_url,
        })
        
    return postings


# Static obfuscated field identifiers compiled into MarketScreener's frontend JS (prod-*.min.js):
# These represent the 'startDate' and 'endDate' inputs of the date range picker.
DATE_FILTER_START_KEY = 'ZjBKQkREL20yZXJmSVBMRFIxNDc2UT09'
DATE_FILTER_END_KEY = 'KzE1UXROTG5rYmhXUFFtZDlkZGhVZz09'


def scrape_calendar(target_date="tomorrow", max_pages=10):
    """
    Fetch financial calendar postings for a specific date (default: tomorrow).
    
    1. Initializes session with PHPSESSID cookie via handshake.
    2. Requests base calendar page to extract table attributes and CSRF token.
    3. Calls /async/agenda-screener/query to dynamically generate the 'cf' token
       and retrieve initial postings for the requested target date.
    4. Calls /async/agenda-screener/more to handle pagination with the dynamic 'cf'.
    """
    # Resolve target_date
    if target_date == "tomorrow":
        target_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    elif target_date == "today":
        target_date = datetime.now().strftime('%Y-%m-%d')

    session = requests.Session(impersonate='chrome120')
    base_url = "https://se.marketscreener.com/bors/kalender/finansiell/"
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'referer': 'https://se.marketscreener.com/',
    }
    
    # 1. Warm-up request to establish session cookie (PHPSESSID)
    print("Initializing session handshake...")
    session.get('https://se.marketscreener.com/', headers=headers)
    
    # 2. Fetch base calendar page to obtain CSRF token and base configuration
    print(f"Fetching base calendar page from MarketScreener...")
    response = session.get(base_url, headers=headers)
    print(f"Base Page Status: {response.status_code}")
    
    if response.status_code != 200:
        print("Failed to retrieve calendar base page.")
        return []
        
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.select_one('#eventScreener')
    if not table:
        print("Could not find #eventScreener table.")
        return []

    configuration = table.get('data-configuration')
    parameters = table.get('data-parameters')
    default_config = table.get('data-default-config')
    csrf_elem = soup.select_one('#event-screener-csrf-token')
    token = csrf_elem.text.strip() if csrf_elem else table.get('data-token')
    
    ajax_headers = {
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://se.marketscreener.com',
        'referer': base_url,
        'x-requested-with': 'XMLHttpRequest',
    }

    all_postings = []
    last_date = target_date

    # 3. Call /async/agenda-screener/query to dynamically get the 'cf' token for target_date
    if target_date:
        print(f"Querying calendar specifically for target date: {target_date}...")
        data_query = {
            'configuration': configuration,
            'parameters': parameters,
            'defaultConfig': default_config,
            'token': token,
            f'altered[{DATE_FILTER_START_KEY}]': target_date,
            f'altered[{DATE_FILTER_END_KEY}]': target_date,
        }
        
        resp_query = session.post(
            'https://se.marketscreener.com/async/agenda-screener/query',
            data=data_query,
            headers=ajax_headers
        )
        
        if resp_query.status_code == 200:
            res_json = resp_query.json()
            if res_json.get('error'):
                print(f"Query error: {res_json.get('message')}")
                return []
                
            # Dynamic cf token generated by server for this date
            dynamic_cf = res_json.get('cf')
            if dynamic_cf:
                configuration = dynamic_cf
                print(f"Received dynamic 'cf' token from /query.")
                
            total_expected = res_json.get('nbResults', 0)
            print(f"Total postings scheduled for {target_date}: {total_expected}")
            
            html_query = res_json.get('html', '')
            initial_postings = parse_postings_from_html(f"<table><tbody>{html_query}</tbody></table>", initial_date=target_date)
            all_postings.extend(initial_postings)
            print(f"Loaded {len(initial_postings)} initial postings from /query.")
            
            # Identify lastDate from query response
            soup_query = BeautifulSoup(f"<table><tbody>{html_query}</tbody></table>", 'lxml')
            stickies = soup_query.select('.sticky-second')
            if stickies:
                last_date = stickies[-1].get('data-date') or target_date
        else:
            print(f"/query failed with status {resp_query.status_code}")
            return []
    else:
        # Default calendar view without specific date filtering
        all_postings = parse_postings_from_html(response.text)
        stickies = soup.select('#eventScreener .sticky-second')
        last_date = stickies[-1].get('data-date') if stickies else None
        total_expected = 999999

    # 4. Handle Pagination via /async/agenda-screener/more using the dynamic 'cf'
    page = 1
    while len(all_postings) < total_expected and page <= max_pages:
        data_more = {
            'configuration': configuration,
            'parameters': parameters,
            'page': page,
            'token': token,
            'lastDate': last_date,
        }
        
        resp_more = session.post(
            'https://se.marketscreener.com/async/agenda-screener/more',
            data=data_more,
            headers=ajax_headers
        )
        
        if resp_more.status_code == 200:
            try:
                res_json = resp_more.json()
                if res_json.get('error'):
                    print(f"Server returned error on page {page}: {res_json.get('message')}")
                    break
                    
                html_more = res_json.get('html', '')
                current_results = res_json.get('current_results', len(html_more))
                
                if current_results == 0 or not html_more.strip():
                    break
                    
                new_postings = parse_postings_from_html(f"<table><tbody>{html_more}</tbody></table>", initial_date=last_date)
                if not new_postings:
                    break
                    
                print(f"Page {page}: Loaded {len(new_postings)} additional postings.")
                all_postings.extend(new_postings)
                
                # Update last_date for next page call
                soup_more = BeautifulSoup(f"<table><tbody>{html_more}</tbody></table>", 'lxml')
                more_stickies = soup_more.select('.sticky-second')
                if more_stickies:
                    last_date = more_stickies[-1].get('data-date')
                    
                page += 1
            except Exception as e:
                print(f"Error parsing page {page}: {e}")
                break
        else:
            print(f"Page {page} failed with status {resp_more.status_code}: {resp_more.text[:150]}")
            break

    return all_postings


if __name__ == '__main__':
    # Automatically queries tomorrow's date dynamically (or pass target_date='YYYY-MM-DD')
    postings = scrape_calendar(target_date="tomorrow")
    
    print(f"\n=======================================================")
    print(f" TOTAL POSTINGS SCRAPED: {len(postings)}")
    print(f"=======================================================")
    for idx, item in enumerate(postings, 1):
        date_str = item['date'] or 'Date N/A'
        time_str = item['time'] or 'All day'
        print(f"{idx:2d}. [{date_str}] [{time_str}] {item['company']}")
        print(f"    Event:  {item['event']} {('(' + item['period'] + ')') if item['period'] else ''}")
        if item['url']:
            print(f"    Link:   {item['url']}")
