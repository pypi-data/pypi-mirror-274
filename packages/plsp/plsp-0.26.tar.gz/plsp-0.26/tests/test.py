import subprocess
import sys, os
UP_DIR=os.path.abspath(os.path.join(
		os.path.dirname(__file__),
		".."
	)
)
sys.path.append(UP_DIR)

from plsp import Logger, save_logger
from plsp.formatters.bundled import Time_Formatter



# NOTE: ONLY ONE LOGGER SHOULD EVER BE CREATED PER PROGRAM.
logger = Logger()



# Use below to separate log files based on debug mode instead of debug context.
# NOTE: NOT YET SUPPORTED...
# TODO: IMPLEMENT.
#plsp.set("io_based_on_mode", True)



# The below sets the global context to generic.
logger.set("global_context", "generic")



# Below is adding a debug context.
# It is a bit more complicated than setting up debug contexts so you dont have to set all the parameters at once.
logger.add_debug_context("generic")
logger.add_debug_context("rendering")
logger.add_debug_context("physics")



# Below is adding a debug mode.
logger.add_debug_mode("info")
logger.add_debug_mode("detail")
logger.add_debug_mode("debug")
logger.add_debug_mode("error", separate=True)



# START OF MODIFYING DEBUG CONTEXTS #

# Modification of debug context must be done separately to creation.
# Access the debug context by using the `Logger.debug_contexts` dictionary.

logger.debug_contexts["generic"].set_is_active(True)
logger.debug_contexts["generic"].add_direction(
	do_encode=False,
	file_handle=sys.stdout.fileno(),
	file_path=None
)
logger.debug_contexts["rendering"].set_is_active(True)
logger.debug_contexts["rendering"].add_direction(
	do_encode=False,
	file_handle=sys.stdout.fileno(),
	file_path=None
)
logger.debug_contexts["physics"].set_is_active(True)
logger.debug_contexts["physics"].add_direction(
	do_encode=False,
	file_handle=sys.stdout.fileno(),
	file_path=None
)
					       
# The below will add the time before each log message.
logger.debug_contexts["generic"].add_format_layer(Time_Formatter())
logger.debug_contexts["rendering"].add_format_layer(Time_Formatter())
logger.debug_contexts["physics"].add_format_layer(Time_Formatter())

# END OF MODIFYING DEBUG CONTEXTS #



#
# Now we can use the debug contexts to log messages.
#

logger.set_debug_mode("info")
save_logger(logger, "test_logger")



# SEE: `_inner_test.py` for the actual test.
# We separate in order to test the `save_logger` and `load_logger` functions.
subprocess.run(f"{sys.executable} test_inner.py", shell=True, cwd="tests")
