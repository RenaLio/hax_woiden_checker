import asyncio
import re
import requests
from bs4 import BeautifulSoup
from telebot.async_telebot import AsyncTeleBot

bot_token = ""
bot = AsyncTeleBot(bot_token)


class Hax:
    def check(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39",
            "Content-type": "application/json",
        }
        datas = requests.get(url, headers=headers).text
        return datas

    def get_server_info(self, url):
        html_text = self.check(url)
        soup = BeautifulSoup(html_text, "html.parser")
        zone_list = [x.text for x in soup("h5", class_="card-title mb-4")]
        sum_list = [x.text for x in soup("h1", class_="card-text")]
        vps_list = []
        vps_dict = {}
        vps_str = ""
        for k, v in zip(zone_list, sum_list):
            zone = k.split("-", 1)[0].lstrip("./")
            sum = (
                k.split("-", 1)[1] + "(" + v.rstrip(" VPS") + "♝)"
                if len(k.split("-", 1)) > 1
                else v
            )
            vps_list.append((zone, sum))
        for k_v in vps_list:
            k, v = k_v
            vps_dict.setdefault(k, []).append(v)
        for k, v in vps_dict.items():
            vps_str += ">>" + k + "-" + ", ".join(v) + "\n"
        return vps_str

    def get_data_center(self, url, vir=False):
        html_text = self.check(url)
        soup = BeautifulSoup(html_text, "html.parser")
        ctr_list = [x.text for x in soup("option", value=re.compile(r"^[A-Z]{2,}-"))]
        ctr_str = "\n".join(ctr_list)
        if vir:
            ctr_list = [
                (c.split(" (")[1].rstrip(")"), c.split(" (")[0]) for c in ctr_list
            ]
            ctr_dict = {}
            ctr_str = ""
            for k_v in ctr_list:
                k, v = k_v
                ctr_dict.setdefault(k, []).append(v)
            for k, v in ctr_dict.items():
                ctr_str += "★" + k + "★ " + ", ".join(v) + "\n"
        return ctr_str

    def main(self):
        hax_str = self.get_server_info("https://hax.co.id/data-center")
        hax_stat = f"[🛰Hax Stats / Hax 开通数据]\n{hax_str}\n"
        vir_str = self.get_data_center("https://hax.co.id/create-vps", True)
        woiden_str =self.get_data_center("https://woiden.id/create-vps",True)
        data_center = f'[🚩Available Centers / 可开通区域]\n`hax.co.id`\n{vir_str}`woiden.id`\n{woiden_str}\n'
        msg = hax_stat + data_center
        return msg


@bot.message_handler(commands=['ping'])
async def send_welcome(message):
    await bot.send_message(message.chat.id, "pong")



@bot.message_handler(commands=['both'])
async def echo_message(message):
    res = Hax().main()
    await bot.send_message(message.chat.id, res)

if __name__ == "__main__":
    asyncio.run(bot.polling())


