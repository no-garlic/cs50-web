
Todo:
- read the Harvard project spec again, make sure nothing is missing or excluded
- move css, images, and js into subdirs
- create admin classes and register them
- requirements.txt
- refactor CSS so it looks less like it was done with gpt
- remove unused CSS
- create CSS variables
- CSS file documentation
- refactor javascript to look more hand written, and use snake case
- javascript file documentation & comments
- update scemantic search when adding a quiz
- update the migration to add multiple scores for each user
* left margin for sidebar is broken
- add more test data, break up the json file into one file per language
- document all code with # comments
- add docstrings
- review all code to look hand written
- handle error conditions in views & html
- remove unused imports
- remove unused functions in Models
- html file documentation

Why more complex:
- javascript for creating a quiz
- bootstrap icons, google fonts
- multiple stylesheets
- landing page
- more professional looking css
- properly support responsiveness
- full error checking from all views, and in javascript
- more complex schema - saving a quiz is multiple entries in multiple tables
- similarity search with vector database


Put into readme:
- generate a project description from gpt
- schema from miro
- ui design from miro


Requirements:
- faiss-cpu
- sentence-transformers
- numpy
