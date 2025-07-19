import pandas as pd
from typing import List, Dict
import csv

def write_to_CSV(papers: List[Dict[str, str]], filename: str) -> None:
    """
    exporting the the details from api to csv file
    """
    # step1:open a file in write mode
    # filename='output.csv'
    with open(filename, 'w',newline='', encoding='utf-8') as csvfile:
        # step2: create a csv writer object
        fieldnames = ['PubmedID', 'Title', 'Publication Date', 'Non-academic Author(s)', 'Company Affiliation(s)', 'Corresponding Author Email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # step3: write the header
        #creates a header row containing al the column names
        writer.writeheader()
        
        # step4: write the data
        for paper in papers:
            writer.writerow({
                'PubmedID': paper['id'],
                'Title': paper['title'],
                'Publication Date': paper['publication_date'],
                'Non-academic Author(s)': ', '.join(paper['Non_academic_authors']),
                'Company Affiliation(s)': ', '.join(paper['Company_affiliations']),
                'Corresponding Author Email': paper['Corresponding_author_email']
            })
    print(f"Data successfully written to {filename}")
    print(f"📝 Writing {len(papers)} rows to {filename}")
