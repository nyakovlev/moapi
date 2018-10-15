def findfiles(search_root, types=["*.*"]):
    import os
    import fnmatch
    matches = []
    for i in range(len(types)):
        matches.append([])
    for root, dirNames, fileNames in os.walk(search_root):
        for fileName in fileNames:
            for i in range(len(types)):
                if fnmatch.fnmatch(fileName, types[i]):
                    matches[i].append(os.path.join(root, fileName))
    return matches


def find_default_files():
    import os
    import data
    with open(os.path.join(os.path.expanduser("~"), "Desktop", "Media Files Found.txt"), "w") as f:
        cwd = os.getcwd()
        file_count = 0
        print "Searching for Picture files of types " + str(data.picture_types)
        f.write("#Picture Files found in " + cwd + "\n")
        for match in findfiles(cwd, data.picture_types):
            for item in match:
                f.write(item + "\n")
                file_count += 1
        print "Done"
        f.write("#Video Files found in " + cwd + "\n")
        print "Searching for Video files of types " + str(data.video_types)
        for match in findfiles(cwd, data.video_types):
            for item in match:
                f.write(item + "\n")
                file_count += 1
        print "Done"
        f.write("#Audio Files found in " + cwd + "\n")
        print "Searching for Audio files of types " + str(data.audio_types)
        for match in findfiles(cwd, data.audio_types):
            for item in match:
                f.write(item + "\n")
                file_count += 1
        print "Done"
        f.write("#Executable Files found in " + cwd + "\n")
        print "Searching for Executable files of types " + str(data.executable_types)
        for match in findfiles(cwd, data.executable_types):
            for item in match:
                f.write(item + "\n")
                file_count += 1
        raw_input("Done, found " + str(file_count) + " files. Press enter to continue.")
        f.close()
if __name__ == "__main__":
    find_default_files()
