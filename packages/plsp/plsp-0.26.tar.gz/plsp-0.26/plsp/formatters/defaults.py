from .I_Final_Formatter import I_Final_Formatter as __I_Final_Formatter







class Default_Final_Formatter(__I_Final_Formatter):



	def raw_handle(self, string:str) -> str:
		return self._strip_postfixes(string)
	





