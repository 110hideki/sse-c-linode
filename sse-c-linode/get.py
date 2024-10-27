#!/usr/bin/env python3
import boto3
import argparse
import json

# 固定の設定ファイル名
CONFIG_FILE = "config.json"

# 引数を設定
parser = argparse.ArgumentParser(description="Upload, download, and delete a file with SSE-C encryption in S3.")
parser.add_argument("read_file", type=str, help="The input file to upload.")
parser.add_argument("output_file", type=str, help="The file name to save the downloaded content.")
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

# S3 固定の設定ファイル名
VAR_FILE = "var.json"

# 設定ファイルの読み込み
with open(VAR_FILE, 'r') as var_file:
    var_config = json.load(var_file)

ENCRYPTION_KEY = var_config["encryption_key"]
ALGO = var_config["algorithm"]
BUCKET = var_config["bucket_name"]

FILE = args.read_file

# S3クライアントの作成
client = boto3.client("s3", **aws_cfg)

print("Downloading encrypted Object Storage file.")

r2 = client.get_object(
    SSECustomerKey=ENCRYPTION_KEY,
    SSECustomerAlgorithm=ALGO,
    Bucket=BUCKET,
    Key=FILE
)

with open(args.output_file, 'wb') as output_file:
    output_file.write(r2["Body"].read())

print(f"Decrypted object saved to: {args.output_file}")

