import os
import sys
import shutil
import subprocess

input_file = 'foss_poly_1.inp'

experiment_name = 'foss_varying_roughness'
results_dir = experiment_name+'/'
database_name = experiment_name+'.csv'

rough_positions = []
for pos in range(1, 59):
	rough_positions.append(str(pos))

initial_roughness = 150  # Initial roughness value
step = 50                # Added roughness value per-step
step_count = 5           # Number of steps

def change(inputfile, outputfile, category, idname, pos, val):
	try:
		fileobj = open(inputfile, 'r')
		lines = fileobj.readlines()
		fileobj.close()
	except:
		print('Input file open error')
	try:
		fileout = open(outputfile, 'w')
	except:
		print('Output file open error ')

	incategory = False
	nl = len(lines)
	for i in range(0, nl):
		sss = lines[i].split(' ')
		ss = list(filter(lambda x: x != '', sss))
		
		if (incategory):
			if (len(ss) == 1):
				incategory = False
			else:
				if ((ss[0] == idname) or (idname == '*' and ss[0][0] != ';')):
					ss[pos] = val
					sep = "    "
					lines[i] = sep.join(ss)

		if (ss[0].find(category) > -1):
			incategory = True
		fileout.write(lines[i])

	fileout.close()

def getflows(linkfile):
	try:
		fileobj = open(linkfile, 'r')
		lines = fileobj.readlines()
		fileobj.close()
	except:
		print('Link file open error')

	nl = len(lines)
	np = nl-2 
	flows = []

	for i in range(0, np):
		ss = lines[i+2].split('\t')
		flows.append(ss[5])

	return flows

def getpressures(nodefile):
	try:
		fileobj = open(nodefile, 'r')
		lines = fileobj.readlines()
		fileobj.close()
	except:
		print('Node file open error')
    
	nl = len(lines)
	np = nl-2
	pressures = []

	for i in range(0, np):
		ss = lines[i+2].split('\t')
		pressures.append(ss[4])
	
	return pressures

def getheads(nodefile):
	try:
		fileobj = open(nodefile, 'r')
		lines = fileobj.readlines()
		fileobj.close()
	except:
		print('Node file open error')

	nl = len(lines)
	np = nl-2
	heads = []

	for i in range(0, np):
		ss = lines[i+2].split('\t')
		heads.append(ss[5])

	return heads

def getdemands(nodefile):
	try:
		fileobj = open(nodefile, 'r')
		lines = fileobj.readlines()
		fileobj.close()
	except:
		print('Node file open error')
    
	nl = len(lines)
	np = nl-2
	demands = []

	for i in range(0, np):
		ss = lines[i+2].split('\t')
		demands.append(ss[6].replace("\n", ""))

	return demands

def changeroughness(pp, rp, r):
    infilename = input_file
    fid = 1
    for p in rough_positions:
        outfilename = 'tmp'+str(fid)+'.inp'
        if pp == p:
            rpp = rp
            change(infilename, outfilename, 'PIPES', p, 5, rpp+' ')
            finaloutputfile = results_dir+'tmp-PP-'+pp+'-r-'+str(r)+'.inp'
            shutil.move(outfilename, finaloutputfile)
            print(f'Created: {finaloutputfile}')
            break

        fid = fid+1

    return finaloutputfile

def changeroughness2(pp, rp, r):
    infilename = input_file
    finaloutputfile = results_dir+'tmp-PP-'+pp+'-r-'+str(r)+'.inp'
    change(infilename, finaloutputfile, 'PIPES', pp, 5, rp+' ')
    print(f'Created: {finaloutputfile}')
    return finaloutputfile

def getdata(finaloutputfile):
    flows = getflows(finaloutputfile+'.links.out')
    pressures = getpressures(finaloutputfile+'.nodes.out')
    heads = getheads(finaloutputfile+'.nodes.out')
    demands = getdemands(finaloutputfile+'.nodes.out')
    return flows + pressures + heads + demands

if __name__ == "__main__":
    try:
        database_file = open(results_dir + database_name, 'w')
    except:
        print('Database file open error ')

    for r in range(0, step_count + 1):
        for pp in rough_positions:
            rp = str(initial_roughness + step*r)
            finaloutputfile = changeroughness2(pp, rp, r)
            # fid = 1
            # for p in rough_positions:
            #     outfilename = 'tmp'+str(fid)+'.inp'
            #     if str(l+1) == p:
            #         rp = str(initial_roughness + step*r)
            #         rpp = rp
            #     else:
            #         rpp = str(initial_roughness)
            #     change(infilename, outfilename, 'PIPES', p, 5, rpp+' ')
                
            #     if infilename != input_file:
            #         os.remove(infilename)

            #     infilename = outfilename
            #     fid = fid+1
            
            # finaloutputfile = results_dir+'tmp-PP-'+pp+'-r-'+str(r)+'.inp'
            
            # shutil.move(infilename, finaloutputfile)
            # print(f'Created: {finaloutputfile}')

            
            subprocess.call(["java", "-cp", "AwareEpanetNoDeps.jar", "org.addition.epanet.EPATool",
                    finaloutputfile])
            
            opparams = [pp, rp]
            sep = ","
            csv_record = sep.join(opparams+getdata(finaloutputfile))
            database_file.write(csv_record+'\n')

    database_file.close()
    print('Finished')
