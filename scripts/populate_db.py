import sys
# This is needed so as to be run on CLI
sys.path.append('/home/gfot/cucm-cdr-analyzer')

from modules import module_funcs

module_funcs.populate_db()


