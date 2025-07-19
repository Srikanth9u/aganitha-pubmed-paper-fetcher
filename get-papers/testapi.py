# test_api.py

from fetch_papers.api import fetch_paper_ids,fetch_paper_details
from fetch_papers.csv_writer import write_to_CSV
def test_pubmed_api():
    # Sample test query (can be anything PubMed supports)
    query = "covid AND vaccine"
    
    print(f"Searching PubMed for: {query}")
    pubmed_ids = fetch_paper_ids(query, max_results=3)
    print(f"Found PubMed IDs: {pubmed_ids}")
    
    if not pubmed_ids:
        print("No PubMed IDs returned.")
        return

    print("\nFetching metadata for retrieved IDs...\n")
    papers = fetch_paper_details(pubmed_ids)
    
    for paper in papers:
        print("-" * 60)
        print(f"PubmedID: {paper['id']}")
        print(f"Title: {paper['title']}")
        print(f"Publication Date: {paper['publication_date']}")
        print(f"Non-academic Author(s): {paper['Non_academic_authors']}")
        print(f"Company Affiliation(s): {paper['Company_affiliations']}")
        print(f"Corresponding Author Email: {paper['Corresponding_author_email']}")
        print("-" * 60 + "\n")
    print(f"Number of papers fetched: {len(papers)}")
    

    print("\n💾 Writing results to output.csv...")
    write_to_CSV(papers, "output.csv")
    print("CSV file saved successfully as 'output.csv'")

# Run the test
if __name__ == "__main__":
    test_pubmed_api()
