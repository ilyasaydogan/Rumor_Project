from src.get_announcement import get_announce
from src.get_statement import get_statement
from src.get_analysis import get_analysis_output
from src.get_statement import delete_pdf_files
from src.get_comments import get_comments
from datetime import datetime,timedelta

def main():
    todate = datetime.today().date()
    directory_to_clean = f'document_output/{todate}'
    get_announce()
    get_statement()
    get_analysis_output()
    delete_pdf_files(directory_to_clean)
    get_comments()
    
if __name__ == "__main__":
    main()
