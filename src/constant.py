INITIAL_INP_FILE = 'input/its_water_distribution.inp'
NUMBER_OF_JUNCTIONS = 94  # TODO: Dynamically extract from the initial inp file
NUMBER_OF_PIPES = 104  # TODO: Dynamically extract from the initial inp file

EPANET_JAR_FILE = r"AwareEpanetNoDeps.jar"

CATEGORY_JUNCTIONS = 'JUNCTIONS'
CATEGORY_PIPES = 'PIPES'
CATEGORY_EMITTERS = 'EMITTERS'

JUNCTION_IDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95]

INITIAL_ROUGHNESS = 150
ROUGHNESS_INTERVAL_PER_VARIANT = 50
NUMBER_OF_ROUGHNESS_VARIANTS = 5

INITIAL_EMIT = 0
EMIT_INTERVAL_PER_VARIANT = 0.02
NUMBER_OF_EMIT_VARIANTS = 5

OUTPUT_DIR = 'output/'

OUTPUT_ROUGHNESS_DIR = 'output/roughness/'
OUTPUT_ROUGHNESS_FILE = 'water_flow_forecast.csv'

OUTPUT_EMIT_DIR = 'output/emit/'
OUTPUT_EMIT_FILE = 'water_flow_forecast.csv'
