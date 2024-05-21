from doiExtractor.doiExtractor import search_papers, merge_csv, remove_duplicates, csv_to_json, create_txt, find_file_by_name
from doiExtractor.openAlex import add_primary_location_to_csv
import argparse
import logging
import os

logging.basicConfig(level=logging.INFO)

def cli():
    parser = argparse.ArgumentParser(description="DOI Extractor Tool")
    parser.add_argument("--start", action="store_true", help="Start the extraction process")
    parser.add_argument("--url", default="https://portalcientifico.upm.es/es/ipublic/entity/16247", help="URL to extract DOIs from")
    parser.add_argument("--output", default="doiExtractor/Outputs", help="File path for the outputs")
    args = parser.parse_args()

    if args.start:
        url = args.url + "#14"
        url_docs = args.url

        # Files to write the output
        txt_filename = args.output + "/dois.txt"
        csv_filename = args.output + "/results.csv"
        json_filename = args.output + "/results.json"

        os.makedirs(args.output, exist_ok=True)

        # ExistingPapers
        papers = find_file_by_name("name_doi_papers.csv")

        logging.info("DOI Extractor Tool started")
        logging.info(f"Search in: {url}, Output csv: {csv_filename}, Output txt: {txt_filename}")
        logging.info(f"Existing papers in: {papers}")

        # Delete contents of the files if already created
        if os.path.exists(csv_filename):
            open(csv_filename, 'w').close()
        if os.path.exists(txt_filename):
            open(txt_filename, 'w').close()
        if os.path.exists(json_filename):
            open(json_filename, 'w').close()

        # Extract dois from url
        search_papers(url, url_docs, csv_filename)

        # Merge them with the existing from the papers
        merge_csv(csv_filename, papers)

        # Check for duplicated dois after the merge
        remove_duplicates(csv_filename)

        # Add URLs from OpenAlex
        add_primary_location_to_csv(csv_filename)

        # After adding missing dois with OpenAlex, create the .txt file containing the .pdf if it was found or the DOI if it wasn't
        create_txt(csv_filename, txt_filename)

        # Create a JSON with the information extracted
        csv_to_json(csv_filename, json_filename)

        logging.info(f"Data saved to {csv_filename} and {txt_filename}")
    else:
        logging.info("Use --start flag to start the extraction process")
