import subprocess

import constant
import input
import output
import roughness

rough_positions = []
for pos in range(1, 59):
    rough_positions.append(str(pos))


if __name__ == "__main__":
    database_file = output.open_file()

    for r in range(0, constant.STEP_COUNT + 1):
        for pp in rough_positions:
            rp = str(constant.INITIAL_ROUGHNESS + constant.STEP * r)
            finaloutputfile = roughness.changeroughness2(pp, rp, r)
            
            subprocess.call(["java", "-cp", constant.EPANET_JAR_FILE, "org.addition.epanet.EPATool",
                    finaloutputfile])
            
            opparams = [pp, rp]
            sep = ","
            csv_record = sep.join(opparams + input.getdata(finaloutputfile))
            database_file.write(csv_record+'\n')

    database_file.close()
    print('Finished')
