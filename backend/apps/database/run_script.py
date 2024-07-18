import os, sys 
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) 

import re
from database.session import get_engine, create_engine, create_database
from sqlalchemy import text

DEFAULT_DBURL = "sqlite:///shu_database.db"

def run_scripts(script_paths): 
    with get_engine.connect() as conn:
        for path in script_paths:
            with open(path, "r") as file:
                statements = re.split(r';\s*$', file.read(), flags=re.MULTILINE)
                for stmt in statements:
                    query = text(stmt)
                    conn.execute(query)

if __name__ == "__main__":
    ## check length of sys.argv 
    if len(sys.argv) < 2:
        db_url = DEFAULT_DBURL 
    else: 
        db_url = sys.argv[1] 
    # print(db_url)
    create_engine(db_url)
    create_database() 
    print("Create database successfully") 

    # script_paths = sys.argv[2:] 
    # run_scripts(script_paths)