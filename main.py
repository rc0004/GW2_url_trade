import requests
from bs4 import BeautifulSoup
import sys
import pandas as pd
import lxml

# url = "https://www.gw2bltc.com/en/tp/search?"

# other_param = "profit-min=1500&profit-pct-min=20&profit-pct-max=1000&sold-day-min=10&bought-day-min=10"

# Create class for search profiles and a way to construct URLs of any search inputs

class ItemSearch:
    def __init__(self, profit_min, roi_min, roi_max, sold, bought):
        self.profit_min = profit_min
        self.roi_min = roi_min
        self.roi_max = roi_max
        self.sold = sold
        self.bought = bought
        base_url = "https://www.gw2bltc.com/en/tp/search?"
        self.url = base_url +'profit-min=' + str(self.profit_min) + '&profit-pct-min=' + str(self.roi_min) +\
                              '&profit-pct-max=' + str(self.roi_max) + '&sold-day-min=' + str(self.sold) \
                              + '&bought-day-min=' + str(self.bought) + '&ipg=200'


    #def url_search(self):
    #    base_url = "https://www.gw2bltc.com/en/tp/search?"
    #   full_url = base_url + 'profit-min=' + str(self.profit_min) + '&profit-pct-min=' + str(self.roi_min) +\
      #                        '&profit-pct-max=' + str(self.roi_max) + '&sold-day-min=' + str(self.sold) \
     #                         + '&bought-day-min=' + str(self.bought) + '&ipg=200'
      #  return full_url


#Replaced by placing all the search settings into a list of tuples.
#first_list = ItemSearch(1000, 15, 1000, 50, 50)
#second_list = ItemSearch(1500, 20, 1000, 10, 10)
#third_list = ItemSearch(3000, 15, 1000, 25, 25)
#fourth_list = ItemSearch(4000, 12, 300, 10, 10)
#fifth_list = ItemSearch(10000, 12, 1000, 20, 20)
#sixth_list = ItemSearch(3000, 15, 1000, 5, 5)

## Need access to multiple pages inside the html -- <a class="btn btn-default"


# The following function can sometimes return None, if there's only a single page of results
# Need to create a way to handle this


def find_page_links(soup_content):
    pages_list = []
    button_html = soup_content.find_all('a', class_="btn btn-default", href=True)
    # This is the part causing issues in the function.
    # Note that the i does not want to be inside square brackets, as it gives
    # TypeError: 'builtin_function_or_method' object is not subscriptable
    # Issue can really just be due to lack of parentheses after .add
    # Fixing this gives issue: TypeError: list indices must be integers or slices, not str
    # This might be due to using .add instead of .update
    for x in button_html:
        pages_list.append(x.attrs['href'])
    page_urls = list(dict.fromkeys(pages_list))
    print(page_urls)
    return page_urls

# Finally solved this! Produces a list of tags, and only the ones I want. Will still need to clean this up so
# it only has the /en/item/ItemID-Item-Name-Here portion.


def item_urls(item_soup):
    item_url = []
    for item in item_soup:
        item_url.append(item.contents[0])
    return item_url


# Function to work through item_url_list, and pull out only the href link as a string, and the item name.
# Input: item_url_list [list of tags]
# Output: [[href, name], [href2, name2]]
# Because this may later need to be modified, makes sense to store as a list instead of a dictionary
# Current output has too many nested lists. Likely being caused by line 89. Temporarily list is having a list app.
# to it. So [[1,2], [3,4]]
# Then this temporarily list is being appended to another list item_name_urls [[[1,2,]...]]]
# Removed the temp_list and append directly to item_name_urls. This is working!
# Starts with empty list, then appends a list of length 2 that contains the contents[0] for name, and 'href' for
#HTML string.

def item_n_url(list_of_item_urls):
    item_name_urls = []
    for all_items in list_of_item_urls:
        #temp_list = []
        #temp_list.append([str(all_items.contents[0]),all_items['href']])
        item_name_urls.append([str(all_items.contents[0]), all_items['href']])
        #item_name_urls.append([tuple(all_items['href'], all_items.contents[0])])
    return item_name_urls


# ACTUALLY RUN CODE HERE

