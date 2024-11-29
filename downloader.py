
import requests
import subprocess
from datetime import datetime, timedelta


def runcmd(cmd, verbose = False, *args, **kwargs):

    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass


zone ="a"
zone = str(input("hemisphere Nord Sud ou tout ?"))

if zone == "nord" :
    toplat = "90"
    bottomlat = "0"
elif zone == "sud" : 
    toplat = "0"
    bottomlat = "-90"
else : 
    toplat = "90"
    bottomlat = "-90"



baseURL = 'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t'
productListURL = str("&lev_10_m_above_ground=on&var_UGRD=on&var_VGRD=on&leftlon=0&rightlon=360&toplat=" + toplat + "&bottomlat=" + bottomlat + "&dir=%2Fgfs.")
 
today = datetime.today()
D = today.strftime("%Y%m%d")
hour = datetime.utcnow() - timedelta(hours = 3)
print(hour)
H = hour.strftime("%H")
Hrun = 00
if 0 < int(H) <= 6 :
    Hrun == "00"
elif 6 < int(H) <= 12 :
    Hrun == "06"
elif 12 < int(H) <= 18 :
    Hrun = "12"
else :
    Hrun = "18"
    yesterday = today - timedelta(days = 1)
    D = yesterday.strftime("%Y%m%d")
runcmd("del merged.grb2")
for i in range(0, 385) : 
    if 0 <= i <= 9 :
        number = str("00" + str(i))
    elif 10 <= i <= 99 :
        number = str("0" + str(i))
    else :
        number = str(i)
    url = str(baseURL + Hrun + 'z.pgrb2.0p25.f' + number + productListURL + D + "%2F" + Hrun + "%2Fatmos")
    print(url)
 
    response = requests.get(url)

    with open(str("tomerge." + number + ".grb2"), mode="wb") as file:
        file.write(response.content)


runcmd("type tomerge* > merged.grb2")
runcmd("del tomerge*")