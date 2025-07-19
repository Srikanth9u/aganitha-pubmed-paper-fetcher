
# CLI entry point for the PubMed paper fetcher using Typer.


import typer  # for CLI
from typing import Optional
from fetch_papers.api import fetch_paper_ids, fetch_paper_details
from fetch_papers.csv_writer import write_to_CSV

# Initializing Typer app and its description

app = typer.Typer(help="Fetch PubMed papers with non-academic authors and export to CSV.")


@app.command()
def fetch(
    query: str = typer.Argument(..., help="PubMed search query."),
    file: Optional[str] = typer.Option(None, "--file", "-f", help="Output CSV file name."),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug output.")
):
    """
    Fetch papers from PubMed using a search query and optionally write to CSV.
    """
    if debug:
        print(f"Query: {query}")
        print("Fetching paper IDs...")

    pubmed_ids = fetch_paper_ids(query)
    if debug:
        print(f"Found {len(pubmed_ids)} PubMed IDs: {pubmed_ids}")

    papers = fetch_paper_details(pubmed_ids)

    if debug:
        print(f"Processed {len(papers)} papers.")
        for paper in papers:
            print(paper)

    if file:
        write_to_CSV(papers, file)
        print(f"Results written to {file}")
    else:
        # If no file, print to console
        for paper in papers:
            print("-" * 60)
            for key, value in paper.items():
                print(f"{key}: {value}")


if __name__ == "__main__":
    app()
