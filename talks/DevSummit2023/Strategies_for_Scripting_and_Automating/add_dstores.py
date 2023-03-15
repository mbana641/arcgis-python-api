from arcgis import GIS

gis = GIS(profile="your_profile", verify_cert=False)

# use the federation to get Server ids for the servers in the organization's federation
servers_dict = gis.admin.federation.servers
server_list = servers_dict["servers"]
host_id = [srvr["id"] for srvr in server_list if srvr["serverRole"] == "HOSTING_SERVER"][0]
nb_id = [srvr["id"] for srvr in server_list if srvr["serverFunction"] == "NotebookServer"][0]

# use the ServerManager to get the hosting server Server object and use the datastores
# property to get that Server's DatastoreManager
host = gis.admin.servers.get(role="HOSTING_SERVER")[0]
host_dsmgr = host.datastores

# Mac
conn_file_sql = r"/path/to/your/egdb/connection_file.sde"
conn_string_sql = host_dsmgr.generate_connection_string(conn_file_sql)

# create the text parameter for the datastore item
# Data Store: items https://enterprise.arcgis.com/en/portal/latest/use/data-store-items.htm
# Data Item: https://developers.arcgis.com/rest/enterprise-administration/server/dataitem.htm
# Portal datastore Rest: https://developers.arcgis.com/rest/users-groups-and-items/datastore.htm
# Example: https://developers.arcgis.com/rest/users-groups-and-items/add-item.htm#GUID-19C2C3E8-704C-4420-B09E-B78A681CE33C

text_param = {"info": {"isManaged": "false",
                       "dataStoreConnectionType": "shared",
                       "connectionString": conn_string_sql},
              "type": "egdb",
              "path": "/enterpriseDatabases/sql_server_datastore_item"}

# add a datastore item
item_properties = {"title": "Sql Server Datastore Item API",
                   "type": "Data Store",
                   "tags": "api_created,datastore_item,bulk_publishing",
                   "snippet": "Adding a datastore item to use api for management."}

ds_item = gis.content.add(item_properties=item_properties,
                          text=text_param)

# datastore property returns an instance of PortalDataStore
p_ds = gis.datastore

# validate the data store item can be connected to before registering
validation_state = p_ds.validate(server_id=host_id,
                                 item=ds_item)

# use portal datastore to register the item with the host server
p_ds.register(item=ds_item,
              server_id=host_id,
              bind=False)

print("...Script complete.")
