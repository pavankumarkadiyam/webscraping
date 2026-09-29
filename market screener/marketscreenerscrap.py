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
            
        # Company name and profile link
        company_elem = tr.select_one('td div span a') or tr.select_one('a')
        company_name = company_elem.text.strip() if company_elem else 'Unknown'
        company_url = company_elem.get('href', '') if company_elem else ''
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


def scrape_calendar(cf_config=None, target_date=None, max_pages=5):
    """
    Fetch the financial calendar, extract postings, and handle pagination via /more.
    """
    session = requests.Session(impersonate='chrome120')
    
    if cf_config:
        url = f"https://se.marketscreener.com/bors/kalender/finansiell/?cf={cf_config}"
    else:
        url = "https://se.marketscreener.com/bors/kalender/finansiell/"
        
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'referer': 'https://se.marketscreener.com/',
    }
    
    # 1. Warm-up request to establish session cookie (PHPSESSID).
    # MarketScreener's backend requires an active PHPSESSID before rendering
    # the page so the CSRF token in #event-screener-csrf-token is properly
    # bound to the session in $_SESSION for subsequent /more AJAX POST calls.
    print("Initializing session handshake...")
    session.get('https://se.marketscreener.com/', headers=headers)
    
    # 2. Fetch the calendar page with the established session
    print(f"Fetching calendar from MarketScreener...")
    response = session.get(url, headers=headers)
    print(f"Initial Page Status: {response.status_code}")
    
    if response.status_code != 200:
        print("Failed to retrieve calendar.")
        return []
        
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.select_one('#eventScreener')
    
    # Extract metadata for pagination
    configuration = table.get('data-configuration') if table else cf_config
    parameters = table.get('data-parameters') if table else None
    csrf_elem = soup.select_one('#event-screener-csrf-token')
    token = csrf_elem.text.strip() if csrf_elem else (table.get('data-token') if table else None)
    
    # Parse initial postings
    all_postings = parse_postings_from_html(response.text)
    print(f"Loaded {len(all_postings)} postings from initial page.")
    
    # Identify lastDate from the last date header on the initial page
    stickies = soup.select('#eventScreener .sticky-second')
    last_date = stickies[-1].get('data-date') if stickies else None
    
    # Handle Pagination (via /async/agenda-screener/more)
    page = 1
    ajax_headers = {
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://se.marketscreener.com',
        'referer': url,
        'x-requested-with': 'XMLHttpRequest',
    }
    
    while page <= max_pages:
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
                    print("Reached end of results.")
                    break
                    
                new_postings = parse_postings_from_html(f"<table><tbody>{html_more}</tbody></table>", initial_date=last_date)
                if not new_postings:
                    print("No more postings parsed.")
                    break
                    
                print(f"Page {page}: Loaded {len(new_postings)} additional postings.")
                all_postings.extend(new_postings)
                
                # Update last_date for next page call
                soup_more = BeautifulSoup(f"<table><tbody>{html_more}</tbody></table>", 'lxml')
                more_stickies = soup_more.select('.sticky-second')
                if more_stickies:
                    last_date = more_stickies[-1].get('data-date')
                    
                # If target_date is set and we've already loaded past it, stop paginating
                if target_date and last_date and last_date > target_date:
                    print(f"Reached beyond target date ({target_date}). Stopping pagination.")
                    break
                    
                page += 1
            except Exception as e:
                print(f"Error parsing page {page}: {e}")
                break
        else:
            print(f"Page {page} failed with status {resp_more.status_code}: {resp_more.text[:150]}")
            break

    # Filter for target date if specified
    if target_date:
        filtered = [p for p in all_postings if p['date'] == target_date]
        return filtered
        
    return all_postings


if __name__ == '__main__':
    # Configuration string from MarketScreener for the financial calendar view
    cf = 'OWd3ZEJRQUh3cE9sMzBQekpXVTNQRVBGTVdmRytnVzU1ekRUeGNvb1N2R0NnMXZEbTdpOWRKLzVpZHZxTXpXNHdDTyt5ekRFY3dtNFI1akI2VXZzajFUQ043VGV5bHovR3lpV0hUNm5xcEhweDVWOSs3cEFya0JCc1VTRkpHZW4'
    
    # Scrape with pagination support
    postings = scrape_calendar(cf_config=cf)
    
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
