Data:

-   add more test data, break up the json file into one file per language
-   update the migration to add multiple scores for each user
-   Move the json files to the migrations folder

Doc:

-   javascript file documentation & comments
-   CSS file documentation

Cleanup:

-   refactor CSS so it looks less like it was done with gpt
-   remove unused CSS
-   create CSS variables
-   refactor javascript to look more hand written, and use snake case
-   attempt.js - remove for and remove it from the html
-   hero button - why hero? rename.

Packaging:

-   read the Harvard project spec again, make sure nothing is missing or excluded
-   requirements.txt
-   readme.md

---

Why more complex:

-   javascript for creating a quiz
-   bootstrap icons, google fonts
-   multiple stylesheets
-   landing page
-   more professional looking css
-   properly support responsiveness
-   full error checking from all views, and in javascript
-   more complex schema - saving a quiz is multiple entries in multiple tables
-   similarity search with vector database
-   threading and synchronization with python, and background loading the search database for better UX

Put into readme:

-   generate a project description from gpt
-   schema from miro
-   ui design from miro

Requirements:

-   faiss-cpu
-   sentence-transformers
-   numpy

To generate data:
langchain>=0.1.14
langchain-core>=0.1.7
langchain-ollama>=0.1.0
