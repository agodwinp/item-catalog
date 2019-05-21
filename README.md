
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

***

## Installation

### Installing the VM software
To run this web application application, you need to install and configure a Linux VM on top of your operating system. For this, you will need to install two pieces of software:
- **VirtualBox**: https://www.virtualbox.org/wiki/Downloads
    - This is the software that actually runs the VM. Install the *platform package* for your operating system, you do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it, we can do this via Vagrant. 
- **Vagrant**: https://www.vagrantup.com/downloads.html
    - Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem.

You will also need a Unix-style terminal program. On Mac or Linux systems you can use the built-in Terminal. On Windows, Git Bash is recommended. 

### Starting the VM Image
Once you have VirtualBox and Vagrant installed, open a terminal and run the following commands:

    $ mkdir item_catalog
    $ cd item_catalog

This will create a new directory for this project. Then, download this ZIP file:
- https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip

This will download the Linux image `FSND-Virtual-Machine` into your downloads folder. Once it's finished downloading, open the folder `FSND-Virtual-Machine` and move everything within it into your `item_catalog` folder. The Linux instance is now within the `item_catalog` directory. Now we want to start the image. Navigate to your `item_catalog` folder and issue the following commands:

    $ cd vagrant
    $ vagrant up

Next, to log into the Linux instance, run:

    $ vagrant ssh

Congratulations! You've now installed the Linux image, started the VM and are logged into the VM via ssh. If you log out of the Linux instance or close the terminal, the next time you want to use it you only need to run `cd logs_analysis` and `vagrant ssh`.

