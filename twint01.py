import twint

def aa() :
    c = twint.Config()
    c.Proxy_host = '127.0.0.1'
    c.Proxy_port = 11000
    c.Proxy_type = 'HTTP' # Using HTTP or Socks5
    #c.Username = "realDonaldTrump"
    #c.Search = "(from:yux0829) until:2021-10-16 since:2021-10-14"
    c.Search = "(from:yux0829)"
   # c.Custom["tweet"] = ["id"]
    #c.Custom["user"] = ["yux0829"]
   # c.User_id='yux0829'
    #c.Lang='zh-cn'
    c.Since='2021-10-14 00:00:00'
    c.Until ='2021-10-16 23:59:59'
    c.Output = "d1.json"
    c.Store_json =True
    #c.Database ='data.db'

    # Run
    twint.run.Search(c)

def bb() :
    c = twint.Config()
    c.Username = "yux0829"
    c.Limit = 100
    c.Store_csv = True
    c.Output = "none.csv"
   # c.Lang = "en"
   # c.Translate = True
   # c.TranslateDest = "it"
    twint.run.Search(c)

aa()


#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())