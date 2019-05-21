
# Item Catalog

This item catalog project is a web application designed for a store with the ability to:

1. Create,
2. Read,
3. Update,
4. And delete...

items and item categories within a catalog. Security features have been implemented to protect resources from being edited or removed by un-authorised users.

***

## Solution Architecture

The architecture for this web application consists of a Flask application accessing data from a SQLite database, being served from a Linux Virtual Machine (VM). The front end has been built HTML, CSS, JavaScript, JQuery and AJAX. The backend was built using Python and SQLAlchemy. See the below architecture diagram for a detailed overview.

The backend is made of 3 tables:

1. Item - for the items within the catalog
2. Category - for the categories within the catalog
3. Users - for the users that have ownership of categories and items

See the beloe data model diagram for a detailed understanding of the data.



