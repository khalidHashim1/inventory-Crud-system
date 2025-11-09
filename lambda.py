import json
import boto3
import csv
import io
import base64
import uuid
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("InventoryDB")

# Helper to convert Decimal back to float for JSON responses
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

# Standard API response
def response(status, body=None, content_type="application/json"):
    if isinstance(body, (dict, list)):
        body = json.dumps(body, default=decimal_default)
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": content_type,
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,PATCH,DELETE,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": body or ""
    }

# Recursively convert floats/ints to Decimal for DynamoDB
def convert_to_decimal(obj):
    if isinstance(obj, dict):
        return {k: convert_to_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_decimal(i) for i in obj]
    elif isinstance(obj, float) or isinstance(obj, int):
        return Decimal(str(obj))
    else:
        return obj

# List of DynamoDB reserved keywords
RESERVED_KEYWORDS = {"name", "status", "size", "type", "date"}

def lambda_handler(event, context):
    method = event["requestContext"]["http"]["method"]
    path = event["rawPath"]
    path_params = event.get("pathParameters") or {}

    # ----- CORS preflight -----
    if method == "OPTIONS":
        return response(200, "")

    # ----- GET /items -----
    if path == "/items" and method == "GET":
        items = table.scan().get("Items", [])
        items.sort(key=lambda x: x.get("id", ""))
        return response(200, items)

    # ----- POST /items -----
    if path == "/items" and method == "POST":
        data = json.loads(event.get("body") or "{}")
        if "name" not in data:
            return response(400, {"error": "Name required"})
        item = {
            "id": str(uuid.uuid4()),
            "name": data["name"],
            "quantity": Decimal(str(data.get("quantity", 0))),
            "price": Decimal(str(data.get("price", 0)))
        }
        table.put_item(Item=item)
        return response(201, item)

    # ----- PATCH /items/{id} -----
    if path.startswith("/items/") and method == "PATCH":
        item_id = path_params.get("id") or path.split("/")[-1]
        if not item_id:
            return response(400, {"error": "Missing item id"})
        data = json.loads(event.get("body") or "{}")

        update_expr = []
        expr_vals = {}
        expr_names = {}

        for key in ["name", "quantity", "price"]:
            if key in data:
                val = data[key]
                if key in ["quantity", "price"]:
                    val = Decimal(str(val))

                # Use ExpressionAttributeNames for reserved keywords
                if key in RESERVED_KEYWORDS:
                    placeholder = f"#{key}"
                    expr_names[placeholder] = key
                else:
                    placeholder = key

                update_expr.append(f"{placeholder} = :{key}")
                expr_vals[f":{key}"] = val

        if not update_expr:
            return response(400, {"error": "No fields to update"})

        table.update_item(
            Key={"id": item_id},
            UpdateExpression="SET " + ", ".join(update_expr),
            ExpressionAttributeValues=expr_vals,
            ExpressionAttributeNames=expr_names if expr_names else None
        )

        item = table.get_item(Key={"id": item_id}).get("Item")
        return response(200, item)

    # ----- DELETE /items/{id} -----
    if path.startswith("/items/") and method == "DELETE":
        item_id = path_params.get("id") or path.split("/")[-1]
        if not item_id:
            return response(400, {"error": "Missing item id"})
        table.delete_item(Key={"id": item_id})
        return response(204, "")

    # ----- POST /import -----
    if path == "/import" and method == "POST":
        if event.get("isBase64Encoded"):
            content = base64.b64decode(event["body"])
        else:
            content = event["body"].encode("utf-8")
        reader = csv.DictReader(io.StringIO(content.decode("utf-8")))
        count = 0
        with table.batch_writer() as batch:
            for row in reader:
                batch.put_item(Item={
                    "id": str(uuid.uuid4()),
                    "name": row.get("name", ""),
                    "quantity": Decimal(str(row.get("quantity", 0))),
                    "price": Decimal(str(row.get("price", 0)))
                })
                count += 1
        return response(200, {"imported": count})

    # ----- GET /export -----
    if path == "/export" and method == "GET":
        items = table.scan().get("Items", [])
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["id", "name", "quantity", "price"])
        writer.writeheader()
        writer.writerows(items)
        return response(200, output.getvalue(), "text/csv")

    # ----- 404 -----
    return response(404, {"error": "Not found"})
