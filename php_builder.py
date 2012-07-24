# -*- coding: utf-8 -*-
##j## BOF

"""
This is the main PHP "make" worker class file.

@internal   We are using epydoc (JavaDoc style) to automate the
            documentation process for creating the Developer's Manual.
            Use the following line to ensure 76 character sizes:
----------------------------------------------------------------------------
@author     direct Netware Group
@copyright  (C) direct Netware Group - All rights reserved
@package    ext_core
@subpackage phpBuilder
@since      v0.1.00
@license    http://www.direct-netware.de/redirect.php?licenses;w3c
            W3C (R) Software License
"""
"""n// NOTE
----------------------------------------------------------------------------
phpBuilder
Build PHP code for different release targets
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.php?phpBuilder

This work is distributed under the W3C (R) Software License, but without any
warranty; without even the implied warranty of merchantability or fitness
for a particular purpose.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.php?licenses;w3c
----------------------------------------------------------------------------
#echo(phpBuilderVersion)#
phpBuilder/#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

import re

from builder_skel import direct_builder_skel

class direct_php_builder (direct_builder_skel):
#
	"""
Provides a PHP "make" environment object.

@author     direct Netware Group
@copyright  (C) direct Netware Group - All rights reserved
@package    ext_core
@subpackage phpBuilder
@since      v1.0.0
@license    http://www.direct-netware.de/redirect.php?licenses;w3c
            W3C (R) Software License
	"""

	def data_parse (self,data,file_pathname,file_name):
	#
		"""
Parse the given content and return a line based array.

@param  data Data to be parsed
@param  file_pathname File path
@param  file_name File name
@return (mixed) Line based array; False on error
@since  v0.1.00
		"""

		data = direct_builder_skel.data_parse (self,data,file_pathname,file_name)
		return re.split ("\n",(self.parser ("/*#",data)))
	#

	def parser_change (self,tag_definition,data,tag_position,data_position,tag_end_position):
	#
		"""
Parse the given content and return a line based array.

@param  data Data to be parsed
@param  file_pathname File path
@param  file_name File name
@return (mixed) Line based array; False on error
@since  v0.1.00
		"""

		f_return = data[:tag_position]
		f_data_closed = data[self.parser_tag_find_end_position (data,tag_end_position,"*/"):]

		if (tag_definition[0] == "/*#ifdef"):
		#
			f_variable = re.match("^/\*#ifdef\((\w+)\)",data[tag_position:data_position]).group (1)
			f_tag_end = data[tag_end_position:self.parser_tag_find_end_position (data,tag_end_position,"*/")]

			if (self.get_variable (f_variable) == None):
			#
				if (data[data_position:(data_position + 1)] == "\n"): f_return += data[(data_position + 1):tag_end_position].replace ("*\\/","*/")
				else: f_return += data[data_position:tag_end_position].replace ("*\\/","*/")
			#

			if ((f_tag_end == "/* #\\n*/") or (f_tag_end == ":#\\n*/")): f_data_closed = re.sub ("^\n","",f_data_closed)
			f_return += f_data_closed
		#
		elif (tag_definition[0] == "/*#ifndef"):
		#
			f_variable = re.match("^/\*#ifndef\((\w+)\)",data[tag_position:data_position]).group (1)
			f_tag_end = data[tag_end_position:self.parser_tag_find_end_position (data,tag_end_position,"*/")]

			if (self.get_variable (f_variable) == None):
			#
				if (data[data_position:(data_position + 1)] == "\n"): f_return += data[(data_position + 1):tag_end_position].replace ("*\\/","*/")
				else: f_return += data[data_position:tag_end_position].replace ("*\\/","*/")
			#

			if ((f_tag_end == "/* #\\n*/") or (f_tag_end == ":#\\n*/")): f_data_closed = re.sub ("^\n","",f_data_closed)
			f_return += f_data_closed
		#
		elif (tag_definition[0] == "/*#use"):
		#
			f_function = re.match("^/\*#use\((\w+)\) \*/",data[tag_position:data_position]).group (1)
			f_tag_end = data[tag_end_position:self.parser_tag_find_end_position (data,tag_end_position,"*/")]

			if (self.get_variable ("PHP5n") != None):
			#
				f_return += re.sub ("^\n","",data[data_position:tag_end_position])
				if (f_tag_end == "/* #\\n*/"): f_data_closed = re.sub ("^\n","",f_data_closed)
			#
			else:
			#
				f_re_objects = re.finditer ("(\n|^)(.*?)use(\s*)(.+?)(\s*);",data[data_position:tag_end_position],( re.I | re.M | re.S ))
				for f_re_object in f_re_objects: f_return += "{0}{1}{2}('{3}');{4}".format (f_re_object.group (2),f_function,(f_re_object.group (3)),(f_re_object.group (4)),(f_re_object.group (5)))
			#

			f_return += f_data_closed
		#
		else: f_return += f_data_closed

		return f_return
	#

	def parser_check (self,data):
	#
		"""
Parse the given content and return a line based array.

@param  data Data to be parsed
@param  file_pathname File path
@param  file_name File name
@return (mixed) Line based array; False on error
@since  v0.1.00
		"""

		f_return = None

		if (data[:8] == "/*#ifdef"):
		#
			f_re_object = re.match ("^/\*#ifdef\((\w+)\) \*/",data)

			if (f_re_object == None):
			#
				f_re_object = re.match ("^/\*#ifdef\((\w+)\):",data)

				if (f_re_object == None): f_return = None
				else: f_return = ( "/*#ifdef",":",( ":#\\n*/",":#*/" ) )
			#
			else: f_return = ( "/*#ifdef","*/",( "/* #\\n*/","/* #*/" ) )
		#
		elif (data[:9] == "/*#ifndef"):
		#
			f_re_object = re.match ("^/\*#ifndef\((\w+)\) \*/",data)

			if (f_re_object == None):
			#
				f_re_object = re.match ("^/\*#ifndef\((\w+)\):",data)

				if (f_re_object == None): f_return = None
				else: f_return = ( "/*#ifndef",":",( ":#\\n*/",":#*/" ) )
			#
			else: f_return = ( "/*#ifndef","*/",( "/* #\\n*/","/* #*/" ) )
		#
		elif (data[:6] == "/*#use"):
		#
			f_re_object = re.match ("^/\*#use\((\w+)\) \*/",data)
			if (f_re_object != None): f_return = ( "/*#use","*/",( "/* #\\n*/","/* #*/" ) )
		#

		return f_return
	#
#

##j## EOF