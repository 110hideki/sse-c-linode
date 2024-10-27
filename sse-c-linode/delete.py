#!/usr/bin/env python3
import boto3
import argparse
import json

# 固定の設定ファイル名
CONFIG_FILE = "config.json"
VAR_FILE = "var.json"

# 引数を設定
parser = argparse.ArgumentParser(description="Delete a file from Object Storage with confirmation.")
parser.add_argument("delete_file", type=str, help="The file name to delete from Object Storage.")
args = parser.parse_args()

# 設定ファイルの読み込み
with open(CONFIG_FILE, 'r') as config_file:
    config = json.load(config_file)

# AWS設定と変数を取得
aws_cfg = {
    "aws_access_key_id": config["aws_access_key_id"],
    "aws_secret_access_key": config["aws_secret_access_key"],
    "endpoint_url": config["endpoint_url"]
}

# 変数ファイルの読み込み
with open(VAR_FILE, 'r') as var_file:
    var_config = json.load(var_file)

ENCRYPTION_KEY = var_config["encryption_key"]
ALGO = var_config["algorithm"]
BUCKET = var_config["bucket_name"]

DELETE_FILE = args.delete_file

# S3クライアントの作成
client = boto3.client("s3", **aws_cfg)

# 削除確認のプロンプト
confirmation = input(f"Are you sure you want to delete '{DELETE_FILE}' from bucket '{BUCKET}'? Type 'yes' to confirm: ")

if confirmation.lower() == 'yes':
    print("Deleting encrypted Object Storage file.")
    r3 = client.delete_object(
        Bucket=BUCKET,
        Key=DELETE_FILE
    )

    if r3["ResponseMetadata"]["HTTPStatusCode"] == 204:
        print("Deletion successful.")
    else:
        print("Deletion failed.")
else:
    print("Deletion canceled.")

