########################################################################################################### workflow for building manufacturing process related tables
################################################################################ import modules
from surfaicedbms import tsdbTransactions

################################################################################ initialize tsdb transactions
obj=tsdbTransactions.TsdbTransactions()

################################################################################ create id meta data and items tables
obj.createIdMetaDataTable()
obj.createItemsTable()
obj.registerItemsTrigger()

################################################################################ create tables for raw data
obj.createAccTable()
obj.createNcTable()

################################################################################ create table for merging tables
obj.createLiveDataTable()

################################################################################ create function and trigger to merge tables
obj.joinTables()

################################################################################ create continous aggregate
obj.continousAggregate()

################################################################################ create manufacturing_operations table
obj.createManufacturingOperationsTable()

################################################################################ create manufacturing_operations table
obj.createRarzTable()






