# -*- coding: utf-8 -*-
##j## BOF

"""
This is a Python "make" script to generate different output PHP scripts
based on "makefile.py" definitions for example for GPL/commercial
differences.
"""
"""n// NOTE
----------------------------------------------------------------------------
phpBuilder
Build PHP code for different release targets
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.php?php;builder

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.php?licenses;mpl2
----------------------------------------------------------------------------
#echo(phpBuilderVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from optparse import OptionParser
from php_builder import direct_php_builder
import os, re, sys

sys.path.append(os.getcwd())

try: import makefile
except: pass

_direct_php_builder_make = None

class direct_make(object):
#
	"""
"direct_make" is the main application object.

:author:    direct Netware Group
:copyright: direct Netware Group - All rights reserved
:package:   phpBuilder
:since:     v0.1.00
:license:   http://www.direct-netware.de/redirect.php?licenses;mpl2
            Mozilla Public License, v. 2.0
	"""

	option_parser = None
	"""
OptionParser instance
	"""

	"""
----------------------------------------------------------------------------
Construct the class
----------------------------------------------------------------------------
	"""

	def __init__(self):
	#
		"""
Constructor __init__ (direct_make)

:since: v0.1.00
		"""

		self.option_parser = OptionParser()
		self.option_parser.add_option("--define", action = "store", type = "string", dest = "define")
		self.option_parser.add_option("--filetype", action = "store", type = "string", dest = "filetype")
		self.option_parser.add_option("--include", action = "store", type = "string", dest = "include")
		self.option_parser.add_option("--output_path", action = "store", type = "string", dest = "output_path")
		self.option_parser.add_option("--exclude", action = "store", type = "string", dest = "exclude")
		self.option_parser.add_option("--exclude_dirs", action = "store", type = "string", dest = "exclude_dirs")
		self.option_parser.add_option("--exclude_files", action = "store", type = "string", dest = "exclude_files")
		self.option_parser.add_option("--strip_prefix", action = "store", type = "string", dest = "strip_prefix")
	#

	def run(self):
	#
		"""
Executes registered callbacks for the active application.

:since: v0.1.00
		"""

		( options, invalid_args ) = self.option_parser.parse_args()

		global _direct_phpBuilder_parameters
		targets = [ ]

		if (len(_direct_phpBuilder_parameters) > 0 and type(_direct_phpBuilder_parameters) == list):
		#
			for target in _direct_phpBuilder_parameters:
			#
				if ("make_output_path" in target): targets.append(target)
			#
		#
		elif (options.output_path != None):
		#
			_direct_phpBuilder_parameters.update({ "make_output_path":options.output_path })
			targets.append(_direct_phpBuilder_parameters)
		#

		if (options.filetype == None or options.include == None or len(targets) == 0): self.option_parser.print_help()
		else:
		#
			php_builder = None
			self.option_parser = None

			for target in targets:
			#
				if (options.define != None):
				#
					define_array = options.define.split(",")
					re_define = re.compile("^(\w+)\=(.+?)$")

					for define in define_array:
					#
						result_object = re_define.match(define)

						if (result_object == None):
						#
							define_key = define
							define_value = True
						#
						else:
						#
							define_key = result_object.group(1)
							define_value = result_object.group(2)
						#

						target[define_key] = define_value
					#
				#

				if (php_builder == None): php_builder = direct_php_builder(target, options.include, target['make_output_path'], options.filetype)
				else: php_builder.set_new_target(target, options.include, target['make_output_path'], options.filetype)

				if (options.exclude != None): php_builder.set_exclude(options.exclude)
				if (options.exclude_dirs != None): php_builder.set_exclude_dirs(options.exclude_dirs)
				if (options.exclude_files != None): php_builder.set_exclude_files(options.exclude_files)
				if (options.strip_prefix != None): php_builder.set_strip_prefix(options.strip_prefix)
				php_builder.make_all()
			#
		#
	#
#

print("""
----------------------------------------------------------------------------
phpBuilder #echo(phpBuilderVersion)#
(C) direct Netware Group - All rights reserved
----------------------------------------------------------------------------
""");

try:
#
	if (hasattr(makefile, "direct_makefile_php_set")): _direct_phpBuilder_parameters = makefile.direct_makefile_php_set()
	else: _direct_phpBuilder_parameters = makefile.direct_makefile_set()
#
except: _direct_phpBuilder_parameters = { }

try:
#
	_direct_php_builder_make = direct_make()
	_direct_php_builder_make.run()
#
except:
#
	sys.stderr.write("{0!r}".format(sys.exc_info()))
	sys.exit(1)
#
else: sys.exit(0)

##j## EOF