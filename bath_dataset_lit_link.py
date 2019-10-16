import fileinput
import json
import requests

API = 'http://api.scholexplorer.openaire.eu/v2/Links'

dois_found = []
json_data = "records.json"
dataset_links = 'bath_dataset_links.tsv'
count = 0

j = open(json_data, 'w')
link_list = open(dataset_links, 'w')

# For DOIs in input file write json output
for doi in fileinput.input():
    doi = doi.rstrip()
    count += 1
    print("###  " + str(count ) + "  ### \n")
    if not doi:
        #do nothing
        print('found empty line...ignored')
        break
    payload = {'sourcePid': doi}

    # Make API Get request
    r = requests.get(API, params=payload)
    if r.raise_for_status() == None:
        print('Processing doi ' + doi)
        # log.write('Processing doi ' + doi +"\n")

        try:
            json_data = r.json()
        except ValueError:
            print('Invalid JSON')
            # log.write("........Invalid JSON")
        else:
            json_string = json.dumps(json_data, indent=4)
            j.write(json_string)
            my_result = json_data['result']

            # Process json output unless empty
            if len(my_result) != 0:
                for data in my_result:
                    source = data['source']
                    target = data['target']
                    obj_type = target['Type']
                    # set the condition for the object to be a dataset because there are lit-lit links
                    if obj_type == 'literature':
                        title = target['Title']

                        # get all publisher names from array
                        pub_list = target['Publisher'] #list of pubs
                        pub_names = ""
                        for index in range(len(pub_list)):
                            pub_names = pub_names + pub_list[index]['name'] + ' ; '

                        # get all dataset creator names
                        lit_creator = target['Creator'] #list of creators
                        lit_creators = ""
                        for index in range(len(lit_creator)):
                            lit_creators = lit_creators + lit_creator[index]['Name'] + ' ; '

                        dataset_creator = source['Creator']
                        data_creators = ""
                        for index in range(len(dataset_creator)):
                            data_creators = data_creators + dataset_creator[index]['Name'] + ' ; '

                        id_field = target['Identifier']
                        for id in id_field:
                            lit_doi = id['ID']
                            scheme = id['IDScheme']
                            found = 0
                            if scheme == 'doi':
                                for d in dois_found:
                                #no dups allowed
                                    if d == lit_doi:
                                        found = 1
                                if found == 0:
                                    dois_found.append(lit_doi)
                                    link_list.write(doi + '\t' + data_creators.encode("utf-8") + '\t' + lit_doi.encode("utf-8")+ '\t' + "Title: " + title.encode('utf-8') +"; Publisher: "+ pub_names.encode('utf-8') + "; Creators: "+ lit_creators.encode("utf-8") +'\n')


j.close()
link_list.close()
