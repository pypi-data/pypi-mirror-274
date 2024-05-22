from surfaicedbms import mongoTransactions


########################################################################### starting data export
mongo = mongoTransactions.MongoTransactions()
mongo.queryTotalMrJSON()
print("Query results for total material removal of tool IDs have been generated.")


