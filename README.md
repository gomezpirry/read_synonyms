# read_synonyms

Find synonyms in common between nodes of an obo file. Program written in python 3

## Usage

### Run locally 

Install dependencies

```
pip install requeriments.txt
```

Find synonyms in input_file.obo and store the results in output.csv file

```
cd read_synonyms
python3 read_synonyms -i input_file.obo
```

Find synonyms in input_file.obo and store the results in output_file.csv file

```
cd read_synonyms
python3 read_synonyms -i input_file.obo -o output_file.csv
```

### Run in Docker

Build dockerfile 

```
cd read_synonyms
docker build -t read_synonyms .
```

Run the docker repository. 

The option __-v__ allows connect a host folder with a docker volume. 
As __-v__ option argument pass the host folder path where the obo file is
followed by(:) and the volume path in docker (you decide the name of 
volume path). With this option, the host folder and volume docker are 
synchronized (shared files). The value of input __-i__ argument  and 
output __o__ argument are the volume path followed by input file name 
and output file name respectively   
   
```
docker run -v /path/to/folder:/path_to_docker read_synonyms -i /path_to_docker/input_file.obo -o /path_to_docker/output_file.csv
```