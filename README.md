MYAS_SCRAPER is a LEB2 Assignment Tracker

Prerequisites:

- Python 3.x
- Dependencies from requirements.txt
- LEB2 account with valid credentials

Installation:

1. Clone the repository:
```
   git clone https://github.com/Bukharney/MYAS_SCRAPER.git
   cd MYAS_SCRAPER
```

2. Install dependencies:
```
   pip install -r requirements.txt
```
3. Create a .env file and add your LEB2 credentials:
```
   USERNAME=your_username
   PASSWORD=your_password
```
Usage:

Run the script to fetch and track assignments:
```
python scraper.py
```
The script will log in to your LEB2 account, fetch assignment details, and save them in assignments.json.

Configuration:

- Adjust headless parameter in the script if you want to run the browser in headless mode.
- Customize the file name and path in the script where the JSON data is saved.

Contributing:

Feel free to contribute to the project by opening issues or submitting pull requests.
