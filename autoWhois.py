import os
import json
#from urllib import request
import requests



if __name__ == "__main__" :
    
    country_tag = ""
    ip_all = dict()
    try :
        with open("all_ip.csv", "r", encoding="UTF8") as f :
            while True:
                s = f.readline()
                s = s.replace("\n", "").replace("\r", "")
                ip_all[s] = 'Unknow'
                if len(s) == 0:
                    break
        
        print("全部 ip 讀取")
        #print(ip_all)
        
        with open("ip_to_conutry.txt", "w", encoding="UTF8") as f1 :
            print("查詢中 ~~~")
            for ip_k in ip_all.keys():
                json_ret = requests.get("http://wq.apnic.net/query?searchtext=" + ip_k)
                
                country_tag = "Unknow"
                
                try:
                    #if json_ret.json()[4]['attributes'][5]['name'] == "country" :
                    #    #print(s + "\t" + json_ret.json()[4]['attributes'][5]['values'][0])
                    #    country_tag = json_ret.json()[4]['attributes'][5]['values'][0]
                    #    f1.write(s + "," + country_tag + "\n")
                    #elif json_ret.json()[4]['attributes'][6]['name'] == "country" :
                    #    #print(s + "\t" + json_ret.json()[4]['attributes'][6]['values'][0])
                    #    country_tag = json_ret.json()[4]['attributes'][6]['values'][0]
                    #    f1.write(s + "," + country_tag + "\n")
                    
                    
                    json_str = json.dumps(json_ret.json(),separators=(',', ':'))
                    f_s = json_str.find("{\"name\":\"country\",\"values\":[\"") + len("{\"name\":\"country\",\"values\":[\"")
                    country_tag = json_str[f_s:f_s+2]
                    #print("find country tag: " + country_tag)
                                            
                    ip_all[ip_k] = country_tag
                except Exception as err :
                    json_str = json.dumps(json_ret.json(),separators=(',', ':'))
                    f_s = json_str.find("{\"name\":\"country\",\"values\":[\"") + len("{\"name\":\"country\",\"values\":[\"")
                    country_tag = json_str[f_s:f_s+2]
                    #print("find country tag: " + country_tag)
                                            
                    ip_all[ip_k] = country_tag
                    
                    with open(s + ".ip_err", "w", encoding="UTF8") as f2:
                        f2.write(json_ret.text)
                        f2.write("\n")
                        f2.write(str(err))
                    
                #print(ip_k + "查詢成功 tag 是 " + country_tag)
                    
                if country_tag == "TW" :
                    print(ip_k + "\t" + country_tag)
                    with open("ip_TW.txt", "a", encoding="UTF8") as f3:
                        f3.write(ip_k + "\t" + country_tag + "\n")

            
            json.dumps(ip_all, f1)
                            
    except Exception as outer_err:
        print(str(outer_err))