# Create list of tuples of search settings, format: Profit min (in copper) ROI min, ROI max, sold, bought)
search_list_settings = [(1000, 15, 1000, 50, 50), (1500, 20, 1000, 10, 10), (3000, 15, 1000, 25, 25),
                        (4000, 12, 300, 10, 10), (10000, 12, 1000, 20, 20), (3000, 15, 1000, 5, 5)]

# Create list of ItemSearch instances by unpacking the arguments of search_list_settings
item_search_list = []
for args in search_list_settings:
    ItemSearchobj = ItemSearch(*args)  # The * operator unpacks the 'args' tuple.
    item_search_list.append(ItemSearchobj)


# Use requests to get data from the URL portion
# To avoid getting stuck, added a timeout of 10 seconds

r = requests.get(item_search_list[5].url, timeout=10)
soup = BeautifulSoup(r.content, 'html.parser')

# Need to make a loop of requests!!!
# This actually takes a while, and can freeze up pycharm.

for search in item_search_list:
    r = requests.get(search.url, timeout=10)
    soup = BeautifulSoup(r.content, "lxml")
    page_url_uniques = find_page_links(soup)
    df = pd.read_html(r.text)
    item_info = soup.find_all('td', class_='td-name')
    item_url_list = item_urls(item_info)
    item_name_url = item_n_url(item_url_list)
    print(r.url)

# Coming up with extra results which are to do with the chevron buttons.
# But there are way more than there should be, above the table, and below it. Need to remove duplicates,
# which is being done by adding to a set.

page_url_uniques = find_page_links(soup)

#soup = BeautifulSoup(r.text, 'html.parser')
#with open("extra_page.txt", "w") as sys.stdout:
#    print(soup.prettify())
#sys.stdout.close()
#sys.stdout= sys.__stdout__

#print(r.text)


# The following code gives us a dataframe of the first page of results, around 200 items.
# From this point, need to think about how to utilise the historic trend data. Could keep this dataframe,
# use the other HTML information to throw the ItemID into a URL search to pull data from the arrays for the last 7
# days on sell price. Then calculate a single number for moving average of last 7 days, and create new cell in the
# data frame that corresponds to that. Then filter the dataframe to compare Sell and MovingAvg.
df = pd.read_html(r.text)

# List object has no attribute head
#df.head()


soup = BeautifulSoup(r.content, 'html.parser')

with open("list.txt", "w") as sys.stdout:
    print(soup.prettify())
sys.stdout.close()
sys.stdout = sys.__stdout__


# td class="td-name contains the a href we want: <a href="/en/item/43320-Jorbreaker">Jorbreaker</a>

# Gets the right data, but still includes all the info we don't want.
# Can we remove div class gw2po-btn??
# And remove i class +fa fa-code"
# And remove a class = "gw2po-btn-xs
# NOTE: "The call will still produce a sequence of tag objects, to get just the attributes, use subscription:"
# urls = [t['href'] for t in tags]

# Gives better list, but still gives entire td class tag, which includes the link to the wiki etc.
# It is classed as a bs4.element.ResultSet.
# Can't seem to loop through like a list to access tags[i].contents[0] -- i was doing this wrong!! i is the contents,
# not the index.
item_info = soup.find_all('td', class_='td-name')


#tags = soup.find_all('td', 'a', class_='td-name')

#tags.find('a')


# Call the function to get the URL list of all items on the first page
item_url_list = item_urls(item_info)

# item_url_list[0]['href'] points to the attrs dictionary object with key of 'href' and a string value of the URL.
# The question is what to do with this information - what happens if I extract these strings into their own list??
# Loop through list of URL strings, grab historical data of last 7 days.

# item_url_list[0]['href']

# At this stage we only have the URLs of the items - we have thrown away all the buy and sell data we probably
# want to use and compare to.
# ALl data of interest is in the <body> of the HTML, with each item being a table row <tr>, and each data cell being
# <td>


#Jorbreaker" class="gw2po-btn-xs" target="_blank" title="Guild Wars 2 Wiki"><i class="fa fa-wikipedia-w"></i></a></div></td> <td class="no-wrap text-right">" \
# "<span class="cur-t1c">3<i class="cur-1c" title="Gold Coin"></i></span><span class="cur-t1b">09<i class="cur-1b" title="Silver Coin"></i></span><span class="cur-t1a">94<i class="cur-1a" title="Copper Coin"></i>
# </span></td>
# Price 3g09s94c

#def url_stripped(object