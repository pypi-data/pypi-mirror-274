<h1 align="center">
  Godork - Scrape Google search quickly
</h1>

<div align="center">
  <img src="assets/images/godork-logo.png" alt="godork" width="300px">
  <br>
</div>

<p align="center">
  <a href="https://python.org"><img src="https://img.shields.io/badge/Built%20with-Python-Blue"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-_red.svg"></a>
  <a href="https://github.com/thd3r/godork/issues"><img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat"></a>
</p>

<p align="center">
  <a href="#installation-instructions">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#running-godork">Run</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#support">Support</a>
</p>

**godork** can scrape results from google searches quickly by using the [asyncio](https://docs.python.org/3/library/asyncio.html) library which uses **cooperative multitasking** in combination with [aiohttp](https://docs.aiohttp.org)

# Installation

**godork** requires **python 3.8** or higher to install successfully. Run the following command to get the repo:

```sh
git clone https://github.com/thd3r/godork.git && python3 -m pip install -r requirements.txt
```

# Usage

```sh
python3 godork.py -help
```

### This will display help for the tool. Here are all the switches it supports.


```console
                __         __  
  ___ ____  ___/ /__  ____/ /__
 / _ `/ _ \/ _  / _ \/ __/  '_/
 \_, /\___/\_,_/\___/_/ /_/\_\ 
/___/                                                                                                            
        v1.2.0 - @thd3r

usage: godork [ --query [default arguments] ] [ arguments ] 

Options:
  -help         show this help message and exit
  -version      show program's version number and exit
  -query QUERY  search query
  -sleep        use this option to prevent banning
  -proxy PROXY  http proxy to use with godork (eg http://127.0.0.1:8080) 
```

# Running godork

## Scrape

### It will run its tool to scrape titles and links from google search

```console
godork -query "site:*.gov"

                __         __  
  ___ ____  ___/ /__  ____/ /__
 / _ `/ _ \/ _  / _ \/ __/  '_/
 \_, /\___/\_,_/\___/_/ /_/\_\ 
/___/                                                                                                            
        v1.2.0 - @thd3r

[INF] Enumerating now for site:*.gov querys

Florida Board of Nursing - Licensing, Renewals & Information [https://floridasnursing.gov/]
SAM.gov | Home [https://floridasnursing.gov/]
Consumer Financial Protection Bureau [https://floridasnursing.gov/]
New Mexico Department of Workforce Solutions > Home [https://floridasnursing.gov/]
City of Philadelphia [https://floridasnursing.gov/]
Minnesota Unemployment Insurance / Unemployment Insurance ... [https://floridasnursing.gov/]
Bureau of Labor Statistics [https://floridasnursing.gov/]
Maryland Health Connection: Home [https://floridasnursing.gov/]
New York Lottery: Official Site [https://floridasnursing.gov/]
Home | The Thrift Savings Plan (TSP) [https://floridasnursing.gov/]
U.S. Census Bureau [https://www.sba.gov/]
Small Business Administration [https://www.sba.gov/]
Department of Energy [https://www.sba.gov/]
Department of Workforce Services [https://www.sba.gov/]
Internal Revenue Service | An official website of the United States ... [https://www.sba.gov/]
Saint Lucie County Property Appraiser | Our Promise to You ... [https://www.sba.gov/]
HRSA: Health Resources and Services Administration [https://www.sba.gov/]
VA Careers [https://www.sba.gov/]
The Official Web Site for The State of New Jersey [https://www.sba.gov/]
Georgia Department of Public Health [https://www.sba.gov/]
Illinois.gov - IL Application for Benefits Eligibility (ABE) ABE Home ... [https://www.ice.gov/]
Welcome to Medicare | Medicare [https://www.ice.gov/]
ICE | U.S. Immigration and Customs Enforcement [https://www.ice.gov/]
City of Cleveland Ohio: Home [https://www.ice.gov/]
Philadelphia Water Department [https://www.ice.gov/]
U.S. Department of Defense [https://www.ice.gov/]
Connecticut Judicial Branch [https://www.ice.gov/]
Recreation.gov - Camping, Cabins, RVs, Permits, Passes & More [https://www.ice.gov/]
Washington State's Paid Family and Medical Leave – Washington ... [https://www.ice.gov/]
Arizona Department of Health Services [https://www.ice.gov/]
Search - SAM.gov [https://www.coloradosos.gov/]
U.S. Embassy & Consulates in Japan: Homepage [https://www.coloradosos.gov/]
ILCC [https://www.coloradosos.gov/]
Colorado Secretary of State [https://www.coloradosos.gov/]
City of Detroit | Opportunity Rising [https://www.coloradosos.gov/]
Información de Salud de la Biblioteca Nacional de ... - MedlinePlus [https://www.coloradosos.gov/]
USCIS | myUSCIS Home Page [https://www.coloradosos.gov/]
West Virginia Legislature [https://www.coloradosos.gov/]
Iowa Child Support - Home [https://www.coloradosos.gov/]
Missing Mail and Lost Packages - USPS [https://www.coloradosos.gov/]
Missing Mail and Lost Packages - USPS [https://www.usa.gov/holidays]
What We Investigate - FBI [https://www.usa.gov/holidays]
Fossil - Department of Energy [https://www.usa.gov/holidays]
Emphysema Symptoms | Emphysema Treatment - MedlinePlus [https://www.usa.gov/holidays]
American holidays | USAGov [https://www.usa.gov/holidays]
Home : Occupational Outlook Handbook - Bureau of Labor Statistics [https://www.usa.gov/holidays]
Guide to Good Posture - MedlinePlus [https://www.usa.gov/holidays]
Antibiotics - MedlinePlus [https://www.usa.gov/holidays]
NASA TV Live [https://www.usa.gov/holidays]
Contact Us | The White House [https://www.usa.gov/holidays]
How the president is elected | USAGov [https://www.azed.gov/esa]
Welcome to the Texas Secretary of State [https://www.azed.gov/esa]
Viral Infection - Viruses - MedlinePlus [https://www.azed.gov/esa]
Fever treatment: Quick guide to treating a fever - Mayo Clinic [https://www.azed.gov/esa]
Diabetic Foot | MedlinePlus [https://www.azed.gov/esa]
Empowerment Scholarship Account | Arizona Department of Education [https://www.azed.gov/esa]
Hormones | Endocrine Glands - MedlinePlus [https://www.azed.gov/esa]
Saturn - NASA Science [https://www.azed.gov/esa]
Welcome Applicants! - Minnesota Unemployment Insurance [https://www.azed.gov/esa]
Staphylococcal Infections - MedlinePlus [https://www.azed.gov/esa]

[INF] Saving results to file /tmp/godork/output/2024-05-20-16:45:10_godork.json
[INF] Found 60 links in 0.664 seconds
```

# Documentation

Documentation is available at https://thd3r.github.io

# Support

Support me on teste