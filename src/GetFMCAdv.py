#!/usr/bin/env python
# -*- coding: UTF-8 -*-# enable debugging

#print """
#--------------------
#Copyright (c) 2019 Cisco and/or its affiliates.
#This software is licensed to you under the terms of the Cisco Sample
#Code License, Version 1.0 (the "License"). You may obtain a copy of the
#License at
#               https://developer.cisco.com/docs/licenses
#
#All use of the material herein must be in accordance with the terms of
#the License. All rights not expressly granted by the License are
#reserved. Unless required by applicable law or agreed to separately in
#writing, software distributed under the License is distributed on an "AS
#IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#or implied.
#---------------------
#"""

__author__ = "Dirk Woellhaf <dwoellha@cisco.com>"
__contributors__ = [
    "Dirk Woellhaf <dwoellha@cisco.com>"
]
__copyright__ = "Copyright (c) 2019 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.0"

import requests
import json
import time
import ConfigParser
import base64
import logging
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def FMC_Login(Settings):
  #print "FMC Login..."
  server = "https://"+Settings["FMC_IP"]
  
  r = None
  headers = {'Content-Type': 'application/json'}
  api_auth_path = "/api/fmc_platform/v1/auth/generatetoken"
  auth_url = server + api_auth_path
  r = requests.post(auth_url, headers=headers, auth=requests.auth.HTTPBasicAuth(Settings["FMC_USER"], Settings["FMC_PWD"]), verify=False)
  if r.status_code != 204:
    print "FMC Login failed. "+str(headers)+" "+r.text
    sys.exit()
    
  return r.headers["X-auth-access-token"]

def FMC_Logout(Settings):
    #print "FMC Logout..."
    api_path = "/api/fmc_platform/v1/auth/revokeaccess"
    # Create custom header for revoke access
    headers = {'X-auth-access-token' : Settings["FMC_X-auth-access-token"]}
    # log in to API
    post_response = requests.post("https://"+str(Settings["FMC_IP"])+api_path, headers=headers, verify=False)
    if post_response.status_code != 204:
      #print "FMC Logout succesful. Token: "+str(headers["X-auth-access-token"])
      print "FMC Logout failed. "+str(headers)+" "+post_response.text

def FMC_Get(Settings, api_path):
  server = "https://"+Settings["FMC_IP"]
  url = server + api_path
  if (url[-1] == '/'):
      url = url[:-1]
  headers = {'X-auth-access-token' : Settings["FMC_X-auth-access-token"]}
  try:
      # REST call with SSL verification turned off:
      r = requests.get(url, headers=headers, verify=False)
      status_code = r.status_code
      resp = r.text
      json_resp = json.loads(resp)
      if (status_code == 200):
          #print("GET successful. Response data --> ")
          return json_resp
      else:
          r.raise_for_status()
          print("Error occurred in GET")
          print json_resp["error"]["severity"]+": "+json_resp["error"]["messages"][0]["description"]
  except requests.exceptions.HTTPError as err:
      print ("Error in connection --> "+str(err))
      print ("Error occurred in GET")
      print json_resp["error"]["severity"]+": "+json_resp["error"]["messages"][0]["description"]
  finally:
      if r : r.close()
      
def FMC_Put(Settings, fmc_data, api_path):
  server = "https://"+Settings["FMC_IP"]

  url = server + api_path
  if (url[-1] == '/'):
      url = url[:-1]
  headers = {'X-auth-access-token' : Settings["FMC_X-auth-access-token"]}
  r = requests.put(url, json=fmc_data, headers=headers, verify=False)
  status_code = r.status_code
  resp = r.text
  if status_code == 200 or status_code == 201 or status_code == 202:
      json_resp = json.loads(resp)
      if "id" in json_resp:
        #print "FMC POST succesful for Object "+json_resp["id"]
        return json_resp["id"]




def GetDevices(Settings):
    Devices = FMC_Get(Settings, "/api/fmc_config/v1/domain/default/devices/devicerecords?expanded=true")
    if "items" in Devices:
        print "fmc,hostname="+Settings["FMC_IP"]+" Devices="+str(Devices["paging"]["count"])
    else:
        print "fmc,hostname="+Settings["FMC_IP"]+" Devices=0"

def GetDeployableDevices(Settings):
    DeployableDevices = FMC_Get(Settings, "/api/fmc_config/v1/domain/default/deployment/deployabledevices")
    if "items" in DeployableDevices:
        print "fmc,hostname="+Settings["FMC_IP"]+" DeployableDevices="+str(len(DeployableDevices["items"]))
    else:
        print "fmc,hostname="+Settings["FMC_IP"]+" DeployableDevices=0"

def GetDeviceGroups(Settings):
    DeviceGroups = FMC_Get(Settings, "/api/fmc_config/v1/domain/default/devicegroups/devicegrouprecords")
    if "items" in DeviceGroups:
        print "fmc,hostname="+Settings["FMC_IP"]+" DeviceGroups="+str(len(DeviceGroups["items"]))
    else:
        print "fmc,hostname="+Settings["FMC_IP"]+" DeviceGroups=0"

def GetHAPairs(Settings):
    HAPairs = FMC_Get(Settings, "/api/fmc_config/v1/domain/default/devicehapairs/ftddevicehapairs")
    if "items" in HAPairs:
        print "fmc,hostname="+Settings["FMC_IP"]+" HAPairs="+str(len(HAPairs["items"]))
    else:
        print "fmc,hostname="+Settings["FMC_IP"]+" HAPairs=0"

