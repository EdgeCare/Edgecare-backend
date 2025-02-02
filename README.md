## This repo contains all API controllers, RAG system, Multi-agent message passing logic of the EdgeCare org.
### How to setup:
- First, create/ activate virtual env:
        create:  python -m venv .backend-env
        activate:  source .backend-env/bin/activate

- Install PyTorch suitable for your system's CUDA version by following the [official instructions](https://pytorch.org/get-started/locally/) (2.1.1+cu121 in our case).

- `Git-lfs` is required to download and load corpora for the first time.

- Then, install the remaining requirements using: `pip install -r requirements.txt`

- Re-install huggingfacehub using following commands:
        ```pip uninstall huggingface_hub -y```
  and 
        `pip install huggingface_hub==0.24.0`




## To Run Server

Start server in port 8000 without 8080/proxy/
```
uvicorn main:app --host 0.0.0.0 --port 8000
```

## To kill a running process in a port
```
lsof -i :8000
sudo kill -9 <PID>
```

## File Structure

```
Edgecare-backend/
├── main.py               # Entry point for the FastAPI application
├── README.md             # Documentation for the project
├── requirements.txt      # List of Python dependencies
├── .ec-env               # Environment variables
├── agents/
│   ├── manager_agent.py        # Manager agent for orchestration
│   ├── qa_agent.py             # Question-Answering agent
│   ├── retrieval_agent.py      # Retrieval agent
│   ├── query_refiner.py        # User query refinement agent
│   ├── keyword_agent.py        # Keyword extraction agent
│   └── 
├── workflows/            # Workflows combining multiple agents
│   ├── multi_agent_workflow.py 
├── db/                   # Database connection and initialization
│   ├── __init__.py
│   ├── database.py       # Database session and engine configuration
│   └── models/           # Directory for database model modules
│       ├── __init__.py
│       ├── user.py       # User database model
│       └── public.py     # Public database model (if applicable)
├── schemas/              # Pydantic schemas for request/response validation
│   ├── __init__.py
│   ├── user.py           # Schemas for user-related APIs
│   └── public.py         # Schemas for public-related APIs (if applicable)
├── rag/                  # EdgeCare RAG
├── routes/               # API route definitions
│   ├── user.py           # User-related endpoints
│   └── public.py         # Public-related endpoints
└── utils/                # Utility functions and reusable components
    └── helpers.py        # Helper functions for the app
```


## Database

### View tables in database Command-Line

1. Connect to the PostgreSQL database:
``` psql -h localhost -U your_username -d your_database ```

2. To list all tables:
``` \dt ```

3. View Table Rows
``` SELECT * FROM table_name; ```

4. delete a raw
``` DELETE FROM users WHERE id = 4; ```

5. View columns in a table
```\d table_name```

### Additional Commands

List all databases:

``` \l ```

Connect to a specific database:

``` \c database_name ``` 

Quit the psql interface

``` \q ``` 

### edit table columns as admin (DO NOT LOGIN USING THIS USER UNLESS YOU HAVE...)

1. connect to database
```
sudo -i -u postgres
psql
\c edge_care_db
```

2. See table details
```
\d users
```

3. any SQL command to do the change
eg-
```
ALTER TABLE users RENAME COLUMN username TO email;
```

4. give table permission to <COMMON_USER> - give permission to <COMMON_USER> after creating a new table
```
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE <TABLE_NAME> TO <COMMON_USER>;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE <TABLE_NAME>_id_seq TO <COMMON_USER>;
```

4. quit
```
\q
exit 
```