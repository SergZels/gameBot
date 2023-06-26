from aiogram import types

keyb_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyb_main.add("Вгадай число7️⃣3️⃣","Камінь🪨 ножиці✂️ бумага📜")

keyb_st = types.InlineKeyboardMarkup()
stone = types.InlineKeyboardButton(text="Камінь🪨", callback_data="stone")
cross = types.InlineKeyboardButton(text="Ножиці✂️", callback_data="cross")
paper = types.InlineKeyboardButton(text="Папір📜", callback_data="paper")
keyb_st.add(stone).add(cross).add(paper)

