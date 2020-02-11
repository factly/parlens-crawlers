from scrapy.exceptions import DropItem
import datetime
import time
import json
import pymongo

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

class DuplicateCleaner(object):
    def open_spider(self, spider):
        config = json.load(open("./../config.cfg"))
        
        self.client = pymongo.MongoClient(config['mongodb_uri'])
        db = self.client[config['database']]
        questionDict = list(db.all_members.find({'terms.to': { '$gt': datetime.datetime.now().timestamp() * 1000 } }, {'RSID': 1}))
       
        self.membersPresent = list()
        
        for each in questionDict:
            self.membersPresent.append(each['RSID'])

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
       
        if(item['RSID'] not in self.membersPresent):
            return item
        else:
            raise DropItem('already_there')

class GeoTermCleaner(object):
    def open_spider(self, spider):
        config = json.load(open("./../config.cfg"))
        
        self.client = pymongo.MongoClient(config['mongodb_uri'])
        db = self.client[config['database']]
        states = list(db.all_geography.find({'type': 'state'}))
       
        self.statesDict = dict()
        for each in states:
            self.statesDict[each['name']] = each['GID']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if(item['geography'] in self.statesDict):
            item['geography'] = self.statesDict[item['geography']]
            return item
        else:
            missing_message = {
                'RSID': item['RSID'],
                'item': item['geography'],
                'message': "geography not found"
            }
            spider.error.write(json.dumps(missing_message) + "\n")
            raise DropItem('geo_not_found')

class PartyTermCleaner(object):
    def open_spider(self, spider):
        config = json.load(open("./../config.cfg"))
        
        self.client = pymongo.MongoClient(config['mongodb_uri'])
        db = self.client[config['database']]
        parties = list(db.all_parties.find({}))
       
        self.partiesDict = dict()
        for each in parties:
            self.partiesDict[each['name']] = each['PID']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        
        if(item['party'] in self.partiesDict):
            item['party'] = self.partiesDict[item['party']]
            return item
        else:
            missing_message = {
                'RSID': item['RSID'],
                'item': item['party'],
                'message': "party not found"
            }
            spider.error.write(json.dumps(missing_message) + "\n")
            raise DropItem('party_not_found')

class TermConstructor(object):
    def process_item(self, item, spider):
        item['term'] = {
            'geography': item['geography'],
            'party': item['party'],
            'house': 2,
            'session': None,
            'from': None,
            'to': None
        }

        del item['geography']
        del item['party']

        return item