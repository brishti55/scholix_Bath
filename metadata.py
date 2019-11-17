import fileinput
import json
import requests

datacite_prefix = '10.15125'  #Bath prefix
repo_name = '* Bath Archive *'
API = 'http://api.scholexplorer.openaire.eu/v2/Links'
dois_found = []
json_data = "records.json"
no_hits ="no_hits.txt"
logfile = 'log.txt'
bath_doi = 'bath.txt'
non_bath_doi = 'non_bath.tsv'
doi_links = {}
count = 0

print('opening file for JSON records: ' + json_data)
j = open(json_data, 'w')
# bib = open(citations,  'w')
log = open(logfile, 'w')
bath = open(bath_doi, 'w')
non_bath = open(non_bath_doi, 'w')
no_doi_found = open(no_hits, 'w')

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
        # log.write('Processing doi ' + doi +"\n")

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
                no_doi_found.write("No research data found for research output DOI " + doi + "\n")
            else:
                for data in my_result:
                    source = data['source']
                    target = data['target']
                    lit_creators_list = target['Creator']
                    obj_type = source['Type']
                    # set the condition for the object to be a dataset because there are lit-lit links
                    if obj_type == 'dataset':
                        title = source['Title']
                        dataset_creator = source['Creator'] #list of creators

                        # get all publisher names from array
                        pub_list = source['Publisher'] #list of pubs
                        pub_names = ""
                        for index in range(len(pub_list)):
                            pub_names = pub_names + pub_list[index]['name'] + ' ; '

                        # get all dataset creator names
                        data_creators = ""
                        for index in range(len(dataset_creator)):
                            data_creators = data_creators + dataset_creator[index]['Name'] + ' ; '

                        # get literature creator names from the list lit_creators_list
                        lit_creators =""
                        for index in range(len(lit_creators_list)):
                            lit_creators = lit_creators + lit_creators_list[index]['Name'] + ' ;'
                            # print(lit_creators)

                        id_field = source['Identifier']
                        for id in id_field:
                            data_doi = id['ID']
                            if data_doi.startswith(datacite_prefix):
                                print('Ignoring link to local data repository')
                                log.write("Ignoring link to local data repository \n")
                                bath.write(doi + " " + repo_name.encode("utf-8") + data_doi + "\n")
                            else:
                                #process id
                                scheme = id['IDScheme']
                                found = 0
                                test_str = ""
                                if scheme == 'doi':
                                    for d in dois_found:
                                    #no dups allowed
                                        if d == data_doi:
                                            found = 1
                                    if found == 0:
                                        dois_found.append(data_doi)
                                        non_bath.write(doi + '\t' + lit_creators.encode("utf-8") + '\t' + data_doi.encode("utf-8")+ '\t' + "Title: " + title.encode('utf-8') +" Publisher: "+ pub_names.encode('utf-8') + " Creators: "+ data_creators.encode("utf-8") +'\n')

                                        # list publisher names only
                                        # non_bath.write(doi + '\t'  + data_doi.encode("utf-8")+ '\t' + pub_names.encode('utf-8') +'\n')


                    else:
                        log.write('Not a dataset \n')
                        print("Not a dataset")