def GetUpgradePackages(Settings):
    UpgradePackages = FMC_Get(Settings, "/api/fmc_platform/v1/updates/upgradepackages")
    if "items" in UpgradePackages:
        print "fmc,hostname="+Settings["FMC_IP"]+" UpgradePackages="+str(len(UpgradePackages["items"]))
    else:
        print "fmc,hostname="+Settings["FMC_IP"]+" UpgradePackages=0"

def GetDeviceID(Settings):
  #Devices = FMC_Get(Settings, "/api/fmc_config/v1/domain/default/devicehapairs/ftddevicehapairs")
  Devices = FMC_Get(Settings, "/api/fmc_config/v1/domain/default/devices/devicerecords?expanded=true")

  for Device in Devices["items"]:
    #print Device
    if Settings["FMC_DEVICE"] == Device["name"]:
      print Device["id"]
      return Device["id"]

def GetACP(Settings):
    ACP = FMC_Get(Settings, "/api/fmc_config/v1/domain/default/policy/accesspolicies")
    if "items" in ACP:
        print "fmc,hostname="+Settings["FMC_IP"]+" ACP="+str(len(ACP["items"]))
    else:
        print "fmc,hostname="+Settings["FMC_IP"]+" ACP=0"

def GetNetworks(Settings):
    NET = FMC_Get(Settings, "/api/fmc_config/v1/domain/default/object/networks")
    if "items" in NET:
        print "fmc,hostname="+Settings["FMC_IP"]+" Networks="+str(len(NET["items"]))
    else:
        print "fmc,hostname="+Settings["FMC_IP"]+" Networks=0"

def GetHosts(Settings):
    HOST = FMC_Get(Settings, "/api/fmc_config/v1/domain/default/object/hosts")
    if "items" in HOST:
        print "fmc,hostname="+Settings["FMC_IP"]+" Hosts="+str(len(HOST["items"]))
    else:
        print "fmc,hostname="+Settings["FMC_IP"]+" Hosts=0"

def GetAccessPolicies(Settings):
  AccessPolicies = FMC_Get(Settings, "/api/fmc_config/v1/domain/default/policy/accesspolicies")

  for AccessPolicy in AccessPolicies["items"]:
    #print AccessPolicy["name"]
    if Settings["FMC_ACPNAME"] == AccessPolicy["name"]:
      return AccessPolicy["id"]

def RefreshHitCounts(Settings):
    Refresh = FMC_Put(Settings, "", '/api/fmc_config/v1/domain/default/policy/accesspolicies/'+Settings["FMC_ACPID"]+'/operational/hitcounts?filter=deviceId:'+Settings["FMC_DEVICEID"])
    #print "Refreshing Hit Counts. Waiting 5sec."
    time.sleep(5)

def GetHitCounts(Settings):
    Settings["FMC_DEVICEID"] = GetDeviceID(Settings)
    Settings["FMC_ACPID"] = GetAccessPolicies(Settings)
    RefreshHitCounts(Settings)    
    HitCounts = FMC_Get(Settings, "/api/fmc_config/v1/domain/default/policy/accesspolicies/"+Settings["FMC_ACPID"]+"/operational/hitcounts?filter=deviceId:"+Settings["FMC_DEVICEID"]+"&expanded=true")
    #t = PrettyTable(['Nr#', 'Name', 'Last Fetch', 'Last Hit', 'Hit Count'])
    TotalHits=0
    for Hits in HitCounts["items"]:
        TotalHits += Hits["hitCount"]
        print "fmc,hostname="+Settings["FMC_IP"]+",acp="+Settings["FMC_ACPNAME"]+",rule="+Hits["rule"]["name"].replace(" ", "_")+" Hits="+str(Hits["hitCount"])
        #t.add_row([Hits["metadata"]["ruleIndex"],Hits["rule"]["name"], Hits["lastFetchTimeStamp"], Hits["lastHitTimeStamp"], Hits["hitCount"]])
    
    #t.add_row(["..","Total Hits", Hits["lastFetchTimeStamp"], "", TotalHits])

    #print t
    print "fmc,hostname="+Settings["FMC_IP"]+",acp="+Settings["FMC_ACPNAME"]+" TotalHits="+str(TotalHits)

if __name__ == "__main__":
    Settings={}

    Settings["FMC_IP"] = "devnet-fmc-01"
    Settings["FMC_USER"] = "devnet-api-01"
    Settings["FMC_PWD"] = "devnet123"
    Settings["FMC_VERSION"] = 6.4

    Settings["FMC_ACPNAME"] = "DevNet.Pol"
    Settings["FMC_DEVICE"] = "DevNet-FTD-01"


    #print "Login..."
    Settings["FMC_X-auth-access-token"] = FMC_Login(Settings)

    GetDevices(Settings)      
    GetDeployableDevices(Settings)
    GetDeviceGroups(Settings)
    #GetHAPairs(Settings)
    GetUpgradePackages(Settings)
    GetACP(Settings)
    GetNetworks(Settings)
    GetHosts(Settings)
#    if Settings["FMC_VERSION"] > 6.3:
#      GetHitCounts(Settings)

    FMC_Logout(Settings)
