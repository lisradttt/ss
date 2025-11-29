from pyrogram import Client, filters
from youtubesearchpython.__future__ import VideosSearch 
import os
import aiohttp
import requests
import random 
import asyncio
import yt_dlp
from datetime import datetime, timedelta
from youtube_search import YoutubeSearch
import pytgcalls
from pytgcalls.types.input_stream.quality import (HighQualityAudio,
                                                  HighQualityVideo,
                                                  LowQualityAudio,
                                                  LowQualityVideo,
                                                  MediumQualityAudio,
                                                  MediumQualityVideo)
from typing import Union
from pyrogram import Client, filters 
from pyrogram import Client as client
from pyrogram.errors import (ChatAdminRequired,
                             UserAlreadyParticipant,
                             UserNotParticipant)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType, ChatMemberStatus
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.exceptions import (AlreadyJoinedError,
                                  NoActiveGroupCall,
                                  TelegramServerError)
from pytgcalls.types import (JoinedGroupCallParticipant,
                             LeftGroupCallParticipant, Update)
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.stream import StreamAudioEnded
from config import API_ID, API_HASH, MONGO_DB_URL, VIDEO, OWNER, OWNER_NAME, LOGS, GROUP, CHANNEL, PHOTO
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from pymongo import MongoClient
from bot import bot as man
from KERO.info import (db, add, is_served_call, add_active_video_chat, add_served_call, add_active_chat, gen_thumb, download, remove_active, joinch)
from KERO.Data import (get_logger, get_userbot, get_call, get_logger_mode, get_group, get_channel)
import asyncio
             
mongodb = _mongo_client_(MONGO_DB_URL)
pymongodb = MongoClient(MONGO_DB_URL)
Bots = pymongodb.Bots


async def join_assistant(client, chat_id, message_id, userbot, file_path):
        join = None
        try:
            try:
                user = userbot.me
                user_id = user.id
                get = await client.get_chat_member(chat_id, user_id)
            except ChatAdminRequired:
                await client.send_message(chat_id, f"**قم بترقية البوت مشرف .⚡**", reply_to_message_id=message_id)
            if get.status == ChatMemberStatus.BANNED:
                await client.send_message(chat_id, f"**قم بالغاء الحظر عن الحساب المساعد لتفعيل البوت**.\n\n @{user.username} : **الحساب المساعد **⚡.\n** قم بتنظيف قايمه المستدخمين تمت ازالتهم ⚡.**\n\n** @ISIIQ | @ISIIQ : او تواصل مع المطور من هنا ⚡.**", reply_to_message_id=message_id)
            else:
              join = True
        except UserNotParticipant:
            chat = await client.get_chat(chat_id)
            if chat.username:
                try:
                    await userbot.join_chat(chat.username)
                    join = True
                except UserAlreadyParticipant:
                    join = True
                except Exception:
                 try:
                  invitelink = (await client.export_chat_invite_link(chat_id))
                  if invitelink.startswith("https://t.me/+"):
                        invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
                  await asyncio.sleep(3)
                  await userbot.join_chat(invitelink)
                  join = True
                 except ChatAdminRequired:
                    return await client.send_message(chat_id, f"**قم اعطاء البوت صلاحيه اضافه المستخدمين عبر الرابط .⚡**", reply_to_message_id=message_id)
                 except Exception as e:
                   await client.send_message(chat_id, f"** حدث خطأ حاول مرا آخري لاحقا**\n**{GROUP} : او تواصل مع الدعم من هنا .⚡**", reply_to_message_id=message_id)
            else:
                try:
                    try:
                       invitelink = chat.invite_link
                       if invitelink is None:
                          invitelink = (await client.export_chat_invite_link(chat_id))
                    except Exception:
                        try:
                          invitelink = (await client.export_chat_invite_link(chat_id))
                        except ChatAdminRequired:
                          await client.send_message(chat_id, f"**قم اعطاء البوت صلاحيه اضافه مستخدمين عبر الرابط .⚡**", reply_to_message_id=message_id)
                        except Exception as e:
                          await client.send_message(chat_id, f"** حدث خطأ حاول مرا آخري لاحقا**\n**{GROUP} : او تواصل مع الدعم من هنا .⚡**", reply_to_message_id=message_id)
                    m = await client.send_message(chat_id, "**انتظر قليلاً جاري تفعيل البوت .⚡**")
                    if invitelink.startswith("https://t.me/+"):
                        invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
                    await userbot.join_chat(invitelink)
                    join = True
                    await m.edit(f"**{user.mention} : انضم الحساب المساعد **\n**وتم تفعيل البوت يمكنك التشغيل الان .⚡**")
                except UserAlreadyParticipant:
                    join = True
                except Exception as e:
                    await client.send_message(chat_id, f"** حدث خطأ حاول مرا آخري لاحقا**\n**{GROUP} : او تواصل مع الدعم من هنا .⚡**", reply_to_message_id=message_id)
        return join        

