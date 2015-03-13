#!/usr/bin/env python3
"""
SYNOPSIS

    translate_connectivity_info.py [-h,--help] [-v,--verbose] [--version]

DESCRIPTION

    This script translates multiple .txt input files generated by the CAID
    program containing information about the local and global indexing data 
    for a finite element calculation.  The necessary input files are:

    ID.txt
    IEN_0.txt
    IEN_1.txt
    IEN_2.txt
    .
    .
    .
    LM_0.txt
    LM_1.txt
    LM_2.txt
    .
    .
    .

    of which only the first file ID.txt should be passed as arguments. The
    first argument is however: 
    - the number of patches
    
    The script generates one main information file with the name:

    - [base_name]_element_connectivity_main.nml

    Where [base_name] is the name given to the transformation when it was
    generated by the CAID program. This is extracted from the file 
    [base_name]_info.txt which should be located in the same directory where
    all the other files ID.txt, IEN_1.txt, etc. are located. The output also
    contains a list of 2*number_patches additional .nml files containing the 
    local and local to global indexing information in a format understandable
    by Selalib.

EXAMPLES

    ./translate_connectivity_info.py 4 ID.txt 

EXIT STATUS

    TODO:

AUTHOR

    Edwin CHACON-GOLCHER <golcher@math.unistra.fr>

LICENSE

    Same as Selalib's...

VERSION

    1.0
"""

import sys, os, traceback, optparse
import time
import re
import pprint
import glob
from string import *

sys.stdout = open('translate_connectivity_info.out', 'w')

