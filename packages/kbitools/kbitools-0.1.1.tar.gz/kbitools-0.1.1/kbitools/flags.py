import argparse

def get_arguments():
    parser = argparse.ArgumentParser(description="Flags and arguments for your KerBI's engine.\n\n")
  # SERVER ARGS
    parser.add_argument('-s', '--server', action='store_true', help="Enable the kerbiserver, a REST server. Defaults to localhost:9393.\n\n")
    parser.add_argument('-sA', '--server_address', type=str, help="Override the configured server address.")
    parser.add_argument('-sP', '--server_port', type=str, help="Override the configured server port.\n\n")
    parser.add_argument('-c', '--console', action='store_true', help="Enable interactive console access to the HOME channel.\n")
  # CONFIGURATION OVERRIDES
    parser.add_argument('-C', '--configuration_file', type=str, help="Load <file> as configuration file instead of the default (.env).\n\n")
    parser.add_argument('-D', '--driver', type=str, help="Load a specific kdriver. Must be in the kdrivers folder.\n")
    parser.add_argument('-M', '--memory_file', type=str, help="Load a JSON file as initial memory.\n\n")
    parser.add_argument('-R', '--kroot', type=str, help="Specify a root directory to run from. EXPERIMENTAL\n")
    parser.add_argument('-L', '--legacy', action='store_true', help="Legacy mode will check the beginning of all text fields for execution codes. EXPERIMENTAL\n")
    return parser



