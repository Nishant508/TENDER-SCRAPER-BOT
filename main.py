#main.py
import os
from bot.db_connector import connect_to_oracle, get_tender_sources, get_tender_keywords
from bot.db_writer import insert_tender_documents
from bot.scanner import perform_scan
from bot.llm_parser import process_saved_html

def main():
    """
    Main function to orchestrate the process.
    1. Connects to the database and fetches URLs/keywords.
    2. Runs the web scanner to scrape data.
    3. Runs the LLM parser to structure and filter the data.
    4. Inserts tender data and document paths into their respective tables.
    """
    db_conn = connect_to_oracle()

    tender_sources = get_tender_sources(db_conn)
    tender_keywords = get_tender_keywords(db_conn)
    
    if not tender_sources:
        print("\n--- No tender sources found in the database. Exiting scan. ---")
        return

    if not tender_keywords:
        print("\n--- No keywords found in the database. Exiting. ---")
        return

    scanned_data = perform_scan(website_configs=tender_sources)
    
    if scanned_data:
        final_tenders = process_saved_html(tender_keywords, scanned_data)
        
        if final_tenders:
            for tender in final_tenders:
                try:
                    # Step 1: Insert or update the main tender record and get its ID
                    # To temporarily skip this step, comment out the line below:
                    lead_id = insert_or_update_tender(tender, db_conn)
                    # lead_id = 12345 # <- Use this line to test with a dummy ID

                    if lead_id and tender.get('DOCUMENTS'):
                        # Step 2: Insert the associated documents into the new table
                        insert_tender_documents(lead_id, tender['DOCUMENTS'], db_conn)
                        
                except Exception as e:
                    print(f" (!) An error occurred while processing tender {tender.get('REF_NO')}: {e}")
        else:
            print("--- No new tenders were approved by the LLM. Skipping database write. ---")

    else:
        print("\n--- No new data was scanned. Skipping LLM processing. ---")
    
    if db_conn:
        db_conn.close()
        print("\n-> Database connection closed.")


if __name__ == "__main__":
    main()