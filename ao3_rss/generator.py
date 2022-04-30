from datetime import datetime
from bs4 import BeautifulSoup
from rfeed import Guid, Item, Feed, Image
from requests import Session
import AO3
from .extensions import WebfeedsIcon, Webfeeds

session = Session()

AO3_IMAGE = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD0AAAAqCAMAAAA3b6P4AAACslBMVEWXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACXAACpit0XAAAA5XRSTlMAAQIDBAUGBwgJCgsMDQ4PEBESFBUWFxgZGhscHR4fICEiIyQlJygpKissLi8wMTM0NTY3ODk6Ozw9PkBBQkNFR0hJSktMTU5PUFFSVFVWV1hZWltcXV5fY2RlZmhpamtsbW5vcHFyc3V2d3p7fX5/gIGCg4SFhoeIiouMjY6PkJGSlJWWl5iZmpucnZ6foKGipKWnqKmrrK2ur7CxsrO0tba3uLm6u7y9vr/AwsPFxsfIycrLzM7P0NLT1NXW19na29zd3t/g4eLj5OXm5+jp6uvs7e7v8PHy8/T19vf4+fr7/P3+b1plRQAABBRJREFUSMedlvtb1FUQxgcEBMtQggUCxVACu1ApYmRmUqESkCkUREaS4h3JCDONEFPBoBQCJcDIGxkGKYGBkgGSAq4BARIXWWA//0c/7J39LvY0P82cd97nzJlzZuaIKvBRmVqmP/XOrrQNIbOVsNfyjq/3nYrs/1GlWjPe90v28wrgnOiDP7ddeN9WAE47O9DLQI6PksfDMWVjnfuDlCC3b4HbpYcOFjUC9UHKWywtQZNpjTmdgu60uSIis979HRr8bIT4YjVDqV6TFlPgVqjxjBegyM4MfSPepDsm9tAcb5mwHnpfMJmq39C+ZLQCytrfM3deUAylwWYL2+BTc4eICU4aNk/pLgm0DNQuqY+/Nk8zmuX0PmFx83V0eIiIyOPlmq3Wpw+tg1OG7Lk1c8YSzmZsqYhIhLp7pVLy3AugLUqnz73L15boHogUke1cW6ic+5n7QJvhLCLic4cTlmAGRIhdFhfdlcmPpUjCfSj3FpEZ9dQ5W6CFDPrLIc652rj2FWUi0f1wdZGI5DERbg56dlIvO6hyt1UTe8pEZKUa1JEiMVBhDu6GzbHc8LFZUSXHRUTC/oShBHG5DKkmbPUg1xPujSyxSba/sltEREJuA9tl0Qikz9JD8f1ovrjOVtvF7NexRqcsVgOfSIIW6pMDVe7z3zwLHDjFeSfb7GV/P6fXwrqATInuAvraWruB0U2bx4aenqKRJA/MMairhoAsCczr1TWH8dPLfO7w2VRtqKDZFFjsOHBY5JmNX549dzQ5ROQkLY9MQbZvKDCzNgHkGCvaLRGOznS2zQ6e2GJu7gXY7/3kiqQj52ubbo9C143asm2hLsrsD3jV8l2PAbcGsBRN9VuK7B+Gvc3N+WnDKEuqAtlz8FdT37J/5dhdk3vbxUb4Y23UusT08nZAobyTSDeoD8VUmKja3DCVcylk6LB5J7Qcts54Ncv13PVXDMQWLfC9o4SOMxqmd/TqocSKvZirTiIiTusM3NbM5aq9AGccPoYaB73jwn/ItWJ/xQ4RkTWVOupg4VqViEw7ApBTA5l6P9/T8LrV1veHA0RCirQANKU/q193KdZHEiUiMjc2vxUO2E9ml5MlXhn9ANRsVJmAWdUAjAaLiKoRaN9pRX6bdv9VjQD8FGv5HgNuAjS5ioj3Hd3jnyS+7RQfA+BSpONkMFwD5OvOVzEClZNmuV0hE/cAqqOmK7yjD4ENen1Jhpo+y6xt1SXmWoKNEtzS8qOn0Zi3jw7z1hg+BNCZ5m2z/DxmmFuZ7DKbATeBsYKgKX8/C6JNehjfmEZ3DlAb8YC/k1dVlrHx5LHaNNZ7GElzlQdJwOXaOA8REb9sSh2Myw5xn78s/0Fmpzc0V+TmVY1y2lP+h3jF5l9qvPpdnP4I/wITXDY67Xw1sAAAAABJRU5ErkJggg=="

def download_chapter(chapter: AO3.Chapter):
	chapter_res = session.get(chapter.url)
	chapter_res.raise_for_status()

	soup = BeautifulSoup(chapter_res.text, "lxml")
	href = soup.select_one("a[href*=html][href*=downloads]")["href"]
	
	res = session.get("https://archiveofourown.org" + href)
	res.raise_for_status()
	return res.text

def generate_item(chapter: AO3.Chapter) -> Item:
	info = {}

	info["title"] = chapter.title

	authors = chapter.work.authors
	info["author"] = ", ".join(author.username for author in authors)

	url = chapter.url
	info["link"] = url
	info["guid"] = Guid(url)

	chapter_html = download_chapter(chapter)
	info["description"] = chapter_html

	return Item(**info)

def create_feed(work_id: int):
	work = AO3.Work(work_id)
	chapters = work.chapters

	url = work.url

	image = Image(
		AO3_IMAGE,
		"Logo for Archive of Our Own",
		url,
	)
	icon = WebfeedsIcon(AO3_IMAGE)

	info = {
		"title": work.title,
		"description": work.summary,
		"link": url,
		"items": map(generate_item, chapters),
		"extensions": [
			Webfeeds(),
			icon,
		],
		"image": image,
		"lastBuildDate": datetime.now(),
	}

	return Feed(**info)
