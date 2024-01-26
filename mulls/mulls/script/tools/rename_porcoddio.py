import os
import argparse

# python3 rename_porcoddio.py -p /media/simone/PortableSSD/datasets/os0_newer_college/catacombs_easy/pcd_small -f .pcd

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="porcoddio")
	parser.add_argument("-p","--path", type=str)
	parser.add_argument("-f","--format", type=str)
	args = parser.parse_args()
	
	filenames = list(filter(lambda x: args.format in x, os.listdir(args.path)))
	float_filenames = list(map(lambda x: float(x[:-len(args.format)]), filenames))
	indeces_sorted = sorted(range(len(float_filenames)), key=lambda k: float_filenames[k])
	
	for idx, x in enumerate(indeces_sorted):
		new_file_name = str(idx+1).zfill(5) + args.format
		print("rename: "+ filenames[x] + " to: " +new_file_name)
		os.rename(os.path.join(args.path,filenames[x]), os.path.join(args.path,new_file_name))
	
	
	
