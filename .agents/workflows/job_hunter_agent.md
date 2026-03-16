---
description: Job Hunter Agent Workflow
---
# Job Hunter Agent Workflow

This is a skill-based workflow designed to guide the Antigravity agent in autonomously searching, extracting, and validating job postings. It follows a robust Plan-Execute-Verify cycle that avoids the brittleness of traditional scrapers.

## Mission Configuration Requirements
When executing this workflow, ensure the following are understood:
- **Capabilities**: Browser, Shell, and File System must be active.
- **Tooling**: Assume access to browser automation (`@go-playwright`) or scraping libraries (`python-jobspy`).

## Workflow Steps

When the user invokes this workflow or gives a job hunt master prompt, follow these exact phases:

### Phase 1: Planning
1. **Analyze Requirements**: Parse the user's target role, location, recency (e.g., last 24 hours), and target sites (LinkedIn, Indeed, Glassdoor, etc.).
2. **Strategy Creation**: Acknowledge that different sites require different approaches (e.g., LinkedIn DOM structure vs. Indeed). Note down the approach you will take for each site.

### Phase 2: Discovery
3. **Initiate Search**: Open the browser or run the scraping scripts for each target site.
4. **Obstacle Handling**: Watch out for CAPTCHAs, bot protections, or login walls. **CRITICAL:** If you encounter a hard block, PAUSE immediately and alert the user to solve it manually or provide guidance. Do not fail silently.

### Phase 3: Extraction & Maiden Voyage
5. **Initial Sample**: Perform a test run by scraping exactly **5 job postings** from the target sites.
6. **Data Cleaning**: Standardize the extracted data (clean up raw HTML characters, format salaries uniformly, standardize job titles and company names).
7. **User Validation**: Save this sample to `sample_jobs.json` or present it directly to the user. **Ask the user for explicit approval**: *"Is this data structure what you wanted?"* DO NOT proceed until the user approves the schema and quality.

### Phase 4: Full Scale Extraction & Validation
8. **Bulk Scraping**: Upon user approval, resume the extraction to pull all matching jobs within the target criteria.
9. **Cross-Referencing**: Process the aggregated jobs. Identify and merge duplicate listings (e.g., the same "Software Engineer at Google" role posted on both Indeed and LinkedIn).
10. **Data Output**: Save the final, deduped dataset into a `jobs.csv` file in the workspace context.

### Phase 5: Synthesis
11. **Final Reporting**: Analyze the saved CSV and output a concise summary to the user in the chat, specifically highlighting the **top 5 highest-paying roles** along with their links.

***

**User Note:** 
To run this autonomously every day, consider setting up the **Antigravity Bridge**: 
Spin up a local bridge server (e.g., on port 5000) and use a cron job to send your master prompt payload daily. The agent will wake up, perform the routine behind the scenes, and drop the CSV into your workspace.
