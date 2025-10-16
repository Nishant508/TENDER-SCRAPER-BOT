import oracledb
import os

def test_connection_and_data():
    """
    Attempts to connect to the Oracle database and then queries your tables,
    including the TND_NEW table to verify data insertion.
    """
    conn = None
    try:
        username = "sys"
        password = "Techno@1001"
        dsn = "172.18.28.206:1521/xepdb1"
        
        # Connect with the separate user, password, and dsn arguments
        conn = oracledb.connect(
            user=username, 
            password=password, 
            dsn=dsn, 
            mode=oracledb.SYSDBA
        )
        
        print("--- Successfully connected to Oracle Database! ---")
        
        # --- Check the TND_LEAD_SOURCES table ---
        print("\n--- Fetching data from TND_LEAD_SOURCES table ---")
        cursor = conn.cursor()
        cursor.execute("SELECT name, url, status FROM TEECL_DEMO.TND_LEAD_SOURCES")
        
        rows = cursor.fetchall()
        if not rows:
            print("(!) The TND_LEAD_SOURCES table is empty.")
        else:
            print("Found the following tender sources:")
            for row in rows:
                print(f"  - Name: {row[0]}, URL: {row[1]}, Status: {row[2]}")
        
        # --- Check the TND_BOT_KEYWORDS table ---
        print("\n--- Fetching data from TND_BOT_KEYWORDS table ---")
        cursor.execute("SELECT name FROM TEECL_DEMO.TND_BOT_KEYWORDS")
        
        rows = cursor.fetchall()
        if not rows:
            print("(!) The TND_BOT_KEYWORDS table is empty.")
        else:
            print("Found the following keywords:")
            for row in rows:
                print(f"  - {row[0]}")
        
        # --- Check the TND_NEW table ---
        print("\n--- Fetching the latest 5 records from TND_NEW table ---")
        cursor.execute("""
            SELECT 
                REF_NO, 
                DESCRIPTION, 
                CUSTOMER_NAME, 
                PUBLISH_DATE, 
                BID_SUBMIT_CLOSING_DATE,
                SOURCE,
                SOURCE_DESCR
            FROM TEECL.TND_NEW
            ORDER BY CREATED_ON DESC
            FETCH NEXT 5 ROWS ONLY
        """)

        rows = cursor.fetchall()
        if not rows:
            print("(!) The TND_NEW table is empty. No tenders have been inserted yet.")
        else:
            print("Found the following recent records in TND_NEW:")
            # Print column headers
            print(f"{'REF_NO':<15} | {'DESCRIPTION':<35} | {'CUSTOMER_NAME':<25} | {'PUBLISH_DATE':<15} | {'BID_SUBMIT_CLOSING_DATE':<25} | {'SOURCE':<10} | {'SOURCE_DESCR':<20}")
            print("-" * 150)
            for row in rows:
                ref_no = str(row[0]) if row[0] is not None else 'N/A'
                description = str(row[1])[:30] + '...' if row[1] and len(str(row[1])) > 30 else str(row[1]) if row[1] is not None else 'N/A'
                customer_name = str(row[2])[:20] + '...' if row[2] and len(str(row[2])) > 20 else str(row[2]) if row[2] is not None else 'N/A'
                publish_date = row[3].strftime('%Y-%m-%d') if row[3] else 'N/A'
                closing_date = row[4].strftime('%Y-%m-%d') if row[4] else 'N/A'
                source = str(row[5]) if row[5] is not None else 'N/A'
                source_descr = str(row[6])[:15] + '...' if row[6] and len(str(row[6])) > 15 else str(row[6]) if row[6] is not None else 'N/A'
                
                # Check for None values again to ensure they are handled
                print(f"{ref_no:<15} | {description:<35} | {customer_name:<25} | {publish_date:<15} | {closing_date:<25} | {source:<10} | {source_descr:<20}")

    except oracledb.Error as e:
        print("(!) Failed to connect to Oracle Database.")
        print("Error details:", e)
        
    finally:
        if conn:
            conn.close()
            print("\n-> Connection closed.")

if __name__ == "__main__":
    test_connection_and_data()