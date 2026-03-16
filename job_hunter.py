import csv
import json
import argparse
from jobspy import scrape_jobs
import pandas as pd

def perform_scrape(results_wanted: int, location: str, is_remote: bool = False):
    print(f"Scraping top {results_wanted} jobs for Network/SDWAN in {location} (Remote: {is_remote})...")
    jobs = scrape_jobs(
        site_name=["indeed", "linkedin", "glassdoor"],
        search_term="network OR sdwan OR \"sd-wan\"",
        location=location,
        results_wanted=results_wanted,
        hours_old=24,
        country_ecea="india",
        is_remote=is_remote
    )
    return jobs

def maiden_voyage():
    print("Initiating Maiden Voyage (Test Run)...")
    
    # We will test one specific location for the maiden voyage to get a quick sample
    jobs = perform_scrape(results_wanted=5, location="Pune")
    
    if jobs.empty:
        print("No jobs found in the test run.")
        return

    # Convert to standard python dicts for JSON
    jobs_dict = jobs.to_dict(orient="records")
    
    # Clean up the dictionaries so they are JSON serializable
    for job in jobs_dict:
        for k, v in job.items():
            if pd.isna(v):
                job[k] = None
            elif hasattr(v, 'isoformat'):
                job[k] = v.isoformat()
    
    with open("sample_jobs.json", "w", encoding="utf-8") as f:
        json.dump(jobs_dict, f, indent=2, ensure_ascii=False)
        
    print("Saved 5 sample jobs to `sample_jobs.json`.")
    print("Please review this file to ensure the data structure meets your needs.")

def full_scrape():
    print("Initiating Full Scrape for Network/SDWAN...")
    
    locations = ["Pune", "Hyderabad"]
    all_jobs_dfs = []
    
    # Scrape specific locations
    for loc in locations:
        jobs = perform_scrape(results_wanted=50, location=loc)
        if not jobs.empty:
            all_jobs_dfs.append(jobs)
            
    # Scrape remote jobs (location parameter usually needs a country/region when remote=True, we'll use "India")
    remote_jobs = perform_scrape(results_wanted=50, location="India", is_remote=True)
    if not remote_jobs.empty:
        all_jobs_dfs.append(remote_jobs)
    
    if not all_jobs_dfs:
        print("No jobs found in the full scrape across all parameters.")
        return
        
    # Combine all results
    combined_jobs = pd.concat(all_jobs_dfs, ignore_index=True)
    
    # Deduplicate based on job_url
    combined_jobs.drop_duplicates(subset=['job_url'], keep='first', inplace=True)
        
    print(f"Scraped a total of {len(combined_jobs)} unique jobs. Cleaning and exporting to CSV...")
    
    # Save raw to CSV
    combined_jobs.to_csv("jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)
    print("Exported to `jobs.csv`.")
    
    synthesize_results(combined_jobs)

def synthesize_results(jobs_df: pd.DataFrame):
    print("\n--- SYNTHESIS: TOP 5 HIGHEST PAYING ROLES ---")
    
    # Check if we have salary data
    if "min_amount" not in jobs_df.columns or "max_amount" not in jobs_df.columns:
        print("Salary data is not available in the requested jobs.")
        return
        
    # Create an estimated average salary column for sorting
    jobs_df["estimated_salary"] = jobs_df[["min_amount", "max_amount"]].mean(axis=1)
    
    # Drop rows without salary
    jobs_has_salary = jobs_df.dropna(subset=["estimated_salary"])
    
    if jobs_has_salary.empty:
        print("None of the scraped jobs listed a salary.")
        return
        
    # Sort and get top 5
    top_jobs = jobs_has_salary.sort_values(by="estimated_salary", ascending=False).head(5)
    
    for index, row in top_jobs.iterrows():
        title = row.get("title", "Unknown Title")
        company = row.get("company", "Unknown Company")
        salary_min = row.get("min_amount")
        salary_max = row.get("max_amount")
        currency = row.get("currency", "")
        interval = row.get("interval", "yearly")
        url = row.get("job_url", "No URL")
        
        print(f"{title} at {company}")
        print(f"Pay: {salary_min} - {salary_max} {currency} ({interval})")
        print(f"Link: {url}")
        print("-" * 40)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Job Hunter Agent using Python JobSpy")
    parser.add_argument("--test", action="store_true", help="Run the Maiden Voyage (sample 5 jobs)")
    parser.add_argument("--full", action="store_true", help="Run the Full Scrape and Synthesis")
    
    args = parser.parse_args()
    
    if not args.test and not args.full:
        print("Please specify --test for a 5-job sample or --full for a complete scrape.")
        parser.print_help()
    elif args.test:
        maiden_voyage()
    elif args.full:
        full_scrape()
