formatted_input = ["generate", "A320", "BKK", "CNX"]
keyword, *params = formatted_input		# unpack value in list
print(f"keyword type:  {type(keyword)}")
print(f"keyword value: {keyword}")
print(f"params  type:  {type(params)}")
print(f"params  value: {params}")