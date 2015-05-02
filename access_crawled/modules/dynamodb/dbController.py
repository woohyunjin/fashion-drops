# Copyright 2014. Amazon Web Services, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from boto.dynamodb2.exceptions import ConditionalCheckFailedException
from boto.dynamodb2.exceptions import ItemNotFound
from boto.dynamodb2.exceptions import JSONResponseError
from boto.dynamodb2.exceptions import ValidationException
from boto.dynamodb2.items   import Item
from boto.dynamodb2.table   import Table
import time

class DBController:
    """
    This DBController class basically acts as a singleton providing the necessary 
    DynamoDB API calls.
    """
    def __init__(self, connectionManager):
        self.cm = connectionManager
        self.ResourceNotFound = 'com.amazonaws.dynamodb.v20120810#ResourceNotFoundException'
    

    # Data Insertion template
    def createNewMall(self, name, desc='', interval=5000):
        now = int(time.time())
        item = Item(self.cm.getMallTable(), data= {
                            "Name"      : name,
                            "Desc"      : desc,
                            "Timer"     : interval,
                            "InsertDateTime"       : now,
                        })
        
        return item.save()
    
    def checkIfTableIsActive(self, table):
        description = self.cm.db.describe_table(table)
        status = description['Table']['TableStatus']
    
        return status == "ACTIVE"
    
    def getMall(self, mallName):
        try:
            item = self.cm.getMallTable().get_item(Name=mallName)
        except ItemNotFound, inf:
            return None
        except JSONResponseError, jre:
            return None 
    
        return item
    
    # update query example
    def update_query_example(self, game):
        date = str(datetime.now())
        status = "IN_PROGRESS_"
        statusDate = status + date
        key = {
                "GameId" : { "S" : game["GameId"] }
            }
    
        attributeUpdates = {
                        "StatusDate" : {
                            "Action" : "PUT",
                            "Value"  : { "S" : statusDate }
                            }
                        }
    
        expectations = {"StatusDate" : {
                            "AttributeValueList": [{"S" : "PENDING_"}],
                            "ComparisonOperator": "BEGINS_WITH"}
                    }
    
        try:
            self.cm.db.update_item("Games", key=key, 
                        attribute_updates=attributeUpdates,
                        expected=expectations)
        except ConditionalCheckFailedException, ccfe:
            return False
    
        return True
    
    # delete query example
    def deleteProduct(self, product):
        """
        """
        
        key = {
                "MallName": { "S" : product.mallname }
                "Code": { "S" : product.code }
        }
        # expectation format
        expectation = {"StatusDate" : {
                            "AttributeValueList": [{"S" : "PENDING_"}],
                            "ComparisonOperator": "BEGINS_WITH" }
                    }
    
        try:
            self.cm.db.delete_item("Products", key, expected=None)
        except Exception, e:
            return False
    
        return True
    
    ############
    # Products #
    ############
    def getProducts(self, mallName=None, code=None, category=None, limit=10):
        """
        Get product items
        """

        products = []
        if not mallName and not category:
            return products

        conditions = {}
        if mallName:
            conditions['MallName__eq'] = mallName
        if category:
            conditions['index'] = 'CategoryMain-index'
            conditions['CategoryMain__eq'] = category
        if code:
            conditions['Code__beginswith'] = code
        conditions['limit'] = limit

        productIndex = self.cm.getProductTable().query(**conditions)

        for i in range(limit):
            try:
                product = productIndex.next()
            except StopIteration, si:
                break
            except ValidationException, ve:
                break
            except JSONResponseError, jre:
                if jre.body.get(u'__type', None) == self.ResourceNotFound:
                    return None
                else:
                    raise jre
                
            products.append(product)
    
        return products
