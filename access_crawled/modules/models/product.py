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
from boto.dynamodb2.items import Item
from datetime             import datetime

class Product:
    """
    Product item
    """
    
    KEYS = [
        "MallID", 
        "Code", 
        "Name",
        "MallName",
        "Url",
        "Price"
        "CategoryMain",
        "CategoryAll", 
        "ImageUrl",
        "InsertDateTime",
    ]

    def __init__(self, item):
        self.item = item
        for key in KEYS:
            exec 'self.{0} = \'\''.format(key.lower())
            exec 'if \'{1}\' in data: self.{0} = data[\'{1}\']'.format(key.lower(), key)

    # template code of operator overloading
    def __eq__(self, other):
        return (self.mallid == other.mallid and self.code == other.code)
