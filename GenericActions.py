import json

class GenericActions(object):
        """All basic operations that can be performed using PAPI """
        final_response = "NULL" #This variable holds the SUCCESS or FAILURE reason
        headers = {
            "Content-Type": "application/json"
        }

        def getPropertyInfo(self,session,propertyObject,groupsInfo):
            """
            Function to fetch property ID and update the proerty object with corresponding values
            """
            for eachDataGroup in groupsInfo.json()['groups']['items']:
                try:
                    contractId = [eachDataGroup['contractIds'][0]]
                    groupId = [eachDataGroup['groupId']]
                    url = 'https://' + propertyObject.access_hostname + '/papi/v0/properties/?contractId=' + contractId[0] +'&groupId=' + groupId[0]
                    propertiesResponse = session.get(url)
                    if propertiesResponse.status_code == 200:
                        propertiesResponseJson = propertiesResponse.json()
                        propertiesList = propertiesResponseJson['properties']['items']
                        for propertyInfo in propertiesList:
                            propertyName = propertyInfo['propertyName']
                            propertyId = propertyInfo['propertyId']
                            propertyContractId = propertyInfo['contractId']
                            propertyGroupId = propertyInfo['groupId']
                            if propertyName == propertyObject.name or propertyName == propertyObject.name + ".xml":
                                #Update the propertyObject attributes with correct values
                                propertyObject.groupId = propertyGroupId
                                propertyObject.contractId = propertyContractId
                                propertyObject.propertyId = propertyId
                                self.final_response = "SUCCESS"
                                return propertyObject
                except KeyError:
                    pass
            #Return the propertyObject as it is without updated information
            self.final_response = "FAILURE"
            return propertyObject


        def getGroups(self,session,propertyObject):
            """
            Function to fetch all the groups under the contract
            """
            groupUrl = 'https://' + propertyObject.access_hostname + '/papi/v0/groups/'
            groupResponse = session.get(groupUrl)
            if groupResponse.status_code == 200:
                self.final_response = "SUCCESS"
                return groupResponse
            else:
                self.final_response = "FAILURE"

        def getPropertyRules(self,session,propertyObject):
            """
            Function to download rules from a property
            """
            rulesUrl = 'https://' + propertyObject.access_hostname  + '/papi/v0/properties/' + propertyObject.propertyId +'/versions/'+str(propertyObject.version)+'/rules/?contractId='+propertyObject.contractId+'&groupId='+propertyObject.groupId
            rulesResponse = session.get(rulesUrl)
            if rulesResponse.status_code == 200:
                self.final_response = "SUCCESS"
            else:
                self.final_response = rulesResponse.json()['detail']
            return rulesResponse

        def createVersion(self,session,propertyObject,baseVersion):
            """
            Function to create or checkout a version of property
            """
            newVersionData = """
            {
                "createFromVersion": %s
            }
            """ % (baseVersion)
            createVersionUrl = 'https://' + propertyObject.access_hostname + '/papi/v0/properties/' + propertyObject.propertyId + '/versions/?contractId=' + propertyObject.contractId + '&groupId=' + propertyObject.groupId
            createVersionResponse = session.post(createVersionUrl, data=newVersionData,headers=self.headers)
            if createVersionResponse.status_code == 201:
                self.final_response = "SUCCESS"
            return createVersionResponse

        def getVersion(self,session,propertyObject,activeOn="LATEST"):
            """
            Function to get the latest or staging or production version
            """
            if activeOn == "LATEST":
                VersionUrl = 'https://' + propertyObject.access_hostname + '/papi/v0/properties/' + propertyObject.propertyId + '/versions/latest?contractId=' + propertyObject.contractId +'&groupId=' + propertyObject.groupId
            elif activeOn == "STAGING":
                VersionUrl = 'https://' + propertyObject.access_hostname + '/papi/v0/properties/' + propertyObject.propertyId + '/versions/latest?contractId=' + propertyObject.contractId +'&groupId=' + propertyObject.groupId + '&activatedOn=STAGING'
            elif activeOn == "PRODUCTION":
                VersionUrl = 'https://' + propertyObject.access_hostname + '/papi/v0/properties/' + propertyObject.propertyId + '/versions/latest?contractId=' + propertyObject.contractId +'&groupId=' + propertyObject.groupId + '&activatedOn=PRODUCTION'
            VersionResponse = session.get(VersionUrl)
            return VersionResponse

        def uploadRules(self,session,propertyObject,updatedData):
            """
            Function to upload rules to a property
            """
            updateurl = 'https://' + propertyObject.access_hostname  + '/papi/v0/properties/'+ propertyObject.propertyId + "/versions/" + str(propertyObject.version) + '/rules/' + '?contractId=' + propertyObject.contractId +'&groupId=' + propertyObject.groupId
            updatedData = json.dumps(updatedData)
            updateResponse = session.put(updateurl,data=updatedData,headers=self.headers)
            if updateResponse.status_code == 403:
                print("Property cannot be updated due to reasons")
            elif updateResponse.status_code == 404:
                print("The requested property version is not available")
            elif updateResponse.status_code == 200:
                self.final_response == "SUCCESS"
                print("Bingo.... Property is updated")
            return updateResponse

        def activateConfiguration(self,session,propertyObject):
            """
            Function to activate a configuration or property
            """
            emails = []
            emails.append(propertyObject.emails)
            emails = json.dumps(emails)
            activationDetails = """
                 {
                    "propertyVersion": %s,
                    "network": "STAGING",
                    "note": "%s",
                    "notifyEmails": %s
                } """ % (propertyObject.version,propertyObject.notes,emails)
            actUrl  = 'https://' + propertyObject.access_hostname + '/papi/v0/properties/'+ propertyObject.propertyId + '/activations/?contractId=' + propertyObject.contractId +'&groupId=' + propertyObject.groupId
            activationResponse = session.post(actUrl, data=activationDetails, headers=self.headers)
            try:
                if activationResponse.status_code == 400 and activationResponse.json()['detail'].find('following activation warnings must be acknowledged'):
                    acknowledgeWarnings = []
                    print("Following are the WARNINGS...\n")
                    for eachWarning in activationResponse.json()['warnings']:
                        print("WARNING: " + eachWarning['detail'])
                        acknowledgeWarnings.append(eachWarning['messageId'])
                        acknowledgeWarningsJson = json.dumps(acknowledgeWarnings)
                    acknowledged = input("\nPress 1 if you acknowledge the warnings.\n")
                    if acknowledged == "1":
                        #acknowledgeWarnings = json.dumps(acknowledgeWarnings)
                        #The details has to be within the three double quote or comment format
                        updatedactivationDetails = """
                             {
                                "propertyVersion": %s,
                                "network": "STAGING",
                                "note": "%s",
                                "notifyEmails": %s,
                                "acknowledgeWarnings": %s
                            } """ % (propertyObject.version,propertyObject.notes,emails,acknowledgeWarningsJson)
                        updatedactivationResponse = session.post(actUrl,data=updatedactivationDetails,headers=self.headers)
                        print("Please wait while we activate the config for you.. Hold on... \n")
                        if updatedactivationResponse.status_code == 201:
                            print("Here is the activation link, that can be used to track\n")
                            print(updatedactivationResponse.json()['activationLink'])
                            self.final_response = "SUCCESS"
                        else:
                            self.final_response = "FAILURE"
                            print(updatedactivationResponse.json())
                elif activationResponse.status_code == 422 and activationResponse.json()['detail'].find('version already activated'):
                    print("Property version already activated")
            except KeyError:
                self.final_response = "FAILURE"
                print("Looks like there is some error in configuration\n")
