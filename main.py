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
parser.add_argument("-act","--activate", help="Activate configuration specified in property_name in .config.txt", action="store_true")
parser.add_argument("-copy","--copyrules", help="Used to copy source configuration to destination configuration", action="store_true")
parser.add_argument("-d","--download", help="Download configuration and display JSON in console", action="store_true")
args = parser.parse_args()



try:
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
    session = requests.Session()
    session.auth = EdgeGridAuth(
    			client_token = client_token,
    			client_secret = client_secret,
    			access_token = access_token
                )
    if args.copyrules:
        #Optionally read these config values if we are copying the rules
        dest_property_name = config['PROPERTY']['dest_property_name']
        dest_version = config['PROPERTY']['dest_version']
        dest_notes = config['PROPERTY']['dest_notes']
        dest_emails = config['PROPERTY']['dest_emails']
        dest_client_token = config['CREDENTIALS']['dest_client_token']
        dest_client_secret = config['CREDENTIALS']['dest_client_secret']
        dest_access_token = config['CREDENTIALS']['dest_access_token']
        dest_access_hostname = config['CREDENTIALS']['dest_access_hostname']
        destSession = requests.Session()
        destSession.auth = EdgeGridAuth(
        			client_token = dest_client_token,
        			client_secret = dest_client_secret,
        			access_token = dest_access_token
        )
except (NameError,AttributeError):
    print("\nUse -h to know the options to run program\n")
    exit()

if not args.copyrules and not args.download and not args.activate:
    print("\nUse -h to know the options to run program\n")
    exit()


if args.activate:
    print("\nHang on... while we activate configuration.. This will take time..")
    propertyObject = PropertyDetails.Property(access_hostname, property_name, version, notes, emails)
    genericActionsObject = GenericActions.GenericActions()
    genericActionsObject.activateConfiguration(session, propertyObject)

if args.copyrules:
    #Initialise Source Property Information
    print("\nHang on... while we copy rules.. This will take time..")
    sourcePropertyObject = PropertyDetails.Property(access_hostname, property_name, version, notes, emails)
    genericActionsObject = GenericActions.GenericActions()
    sourceGroupsInfo = genericActionsObject.getGroups(session, sourcePropertyObject)
    genericActionsObject.getPropertyInfo(session, sourcePropertyObject, sourceGroupsInfo)
    sourcePropertyRules = genericActionsObject.getPropertyRules(session, sourcePropertyObject).json()['rules']
    #Initialise destination Property Information
    destPropertyObject = PropertyDetails.Property(dest_access_hostname, dest_property_name, dest_version, dest_notes, dest_emails)
    destGroupsInfo = genericActionsObject.getGroups(destSession, destPropertyObject)
    genericActionsObject.getPropertyInfo(destSession, destPropertyObject, destGroupsInfo)
    destPropertyRules = genericActionsObject.getPropertyRules(destSession, destPropertyObject).json()
    destPropertyRules['rules'] = sourcePropertyRules
    genericActionsObject.uploadRules(destSession, destPropertyObject, destPropertyRules)

if args.download:
    print("\nHang on... while we download the json data.. This will take time..")
    propertyObject = PropertyDetails.Property(access_hostname, property_name, version, notes, emails)
    genericActionsObject = GenericActions.GenericActions()
    groupsInfo = genericActionsObject.getGroups(session, propertyObject)
    genericActionsObject.getPropertyInfo(session, propertyObject, groupsInfo)
    rulesObject = genericActionsObject.getPropertyRules(session, propertyObject)
    print(json.dumps(rulesObject.json()['rules']))
