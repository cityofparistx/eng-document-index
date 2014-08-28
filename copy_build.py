import os, shutil

index_files = os.listdir("Z:\\CONSTRUCTION PLANS\\FLAT FILE INDEX")
dist_files = os.listdir("Z:\\CONSTRUCTION PLANS\\FLAT FILE INDEX\\dist")

for f in index_files:
    if f.endswith(".htm"):
        os.remove("Z:\\CONSTRUCTION PLANS\\FLAT FILE INDEX\\" + f)

new_index_files = os.listdir("Build")

for f in new_index_files:
    if f. endswith(".htm"):
       # print os.path.join("Build", f)
       shutil.copyfile(os.path.join("Build", f), "Z:\\CONSTRUCTION PLANS\\FLAT FILE INDEX\\" + f)
        
for f in dist_files:
    if f.endswith(".css") or f.endswith(".js"):
        os.remove("Z:\\CONSTRUCTION PLANS\\FLAT FILE INDEX\\dist\\" + f)
        
new_dist_files = os.listdir("Build\\dist")

for f in new_dist_files:
    if f.endswith(".css") or f.endswith(".js"):
       shutil.copyfile(os.path.join("Build\\dist", f), "Z:\\CONSTRUCTION PLANS\\FLAT FILE INDEX\\dist\\" + f)