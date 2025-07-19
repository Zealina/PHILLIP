#!/usr/bin/env python3
"""This module registers a new group when the bot is added"""

from telegram import Update
from telegram.ext import (
        ChatMemberHandler,
        CommandHandler,
        ContextTypes
    )
from telegram.constants import ChatMemberStatus, ParseMode


def get_groups_data(context):
    return context.bot_data.setdefault("groups", dict())

def get_selected_group_id(context):
    return context.bot_data.setdefault("selected_group", "")


async def group_management(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store full chat member update for group and timestamp it"""
    groups = get_groups_data(context)
    chat_id = str(update.effective_chat.id)
    bot_update = update.my_chat_member

    groups[chat_id] = bot_update.to_dict()

    from json import dumps
    print(dumps(update.to_dict(), indent=4))


async def list_groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all groups where the bot is still a member/admin"""
    if not get_groups_data(context):
        await update.message.reply_text("No group data available.")
        return

    groups = get_groups_data(context)

    active_groups = []
    for group_id, info in groups.items():
        status = info["new_chat_member"]["status"]
        title = info["chat"].get("title", "Unnamed Group")
        if status not in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]:
            active_groups.append((title, status.title(), group_id))

    if not active_groups:
        await update.message.reply_text("Bot is not currently active in any groups.")
        return

    count = len(active_groups)
    response_lines = [f"<b>🤖 Active Groups ({count})</b>\n"]

    for i, (title, status, group_id) in enumerate(active_groups, start=1):
        line = (
            f"<b>{i}. {title}</b>\n"
            f"├ 🟢 <b>Status:</b> <code>{status}</code>\n"
            f"└ 🆔 <code>{group_id}</code>\n"
        )
        response_lines.append(line)

    response_text = "\n".join(response_lines)

    selected_group_id = get_selected_group_id(context)
    if selected_group_id == "":
        selected_group_text = f"\n\nSelected Group: <b>nil</b>"
    else:
        selected_group = groups[selected_group_id]
        selected_group_text = f"\n\nSelected Group: <b>{selected_group['chat']['title']}</b>"

    await update.message.reply_text(response_text + selected_group_text, parse_mode="HTML")


async def select_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Select Active Group"""
    if len(context.args) != 1:
        text = "Usage: /select_group _<GROUP_ID>_"
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                parse_mode=ParseMode.MARKDOWN_V2
            )
    group_id = context.args[0]
    groups = get_groups_data(context)

    if not groups:
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="🚫 No groups found! Add bot to a group to register it."
            )
        return

    if group_id not in groups:
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"⚠️ Group with ID <code>{group_id}</code> doesn’t exist, or the bot hasn’t been added to it yet.",
                parse_mode=ParseMode.HTML
            )
        return

    context.bot_data["selected_group"] = group_id
    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"✅ <b>{groups[group_id]['chat']['title']}</b> is now the active group!",
            parse_mode=ParseMode.HTML
        )



list_groups = CommandHandler("list_groups", list_groups)
select_group = CommandHandler("select_group", select_group)
chat_member_handler = ChatMemberHandler(group_management, ChatMemberHandler.MY_CHAT_MEMBER)
