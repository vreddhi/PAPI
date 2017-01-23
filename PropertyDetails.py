
class Property(object):
    access_hostname = "NULL"
    name = "NULL"
    version = "NULL"
    notes = "NULL"
    emails = "NULL"
    groupId = "NULL"
    contractId = "NULL"
    propertyId = "NULL"

    def __init__(self,access_hostname,name,version,notes,emails,groupId="NULL",contractId="NULL",propertyId="NULL"):
        self.access_hostname = access_hostname
        self.name = name
        self.version = version
        self.notes = notes
        self.emails = emails
        self.groupId = groupId
        self.contractId = contractId
        self.propertyId = propertyId
