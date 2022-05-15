INITIAL_INP_FILE = 'input/its_water_distribution.inp'
NUMBER_OF_JUNCTIONS = 36  # TODO: Dynamically extract from the initial inp file
NUMBER_OF_PIPES = 58  # TODO: Dynamically extract from the initial inp file

EPANET_JAR_FILE = r"AwareEpanetNoDeps.jar"

CATEGORY_JUNCTIONS = 'JUNCTIONS'
CATEGORY_PIPE = 'PIPES'

INITIAL_ROUGHNESS = 150
ROUGHNESS_INTERVAL_PER_VARIANT = 50
NUMBER_OF_ROUGHNESS_VARIANTS = 5

OUTPUT_DIR = 'output/'

OUTPUT_ROUGHNESS_DIR = 'output/roughness/'
OUTPUT_ROUGHNESS_FILE = 'water_flow_forecast.csv'
