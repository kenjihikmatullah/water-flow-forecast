import subprocess
import constant
import data
import roughness

rough_positions = []
for pos in range(1, 59):
	rough_positions.append(str(pos))


if __name__ == "__main__":
    try:
        database_file = open(constant.OUTPUT_DIRECTORY + constant.OUTPUT_FILE, 'w')
    except:
        print('Database file open error ')

    for r in range(0, constant.STEP_COUNT + 1):
        for pp in rough_positions:
            rp = str(constant.INITIAL_ROUGHNESS + constant.STEP * r)
            finaloutputfile = roughness.changeroughness2(pp, rp, r)
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

            
            subprocess.call(["java", "-cp", constant.EPANET_JAR_FILE, "org.addition.epanet.EPATool",
                    finaloutputfile])
            
            opparams = [pp, rp]
            sep = ","
            csv_record = sep.join(opparams + data.getdata(finaloutputfile))
            database_file.write(csv_record+'\n')

    database_file.close()
    print('Finished')
