from rest_framework import parsers

class NestedMultipartParser(parsers.MultiPartParser):

	def parse(self, stream, media_type=None, parser_context=None):

		result = super().parse(stream=stream, media_type=media_type, parser_context=parser_context)

		data = {}
		print(result.data)
		for key, value in result.data.items():
			if '.' in key:
				dict_key = key.split('.')
				nested_dict_key = dict_key[0]
				nested_value_key = dict_key[1]

				if nested_dict_key not in data:
					data[nested_dict_key] = {}

				data[nested_dict_key][nested_value_key] = value 


				# if nested_value_key not in data:
				# 	data[nested_dict_key] = {}
				# 	data[nested_dict_key][nested_value_key] = value
				# else:
				# 	data[key] = value
			else:
				data[key] = value
		return parsers.DataAndFiles(data,result.files)



