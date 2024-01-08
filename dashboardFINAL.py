import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from urllib.parse import urlparse, urlencode, parse_qsl, urlunparse

from dateutil.parser import parse as parse_date

import itertools
import threading
import time

def animate_loading():
    for frame in itertools.cycle(['-', '/', '|', '\\']):
        print('\rLoading ' + frame, end='')
        time.sleep(0.2)

# ANSI escape codes for colors
class Colors:
    WHITE = '\033[97m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'

import feedparser

# def fetch_portswigger_rss():
#     url = "https://portswigger.net/daily-swig/rss"  # RSS feed URL
#     feed = feedparser.parse(url)
    
#     news_items = []

#     for entry in feed.entries:
#         title = entry.title
#         summary = entry.summary
#         link = entry.link
#         published = entry.published  # Or format date as needed

#         news_items.append({"title": title, "summary": summary, "link": link, "published": published})

#     return news_items

def display_news(news_items):
    for item in news_items:
        print(f"Title: {item['title']}")
        print(f"Published: {item['published']}")
        print(f"Summary: {item['summary']}")
        print(f"Link: {item['link']}\n")


def print_table_row(*args, col_widths, end_line=True, color=Colors.WHITE):
    row = "|".join(f"{color}{arg:<{width}}{Colors.ENDC}" for arg, width in zip(args, col_widths))
    print(row)
    if end_line:
        print(Colors.YELLOW + '-' * len(row) + Colors.ENDC)

def encode_url_query(url):
    parsed_url = urlparse(url)
    query = parse_qsl(parsed_url.query)
    encoded_query = urlencode(query)
    return urlunparse(parsed_url._replace(query=encoded_query))

#WORK IN PROGRESS FETCH NEWS FROM PORTWIGGER
# def fetch_portswigger_news(): 
#     url = "https://portswigger.net/daily-swig/dark-web"
#     response = requests.get(url)
#     response.raise_for_status()

#     soup = BeautifulSoup(response.text, 'html.parser')
#     news_items = []

#     for article in soup.find_all("article"):  # Adjust the selector based on actual page structure
#         title = article.find("h2").text.strip()  # Adjust these selectors based on actual structure
#         summary = article.find("p").text.strip()
#         link = article.find("a")["href"].strip()
        
#         news_items.append({"title": title, "summary": summary, "link": link})

#     return news_items

def print_banner():
 banner = """
                                                                    ______           _                   _   _                                                   
                                                                    | ___ \         | |                 | \ | |                                                  
                                                                    | |_/ / __ _  __| | __ _  ___ _ __  |  \| | _____      _____                                 
                                                                    | ___ \/ _` |/ _` |/ _` |/ _ \ '__| | . ` |/ _ \ \ /\ / / __|                                
                                                                    | |_/ / (_| | (_| | (_| |  __/ |    | |\  |  __/\ V  V /\__ \                                
                                                                    \____/ \__,_|\__,_|\__, |\___|_|    \_| \_/\___| \_/\_/ |___/                                
                                                                                        __/ |                                                                    
                                                                                       |___/                                                                              
                                                                                         ___,,___
                                                                                    _,-='=- =-  -`"--.__,,.._
                                                                                 ,-;// /  - -       -   -= - "=.
                                                                               ,'///    -     -   -   =  - ==-=\`.
                                                                              |/// /  =    `. - =   == - =.=_,,._ `=/|
                                                                             ///    -   -    \  - - = ,ndDMHHMM/\b  \\
                                                                           ,' - / /        / /\ =  - /MM(,,._`YQMML  `|
                                                                          <_,=^Kkm / / / / ///H|wnWWdMKKK#""-;. `"0\  |
                                                                                 `""QkmmmmmnWMMM\""WHMKKMM\   `--. \> \\
                                                                          hjm          `""'  `->>>    ``WHMb,.    `-_<@)
                                                                                                         `"QMM`.
                                                                                                            `>>>            
                                                  
                                                                       _ __ __ _ _ __  ___  ___  _ __ _____      ____ _ _ __ ___                                   
                                                                      | '__/ _` | '_ \/ __|/ _ \| '_ ` _ \ \ /\ / / _` | '__/ _ \                                  
                                                                      | | | (_| | | | \__ \ (_) | | | | | \ V  V / (_| | | |  __/                                  
                                                                      |_|  \__,_|_| |_|___/\___/|_| |_| |_|\_/\_/ \__,_|_|  \___|       
                                     _            _          _ _                               _ _             _                               _                               
                                    | |          | |        (_) |                             (_) |           (_)                             | |                              
                                    | | ___  __ _| | __  ___ _| |_ ___   _ __ ___   ___  _ __  _| |_ ___  _ __ _ _ __   __ _    __ _ _ __   __| |  _ __   _____      _____     
                                    | |/ _ \/ _` | |/ / / __| | __/ _ \ | '_ ` _ \ / _ \| '_ \| | __/ _ \| '__| | '_ \ / _` |  / _` | '_ \ / _` | | '_ \ / _ \ \ /\ / / __|    
                                    | |  __/ (_| |   <  \__ \ | ||  __/ | | | | | | (_) | | | | | || (_) | |  | | | | | (_| | | (_| | | | | (_| | | | | |  __/\ V  V /\__ \  _ 
                                    |_|\___|\__,_|_|\_\ |___/_|\__\___| |_| |_| |_|\___/|_| |_|_|\__\___/|_|  |_|_| |_|\__, |  \__,_|_| |_|\__,_| |_| |_|\___| \_/\_/ |___/ (_)
                                                                                                                        __/ |                                                  
                                                                                                                       |___/                                                     
    """
 print(banner)

