import os               # OS module provides functions for interacting with the operating system.
from flask import Flask # Flask is an lightweight framework in Python to create webapps.
import json             # JSON Module Provides an API which Encode Python objects as JSON strings, and decode JSON strings into Python objects.
import ibm_db           # Python driver for IBM DB2 and IBM Informix databases. Uses the IBM Data Server Driver for ODBC and CLI APIs to connect to IBM DB2 and Informix.

app = Flask(__name__)

if 'VCAP_SERVICES' in os.environ:
    db2info = json.loads(os.environ['VCAP_SERVICES'])['dashDB'][0]  
    db2cred = db2info["credentials"]  
   
   
db2conn = ibm_db.connect("DATABASE="+db2cred['db']+";HOSTNAME="+db2cred['hostname']+";PORT="+str(db2cred['port'])+";UID="+db2cred['username']+";PWD="+db2cred['password']+";","","")  

# main page to dump some environment information  
@app.route('/')
def index():  
   page = '<title>Welcome DB2!</title>'  
   page += '<h1>Sample IBM Bluemix Python Application which connects to dashDB!</h1>'  
   if db2conn:  
    # we have a DB2 connection, so obtain system information via ENV_SYS_INFO:  
    stmt = ibm_db.exec_immediate(db2conn,"select host_name,os_name,os_version,total_cpus,configured_cpus, total_memory,os_kernel_version,os_arch_type, os_release,os_full_version from sysibmadm.env_sys_info")  
    # fetch the result  
    result = ibm_db.fetch_assoc(stmt)  
    page += "OS Name: "+result["OS_NAME"]+"<br/>OS Version: "+result["OS_VERSION"]   
    page += "<br/>Hostname: "+result["HOST_NAME"]+"<br/> Total CPUs: "+str(result["TOTAL_CPUS"])  
    page += "<br/>Configured CPUs: "+str(result["CONFIGURED_CPUS"])+"<br/>Total memory: "+str(result["TOTAL_MEMORY"])+" MB"  
    page += "<br/>OS Kernel Version: "+result["OS_KERNEL_VERSION"]+"<br/>OS Architecture Tpye: "+result["OS_ARCH_TYPE"]  
    page += "<br/>OS Release: "+result["OS_RELEASE"]+"<br/>OS full version: "+result["OS_FULL_VERSION"]  
   return page 


if __name__ == '__main__':
    # Bind to PORT/HOST if defined, otherwise default to 5050/localhost.
    PORT = int(os.getenv('VCAP_APP_PORT', '5050'))
    HOST = str(os.getenv('VCAP_APP_HOST', 'localhost'))
    app.run(host=HOST, port=PORT)