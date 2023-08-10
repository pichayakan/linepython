import requests
import schedule
import time
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%d-%m-%Y %H:%M:%S")


def send_line_gold(access_token, gold):
    if gold == "gold":
        url_gold = "https://api.chnwt.dev/thai-gold-api/latest"
        url_oil = "https://api.chnwt.dev/thai-oil-api/latest"
        response_api = requests.get(url_gold)
        data = response_api.json()

        # This is line part

        if response_api.status_code == 200:
            # print("Message sent successfully.")
            # print(data)
            day = data["response"]["date"]
            times = data["response"]["update_time"]
            gold_buy = data["response"]["price"]["gold"]["buy"]
            gold_sell = data["response"]["price"]["gold"]["sell"]
            gold_bar_buy = data["response"]["price"]["gold_bar"]["buy"]
            gold_bar_sell = data["response"]["price"]["gold_bar"]["sell"]
            change = data["response"]["price"]["change"]["compare_previous"]
            message = (
                f"{day} \n"
                f"{times} \n"
                f"###### ราคาทอง ######## \n"
                f"ทองคำแท่งรับซื้อ : {gold_bar_buy} บาท\n"
                f"ทองคำแท่งขายออก : {gold_bar_sell} บาท\n"
                f"ทองรูปพรรณรับซื้อ : {gold_buy} บาท\n"
                f"ทองรูปพรรณขายออก : {gold_sell} บาท\n"
                f" \n"
                f"วันนี้ขึ้น-ลง : {change} \n"
                f"........................ \n"
            )
            line_url = "https://notify-api.line.me/api/notify"
            headers = {"Authorization": f"Bearer {access_token}"}
            line_data = {"message": message}
            response = requests.post(line_url, headers=headers, data=line_data)

            print(f"system time:\n", formatted_datetime + f" \n" + message)

        else:
            print(f"Failed to send message. Status code: {response.status_code}")
            print(response_api.text)


def send_line_oil(access_token, oil):
    if oil == "oil":
        # url_gold = "https://api.chnwt.dev/thai-gold-api/latest"
        url = "https://api.chnwt.dev/thai-oil-api/latest"
        response_api = requests.get(url)
        data = response_api.json()

        # This is line part

        if response_api.status_code == 200:
            day = data["response"]["date"]

            response = data.get("response")
            stations = response.get("stations", {})
            ptt_station = stations.get("ptt", {})
            gasoline_95 = ptt_station.get("gasoline_95", {})
            gasohol_95 = ptt_station.get("gasohol_95", {})
            gasohol_91 = ptt_station.get("gasohol_91", {})
            gasohol_e20 = ptt_station.get("gasohol_e20", {})
            gasohol_e85 = ptt_station.get("gasohol_e85", {})
            diesel = ptt_station.get("diesel", {})
            diesel_b7 = ptt_station.get("diesel_b7", {})
            diesel_b20 = ptt_station.get("diesel_b20", {})
            premium_diesel = ptt_station.get("premium_diesel", {})
            premium_gasohol_95 = ptt_station.get("premium_gasohol_95", {})
            superpower_gasohol_95 = ptt_station.get("superpower_gasohol_95", {})

            message = (
                f"{day} \n"
                f"######## ราคาน้ำมัน ปตท. ########## \n"
                f"{gasoline_95.get('name')} : {gasoline_95.get('price')} บาท\n"
                f"{gasohol_95.get('name')} : {gasohol_95.get('price')} บาท\n"
                f"{gasohol_91.get('name')} : {gasohol_91.get('price')} บาท\n"
                f"{gasohol_e20.get('name')} : {gasohol_e20.get('price')} บาท\n"
                f"{gasohol_e85.get('name')} : {gasohol_e85.get('price')} บาท\n"
                f"{diesel.get('name')} : {diesel.get('price')} บาท\n"
                f"{diesel_b7.get('name')} : {diesel_b7.get('price')} บาท\n"
                f"{diesel_b20.get('name')} : {diesel_b20.get('price')} บาท\n"
                f"{premium_diesel.get('name')} : {premium_diesel.get('price')} บาท\n"
                f"{premium_gasohol_95.get('name')} : {premium_gasohol_95.get('price')} บาท\n"
                f"{superpower_gasohol_95.get('name')} : {superpower_gasohol_95.get('price')} บาท\n"
                f" \n"
                f"........................ \n"
            )
            # message = "oil message"
            line_url = "https://notify-api.line.me/api/notify"
            headers = {"Authorization": f"Bearer {access_token}"}
            line_data = {"message": message}
            response = requests.post(line_url, headers=headers, data=line_data)

            print(f"system time:\n", formatted_datetime + f" \n" + message)

        else:
            print(f"Failed to send message. Status code: {response.status_code}")
            print(response_api.text)


def send_message_periodically():
    access_token = os.environ.get("LINE_TOKEN_TEST")
    gold = "gold"
    oil = "oil"
    send_line_gold(access_token, gold)
    send_line_oil(access_token, oil)


if __name__ == "__main__":
    # Schedule the job to run every 1 minute
    schedule.every(1).minutes.do(send_message_periodically)

    # Schedule the job to run fix time table
    # schedule.every().day.at("09:30").do(send_message_periodically)
    # schedule.every().day.at("11:30").do(send_message_periodically)
    # schedule.every().day.at("13:30").do(send_message_periodically)
    # schedule.every().day.at("15:30").do(send_message_periodically)
    # schedule.every().day.at("16:30").do(send_message_periodically)

    print(f"###### เริ่มเวลา ######:\n", formatted_datetime + f" \n")

    for job in schedule.get_jobs():
        print("Job will be run at {}, {}".format(job.start_day, job.at_time))

    # Keep the script running to execute scheduled jobs
    while True:
        schedule.run_pending()
        time.sleep(1)
