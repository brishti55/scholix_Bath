import fileinput
import json
import requests

datacite_prefix = '10.15125'  #Bath prefix
repo_name = '* Bath Archive *'
API = 'http://api.scholexplorer.openaire.eu/v2/Links'

dois_found = []
json_data = "records.json"
links = 'links.tsv'
logfile = 'log.txt'
bath_doi = 'bath.txt'
non_bath_doi = 'non_bath.txt'
doi_links = {}
count = 0

print('opening file for JSON records: ' + json_data)
j = open(json_data, 'w')
links_tsv = open(links, 'w')
# bib = open(citations,  'w')
log = open(logfile, 'w')
bath = open(bath_doi, 'w')
non_bath = open(non_bath_doi, 'w')

# For DOIs in input file write json output
for doi in fileinput.input():
    doi = doi.rstrip()
    count += 1
    print("###......###\n###  " + str(count ) + "  ###\n###......###\n")
    if not doi:
        #do nothing
        print('found empty line...ignored')
        break
    payload = {'targetPid': doi}
    # Make API Get request
    r = requests.get(API, params=payload)
    if r.raise_for_status() == None:
        print('Processing doi ' + doi)
        log.write('Processing doi ' + doi +"\n")

        try:
            json_data = r.json()
        except ValueError:
            print('Invalid JSON')
            log.write("........Invalid JSON")
        else:
            json_string = json.dumps(json_data, indent=4)
            j.write(json_string)
            my_result = json_data['result']

            # Process json output unless empty
            if len(my_result) == 0:
                log.write("No research data found for research output DOI \n")
            else:
                for data in my_result:
                    source = data['source']
                    obj_type = source['Type']
                    if obj_type == 'dataset':
                        title = source['Title']
                        # log.write((title).encode('utf-8'))
                        creator_list = source['Creator'] #list of creators
                        pub_list = source['Publisher'] #list of pubs
                        pub_names = ""
                        for index in range(len(pub_list)):
                            pub_names = pub_names + pub_list[index]['name'] + ' ; '
                        # links_tsv.write(doi + "\t"+pub_names.encode('utf-8') + '\n')
                        id_field = source['Identifier']
                        for id in id_field:
                            data_doi = id['ID']
                            if data_doi.startswith(datacite_prefix):
                                print('Ignoring link to local data repository')
                                log.write("Ignoring link to local data repository \n")
                                # bath.write(doi + repo_name + data_doi + "\n")
                            else:
                                #process id
                                scheme = id['IDScheme']
                                found = 0
                                if scheme == 'doi':
                                    for d in dois_found:
                                    #no dups allowed
                                        if d == data_doi:
                                            found = 1
                                    if found == 0:
                                        dois_found.append(data_doi)
                                        # non_bath.write(doi +","+ data_doi.encode("utf-8")+ ", Title: " + title.encode('utf-8') +" Publisher: "+ pub_names.encode('utf-8') + '\n')
                    else:
                        log.write('Not a dataset \n')
                        print("Not a dataset")
