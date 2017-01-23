# PAPI
Three files bake the cake !!

**GenericActions.py**
All basic operations that can be performed using PAPI
The class defines following functions:

 - getPropertyInfo - Function to fetch property ID and update the proerty object with corresponding values
 - getGroups - Function to fetch all the groups under the contract
 - getPropertyRules - Function to download rules from a property
 - getVersion - Function to get the latest or staging or production version
 - createVersion - Function to create or checkout a version of property
 - uploadRules - Function to upload rules to a property
 - activateConfiguration - Function to activate a configuration or property

**PropertyDetails.py**
This class defines the basic properties of a configuration or akamai property.

**main.py**
This file does the job of reading the credentials, establish connections and invoke methods from GenericActions.py.

**How to Run the program**
python3 main.py -h (This will give all options available)
python3 main.py -copy (Copied rules from source config to destination configuration)
python3 main.py -download (Downloads the rules and displays in console)
python3 main.py - activate (Activates the configuration)
**NOTE** : The cnofiguration details are read from .config.txt file. Contact developer to know the format.

**Steps to use OR brief understanding :**

 1. Create and object of type PropertyDetails. This initialises the
    necessary property details. 
 2. Create an object of type GenericActions,which should be used to call methods in it. 
 3. Use the methods/functions defined in GenericActions in desired order to achieve the custom functionality. 

***NOTE:*** You will need PropertyDetails Object in all methods, as it operates on attributes     of property.