async def join_call(
        client,
        message_id,
        chat_id,
        bot_username,
        file_path,
        link,
        vid: Union[bool, str] = None):
        userbot = await get_userbot(bot_username)
        Done = None
        try:
          call = await get_call(bot_username)
        except:
          return Done
        file_path = file_path
        audio_stream_quality = MediumQualityAudio()
        video_stream_quality = MediumQualityVideo()
        stream = (AudioVideoPiped(file_path, audio_parameters=audio_stream_quality, video_parameters=video_stream_quality) if vid else AudioPiped(file_path, audio_parameters=audio_stream_quality))
        try:
            await call.join_group_call(chat_id, stream, stream_type=StreamType().pulse_stream)
            Done = True
        except NoActiveGroupCall:
                 h = await join_assistant(client, chat_id, message_id, userbot, file_path)
                 if h:
                  try:
                   await call.join_group_call(chat_id, stream, stream_type=StreamType().pulse_stream)
                   Done = True
                  except Exception:
                      await client.send_message(chat_id, "**قم بتشغيل المكالمة أولاً .🚦**", reply_to_message_id=message_id)
        except AlreadyJoinedError:
             await client.send_message(chat_id, "**قم بإعادة تشغيل المكالمة ..🚦**", reply_to_message_id=message_id)
        except TelegramServerError:
             await client.send_message(chat_id, "**قم بإعادة تشغيل المكالمة ..🚦**", reply_to_message_id=message_id)
        except Exception as a:
            print(a)
            return Done
        return Done

def seconds_to_min(seconds):
    if seconds is not None:
        seconds = int(seconds)
        d, h, m, s = (
            seconds // (3600 * 24),
            seconds // 3600 % 24,
            seconds % 3600 // 60,
            seconds % 3600 % 60,
        )
        if d > 0:
            return "{:02d}:{:02d}:{:02d}:{:02d}".format(d, h, m, s)
        elif h > 0:
            return "{:02d}:{:02d}:{:02d}".format(h, m, s)
        elif m > 0:
            return "{:02d}:{:02d}".format(m, s)
        elif s > 0:
            return "00:{:02d}".format(s)
    return "-"


async def logs(bot_username, client, message):
  try:
   if await get_logger_mode(bot_username) == "OFF":
     return
   logger = await get_logger(bot_username)
   log = LOGS
   if message.chat.type == ChatType.CHANNEL:
     chat = f"[{message.chat.title}](t.me/{message.chat.username})" if message.chat.username else message.chat.title
     name = f"{message.author_signature}" if message.author_signature else chat
     text = f"**Playing History **\n\n**Chat : {chat}**\n**Chat Id : {message.chat.id}**\n**User Name : {name}**\n\n**Played : {message.text}**"
   else:
     chat = f"[{message.chat.title}](t.me/{message.chat.username})" if message.chat.username else message.chat.title
     user = f"User Username : @{message.from_user.username}" if message.from_user.username else f"User Id : {message.from_user.id}"
     text = f"**Playing History **\n\n**Chat : {chat}**\n**Chat Id : {message.chat.id}**\n**User Name : {message.from_user.mention}**\n**{user}**\n\n**Played : {message.text}**"
   await client.send_message(logger, text=text, disable_web_page_preview=True)
   return await man.send_message(log, text=f"[ @{bot_username} ]\n{text}", disable_web_page_preview=True)
  except:
    pass


