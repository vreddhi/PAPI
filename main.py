import PropertyDetails
import GenericActions
import configparser
import requests, logging, json, sys
from akamai.edgegrid import EdgeGridAuth
import urllib
import json
import argparse

#Program start here

parser = argparse.ArgumentParser()
parser.add_argument("-i","--interactive", help="Enter yes to pass the below arguments OR no to read it from file specified in -cf option")
parser.add_argument("-ct","--client_token", help="Enter the client_token")
parser.add_argument("-cs","--client_secret", help="Enter the client_secret")
parser.add_argument("-at","--access_token", help="Enter the access_token")
parser.add_argument("-ah","--access_hostname", help="Enter the access_hostname")
parser.add_argument("-pn","--property_name", help="Enter the property_name")
parser.add_argument("-v","--version", help="Enter the version")
parser.add_argument("-cf","--Config_file", help="Enter the configuration file")
args = parser.parse_args()
try:
    if args.interactive != "yes":
        config = configparser.ConfigParser()
        config.read('.config.txt')
        property_name = config['PROPERTY']['property_name']
        version = config['PROPERTY']['version']
        notes = config['PROPERTY']['notes']
        emails = config['PROPERTY']['emails']
        client_token = config['CREDENTIALS']['client_token']
        client_secret = config['CREDENTIALS']['client_secret']
        access_token = config['CREDENTIALS']['access_token']
        access_hostname = config['CREDENTIALS']['access_hostname']
        dest_property_name = config['PROPERTY']['dest_property_name']
        dest_version = config['PROPERTY']['dest_version']
        dest_notes = config['PROPERTY']['dest_notes']
        dest_emails = config['PROPERTY']['dest_emails']
        dest_client_token = config['CREDENTIALS']['dest_client_token']
        dest_client_secret = config['CREDENTIALS']['dest_client_secret']
        dest_access_token = config['CREDENTIALS']['dest_access_token']
        dest_access_hostname = config['CREDENTIALS']['dest_access_hostname']
except NameError:
    print("Use -h to know the options to run program")
    exit()



session = requests.Session()
session.auth = EdgeGridAuth(
			client_token = client_token,
			client_secret = client_secret,
			access_token = access_token
            )

destSession = requests.Session()
destSession.auth = EdgeGridAuth(
			client_token = dest_client_token,
			client_secret = dest_client_secret,
			access_token = dest_access_token
)

sourcePropertyObject = PropertyDetails.Property(access_hostname, property_name, version, notes, emails)
GenericActionsObject = GenericActions.GenericActions()
sourceGroupsInfo = GenericActionsObject.getGroups(session, sourcePropertyObject)
sourcePropertyObject = GenericActionsObject.getPropertyInfo(session, sourcePropertyObject, sourceGroupsInfo)
if GenericActionsObject.final_response == "SUCCESS":
    sourcePropertyRules = GenericActionsObject.getPropertyRules(session, sourcePropertyObject).json()['rules']
destPropertyObject = PropertyDetails.Property(dest_access_hostname, dest_property_name, dest_version, dest_notes, dest_emails)
destGroupsInfo = GenericActionsObject.getGroups(destSession, destPropertyObject)
destPropertyObject = GenericActionsObject.getPropertyInfo(destSession, destPropertyObject, destGroupsInfo)
destPropertyRules = GenericActionsObject.getPropertyRules(destSession, destPropertyObject).json()
destPropertyRules['rules'] = sourcePropertyRules
GenericActionsObject.uploadRules(destSession, destPropertyObject, destPropertyRules)

#propertyObject = PropertyDetails.Property(access_hostname,property_name,version,notes,emails)
#genericActionsObject = GenericActions.GenericActions()
#groupsInfo = genericActionsObject.getGroups(session,propertyObject)
#propertyObject = genericActionsObject.getPropertyInfo(session, propertyObject, groupsInfo)
#propertyRules = genericActionsObject.getPropertyRules(session, propertyObject)
#genericActionsObject.uploadRules(session, propertyObject)
#actPropertyObject = genericActionsObject.activateConfiguration(session, propertyObject)
