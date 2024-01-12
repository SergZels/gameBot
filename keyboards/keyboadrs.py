from aiogram import types

keyb_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyb_main.add("Guess the number 7️⃣3️⃣","Stone🪨 scissors✂️ paper📜")

keyb_st = types.InlineKeyboardMarkup()
stone = types.InlineKeyboardButton(text="Stone🪨", callback_data="stone")
cross = types.InlineKeyboardButton(text="Scissors✂️", callback_data="cross")
paper = types.InlineKeyboardButton(text="Paper📜", callback_data="paper")
keyb_st.add(stone).add(cross).add(paper)

