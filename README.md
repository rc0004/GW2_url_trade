# GW2 Trading Post Analysis Tool

Because I'm a massive nerd for virtual economies and numbers (can blame VCE Economics for this) I like to trade the commodities in these economies.
Fan made tools exist to find items with desirable spreads and also have an estimate of daily volume. There still exists unavoidable manual work, such as confirming
the volume and existing buy-sell spread is a result of "normal" market activity and not from interference by singular actors wishing to manipulate prices.

To be broadly successful at this kind of commodity trading requires placing bid orders for hundreds of items, and this is far too much manual work to go and check
the price chart history of each item. 

Therefore, I started working on this tool to both obtain a list of items with desirable spreads, and access historical data normally only shown on the website in the form of charts. This way, statistics such as moving averages of buy-sell prices and historical volume can be compared against current data. With this information, the resulting set of recommended trades can be filtered to only include items that are currently not trading above their historical price. 

Furthermore, this can be adapted to longer term trading instead of day trading (profiting on difference between current bid spreads), such as by examining weekly or longer term trends.


## Mechanics
Goes to gw2bltc.com and runs searches by inputting desired settings into a URL. Uses beautifulsoup to parse the HTML responses obtained by the Requests library. Pandas is used to extract tabular data on the resulting HTML result and will hold all needed information on the items.

## Problems already solved



## Current State


