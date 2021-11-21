# Development Notes

- the command module, will use both filesystem and db to perform actions
- the filesystem module, deals with low-level fs operations
- the db module, deals with database operations
- `make` accept params. 
  
  Ex.: 
  ```sh
  make params="add tests/data/.kb/data"
  ``` 
  will execute 

  ```sh
  python -m kb add tests/data/.kb/data
  ```
