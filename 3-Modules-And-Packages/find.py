import os
import time
import argparse
import fnmatch


def find_files(directory=None, name=None,type=None,atime=None,maxdepth=None):
    results=[]          #Final result list. It'll have all the desired outputs
    current_time= time.time()
    if directory is None:
        directory=os.getcwd()  #if directory is None or not provided, take current dir as directory

    directory = os.path.abspath(directory)  # make sure directory is absolute directory
    if atime is not None:
        atime=atime*86400           # convert days to seconds

    def dir_search(directory,atime,type,depth=0):
            
            if maxdepth is not None and depth>maxdepth: #break condition when maxdepth reached
                return
            try:
                if type=='f' or type is None:
                    for i in os.listdir(directory):
                        full_path=os.path.join(directory,i) 
                        
                        if os.path.isfile(full_path) and (name is None or fnmatch.fnmatch(i,name) and (atime is None or atime>(current_time-os.path.getatime(full_path)))): 
                            results.append(full_path)
                            
                        elif os.path.isdir(full_path):
                            dir_search(full_path,atime,type,depth+1)

                elif type =='d':

                    for i in os.listdir(directory):
                        full_path=os.path.join(directory,i)
                        
                        if os.path.isdir(full_path) and (name is None or fnmatch.fnmatch(i,name) and (atime is None or atime>(current_time-os.path.getatime(full_path)))):
                            results.append(full_path)
                            
                        elif os.path.isdir(full_path):
                            dir_search(full_path,atime,type,depth+1)

            except PermissionError:
                pass

    dir_search(directory,atime,type,depth=0)
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find files in a directory with various filters.")
    parser.add_argument("directory")
    parser.add_argument("-name", type=str, help="Filter by filename (supports wildcards like '*.txt').")
    parser.add_argument("-type", type=str, help="Filter by file extension (e.g., 'txt' for .txt files).")
    parser.add_argument("-atime", type=int, help="Find files accessed within the last N seconds.")
    parser.add_argument("-maxdepth", type=int, help="Maximum depth for recursive search.")

    args = parser.parse_args()
    results = find_files(args.directory, args.name, args.type, args.atime, args.maxdepth)

    if results:
        for i in results:
            print(i)
    else:
        print("No results found.")
