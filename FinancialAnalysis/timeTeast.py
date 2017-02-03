import urllib2, csv
import pymongo
import emailUtil
import time

def getStockDto( symbol,company, sector, industry, country, mrktCap, pe, price, change, volume, beta, avgTruRnge, sma20,
                sma50, sma200, week52High, week52Low, relativeStrengthIndex, changeFromOpen, gap):
    if(symbol == "Ticker"):
        return {}
    labels = ["Symbol","Company","Sector","Industry","Country","Market Cap","P/E","Price","Change","Volume","Beta",
              "Average True Range","20 Day SMA","50 Day SMA","200 Day SMA","52 Week High","52 Week Low",
              "Relative Strength Index","Change From Open","Gap"]
    values = [symbol,company, sector, industry, country, mrktCap, pe, price, change, volume, beta, avgTruRnge, sma20,
                sma50, sma200, week52High, week52Low, relativeStrengthIndex, changeFromOpen, gap]
    stock = {}
    for i in range(len(labels)):
        stock[labels[i]] = values[i]
    print stock
    return stock

def insertIntoDb(dbName, collection, doc):
    client = pymongo.MongoClient("mongodb://python:W3lc0me1@35.162.119.179/"+dbName)  # defaults to port 27017

    db = client[dbName]

    dbCol = db[collection]
    post_id = dbCol.insert_one(doc).inserted_id
    print post_id

# try:
def main():
    urlOverview='http://elite.finviz.com/export.ashx?auth=kyrancahill@gmail.com&v=111&f=ind_stocksonly,sh_avgvol_o100,sh_price_o1,ta_highlow52w_b50h,ta_sma20_pb,ta_sma50_pb&ft=4&o=ticker'
    urlTechnical='http://elite.finviz.com/export.ashx?auth=kyrancahill@gmail.com&v=171&f=ind_stocksonly,sh_avgvol_o100,sh_price_o1,ta_highlow52w_b50h,ta_sma20_pb,ta_sma50_pb&ft=4&o=ticker'



    responseOverview = urllib2.urlopen(urlOverview)
    responseTechnical = urllib2.urlopen(urlTechnical)

    crOverview = csv.reader(responseOverview)
    crTechnical= csv.reader(responseTechnical)
    doc = {
        "date": time.strftime("%m/%d/%Y"),
        "stocks": []
    }
    for over, tech in zip(crOverview, crTechnical):
        # overview
        # ['0 No.', '1 Ticker', '2 Company', '3 Sector', '4 Industry', '5 Country', '6 Market Cap', '7 P/E', '8 Price', '9 Change', '10 Volume']

        # tech
        # ['0 No.', '1 Ticker', '2 Beta', '3 Average True Range', '4 20-Day Simple Moving Average', '5 50-Day Simple Moving Average',
        # '6 200-Day Simple Moving Average', '7 52-Week High', '8 52-Week Low', '9 Relative Strength Index (14)', '0 Price', '10 Change',
        #  '11 Change from Open', '12 Gap', '13 Volume']
        stock = getStockDto(over[1], over[2], over[3], over[4], over[5], over[6], over[7], over[8], over[9], over[10],
                            tech[2], tech[3], tech[4], tech[5], tech[6], tech[7], tech[8], tech[9], tech[11], tech[12])
        if stock:
            doc["stocks"].append(stock)

    print(doc)
    if doc:
        f = open('stocks.txt','w')
        f.write(str(doc))
        f.close()
        emailUtil.sendMail('alertmail760@gmail.com', ['dougfrieders@gmail.com'], 'Stock Report '+ time.strftime("%m/%d/%Y"), 'A new Document has arrived!', ['stocks.txt'])

# insertIntoDb("financial_db","daily_finviz_stocks",doc)

# except IndexError as e:
#     print "excetion" , e


try:
    main()
except urllib2.HTTPError, e:
    emailUtil.sendAlert()
except urllib2.URLError, e:
    emailUtil.error()
except Exception:
    emailUtil.sendAlert()