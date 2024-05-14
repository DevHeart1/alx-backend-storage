#!/usr/bin/env python3
""" MongoDB Operations with Python using pymongo """

from pymongo import MongoClient

client = MongoClient()
db = client.logs
collection = db.nginx

# Count documents
total_documents = collection.count_documents({})

# Method counts
method_counts = collection.aggregate([
    {"$group": {"_id": "$method", "count": {"$sum": 1}}}
])

method_dict = {doc["_id"]: doc["count"] for doc in method_counts}

# Status check count
status_check_count = collection.count_documents({"path": "/status"})

# Print output
print(f"{total_documents} logs")
print("Methods:")

for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
    count = method_dict.get(method, 0)
    print(f"\tmethod {method}: {count}")

print(f"{status_check_count} status check")

client.close()