def main ():

    global options, args
    readfilename   = ""
    flattened = []
    patch_li_syms  = []
    patch_li_names = []       # array for names of local index filenames
    patch_loc_glob_syms  = []
    patch_loc_glob_names = [] # array for names of local to global files
    global_indices = []
    num_patches = 0
    pp = pprint.PrettyPrinter(indent=4)
    ngi = 0   # counter, number of global indices
    rows = 0
    cols = 0
    slash_pos = 0
    slash_pos2 = 0
    info_pos   = 0
    path = ""
    info_pathfile = ""
    ien_files_found = []
    IEN_files = []
    LM_files = []

    print('number of arguments passed')
    print(len(args))
    print(args)

    if (len(args) > 1): 
        print( "Incorrect number of arguments. Usage: ")
        print( "user$ ./translate_connectivity_info.py path-to-ID/ID.txt")
        sys.exit()

    # The file name can come each prepended with a path. This path must
    # be extracted as the generated files should end up in the same directory
    # where the original .txt files exist. We must extract the path
    # from the argument, the ID.txt file.
    slash_pos = args[0].rfind('/')
    # Add something here for the case where the character was not found (i.e.:
    # returned -1) Apparently this works fine even when no slash is in the path.
    path = args[0][:slash_pos+1]

    # If the connectivity files are present, then a _info.txt file must exist
    # in this directory. Nevertheless, make sure that the returned list is not
    # empty! FIX THIS!!
    info_pathfile = glob.glob(path+"*_info.txt")[0]
    found_ien_files = glob.glob(path + "IEN_*.txt")
    print("found these many patches: ")
    num_patches = len(found_ien_files)
    slash_pos2   = info_pathfile.rfind('/')
    info_pos     = info_pathfile.rfind('_info.txt')
    inputname    = info_pathfile[slash_pos2+1:info_pos]
    outputname   = path + inputname + "_element_connectivity_main.nml"
    print( "Main output will be written to {0}".format(outputname))
    print("translate_connectivity_info.py current path: " + os.getcwd())


    # Open the ID.txt file to load the global index data. 
    with open(args[0],'r') as readfile, open(outputname,'w') as writefile:
        now  = time.localtime()
        date = str(now[1]) + "/" + str(now[2]) + "/" + str(now[0])
        mytime = str(now[3]) + ":" + str(now[4]) + ":" + str(now[5]) + "\n"
        writefile.write("! Input namelist describing the element connectivity ")
        writefile.write("information. \n")
        writefile.write("! Generated by the call: "+sys.argv[0] + " " +
                        ' '.join(args) + "\n")
        writefile.write("! on: " + date + "," + mytime)
        writefile.write("\n")

        linelist = readfile.readlines()
        for line in linelist:
            ngi = ngi + 1
            linetemp = line.split() # needed to get rid of newlines
            global_indices.append(linetemp[0]) # hardwired assumption!

        writefile.write("&number_global_indices" + "\n")
        writefile.write("     num_global_indices = " + str(ngi) + "\n")
        writefile.write("/" + "\n\n")

        writefile.write("&global_indices" +"\n")
        writefile.write("     global_indices_array = "+' '.join(global_indices))
        writefile.write("\n")
        writefile.write("/" + "\n\n")

        # Create a list of the filenames that will be created to store the
        # information originally contained in the IEN_i.txt files.
        print(int(num_patches))
        for i in range(int(num_patches)):
            patch_li_syms.append(inputname + "_local_indices_patch" + 
                                  str(i) + ".nml")

            patch_li_names.append("\"" + inputname + "_local_indices_patch" + 
                                  str(i) + ".nml\"")
            
        writefile.write("&local_index_files" + "\n")
        writefile.write("     local_index_file_list = " + 
                        ' '.join(patch_li_names) )
        writefile.write("\n")
        writefile.write("/" + "\n\n")

        # Create the list of filenames that will be read. This is composed of
        # the IEN_i.txt files and a second list for the LM_i.txt files.
        for i in range(int(num_patches)):
            IEN_files.append(path + "IEN_" + str(i) + ".txt")
            LM_files.append(path + "LM_" + str(i) + ".txt")

        for i in IEN_files:
            print("IEN files are: " + i)

        for i in LM_files:
            print("LM files are: " + i)

        # Create a list of the filenames that will be created to store the
        # information originally contained in the LM_i.txt files.
        for i in range(int(num_patches)):
            patch_loc_glob_syms.append(inputname + 
                                       "_local_to_global_patch" + str(i) + 
                                       ".nml")

            patch_loc_glob_names.append("\"" + inputname + 
                                        "_local_to_global_patch" + str(i) + 
                                        ".nml\"")
        writefile.write("&local_to_global_files" + "\n")
        writefile.write("     local_to_global_file_list = " + 
                        ' '.join(patch_loc_glob_names) )
        writefile.write("\n")
        writefile.write("/" + "\n\n")

    # At this pont the main connectivity nml file is done.
 
    # Proceed to create the individual files containing the local index 
    # information.
    for i in range(int(num_patches)):
        with open(IEN_files[i],'r') as readfile, \
                open(path+patch_li_syms[i],'w') as writefile:
            print("converting data from: \n" + IEN_files[i] + " to \n" + 
                  path + patch_li_syms[i])
            writefile.write("! Input namelist describing the local index ")
            writefile.write("information. \n")
            writefile.write("! Generated by the call: "+sys.argv[0] + " " +
                            ' '.join(args) + "\n")
            writefile.write("! on: " + date + "," + mytime)
            writefile.write("\n")
            writefile.write("! This file contains the local index information")
            writefile.write(" contained \n! originally in the file: " + \
                                IEN_files[i])
            writefile.write("\n\n")
            local_indices_array = []
            linelist = readfile.readlines()
            rows = 0   # just a counter
            cols = 0   # just a counter
            for line in linelist:
                linetemp = line.split()
                local_indices_array.append(linetemp[:])
                # keep some accounting on the size of the data
                if rows == 0:
                    cols = len(linetemp)
                else:
                    if len(linetemp) != cols:
                        print("There is something suspicious in file: ")
                        print(args[i]) #por aqui!!
                        print("regarding the size of the data. The number ")
                        print("of columns changes from one row to the next.")
                        print(cols)
                rows = rows + 1
            flattened = \
            [item for sublist in local_indices_array for item in sublist]
            writefile.write("&li_dimensions" + "\n")
            writefile.write("     rows = " + str(rows) + "\n")
            writefile.write("     cols = " + str(cols) + "\n")
            writefile.write("     li_total = " + str(len(flattened)) + "\n")
            writefile.write("/" + "\n\n")

            writefile.write("&local_spline_indices" + "\n")
            writefile.write("     local_spline_indices_array = " + 
                            ' '.join([str(item) for item in flattened]) + "\n")
            writefile.write("/" + "\n\n")

    # Proceed to create the individual files containing the local 
    # to global index information.
    for i in range(int(num_patches)):
        with open(LM_files[i],'r') as readfile, \
                open(path+patch_loc_glob_syms[i],'w') as writefile:
            print("converting data from: \n" + LM_files[i] + \
                  " to \n" + path + patch_loc_glob_syms[i])
            writefile.write("! Input namelist describing the local to global ")
            writefile.write("indexing information. \n")
            writefile.write("! Generated by the call: "+sys.argv[0] + " " +
                            ' '.join(args) + "\n")
            writefile.write("! on: " + date + "," + mytime)
            writefile.write("\n")
            writefile.write("! This file contains the local to global index ")
            writefile.write(" information")
            writefile.write(" contained \n! originally in the file: " + 
                            LM_files[i])
            writefile.write("\n\n")
            loc_glob_array = [] #change this name
            linelist = readfile.readlines()
            rows = 0   # just a counter
            cols = 0   # just a counter
            for line in linelist:
                linetemp = line.split()
                loc_glob_array.append(linetemp[:])
                if rows == 0:
                    cols = len(linetemp)
                else:
                    if len(linetemp) != cols:
                        print("There is something suspicious in file: ")
                        print(LM_files[i])
                        print("regarding the size of the data. The number ")
                        print("of columns changes from one row to the next.")
                        print(cols)
                rows = rows + 1
            flattened = \
            [item for sublist in loc_glob_array for item in sublist]
            writefile.write("&l2g_dimensions" + "\n")
            writefile.write("     rows = " + str(rows) + "\n")
            writefile.write("     cols = " + str(cols) + "\n")
            writefile.write("     l2g_total = " + str(len(flattened)) + "\n")
            writefile.write("/" + "\n\n")

            writefile.write("&local_to_global_indices" + "\n")
            writefile.write("     local_to_global_index_array = " + 
                            ' '.join([str(item) for item in flattened]) + "\n")
            writefile.write("/" + "\n\n")



if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), usage=globals()['__doc__'], version='1.0')
        parser.add_option ('-v', '--verbose', action='store_true', default=False, help='verbose output')
        (options, args) = parser.parse_args()
        #if len(args) < 1:
        #    parser.error ('missing argument')
        if options.verbose: print( time.asctime())
        main()
        if options.verbose: print(*time.asctime())
        if options.verbose: print( 'execution time in seconds:')
        if options.verbose: print( (time.time() - start_time))
        sys.exit(0)
    except KeyboardInterrupt as e: # Ctrl-C
        raise e
    except SystemExit as e: # sys.exit()
        raise e
    except Exception as e:
        print( 'ERROR, UNEXPECTED EXCEPTION')
        print( str(e))
        traceback.print_exc()
        os._exit(1)

