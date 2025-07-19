# 📘 Canadian Museum Scraper - README

## 📄 Project Description
This Python project scrapes data from the Canadian Museum Directory (https://museums.ca) and exports relevant details
such as **title**, **address**, and **website link** of each museum to a timestamped CSV file.

It features:
- Random user-agent rotation
- Colored terminal logging
- Robust error handling
- Progress bar for page loading
- CSV output to a `data/` directory

## 📦 Requirements

Install dependencies via pip:

```bash
pip install -r requirements.txt
```

### requirements.txt:
```
requests
beautifulsoup4
termcolor
```

## 📁 Directory Structure
```
project/
├── scrapper.py
├── user_agent.txt         # Contains 1000 user-agents, one per line
├── requirements.txt
└── data/                  # CSV output files are saved here
```

## 🚀 How to Run

```bash
python3 scrapper.py
```

This will:
- Start scraping all pages (1 to 276)
- Show progress in terminal
- Save the output to `data/museums_YYYY-MM-DD_HH-MM-SS.csv`

## 📊 Sample Output (CSV)

```
Title,Address,Link
"Royal Ontario Museum","100 Queens Park, Toronto, ON","https://www.rom.on.ca"
...
```

## ⚙️ Features

✅ Random User-Agent per request  
✅ Handles missing fields gracefully  
✅ Saves with timestamp  
✅ Cross-platform terminal colors (Windows & Linux)  
✅ Logs warnings and errors without interrupting the flow  

## 🧪 Notes

- Make sure your `user_agent.txt` file contains **one user-agent per line**.
- The `data/` directory will be created automatically if it doesn’t exist.
- If the scraping fails on some pages, warnings will be logged, and it will continue scraping remaining pages.

## 🛠️ Troubleshooting

- **`user_agent.txt not found`**: Make sure the file exists in the same directory as `scrapper.py`.
- **Slow scraping**: You can add `time.sleep()` between requests to throttle scraping if the site is sensitive.
- **Non-colored terminal output**: On some terminals, you may need to enable ANSI colors.

## 📬 License

MIT License - Free to use and modify.

## 🙌 Acknowledgements

Built using:
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Requests](https://docs.python-requests.org/)
- [termcolor](https://pypi.org/project/termcolor/)
