# 1.0
- Flask - API endpoint
- Texlive engine - for file conversion
- Docker compose
---
# 2.0
+ Tectonic engine for conversion
---
# 3.0
+ Authentication

---
## deployed on render
https://latex-to-pdf-latest.onrender.com

## endpoints
- GET: /version - testing api health
- POST: /login
- POST: /validate
- POST: /convert

---
# DB
- docker exec -it <docker name> bash

## DB commands

### mysql
- login: `mysql -u auth_user -p`  -> this will provide input for password
- show databases;
- use <db>;
- show tables;

### postgres
- psql -U postgres