@Client.on_message(filters.command(["عشوائي", "تشغيل عشوائي"], ""))
async def aii(client: Client, message):
   if await joinch(message):
            return
   try:
    chat_id = message.chat.id
    bot_username = client.me.username
    rep = await message.reply_text("**جاري اختيار تشغيل عشوائي ♻️**")
    try:
          call = await get_call(bot_username)
    except:
          await remove_active(bot_username, chat_id)
    try:
       await call.get_call(message.chat.id)
    except pytgcalls.exceptions.GroupCallNotFound:
       await remove_active(bot_username, chat_id)
    message_id = message.id
    user = await get_userbot(bot_username)
    req = message.from_user.mention if message.from_user else message.chat.title
    raw_list = []
    async for msg in user.get_chat_history("ELNQYBMUSIC"):
        if msg.audio:
          raw_list.append(msg)
    x = random.choice(raw_list)
    file_path = await x.download()
    file_name = x.audio.title
    title = file_name
    dur = x.audio.duration
    duration = seconds_to_min(dur)
    photo = PHOTO
    vid = True if x.video else None
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else "ISIIQ"
    videoid = None
    link = None
    await add(message.chat.id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
    if not await is_served_call(client, message.chat.id): 
      await add_active_chat(chat_id)
      await add_served_call(client, chat_id)
      if vid:
        await add_active_video_chat(chat_id)
      link = None
      c = await join_call(client, message_id, chat_id, bot_username, file_path, link, vid)
      if not c:
            await remove_active(bot_username, chat_id)
            return await rep.delete()
    await rep.delete()
    button = [[InlineKeyboardButton(text="END", callback_data=f"stop"), InlineKeyboardButton(text="RESUME", callback_data=f"resume"), InlineKeyboardButton(text="PAUSE", callback_data=f"pause")], [InlineKeyboardButton(text="Mimo", url="https://t.me/ISIIQ")] [InlineKeyboardButton(text="Dark", url="https://t.me/dar4k")]]
    await message.reply_photo(photo=photo, caption=f"**Started Stream Random **\n\n**Song Name : {title}**\n**Duration Time : {duration}**\n**Requests By : {req}**", reply_markup=InlineKeyboardMarkup(button))
    await logs(bot_username, client, message)
    await asyncio.sleep(4)
    if os.path.exists(file_path):
      os.remove(file_path)
   except Exception as es:
    pass

@Client.on_message(filters.command(["/play", "play", "/vplay", "شغل", "تشغيل", "فيد", "فيديو"], ""))
async def play(client: Client, message):
  if await joinch(message):
            return
  KERO = message
  bot_username = client.me.username
  chat_id = message.chat.id
  user_id = message.from_user.id if message.from_user else "ISIIQ"
  message_id = message.id 
  gr = await get_group(bot_username)
  ch = await get_channel(bot_username)
  button = [[InlineKeyboardButton(text=".♪ 𝑬𝒏𝒅", callback_data=f"stop"), InlineKeyboardButton(text="𝑹𝒆𝒔𝒖𝒎𝒆", callback_data=f"resume"), InlineKeyboardButton(text="𝑷𝒂𝒖𝒔𝒆 ♪.", callback_data=f"pause")], [InlineKeyboardButton(text="{قــناه الســورس}", url=f"{ch}"), InlineKeyboardButton(text="{جــروب الـدعم}", url=f"{gr}")], [InlineKeyboardButton(text=f"{OWNER_NAME}", url="https://t.me/ISIIQ")], [InlineKeyboardButton(text="اضف البوت الي مجموعتك او قناتك ⚡", url=f"https://t.me/{bot_username}?startgroup=True")]]
  if message.chat.type == ChatType.PRIVATE:
       return await message.reply_text("**♪ لا يمكنك التشغيل هنا للأسف 💎 .\n♪ قم بإضافة البوت اللي مجموعتك للتشغيل 💎 .**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ضف البوت الي مجموعتك او قناتك ⚡", url=f"https://t.me/{bot_username}?startgroup=True")]]))
  if message.sender_chat:
     if not message.chat.type == ChatType.CHANNEL:
      return await message.reply_text("**♪ يمكنك التشغيل بحسابك الخاص فقط 💎 .**")
  if not len(message.command) == 1:
    rep = await message.reply_text("**♪ جاري التشغيل انتظر قليلا 💎 .**")
  try:
          call = await get_call(bot_username)
  except:
          await remove_active(bot_username, chat_id)
  try:
       await call.get_call(message.chat.id)
  except pytgcalls.exceptions.GroupCallNotFound:
       await remove_active(bot_username, chat_id)
  if not message.reply_to_message:
     if len(message.command) == 1:
      if message.chat.type == ChatType.CHANNEL:
        return await message.reply_text("**♪ قم كتابة شيئ لتشغيلة 💎 .**")
      try:
       name = await client.ask(message.chat.id, text="**♪ ارسل اسم او رابط الي تريد تشغيله 💎 .**", reply_to_message_id=message.id, filters=filters.user(message.from_user.id), timeout=200)
       name = name.text
       rep = await message.reply_text("**♪ جاري التشغيل انتظر قليلا 💎 .**")
      except:
       return
     else:
       name = message.text.split(None, 1)[1]
     if "v" in message.command[0] or "ف" in message.command[0]:
       vid = True
     else:
       vid = None 
     await rep.edit("**♪ جاري التشغيل انتظر قليلا ⚡ .**")
     results = YoutubeSearch(name, max_results=5).to_dict()
     [{'id': 'sElE_BfQ67s', 'thumbnails': ['https://i.ytimg.com/vi/sElE_BfQ67s/hq720.jpg?sqp=-oaymwEjCOgCEMoBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLDt0MNsJNz0Mm7DuuKL7C-UWxHWBQ', 'https://i.ytimg.com/vi/sElE_BfQ67s/hq720.jpg?sqp=-oaymwEXCNAFEJQDSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLC6ZBvEwmn0QKTc6EUOo7aAssL3Bg'], 'title': 'Apocalypse - Cigarettes After Sex', 'long_desc': None, 'channel': 'Cigarettes After Sex', 'duration': '4:51', 'views': '311.562.955 Aufrufe', 'publish_time': 'vor 8 Jahren', 'url_suffix': '/watch?v=sElE_BfQ67s&list=RDsElE_BfQ67s&start_radio=1&pp=ygUOY2FzIGFwb2NhbHlwc2WgBwE%3D'}, {'id': '-mnH9-SX2Tg', 'thumbnails': ['https://i.ytimg.com/vi/-mnH9-SX2Tg/hq720.jpg?sqp=-oaymwE9COgCEMoBSFryq4qpAy8IARUAAAAAGAElAADIQj0AgKJDeAHwAQH4Af4JgALQBYoCDAgAEAEYciBGKDgwDw==&rs=AOn4CLDBRs0qCyLxlDs7gK9gJT0SHAPLoQ', 'https://i.ytimg.com/vi/-mnH9-SX2Tg/hq720.jpg?sqp=-oaymwExCNAFEJQDSFryq4qpAyMIARUAAIhCGAHwAQH4Af4JgALQBYoCDAgAEAEYciBGKDgwDw==&rs=AOn4CLBqDDmDREFMADJ5ZdglO8gF3EtcsQ'], 'title': 'Cigarettes After Sex - Apocalypse (Live on KEXP)', 'long_desc': None, 'channel': 'KEXP', 'duration': '5:15', 'views': '8.300.493 Aufrufe', 'publish_time': 'vor 8 Jahren', 'url_suffix': '/watch?v=-mnH9-SX2Tg&list=RD-mnH9-SX2Tg&start_radio=1&pp=ygUOY2FzIGFwb2NhbHlwc2WgBwE%3D'}, {'id': '0IvJEwfghHc', 'thumbnails': ['https://i.ytimg.com/vi/0IvJEwfghHc/hq720.jpg?sqp=-oaymwEjCOgCEMoBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLB1U2-HeVuAUxErZOWFBfSyDNaHng', 'https://i.ytimg.com/vi/0IvJEwfghHc/hq720.jpg?sqp=-oaymwEXCNAFEJQDSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLD_IvHOBC5wjrKDYpyxwCdCYCuGag'], 'title': 'Playlist Cigarettes After Sex Songs for Drizzly Afternoon · Drip Coffee, Matcha Latte, someone you..', 'long_desc': None, 'channel': 'NBFU', 'duration': '1:42:54', 'views': '665.654 Aufrufe', 'publish_time': 'vor 4 Monaten', 'url_suffix': '/watch?v=0IvJEwfghHc&t=1362s&pp=ygUOY2FzIGFwb2NhbHlwc2U%3D'}, {'id': 'AmXdpVnJwt8', 'thumbnails': ['https://i.ytimg.com/vi/AmXdpVnJwt8/hq720.jpg?sqp=-oaymwE9COgCEMoBSFryq4qpAy8IARUAAAAAGAElAADIQj0AgKJDeAHwAQH4Af4JgALQBYoCDAgAEAEYZSBlKGUwDw==&rs=AOn4CLBFlraFcLwl1o0EXvmNZjOOsfghZw', 'https://i.ytimg.com/vi/AmXdpVnJwt8/hq720.jpg?sqp=-oaymwExCNAFEJQDSFryq4qpAyMIARUAAIhCGAHwAQH4Af4JgALQBYoCDAgAEAEYZSBlKGUwDw==&rs=AOn4CLCXZFs7_0OAOypzcXmOsk8Cjf_Nmg'], 'title': 'Cry (Full Album) - Cigarettes After Sex', 'long_desc': None, 'channel': 'Cigarettes After Sex', 'duration': '40:21', 'views': '12.228.288 Aufrufe', 'publish_time': 'vor 3 Jahren', 'url_suffix': '/watch?v=AmXdpVnJwt8&list=RDAmXdpVnJwt8&start_radio=1&pp=ygUOY2FzIGFwb2NhbHlwc2WgBwE%3D'}, {'id': 'iJABBPaRvX0', 'thumbnails': ['https://i.ytimg.com/vi/iJABBPaRvX0/hq720.jpg?sqp=-oaymwE9COgCEMoBSFryq4qpAy8IARUAAAAAGAElAADIQj0AgKJDeAHwAQH4Af4JgALQBYoCDAgAEAEYRiBaKHIwDw==&rs=AOn4CLB-C6Rgp9W1dLirroKMNWHDO-5V3Q', 'https://i.ytimg.com/vi/iJABBPaRvX0/hq720.jpg?sqp=-oaymwExCNAFEJQDSFryq4qpAyMIARUAAIhCGAHwAQH4Af4JgALQBYoCDAgAEAEYRiBaKHIwDw==&rs=AOn4CLBPMuSz5BI6dA1naZsovzcM1S9crg'], 'title': 'Cigarettes After Sex - Apocalypse (rainy day reverb loop)', 'long_desc': None, 'channel': 'Ambient Music Flow', 'duration': '2:05:43', 'views': '70.343 Aufrufe', 'publish_time': 'vor 1 Jahr', 'url_suffix': '/watch?v=iJABBPaRvX0&pp=ygUOY2FzIGFwb2NhbHlwc2U%3D'}]

     link = f"https://youtube.com{results[0]['url_suffix']}"
     if await is_served_call(client, message.chat.id):
         chat_id = message.chat.id
         title = results[0]['title']
         duration = results[0]['duration']
         videoid = results[0]['id']
         file_path = None
         await add(message.chat.id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
         chat = f"{bot_username}{chat_id}"
         position = len(db.get(chat)) - 1
         chatname = f"[{message.chat.title}](https://t.me/{message.chat.username})" if message.chat.username else f"{message.chat.title}"
         chatname = f"{message.author_signature}" if message.author_signature else chatname
         requester = chatname if getattr(KERO, 'views', False) else f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
         if message.from_user:
          if message.from_user.photo:
           photo_id = message.from_user.photo.big_file_id
           photo = await client.download_media(photo_id)
          elif message.chat.photo:
           photo_id = message.chat.photo.big_file_id
           photo = await client.download_media(photo_id)
          else:
           ahmed = await client.get_chat("ISIIQ")
           ahmedphoto = ahmed.photo.big_file_id
         elif message.chat.photo:
          photo_id = message.chat.photo.big_file_id
          photo = await client.download_media(photo_id)
         else:
          ahmed = await client.get_chat("ISIIQ")
          ahmedphoto = ahmed.photo.big_file_id
          photo = await client.download_media(ahmedphoto)
         photo = await gen_thumb(videoid, photo)
         await message.reply(photo=photo, caption=f"**♪ Add Track To Playlist : {position} 🥁 .\n\n♪ Song Name : {title} 🎞️ .\n♪ Duration Time : {duration} ⌚ .\n♪ Request By : {requester} 👤 .**", reply_markup=InlineKeyboardMarkup(button))
         await logs(bot_username, client, message)
     else: 
         chat_id = message.chat.id
         title = results[0]['title']
         duration = results[0]['duration']
         videoid = results[0]['id']
         await add_active_chat(chat_id)
         await add_served_call(client, chat_id)
         if vid:
           await add_active_video_chat(chat_id)
         file_path = await download(bot_username, link, vid)
         await add(message.chat.id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
         c = await join_call(client, message_id, chat_id, bot_username, file_path, link, vid)
         if not c:
            await remove_active(bot_username, chat_id)
            return await rep.delete()
         chatname = f"[{message.chat.title}](https://t.me/{message.chat.username})" if message.chat.username else f"{message.chat.title}"
         chatname = f"{message.author_signature}" if message.author_signature else chatname
         requester = chatname if getattr(KERO, 'views', False) else f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
         if message.from_user:
          if message.from_user.photo:
           photo_id = message.from_user.photo.big_file_id
           photo = await client.download_media(photo_id)
          elif message.chat.photo:
           photo_id = message.chat.photo.big_file_id
           photo = await client.download_media(photo_id)
          else:
           ahmed = await client.get_chat("ISIIQ")
           ahmedphoto = ahmed.photo.big_file_id
         elif message.chat.photo:
          photo_id = message.chat.photo.big_file_id
          photo = await client.download_media(photo_id)
         else:
          ahmed = await client.get_chat("ISIIQ")
          ahmedphoto = ahmed.photo.big_file_id
          photo = await client.download_media(ahmedphoto)
         photo = await gen_thumb(videoid, photo)
         await message.reply_photo(photo=photo, caption=f"**♪ Startling Playing Now 🥁 .\n\n♪ Song Name : {title} 🎞️ .\n♪ Duration Time : {duration} ⌚ .\n♪ Request By : {requester} 👤 .**", reply_markup=InlineKeyboardMarkup(button))
         await logs(bot_username, client, message)
     await rep.delete()
  else:
       if not message.reply_to_message.media:
         return
       rep = await message.reply_text("**♪ جاري تشغيل الملف انتظر قليلا 🚦 .**") 
       photo = "Uploaded to https://graph.org/file/bbe526c61648eebca422c.jpg"
       if message.reply_to_message.video or message.reply_to_message.document:
           vid = True
       else:
           vid = None
       file_path = await message.reply_to_message.download()
       if message.reply_to_message.audio:
         file_name = message.reply_to_message.audio
       elif message.reply_to_message.voice:
         file_name = message.reply_to_message.voice
       elif message.reply_to_message.video:
         file_name = message.reply_to_message.video
       else:
         file_name = message.reply_to_message.document
       title = file_name.file_name
       duration = seconds_to_min(file_name.duration)
       link = None
       if await is_served_call(client, message.chat.id):
         chat_id = message.chat.id
         videoid = None
         await add(message.chat.id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
         chat = f"{bot_username}{chat_id}"
         position = len(db.get(chat)) - 1
         chatname = f"[{message.chat.title}](https://t.me/{message.chat.username})" if message.chat.username else f"{message.chat.title}"
         chatname = f"{message.author_signature}" if message.author_signature else chatname
         requester = chatname if getattr(KERO, 'views', False) else f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
         await message.reply_photo(photo=photo, caption=f"**♪ Add Track To Playlist : {position} 🥁 .\n\n♪ Song Name : {title} 🎞️ .\n♪ Duration Time : {duration} ⌚ .\n♪ Request By : {requester} 👤 .**", reply_markup=InlineKeyboardMarkup(button))
         await logs(bot_username, client, message)
       else:
         chat_id = message.chat.id
         videoid = None
         await add_active_chat(chat_id)
         await add_served_call(client, chat_id)
         if vid:
            await add_active_video_chat(chat_id)
         await add(message.chat.id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
         c = await join_call(client, message_id, chat_id, bot_username, file_path, link, vid)
         if not c:
            await remove_active(bot_username, chat_id)
            return await rep.delete()
         chatname = f"[{message.chat.title}](https://t.me/{message.chat.username})" if message.chat.username else f"{message.chat.title}"
         chatname = f"{message.author_signature}" if message.author_signature else chatname
         requester = chatname if getattr(KERO, 'views', False) else f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
         await message.reply_photo(photo=photo, caption=f"**♪ Startling Playing Now 🥁 .\n\n♪ Song Name : {title} 🎞️ .\n♪ Duration Time : {duration} ⌚ .\n♪ Request By : {requester} 👤 .**", reply_markup=InlineKeyboardMarkup(button))
         await logs(bot_username, client, message)
         try:
             if os.path.exists(file_path):
                 os.remove(file_path)
             if os.path.exists(photo):
                 os.remove(photo)
         except:
             pass
  await rep.delete()


