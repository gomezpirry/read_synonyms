import obonet
import re
import sys
import getopt
import os


def write_csv(csv_file, output_text):
    # write csv file
    file_form = open(csv_file, 'w')
    for key, value in output_text.items():
        file_form.write(str(key) + ';' + str(value['name']) + ';')
        file_form.write(';'.join(value['synonyms']))
        file_form.write('\n')
    # end for
    file_form.close()

    filename_w = os.path.basename(csv_file)
    filename, file_extension = os.path.splitext(filename_w)

    four_file = filename + str(-4) + file_extension

    # write node with 4 or more synonyms
    file_form = open(four_file, 'w')
    for key, value in output_text.items():
        if len(value['synonyms']) > 4:
            file_form.write(str(key) + ';' + str(value['name']) + ';')
            file_form.write(';'.join(value['synonyms']))
            file_form.write('\n')
    # end for
    file_form.close()
# end if


def main(argv):
    # verify numbers of arguments
    if len(argv) < 2:
        print('Number of arguments invalid')
        print('Try with:')
        print('read_synonym.py -i <inputfile obo> -o <outputfile csv>')
        print('read_synonym.py -i <inputfile obo> (store in output.csv)')
        sys.exit()
    # end if

    filename_w_input = os.path.basename(argv[1])
    filename_input, file_extension_input = os.path.splitext(filename_w_input)

    if len(argv) == 4:
        filename_w_output = os.path.basename(argv[3])
        filename_output, file_extension_output = os.path.splitext(filename_w_output)

    # verify if input file exist
    if not os.path.isfile(argv[1]):
        print('Input File does not exist')
        sys.exit()
    # end if

    # verify if inout file is a obo
    if not file_extension_input == '.obo':
        print('Input File must have a .obo extension')
        sys.exit()
    # end if

    if len(argv) == 4:
        # verify if output file exist
        if not os.path.isfile(argv[3]):
            print('Output File does not exist')
            sys.exit()
        # end if

        # verify if inout file is a csv
        if not file_extension_output == '.csv':
            print('Input File must have a .obo extension')
            sys.exit()
        # end if
    # end if

    url = ''
    output = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('read_synonym.py -i <inputfile obo> -o <outputfile csv>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('read_synonym.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            url = arg
        elif opt in ("-o", "--ofile"):
            output = arg
    # end for

    print(url, output)
    graph = obonet.read_obo(url)

    # get all nodes of graph
    nodes = graph.nodes(data=True)

    clean_nodes = []
    result = {}

    # for all nodes in graph
    for node in nodes:
        # get id
        node_id = node[0]

        # get name
        node_name = ""
        if 'name' in node[1]:
            node_name = node[1]['name']
        # end if

        synonyms = []
        # check if node have synonym
        if 'synonym' in node[1]:
            # get synonym list
            synonyms = node[1]['synonym']
        # end if

        # clean exact synonym (if synonym string is equal to node name)
        clean_exact = [x for x in synonyms if '"{}"'.format(node_name) not in x]

        # if node don't have synonyms, continue
        if len(clean_exact) == 0:
            continue
        # end if

        clean_synonym = []
        # get the string value of the synonym
        for synonym in clean_exact:
            clean_synonym.append(re.findall('"([^"]*)"', synonym)[0])
        # end for
        clean_nodes.append({'id': node_id, 'name':node_name, 'synonyms': clean_synonym})
    # end for

    for clean_node in clean_nodes:
        # get node synonyms
        clean_synonyms = clean_node['synonyms']
        for compare_node in clean_nodes:
            # jump the current clean node
            if compare_node['id'] == clean_node['id']:
                continue
            # get intersection between two list (same values in two list)
            same_synonyms = list(set(clean_synonyms).intersection(compare_node['synonyms']))
            # continue if not have synonyms in common
            if len(same_synonyms) == 0:
                continue

            # if node is in result dict
            if clean_node['id'] in result:
                # for each synonym in common
                for synonym in same_synonyms:
                    # continue if synonym is in synonym list for node
                    if synonym in result[clean_node['id']]['synonyms']:
                        continue
                    # append synonym if is not in synonym list for node
                    result[clean_node['id']]['synonyms'].append(synonym)
            else:
                # add node to dictionary if node is not in result
                result[clean_node['id']] = {'name': clean_node['name'], 'synonyms': same_synonyms}
    # end for
    if output != '':
        write_csv(output, result)
    else:
        write_csv('output.csv', result)
# end main


if __name__ == "__main__":
    main(sys.argv[1:])

