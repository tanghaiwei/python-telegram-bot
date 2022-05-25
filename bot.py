# -*- coding: utf-8 -*-
import re

import requests
from bs4 import BeautifulSoup
from telegram.ext import CommandHandler, Updater

updater = Updater("5319342387:AAFCQ3e3jbzuWO3Slhia4FOLRCfob5uZhy0", workers=128)
dispatcher = updater.dispatcher


class Hax:
    def check(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
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
        vir_str = self.get_data_center("https://hax.co.id/create-vps")
        woiden_str = self.get_data_center("https://woiden.id/create-vps")
        data_center = f'[🚩Available Centers / 可开通区域]\n---------- Hax ----------\n{vir_str}\n---------- Woiden ----------\n{woiden_str}\n'
        msg = hax_stat + data_center
        return msg


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="欢迎使用Hax库存查询监控bot！\n输入 /help 获取帮助列表\n/输入get 获取当前库存情况\n输入/ping 检测bot存活状态",
    )


def help(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hax 库存查询监控BOT 帮助菜单\n/help 显示本菜单\n/get 获取当前库存情况\n/ping 检测bot存活状态",
    )


def ping(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="连接正常")


def get(update, context):
    res = Hax().main()
    context.bot.send_message(chat_id=update.effective_chat.id, text=res)


Start = CommandHandler("start", start, run_async=True)
Ping = CommandHandler("ping", ping, run_async=True)
Get = CommandHandler("get", get, run_async=True)
Help = CommandHandler("help", help, run_async=True)
dispatcher.add_handler(Ping)
dispatcher.add_handler(Start)
dispatcher.add_handler(Get)
dispatcher.add_handler(Help)

updater.start_polling()
