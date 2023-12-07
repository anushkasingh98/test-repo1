import os
import subprocess
import file_data

ignore_file_types = [".png",".img",".csv",".ipynb",".MD",".md",".JPG",".jpg",".pyc",".sqlite3",".sample",".pack",".idx"]

def clone_repo(github_link,directory):
    # Extract the repository name from the GitHub link
    repo_name = github_link.split("/")[-1].replace(".git", "")
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Clone the repository to the specified directory
    subprocess.run(["git", "clone", github_link, os.path.join(directory, repo_name)])
    dir = os.path.join(directory, repo_name)
    print("\n Directory after clone_repo: ",dir)
    return dir

def read_files_in_directory(directory, file_contents, file_names):
    print("Directory : ",directory)
    skipped_files=0
    total_files = 0
    i = 0
    for root, dirs, files in os.walk(directory):
        for file in [f for f in files if not f[0] == '.']:
            total_files += 1
            file_path = os.path.join(root, file)
            #ignore files with ext in ignore_file_types
            if any(ext in file for ext in ignore_file_types):
                skipped_files += 1
                continue
            with open(file_path, 'r',  encoding='latin-1') as f:
                contents = f.read()
                print("Reading File: ", file)
                # print(contents)
                file_contents.append(contents)
                file_names.append(file)
    print("\nTotal Files: ",total_files)
    print("Skipped Files: ",skipped_files)
    return file_contents, file_names

def remove_empty_files(file_names,file_contents):
    length = len(file_names)
    list_pop = []
    #remove empty strings from file_contents
    for i in range(length):
        if file_contents[i] == "":
            list_pop.append(i)
    list_pop.sort(reverse=True)
    for i in list_pop:
        file_contents.pop(i)
        file_names.pop(i)
    return file_contents,file_names

def control(github_repo):
    directory = '/Users/anushkasingh/Desktop/Kathalyst/Code/GithubTestRepos'

    # clone repo to directory
    dir = clone_repo(github_repo,directory)

    # read files in directory and create prompt
    file_contents = []
    file_names = []
    file_contents, file_names = read_files_in_directory(dir,file_contents,file_names)
    file_contents, file_names = remove_empty_files(file_names,file_contents)

    return file_contents,file_names,dir