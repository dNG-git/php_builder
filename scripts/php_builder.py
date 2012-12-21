# -*- coding: utf-8 -*-
##j## BOF

"""
This is the main PHP "make" worker class file.
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

import re

from builder_skel import direct_builder_skel

class direct_php_builder(direct_builder_skel):
#
	"""
Provides a PHP "make" environment object.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    ext_core
:subpackage: phpBuilder
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.php?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def data_parse(self, data, file_pathname, file_name):
	#
		"""
Parse the given content.

:param data: Data to be parsed
:param file_pathname: File path
:param file_name: File name

:return: (mixed) Line based array; False on error
:since:  v0.1.00
		"""

		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -phpBuilder.data_parse(data)- (#echo(__LINE__)#)")
		data = self.parser("/*#", direct_builder_skel.data_parse(self, data, file_pathname, file_name))

		if (self.get_variable("dev_comments") == None): return self.data_remove_dev_comments(data)
		else: return data
	#

	def data_remove_dev_comments(self, data):
	#
		"""
Remove all development comments from the content.

:param data: Data to be parsed

:return: (str) Filtered data
:since:  v0.1.00
		"""

		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -phpBuilder.data_remove_dev_comments(data)- (#echo(__LINE__)#)")
		return re.sub("(/\* ---.+?--- \*/\n\n)|(/\*\*\n.+?\n\*/\n)", "", data, 0, re.S)
	#

	def parser_change(self, tag_definition, data, tag_position, data_position, tag_end_position):
	#
		"""
Change data according to the matched tag.

:param tag_definition: Matched tag definition
:param data: Data to be parsed
:param tag_position: Tag starting position
:param data_position: Data starting position
:param tag_end_position: Starting position of the closing tag

:return: (str) Converted data
:since:  v0.1.00
		"""

		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -phpBuilder.parser_change(tag_definition, data, {0:d}, {1:d}, {2:d})- (#echo(__LINE__)#)".format(tag_position, data_position, tag_end_position))
		var_return = data[:tag_position]

		data_closed = data[self.parser_tag_find_end_position(data, tag_end_position, "*/"):]

		if (tag_definition[0] == "/*#ifdef"):
		#
			variable = re.match("^/\*#ifdef\((\w+)\)", data[tag_position:data_position]).group(1)
			tag_end = data[tag_end_position:self.parser_tag_find_end_position(data, tag_end_position, "*/")]

			if (self.get_variable(variable) != None):
			#
				if (data[data_position:data_position + 1] == "\n"): var_return += data[data_position + 1:tag_end_position].replace("/*\\#", "/*#").replace("*\\/", "*/")
				else: var_return += data[data_position:tag_end_position].replace("/*\\#", "/*#").replace("*\\/", "*/")
			#

			if (tag_end == "/* #\\n*/" or tag_end == ":#\\n*/"): data_closed = re.sub("^\n", "", data_closed)
			var_return += data_closed
		#
		elif (tag_definition[0] == "/*#ifndef"):
		#
			variable = re.match("^/\*#ifndef\((\w+)\)", data[tag_position:data_position]).group(1)
			tag_end = data[tag_end_position:self.parser_tag_find_end_position(data, tag_end_position, "*/")]

			if (self.get_variable(variable) == None):
			#
				if (data[data_position:data_position + 1] == "\n"): var_return += data[data_position + 1:tag_end_position].replace("/*\\#", "/*#").replace("*\\/", "*/")
				else: var_return += data[data_position:tag_end_position].replace("/*\\#", "/*#").replace("*\\/", "*/")
			#

			if (tag_end == "/* #\\n*/" or tag_end == ":#\\n*/"): data_closed = re.sub("^\n", "", data_closed)
			var_return += data_closed
		#
		elif (tag_definition[0] == "/*#use"):
		#
			var_function = re.match("^/\*#use\((\w+)\) \*/", data[tag_position:data_position]).group(1)
			tag_end = data[tag_end_position:self.parser_tag_find_end_position(data, tag_end_position, "*/")]

			if (self.get_variable("PHP5n") != None):
			#
				var_return += re.sub("^\n", "", data[data_position:tag_end_position])
				if (tag_end == "/* #\\n*/"): data_closed = re.sub("^\n", "", data_closed)
			#
			else:
			#
				re_objects = re.finditer("(\n|^)(.*?)use(\s*)(.+?)(\s*);", data[data_position:tag_end_position], ( re.I | re.M | re.S ))
				use_lines = ""

				for re_object in re_objects:
				#
					if (len(use_lines) > 0): use_lines += "{0}".format(re_object.group(1))
					use_lines += "{0}{1}('{2}');".format(re_object.group(2), var_function, re_object.group(4))
				#

				var_return += use_lines
			#

			var_return += data_closed
		#
		else: var_return += data_closed

		return var_return
	#

	def parser_check(self, data):
	#
		"""
Check if a possible tag match is a false positive.

:param data: Data starting with the possible tag

:return: (mixed) Matched tag definition; None if false positive
:since:  v0.1.00
		"""

		if (self.event_handler != None): self.event_handler.debug("#echo(__FILEPATH__)# -phpBuilder.parser_check(data)- (#echo(__LINE__)#)")
		var_return = None

		if (data[:8] == "/*#ifdef"):
		#
			re_object = re.match("^/\*#ifdef\((\w+)\) \*/", data)

			if (re_object == None):
			#
				re_object = re.match("^/\*#ifdef\((\w+)\):", data)

				if (re_object == None): var_return = None
				else: var_return = ( "/*#ifdef", ":", ( ":#\\n*/", ":#*/" ) )
			#
			else: var_return = ( "/*#ifdef", "*/", ( "/* #\\n*/", "/* #*/" ) )
		#
		elif (data[:9] == "/*#ifndef"):
		#
			re_object = re.match("^/\*#ifndef\((\w+)\) \*/", data)

			if (re_object == None):
			#
				re_object = re.match("^/\*#ifndef\((\w+)\):", data)

				if (re_object == None): var_return = None
				else: var_return = ( "/*#ifndef", ":", ( ":#\\n*/", ":#*/" ) )
			#
			else: var_return = ( "/*#ifndef", "*/", ( "/* #\\n*/", "/* #*/" ) )
		#
		elif (data[:6] == "/*#use"):
		#
			re_object = re.match("^/\*#use\((\w+)\) \*/", data)
			if (re_object != None): var_return = ( "/*#use", "*/", ( "/* #\\n*/", "/* #*/" ) )
		#

		return var_return
	#
#

##j## EOF