def fetch_and_display(url, start_date, end_date, filter_group=None, filter_post=None):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    col_widths = [12, 50, 50, 20, 50]
    print_table_row("Date", "Post", "Post URL", "Group", "Group URL", col_widths=col_widths, end_line=False, color=Colors.GREEN)
    print(Colors.YELLOW + '-' * sum(col_widths) + '-' * (len(col_widths) - 1) + Colors.ENDC)

    for entry in soup.find_all("tr"):
        if len(entry.find_all("td")) == 3:
            post_td, group_td, date_td = entry.find_all("td")
            
            post_link = post_td.find('a')['href'] if post_td.find('a') else "No URL"
            group_link = group_td.find('a')['href'] if group_td.find('a') else "No URL"
            post_text = post_td.get_text(strip=True)
            group_text = group_td.get_text(strip=True)
            date_text = date_td.text.strip()
            entry_date = datetime.strptime(date_text, "%Y-%m-%d %H:%M:%S.%f").date()

            # Date filtering (only if start_date and end_date are not None)
            if start_date and end_date:
                if not (start_date <= entry_date <= end_date):
                    continue

            # Group and Post filtering
            if (not filter_group or filter_group.lower() in group_text.lower()) and (not filter_post or filter_post.lower() in post_text.lower()):
                encoded_post_link = encode_url_query(post_link)
                encoded_group_link = encode_url_query(group_link)
                print_table_row(date_text[:10], post_text[:48], encoded_post_link[:48], group_text[:18], encoded_group_link[:48], col_widths=col_widths)


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

def fetch_all_feeds(feeds):
    all_news_items = []
    headers = {'User-Agent': USER_AGENT}
    for url in feeds.values():
        response = requests.get(url, headers=headers)
        feed = feedparser.parse(response.content)
        for entry in feed.entries:
            title = entry.title if hasattr(entry, 'title') else "No Title"
            summary = entry.summary if hasattr(entry, 'summary') else "No Summary"
            link = entry.link if hasattr(entry, 'link') else "No Link"
            published = entry.get('published') if hasattr(entry, 'published') else "No Publication Date"
            all_news_items.append({
                "title": title,
                "summary": summary,
                "link": link,
                "published": published
            })
    return all_news_items




def filter_news_by_date(news_items, start_date, end_date):
    filtered_news = []
    for item in news_items:
        # Check if 'published' exists and is not the placeholder text
        if 'published' in item and item['published'] != "No Publication Date":
            try:
                item_date = parse_date(item['published']).date()
                # Perform the comparison with datetime.date objects
                if start_date <= item_date <= end_date:
                    filtered_news.append(item)
            except ValueError:
                # Handle the error if the date format is incorrect but not the placeholder
                pass
    return filtered_news



