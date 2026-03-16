# Job Hunter Agent (JobSpy)

This repository contains a robust Python script (`job_hunter.py`) that uses the [python-jobspy](https://github.com/Bunsly/JobSpy) library to scrape job listings from Indeed, LinkedIn, and Glassdoor, and export them into a clean CSV format.

## Overview

The script follows a **Plan-Execute-Verify** cycle, divided into two execution modes:

1. **Maiden Voyage (`--test`)**: Scrapes 5 sample jobs to ensure the data structure and search parameters are yielding the expected results. It saves the results to `sample_jobs.json`.
2. **Full Scrape (`--full`)**: Scrapes up to 50 jobs per specified location, fetches remote listings, deduplicates the results by job URL, saves everything to `jobs.csv`, and outputs a synthesis of the top 5 highest-paying roles.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SomTakalkar/JobSpy.git
   cd JobSpy
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   - **Windows (PowerShell):** `.\.venv\Scripts\Activate.ps1`
   - **macOS/Linux:** `source .venv/bin/activate`

4. **Install dependencies:**
   ```bash
   pip install python-jobspy pandas
   ```

## How to Configure Your Search

By default, the script has empty search terms and locations so it doesn't run unintentionally. You must define what you are looking for by editing the `job_hunter.py` file.

**Open `job_hunter.py` and modify the following functions:**

### 1. For the Test Run (`maiden_voyage` function)
Around line 22, update the `search_term` and `location` arguments to test your query:
```python
def maiden_voyage():
    ...
    jobs = perform_scrape(results_wanted=5, search_term="Your Job Title", location="City, Country")
```

### 2. For the Full Scrape (`full_scrape` function)
Around line 46, define the master search term and a list of locations to scrape:
```python
def full_scrape():
    ...
    # Define your locations here
    locations = ["Pune", "Hyderabad"]
    search_term = "network OR sdwan OR \"sd-wan\""
```
*(The script is already programmed to automatically perform an extra search specifically for Remote jobs using your `search_term`.)*

## Running the Script

Ensure your virtual environment is activated, then run:

### Test Run (Maiden Voyage)
```bash
python job_hunter.py --test
```
*Review the output in `sample_jobs.json`.*

### Full Scrape
```bash
python job_hunter.py --full
```
*Review the output in `jobs.csv` and check the terminal for the top 5 paying roles.*


