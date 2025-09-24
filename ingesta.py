import os
import csv
import boto3
import pymysql

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "test")
MYSQL_TABLE = os.getenv("MYSQL_TABLE", "alumnos")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_PREFIX = os.getenv("S3_PREFIX", "")
CSV_NAME = os.getenv("CSV_NAME", f"{MYSQL_TABLE}.csv")

if not S3_BUCKET:
    raise SystemExit("Missing env var S3_BUCKET")

def export_table_to_csv():
    conn = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        cursorclass=pymysql.cursors.Cursor,
    )
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM `{MYSQL_TABLE}`")
            rows = cur.fetchall()
            # Column names
            headers = [desc[0] for desc in cur.description]
    finally:
        conn.close()

    out_path = os.path.abspath(CSV_NAME)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"[OK] CSV generado: {out_path}")
    return out_path

def upload_to_s3(file_path: str):
    s3 = boto3.client("s3")
    key = f"{S3_PREFIX}/{os.path.basename(file_path)}" if S3_PREFIX else os.path.basename(file_path)
    s3.upload_file(file_path, S3_BUCKET, key)
    print(f"[OK] subido a s3://{S3_BUCKET}/{key}")

if __name__ == "__main__":
    csv_path = export_table_to_csv()
    upload_to_s3(csv_path)
    print("ingesta completada 🚀")
