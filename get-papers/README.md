This project fetch research papers from [PubMed](https://pubmed.ncbi.nlm.nih.gov/) based on a user search query and filters out papers authored by non-academic affiliations (e.g., industry or biotech companies). The result is saved to a CSV file with metadata such as title, publication date, author affiliations, and contact emails.
Project structure:

fetch-papers/
│
├── fetch_papers/
│ ├── api.py # Logic to fetch paper IDs and metadata from PubMed
│ ├── csv_writer.py # Logic to write results to a CSV file
| ├── __init__.py
│ ├──main.py  # CLI application using Typer
│
├── testapi.py # Standalone script to test functionality end-to-end
├── README.md # Project documentation (this file)
├── poetry.lock # Poetry dependency lock file
├── pyproject.toml # Project configuration and dependencies
└── output.csv # Output CSV file (generated after running)


Requirements:
poetry
-python = ">=3.12"
requests = "^2.32.4"
typer = "^0.16.0"
pandas = "^2.3.1"
rich = "^14.0.0"
install dependencies
--------------------
poetry install
pip install typer[all]
pip install pandas
LLMs tools utilized
-chatgpt(https://chatgpt.com/share/687a820e-e678-8012-8f90-e6273742a1fc)


Objective:
Create a Python CLI tool that:

Fetches research papers from PubMed API based on a user query.

Filters for papers with at least one non-academic author affiliated with a pharma/biotech company.

Outputs the result as a CSV file.

project Implementation Process:
->Step 1: Set Up the Project Environment
Initialize a Git repository.

Create a new Poetry project:

--poetry install
poetry new get_papers
cd get_papers
Add dependencies (like requests, pandas, typer, etc.):



-> Step 2: Query the PubMed API
Use the Entrez E-Utilities API from NCBI.

Required steps:

esearch: Find matching PubMed IDs from the user query.

efetch: Get detailed metadata using PubMed IDs.

Use requests to make API calls.

Step 3: Filter for Non-Academic Authors
Use heuristics like:

Check affiliation strings for:

non academic authors:

1.affiliations containing any of the labels then they are the academics authors

"university", "college", "school", "hospital", "research institute", "gov", "csir", "cnrs", "nih"

2.email domain

Academic Emails usually ends with:

.edu, .ac.in, .ac.uk, .gov

e.g., john@harvard.edu

Collect:

Names of non-academic authors.

Their company affiliations.

Email of corresponding author.

Step 4: Output CSV File

Columns:

PubmedID

Title

Publication Date

Non-academic Author(s)

Company Affiliation(s)

Corresponding Author Email

Use pandas to export to CSV.

🔹 Step 5: CLI Support using Typer

Add command-line arguments:

Query input

--file to save as CSV (optional)

--debug for verbose logs

--help for usage

Use Typer to handle CLI arguments:


poetry run get-papers-list "cancer AND immunotherapy" --file results.csv
Step 6: Structure the Code
Create a Python module (get_papers/):

api.py: Handles PubMed API interactions.

filter.py: Filters out academic authors.

csv_writer.py: Writes to CSV.

main.py: CLI logic using typer.

Follow PEP8 and use type hints.

🔹 Step 7: Setup Executable Command
In pyproject.toml, configure:

toml
Copy
Edit
[tool.poetry.scripts]
get-papers-list = "get_papers.main:app"

how to run: poetry run get-papers-list "covid AND pfizer" --file results.csv
