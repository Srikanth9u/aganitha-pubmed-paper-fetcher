import requests #used to return HTTP/HTTPS requests
import xml.etree.ElementTree as ET #used to parse XML data
from typing import List, Dict 
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
EMAIL = "srikanthande76@gmail.com"  

#function to fetch Paper ids using a string from user  and return list of paper IDs
#using esearch tool to return paper IDs
def fetch_paper_ids(query: str,max_results: int = 20) -> List[str]:
    search_url = f"{BASE_URL}esearch.fcgi"
    params = {
        "db": "pubmed", #database
        "term": query, #search item provided by user
        "retmode": "xml",
        "retmax": str(max_results), #maximum number of ids to return
        "email": EMAIL 
    }
    response = requests.get(search_url, params=params) #fetch data from url 
    response.raise_for_status()  # Raise an error for bad responses
    root = ET.fromstring(response.content) #convert data to xml
    
    ids = [id_elem.text for id_elem in root.findall(".//Id")]
    return ids


#print(fetch_paper_ids("COVID-19", 20)) #test1
"""
function to fetch paper details(id,tittle,Publication Date,Non-academic author,company afiliation, Correspondong Author email)
 using a list of ids by ids returned from fetch_paper_ids function.
"""
def fetch_paper_details(ids: List[str]) -> List[Dict[str, str]]:
    # Function to fetch paper details using efetch tool
    #List[str] to store paper details
    ids_string = ",".join(ids)  # Join the IDs into a single string
    url = f"{BASE_URL}efetch.fcgi" 
    params={
        "db": "pubmed",  # database
        "id": ids_string,  # paper ids
        "retmode": "xml",  # return mode
        "email": EMAIL  # email for NCBI API usage
    }

    response=requests.get(url, params=params)  # fetch data from url
    response.raise_for_status()  # Raise an error for bad responses

    root=ET.fromstring(response.content)  # convert data to xml
    papers_data=[]
    for article in root.findall(".//PubmedArticle"):
        paper_data={}

        #extract paper id
        pmid = article.findtext(".//PMID")
        paper_data["id"] = pmid if pmid is not None else "N/A"

        # extract title
        Tittle = article.findtext(".//ArticleTitle")
        paper_data["title"] = Tittle if Tittle is not None else "N/A"

        # extract publication date
        pub_date_node = article.find(".//PubDate")
        if pub_date_node is not None:
            year = pub_date_node.findtext("Year")
            month = pub_date_node.findtext("Month")
            day = pub_date_node.findtext("Day")
            paper_data["publication_date"] = f"{year or 'N/A'}-{month or 'N/A'}-{day or 'N/A'}"
        else:
            paper_data["publication_date"] = "N/A"
        
        #extract non-academic author
        non_academic_authors = []
        company_affiliations = []
        corresponding_author_email = "N/A"
        #iterate through authors to find details
        for author in article.findall(".//Author"):
            # Full author name
            last_name = author.findtext("LastName") or ""
            fore_name = author.findtext("ForeName") or ""
            full_name = f"{fore_name} {last_name}".strip()
            # Keywords that indicate academic affiliations
            ACADEMIC_KEYWORDS = ["university", "college", "hospital", "school", "institute", "faculty"]

            # Keywords that suggest a company or industry affiliation
            INDUSTRY_KEYWORDS = ["inc", "ltd", "llc", "pharma", "biotech", "solutions", "technologies", "therapeutics", "corporation", "company", "gmbh", "s.a.", "pvt", "labs"]

            # Affiliation
            affiliation = author.findtext(".//Affiliation")
            if affiliation:
                aff_lower = affiliation.lower()
                # Check for non-academic affiliation heuristics
                # if not any(word in aff_lower for word in ["university", "college", "school", "hospital", "research institute", "gov", "csir", "cnrs", "nih"]):
                #     non_academic_authors.append(full_name)
                #     company_affiliations.append(affiliation)
                is_non_academic = (
                            any(word in aff_lower for word in INDUSTRY_KEYWORDS) and
                            not any(word in aff_lower for word in ACADEMIC_KEYWORDS)
                            )

                if is_non_academic:
                    non_academic_authors.append(full_name)
                    company_affiliations.append(affiliation)
                #find corresponding author email
                if "@" in affiliation and corresponding_author_email == "N/A":
                    possible_email = affiliation.split()[-1]
                    if "@" in possible_email:
                        corresponding_author_email = possible_email.strip("()[];.,:")

        paper_data["Non_academic_authors"] = "; ".join(non_academic_authors) or "N/A"
        paper_data["Company_affiliations"] = "; ".join(company_affiliations) or "N/A"
        paper_data["Corresponding_author_email"] = corresponding_author_email or "N/A"

        papers_data.append(paper_data)  # Add the current paper to the list

    return papers_data
