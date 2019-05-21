
# Item Catalog

This item catalog project is a web application designed for a store with the ability to:

1. Create,
2. Read,
3. Update,
4. And delete...

items and item categories within a catalog. Security features have been implemented to protect resources from being edited or removed by un-authorised users.

***

## Solution Architecture

The architecture for this web application consists of a Flask application accessing data from a SQLite database, being served from a Linux Virtual Machine (VM). The front end has been built HTML, CSS, JavaScript, jQuery and AJAX. The backend was built using Python and SQLAlchemy. See the below architecture diagram for a detailed overview.

The backend is made of 3 tables:

1. Item: for the items within the catalog
2. Category: for the categories within the catalog
3. Users: for the users that have ownership of categories and items

See the below diagram for a detailed understanding of the data model. 

The application is built from the below files:

- **application.py**: This script is the application contains the backend logic of the application, routing for each page and JSON endpoints.
- **database.py**: This module consists of 3 classes, representing the 3 tables within the database. The relationships within the data model are reflected within this file.
- **populatedb.py**: This script can be run to populate the empty database after cloning the repository. 
- **client_secrets.json**: Contains client ID and client secrets for Google Sign-In authentication.
**/templates**
- **main**: Contains prerequisities for Google Sign-In, jQuery, fonts, styling and Bootstrap as well as JavaScript and AJAX queries to handle Google Sign-In/Out.
- **header**: Contains navbar and flash messages.
- **loginPage**: Landing page for the web application.
- **welcome**: Welcome page after signing in.
- **allCategories**: Responsive card based page to display all catalog categories.
- **newCategory**: Add a new category after signing in to the catalog.
- **editCategory**: Edit an existing category, if authorised, after signing in.
- **deleteCategory**: Delete an existing category, if authorised, after signing in.
- **showItems**: Show all items within a category.
- **newItem**: Add a new item to a category, if authorised, after signing in.
- **editItem**: Edit an existing item, if authorised, after signing in.
- **deleteItem**: Delete an existing category, if authorised, after signing in.
- **unAuthorisedEntry**: Fallback unauthorised entry page if an unauthorised user tries to create, update or delete data.

