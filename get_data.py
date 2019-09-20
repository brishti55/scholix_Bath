import fileinput
import json
import requests

datacite_prefix = '10.15125'  #Bath prefix
repo_name = '* Bath Archive *'
API = 'http://api.scholexplorer.openaire.eu/v2/Links'


def queryAPI():

    hits = 'hits.txt'
    no_hits = 'no_hits.txt'
    json_data = "records.json"

    doi_list = []
    count = 0
    no_link = 0

    j = open(json_data, 'w')
    hit_doi = open(hits, 'w')
    no_doi_found = open(no_hits,'w')

    for doi in fileinput.input():
        doi = doi.rstrip()
        count += 1
        print("###......###\n###  " + str(count) + "  ###\n###......###\n")
        if not doi:
        # do nothing
            break
        payload = {'targetPid': doi}

        # Make API Get request
        r = requests.get(API, params=payload)
        if r.raise_for_status() == None:
            print('Processing doi ' + doi)
            # log.write('Processing doi ' + doi + "\n")

            try:
                json_data = r.json()
            except ValueError:
                print('Invalid JSON')
            else:
                json_string = json.dumps(json_data, indent=4)
                j.write(json_string)
                my_result = json_data['result']

                # Process json output unless empty
                if len(my_result) == 0:
                    no_doi_found.write("No research data found for " + doi + "\n")
                    no_link += 1
                else:
                    doi_list.append(doi)
                    hit_doi.write(doi + "\n")

    print(doi_list)
    print(len(doi_list))
    print('Did not find a link: ' + str(no_link))

    return;

queryAPI()

