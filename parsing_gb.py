import re
import sys
import textwrap as txt
        
defi = []
version = []
def get_header(record):
    """This is a function that retrieves the version and definition from the GenBank record. It stitches the two which
    forms the first line.

    Args:
        record (List) : contains the list of all 17 files

    Returns: 
        List(str) : returns the stitched version and definition
    """
    for i in range(0, len(record)-1):
        split_list = record[i].split('\n')
        defi.append(split_list[1])
        version.append(split_list[3])

    for i,j in zip(defi, version):
        header = ''
        x = i.replace('DEFINITION', '').lstrip()
        y = j.replace('VERSION', '').lstrip()
        header = '>' + y + " " + x
        header = header.strip('.')
        header_format.append(header)
    return header_format

string_list = []
index = []
temp = []
origin = []
def get_sequence(record):
    """This is a function that looks for the sequence in the genbank file, formats the sequence into upper case,
    removes new lines and extra white spaces and wraps the formatted sequence with width 70.

    Args:
        List(str) : contains the list of all 17 files

    Returns:
        List(str) : returns the converted genbank sequence into FASTA format sequence which is stored in a 
        list
    """
    for i in record:
        #Replacing extra white spaces with no spaces
        join = ''.join(i)
        #Replacing the new lines and extra spaces
        format_str = join.replace("\n", " ").replace(" ", '')
        string_list.append(format_str)

        #Storing the sequences alone in the list
        final_string_list = string_list[0:17]

    #Retriving the index positions of the word ORIGIN
    for i in final_string_list:
        index.append(i.index('ORIGIN'))
        
    #Retrieving the origin sequence
    for i,j in zip(final_string_list, index):
        temp.append(i[j+6:])

    #Removing the numbers in between strings and storing it in a list
    for i in temp:
        res = "".join(filter(lambda x: not x.isdigit(), i))
        upper_case = res.upper()
        tr = "\n".join(txt.wrap(upper_case, width=70))
        origin.append(tr)
    return origin

def split_records(filename):
    """This function takes in the genbank files which has multiple files in it. Splits it based on the pattern
    using regex

    Args:
        filename: a GenBank record
    
    Returns:
        List(str) : outputs seperated genbank files and stores each split as a string and stores all of them 
        into List
    """
    try:
        with open(filename) as f:
            #Splitting the 17 files into 17 list elements which are of type string
            info = f.read()
            split_f = info.split('//\n\n')
            return split_f
    except FileNotFoundError:
        print("<input_file> not found.  Check the file path and try again")
        empty = []
        return empty
    

def main():
    
    input_file  = sys.argv[1]
    fasta_file = ".fasta"

    input_data = split_records(input_file)
    user2 = get_header(input_data)
    user3 = get_sequence(input_data)

    if len(sys.argv) == 2:
        output_filename = "sequences.fasta"
    else:
        output_filename = sys.argv[2]
        # Checking if the output file has the ".fasta" extension
        if fasta_file in output_filename:
            pass
        else:
            output_filename = output_filename+fasta_file

    with open(output_filename, 'a+') as fasta_out:
        for i,j in zip(header_format, origin):
            line = i + '\n' + j + '\n' + '\n'
            fasta_out.write(line)    

if __name__ == '__main__':

    header_format = []
    origin = []
    genbank_file = ".gb"
    
    if len(sys.argv) <= 3:
        if len(sys.argv) > 1:
            if genbank_file in str(sys.argv[1]):
                main()
            else:
                print("Provide a GenBank file to convert to FASTA")
                sys.exit()
        else:
            print("Please enter the input and output file names")
            sys.exit(0)