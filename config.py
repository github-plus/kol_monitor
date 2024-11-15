import telebot

flower = ['SarahJenni22188','jiji_eth','elonmusk','Ola_FDN']      #需要监控的博主名称,名字是@后面的

proxy = {'https':'http://127.0.0.1:8443','http':'http://127.0.0.1:8443'}   #代理


bot = telebot.TeleBot('1946515524:AAHm1E9NZcpnmLoxQlsdsgdfhdFXz4DxY')   #TG的机器人，可通过@BotFather获取
tg_user_id = 855654511 #TG的个人id，可以用过@userinfobot获取