def search_news_items(news_items, keyword):
    keyword_lower = keyword.lower()
    filtered_items = []
    print(f"Searching for keyword: {keyword_lower}")  # Debugging statement
    for item in news_items:
        title_lower = item['title'].lower()
        summary_lower = item['summary'].lower()
        #print(f"Checking: {title_lower}")  # Debugging statement
        if keyword_lower in title_lower or keyword_lower in summary_lower:
            filtered_items.append(item)
    print(f"Found {len(filtered_items)} items matching the keyword.")  # Debugging statement
    return filtered_items



def display_news(news_items):
    for item in news_items:
        print(f"{Colors.GREEN}Title: {Colors.ENDC}{item['title']}")
        print(f"{Colors.YELLOW}Published: {Colors.ENDC}{item['published']}")
        print(f"{Colors.WHITE}Summary: {Colors.ENDC}{item['summary']}")
        print(f"{Colors.GREEN}Link: {Colors.ENDC}{item['link']}\n")

def get_date_range(choice):
    if choice == '1':  # Custom Date Range
        start_date = get_date_input("Enter the start date (YYYY-MM-DD): ")
        end_date = get_date_input("Enter the end date (YYYY-MM-DD): ")
    elif choice == '2':  # Last 7 Days
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
    elif choice == '3':  # Last 3 Days
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=3)
    elif choice == '4':  # Last 24 Hours
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=1)
    return start_date, end_date


def get_date_input(prompt):
    while True:
        date_str = input(prompt)
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")



def main():
    print_banner()
    try:
        while True:
            
            print("Fetching data...")
            rss_feeds = {
                "1": "https://en.0day.today/rss",
                "2": "https://feeds.feedburner.com/TheHackersNews",
                "3": "https://www.welivesecurity.com/en/rss/feed/",
                "4": "https://thecyberexpress.com/",
                "5": "https://www.acunetix.com/blog/feed/",
                "6": "https://ventureinsecurity.net/feed",
                "7": "https://www.cybertalk.org/feed/",
                "8": "https://www.coveware.com/blog?format=RSS",
                "9": "https://ransomware.org/feed/",
                "10": "https://www.cshub.com/rss/categories/attacks",
                "11": "https://ransomware.databreachtoday.com/rss-feeds",
                "12": "https://darkweblive.net/feed",
                "13": "https://www.redhotcyber.com/feed/",
                "14": "https://www.csirt.gov.it/data/indexer/rss",
                "15": "https://community.qualys.com/blogs/securitylabs/feeds/posts",
                "16": "https://thecyberexpress.com/feed/"
            }

            while True:  
                print("Options:")
                print("1. Custom Date Range")
                print("2. Last 7 Days")
                print("3. Last 3 Days")
                print("4. Last 24 Hours")
                print("5. Group Search")
                print("6. Exit")
                choice = input("Choose an option (1-5): ")

                if choice == '6':
                    print("Exiting program.")
                    break

                start_date, end_date = None, None
                filter_group = None

                if choice in ['1', '2', '3']:
                    start_date, end_date = get_date_range(choice)
                elif choice == '5':
                    filter_group = input("Enter a keyword to filter by (for both webpage and RSS feeds): ")

                # Fetch and display webpage data
                url = "https://privtools.github.io/ransomposts/"
                fetch_and_display(url, start_date, end_date, filter_group=filter_group)
                # Start the animation
                # animation_thread = threading.Thread(target=animate_loading)
                # animation_thread.start()
                # Fetch RSS feeds
                all_news_items = fetch_all_feeds(rss_feeds)
                # Stop the animation
                # animation_thread.do_run = False
                # animation_thread.join()



                # Apply filters
                if choice == '4':
                    # For group search, use the keyword filter
                    filtered_news = search_news_items(all_news_items, filter_group)
                else:
                    # For date range searches, filter by date
                    filtered_news = filter_news_by_date(all_news_items, start_date, end_date)

                if filtered_news:
                    print(f"\nFiltered news items:\n")
                    display_news(filtered_news)
                else:
                    print("No news items found for the given criteria.")
                    
                print("\nRefreshing data in 30 minutes...\n")
                # Add a timestamp for the last fetched data
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"\nLast fetched at: {current_time}\n")
                print("\nDo you want to perform another search? (yes/no): ")
                time.sleep(1800)  # Sleep for 30 minutes (1800 seconds)
    except KeyboardInterrupt:
        print("\nProgram terminated by user (Ctrl+C). Exiting gracefully.")

if __name__ == "__main__":
    main()