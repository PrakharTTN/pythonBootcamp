"""Q4) Implement  below options:

`-name`
`-atime`
`-type`
`-maxdepth`

Example use:

To find all ".py" files (not folders) in home directory and 2 level sub-directories which were created recently in last 7 days write

find.py ~/ -name "*.py" -type f -atime -7
"""


import os
import time
import argparse
import fnmatch


def find_files(directory=None, name=None,type=None,atime=None,maxdepth=None):
    results=[]          #Final result list. It'll have all the desired outputs
    current_time= time.time()   
    
    #if directory is None or not provided, take current dir as directory
    if directory is None:
        directory=os.getcwd()  

    #Make sure directory is absolute directory and time is in seconds
    directory = os.path.abspath(directory) 
    if atime is not None:
        atime=atime*86400 

    def dir_search(directory,atime,type,depth=0):
        if maxdepth is not None and depth>maxdepth: #break condition when maxdepth reached
            return
        try:
            # if -type is f or it is not there (default), code to search the file
            for i in os.listdir(directory):
                    full_path=os.path.join(directory,i) 
                    if type=='f' or type is None:
                    
                        #This block of code searches the path and checks if it is a file and matches the arguments provided
                        if os.path.isfile(full_path) and (name is None or fnmatch.fnmatch(i,name) and (atime is None or atime>(current_time-os.path.getatime(full_path)))): 
                            results.append(full_path)
                        
                        #Creating a recursion to ensure every path is searched till the maxdepth of directory is reached
                        elif os.path.isdir(full_path):
                            dir_search(full_path,atime,type,depth+1)

                    elif type =='d':
                        #To check if the path is directory and matches the parameters provided in the arguments
                        if os.path.isdir(full_path) and (name is None or fnmatch.fnmatch(i,name) and (atime is None or atime>(current_time-os.path.getatime(full_path)))):
                            results.append(full_path) 
                        
                        #Else continue with the recursion 
                        elif os.path.isdir(full_path):
                            dir_search(full_path,atime,type,depth+1)

        #If a directory requires sudo priveleges, ignore that path
        except PermissionError:
            pass

    dir_search(directory,atime,type,depth=0)
    return results  

if __name__ == "__main__":

    #Create a parser to parse the command-line arguments
    parser = argparse.ArgumentParser(description="Find files in a directory with various filters.")

    #Added arguments for the parser
    parser.add_argument("directory", help="The directory which you want as the starting point, default = current working dir")
    parser.add_argument("-name", type=str, help="Filter by filename (supports like '*.txt').")
    parser.add_argument("-type", type=str, help="Filter by file extension (e.g., 'txt' for .txt files).")
    parser.add_argument("-atime", type=int, help="Find files accessed within the last days.")
    parser.add_argument("-maxdepth", type=int, help="Maximum depth for recursive search.")


    #Parse the args and return the results from function in a list variable
    args = parser.parse_args()
    results = find_files(args.directory, args.name, args.type, args.atime, args.maxdepth)


    if results:
        for i in results:
            print(i)
    else:
        print("No results found.")

    '''Output: >>>python3 find.py <dir> -name="*.py" -maxdepth 1
    /<dir>/hey.py
    /<dir/library/module.py
    ...
    '''