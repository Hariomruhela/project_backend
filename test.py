import pymysql

try:
    connection = pymysql.connect(
        host="shortline.proxy.rlwy.net",
        port=18557,
        user="root",
        password="NlFInLKdKTbzxBFmqzAsetAMiePraeXi",
        database="railway",
        ssl={"ssl_mode": "REQUIRED"}
    )

    print("SUCCESS CONNECTED")

except Exception as e:
    print("ERROR:", e)