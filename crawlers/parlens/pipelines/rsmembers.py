import datetime
import time

class ChildrenCleaner(object):
    def process_item(self, item, spider):
        if 'children' in item and item['children'] != None:
            units = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

            childList = " ".join(item['children'].split()).lower().split(" ")
            if "son" in childList:
                sonPost = childList.index("son")
                if(sonPost >= 1):
                    sonWord = childList[sonPost - 1]
                    if(sonWord in units):
                        sonUnit = units.index(sonWord)
                        item['sons'] = sonUnit
                    else:
                        print('son unit error', item['name'])
                else:
                    print("son index zero", item['name'])

            elif "sons" in childList:
                sonPost = childList.index("sons")
                if(sonPost >= 1):
                    sonWord = childList[sonPost - 1]
                    if(sonWord in units):
                        sonUnit = units.index(sonWord)
                        item['sons'] = sonUnit
                    else:
                        print('sons unit error', item['name'])
                else:
                    print("sons index zero", item['name'])
            
            if "daughter" in childList:
                daughterPost = childList.index("daughter")
                if(daughterPost >= 1):
                    daughterWord = childList[daughterPost - 1]
                    if(daughterWord in units):
                        daughterUnit = units.index(daughterWord)
                        item['daughters'] = daughterUnit
                    else:
                        print('daughter unit error', item['name'])
                else:
                    print("daughter index zero", item['name'])

            elif "daughters" in childList:
                daughterPost = childList.index("daughters")
                if(daughterPost >= 1):
                    daughterWord = childList[daughterPost - 1]
                    if(daughterWord in units):
                        daughterUnit = units.index(daughterWord)
                        item['daughters'] = daughterUnit
                    else:
                        print('daughter unit error', item['name'])
                else:
                    print("daughter index zero", item['name'])

        if 'sons' not in item:
            item['sons'] = None
        
        if 'daughters' not in item:
            item['daughters'] = None
            
        del item['children']

        return item

class DOBCleaner(object):
    def process_item(self, item, spider):
        if 'dob' in item and item['dob'] != None:
            item['dob'] = int(time.mktime(datetime.datetime.strptime(item['dob'], "%d %B %Y").timetuple()) * 1000)
        else:
            item['dob'] = None

        return item