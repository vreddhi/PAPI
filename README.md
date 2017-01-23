# PAPI
Three files bake the cake !!

**GenericActions.py**
All basic operations that can be performed using PAPI
The class defines following functions:

 - getPropertyInfo 
 - getGroups 
 - getPropertyRules 
 - getVersion 
 - createVersion 
 - uploadRules
 -  activateConfiguration

**PropertyDetails.py**
This class defines the basic properties of a configuration or akamai property.

**main.py**
This file does the job of reading the credentials, establish connections and invoke methods from GenericActions.py.

**Steps to use OR brief understanding :**

 1. Create and object of type PropertyDetails. This initialises the
    necessary property details. 
 2. Create an object of type GenericActions,which should be used to call methods in it. 
 3. Use the methods/functions defined in GenericActions in desired order to achieve the custom functionality. 

***NOTE:*** You will need PropertyDetails Object in all methods, as it operates on attributes     of property.
