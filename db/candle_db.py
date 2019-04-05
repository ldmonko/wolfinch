#
# OldMonk Auto trading Bot
# Desc: order_db impl
# Copyright 2018, Joshith Rayaroth Koderi. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from utils import getLogger
from db import init_db
from sqlalchemy import *

log = getLogger ('CANDLE-DB')


class CandlesDb(object):
    def __init__ (self, exchange_name, product_id):
        self.db = init_db()
        log.info ("init candlesdb")
        self.table_name = "candle_%s_%s"%(exchange_name, product_id)
        if not self.db.engine.dialect.has_table(self.db.engine, self.table_name):  # If table don't exist, Create.
            # Create a table with the appropriate Columns
            log.info ("creating table: %s"%(self.table_name))            
            self.table = Table(self.table_name, self.db.metadata,
#                 Column('Id', Integer, primary_key=True, nullable=False), 
                Column('time', Interval, primary_key=True, nullable=False),
                Column('open', Numeric, default=0),
                Column('high', Numeric, default=0),
                Column('low', Numeric, default=0),
                Column('close', Numeric, default=0),
                Column('volume', Numeric, default=0))
            # Implement the creation
            self.db.metadata.create_all(self.db.engine, checkfirst=True)        
        else:
            log.info ("table %s exists already"%self.table_name)
            self.table = self.db.metadata.tables[self.table_name]
                    
    def __str__ (self):
        return "{time: %s, open: %g, high: %g, low: %g, close: %g, volume: %g}"%(
            str(self.time), self.open, self.high, self.low, self.close, self.volume)


    def db_save_candle (self, candle):
        log.debug ("Adding candle to db")
        self.db.connection.execute(self.table.insert(), candle)
        
    def db_save_candles (self, candles):
        log.debug ("Adding candle list to db")
        self.db.connection.execute(self.table.insert(), candles)
        
    def db_get_all_candles (self):
        log.debug ("retrieving candles from db")
        try:
            query = self.db.select([self.table])
            ResultProxy = self.db.connection.execute(query)
            ResultSet = ResultProxy.fetchall()
            log.info ("Retrieved %d candles for table: %s"%(len(ResultSet, self.table_name)))
            return ResultSet
        except Exception, e:
            print(e.message)        
   
# EOF