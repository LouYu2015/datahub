function toPage(page)
{
	var str = window.location.search;
	if(window.location.search.search("page=") == -1)
	{
		if(str.length >= 1)
			str += "&";
		str += "page=" + page;
	}
	else
		str = str.replace(/page=[0-9a-zA-Z]+/, "page=" + page);
	window.location.search = str;
}