## Using [Scholix](http://www.scholix.org/) to find links between research outputs and any associated datasets with available metadata.

###### This project is built on top of the work done by [Durham University Library](https://github.com/sefnyn/scholix)

There are two different codes for -

a) Finding research output associated with datasets published at University of Bath Archive

b) Finding datasets associated with research outputs from U of Bath

#### Workflow

#### Step 1
The first step is to collect the DOIs of research output or Bath Archive datasets and save them in a .txt or .csv file. The raw output from Scopus or Pure often contain URL or special characters. Make sure the list is clean or the code will break. (The code hasn't been tested against other PID, such as handle.)

#### Step 2
##### Case A - Link between Bath Archive DOIs and associated datasets

##### To run code use : python python_filename file_with_doi

Run the code [bath_dataset_lit_link.py](bath_dataset_lit_link.py). This will create a new output file bath_dataset_links.tsv containing dataset DOI, dataset creators' names, DOI of associated literature, publisher name and author names of the literature.

#### Step 2
##### Case B - Link between research output and any associated datasets

There are two codes ([get_data.py](get_data.py) and [metadata.py](metadata.py)) that can be used depending on the scenario and number of DOIs that need to be tested. Generally the number is bigger than the number of Bath Archive DOIs.
