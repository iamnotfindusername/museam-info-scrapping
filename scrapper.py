import requests
from bs4 import BeautifulSoup
import csv 
import time
import os
import random
from datetime import datetime
from termcolor import colored


def get_random_user_agent(file_path="user_agent.txt"):
    """Selects a random user-agent from a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            agents = [line.strip() for line in f if line.strip()]
        return random.choice(agents)
    except FileNotFoundError:
        print(colored("[ERROR] user_agent.txt not found!", "red"))
        return "Mozilla/5.0"


def fetch_page(url, headers):
    """Fetches HTML content from a URL."""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        # print(colored("[INFO] Page fetched successfully.", "green"))
        return response.text
    except requests.RequestException as e:
        print(colored(f"[ERROR] Failed to fetch page: {e}", "red"))
        return None


def parse_museums(html):
    """Parses museum data from HTML."""
    try:
        soup = BeautifulSoup(html, "html.parser")
        container = soup.find(id="rosterRecords")
        if not container:
            print(colored("[ERROR] 'rosterRecords' element not found.", "red"))
            return []

        blocks = container.find_all("div", class_="postBlock")
        data = []

        for i, block in enumerate(blocks):
            try:
                post_title = block.find("a", class_="postTitle")
                if not post_title:
                    print(colored(f"[WARN] [{i}] Title not found.", "yellow"))
                    continue
                title = post_title.text.strip()

                post_dates = block.find_all("div", class_="postDate")
                if len(post_dates) < 2:
                    print(colored(f"[WARN] [{i}] Insufficient 'postDate' entries.", "yellow"))
                    continue

                addr = post_dates[0].text.strip()
                link_elem = post_dates[1].find("a")
                if not link_elem:
                    print(colored(f"[WARN] [{i}] Link not found.", "yellow"))
                    continue

                link = link_elem.get("href", "").strip()

                # Print to terminal
                # print(colored(f"[DATA] {title} | {addr} | {link}", "cyan"))

                data.append([title, addr, link])

            except Exception as e:
                print(colored(f"[ERROR] [{i}] Parsing error: {e}", "red"))

        return data

    except Exception as e:
        print(colored(f"[ERROR] parse_museums failed: {e}", "red"))
        return []


def save_to_csv(data, output_dir="data"):
    """Saves the data to a timestamped CSV file in the given directory."""
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{output_dir}/museums_{now}.csv"

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Title", "Address", "Link"])
            writer.writerows(data)

        print(colored(f"[INFO] Saved {len(data)} records to '{filename}'", "green"))
    except Exception as e:
        print(colored(f"[ERROR] Failed to save CSV: {e}", "red"))


def extract_data(page_number):
    url = f"https://museums.ca/site/aboutthecma/services/canadianmuseumdirectory?page={page_number}"
    user_agent = get_random_user_agent()
    headers = {"User-Agent": user_agent}

    html = fetch_page(url, headers)

    if html:
        museum_data = parse_museums(html)
        return museum_data
    else:
        print(colored(f"[WARN] Pages [{page_number}] data could not be extracted.", "yellow"))

def print_progress(current, total, bar_length=40):
    """Prints a progress bar to the terminal."""
    percent = current / total
    filled_length = int(bar_length * percent)
    bar = "█" * filled_length + '-' * (bar_length - filled_length)
    print(f"\r[INFO] Progress: |{bar}| {percent*100:6.2f}% ({current}/{total})", end='')

def main():
    start_time = time.time()
    exc_data = []
    total_page = 5 

    for page_number in range(1, total_page + 1):
        data = extract_data(page_number)

        if data:
            exc_data.extend(data)

        # Print progress bar
        print_progress(page_number, total_page)

    if exc_data:
        save_to_csv(exc_data)

    elapsed = time.time() - start_time
    print(colored(f"[INFO] Scraping complete. Total time: {elapsed:.2f} seconds", "blue"))

if __name__ == "__main__":
    main()
