import requests
from telegram import Update , InlineKeyboardButton, InlineKeyboardMarkup , InputTextMessageContent , InlineQueryResultPhoto , InlineQueryResultArticle 
from telegram.ext import ContextTypes , ApplicationBuilder , CommandHandler , CallbackContext , CallbackQueryHandler , InlineQueryHandler , MessageHandler , filters
import datetime
API_TOKEN = '6871068100:AAFSKAJ8H2BzlLZE4XUAHYHxFD1F2Yaux5g'

async def start (update:Update , context:ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    name = update.message.chat.first_name
    text = f"Hello dear {name}❤️ \nIMDb infoBot is a telegram bot that use IMDb api to give information about movies \n"
    reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Search any movie",
                            switch_inline_query_current_chat=' '
                        )
                    ]
                ]
            )
    await context.bot.send_message(text=text ,chat_id=chat_id,reply_markup=reply_markup)
    
button_state = ""
async def search (update:Update , context:ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text
    query = text[8:]
    api_key = "288c363f"
    text = f"you are searching for {query}"
    url = f"http://www.omdbapi.com/?s={query}&apikey={api_key}"
    response = requests.get(url)
    # تبدیل پاسخ به فرمت JSON
    data = response.json()
    # Create options for buttons based on search results
    options = []
    if 'Search' in data and len(data['Search']) > 0:
        for result in data['Search']:
            option_text = f"{result['Title']} ({result['Year']})"
            option_callback = f"{result['imdbID']}"
            options.append([InlineKeyboardButton(option_text, callback_data=option_callback)])
    
    reply_markup = InlineKeyboardMarkup(options)
    await context.bot.send_message(chat_id=chat_id, text="Choose a movie:", reply_markup=reply_markup)

async def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "search_button":
        # Get the chat ID and the user's username
        chat_id = update.effective_chat.id
        username = update.effective_user.username
        # Prepare the text with the username and a space
        text_to_write = f"@{username} "
        # Send a message with switch_inline_query_current_chat
        await context.bot.send_message(
            chat_id=chat_id,
            text=text_to_write,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Let me help you...",
                            switch_inline_query_current_chat='/audio 1'
                        )
                    ]
                ]
            )
        )
    else:
        clicked_option = None
        inline_keyboard = query.message.reply_markup.inline_keyboard
        for row in inline_keyboard:
            for button in row:
                if button.callback_data == query.data:
                   clicked_option = button
                   break
            if clicked_option:
                break
        chat_id = query.message.chat_id
        movie_id = clicked_option.callback_data  # Extract the IMDb ID from the callback data
    
        api_key = "288c363f"
        url = f"http://www.omdbapi.com/?i={movie_id}&apikey={api_key}"
        response = requests.get(url)
        data = response.json()
        message_text = ""
        if len(data) > 0:
        # Construct the message with other movie details
            message_text =f"🎪 [Movie: {data['Title']} ({data['Year']})]({data['Poster']})\n" \
                f"🚦 𝙸ᴍᴅʙ 𝙸ᴅ: {data['imdbID']}\n" \
                f"🕰Dᴜʀᴀᴛɪᴏɴ: {data['Runtime']}\n" \
                f"🗓️ Rᴇʟᴇᴀsᴇ Dᴀᴛᴇ: {data['Released']} ([More info](https://www.imdb.com/title/{data['imdbID']}/releaseinfo))\n" \
                f"💬 Lᴀɴɢᴜᴀɢᴇ: {data['Language']}\n" \
                f"📟 Gᴇɴʀᴇ: {data['Genre']}\n" \
                f"📋 Sᴛᴏʀy Lɪɴᴇ: {data['Plot']} ([More info](https://www.imdb.com/title/{data['imdbID']}/plotsummary/))\n" \
                f"🎥 Dɪʀᴇᴄᴛᴏʀ: {data['Director']} ([More info](https://www.imdb.com/name/{data['Director']}))\n" \
                f"✍️ Wʀɪᴛᴇʀ: {data['Writer']} ([More info](https://www.imdb.com/name/{data['Writer']}))\n" \
                f"🎎 Aᴄᴛᴏʀs: {data['Actors']} ([More info](https://www.imdb.com/name/{data['Actors']}))\n"
        # Send the message with both the photo and the text
            await context.bot.send_photo(chat_id=chat_id, photo=data['Poster'], caption=message_text)
        #await context.bot.send_message(chat_id=chat_id, text=message_text)
        else:
            message_text = "No results found."
    # Edit the message text to include other movie details
        await query.answer()
        await query.edit_message_text(text="Selected movie:")
async def inline_search(update: Update, context: CallbackContext):
    query = update.inline_query.query
    if(not query):
        print("empty")
        current_datetime = datetime.datetime.now()
        current_timestamp_str = str(int(current_datetime.timestamp()))
        message_text = "/start"
        title_text = "Enter a movie name..."
        article_result = InlineQueryResultArticle(
            id=current_timestamp_str,
            title=title_text,
            input_message_content=InputTextMessageContent(message_text)
        )
        results = []
        # Add the result to the list of results
        results.append(article_result)
        await update.inline_query.answer(results, cache_time=0)
    else:
        api_key = "288c363f"
        url = f"http://www.omdbapi.com/?s={query}&apikey={api_key}"
        response = requests.get(url)
        data = response.json()
        results = []
        if 'Search' in data and len(data['Search']) > 0:
            for result in data['Search']:
                id = result["imdbID"]
                title = result['Title']
                year = result['Year']
                poster = result['Poster']
                result_id = f"{title}_{year}"
                # Create an InlineQueryResultPhoto for each movie result with the poster
                results.append(
                    InlineQueryResultPhoto(
                        id=result_id,  # Using poster URL as the ID
                        title=title,
                        photo_url=poster,
                        thumbnail_url =poster,  # Using poster as the thumbnail
                        caption=f"{title}\nYear: {year}",
                        parse_mode='Markdown',  # Enable markdown in the caption
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("View on IMDb", url=f"https://www.imdb.com/title/{id}/")],
                            [InlineKeyboardButton("More Details", callback_data=f"details_{id}")]
                        ]) 
                    )
            )
    
        await update.inline_query.answer(results)

async def more_detail_button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    movie_id = query.data[8:]  # Assuming the movie ID is passed as the callback data
    print(movie_id)
    api_key = "288c363f"  # Your OMDB API key
    url = f"http://www.omdbapi.com/?i={movie_id}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    print(data)
    # Create the detailed caption with Markdown formatting
    if len(data) > 0:
        caption =f"🎪 [Movie: {data['Title']} ({data['Year']})]({data['Poster']})\n" \
                f"🚦 𝙸ᴍᴅʙ 𝙸ᴅ: {data['imdbID']}\n" \
                f"🕰Dᴜʀᴀᴛɪᴏɴ: {data['Runtime']}\n" \
                f"🗓️ Rᴇʟᴇᴀsᴇ Dᴀᴛᴇ: {data['Released']} ([More info](https://www.imdb.com/title/{data['imdbID']}/releaseinfo))\n" \
                f"💬 Lᴀɴɢᴜᴀɢᴇ: {data['Language']}\n" \
                f"📟 Gᴇɴʀᴇ: {data['Genre']}\n" \
                f"📋 Sᴛᴏʀy Lɪɴᴇ: {data['Plot']} ([More info](https://www.imdb.com/title/{data['imdbID']}/plotsummary/))\n" \
                f"🎥 Dɪʀᴇᴄᴛᴏʀ: {data['Director']} ([More info](https://www.imdb.com/name/{data['Director']}))\n" \
                f"✍️ Wʀɪᴛᴇʀ: {data['Writer']} ([More info](https://www.imdb.com/name/{data['Writer']}))\n" \
                f"🎎 Aᴄᴛᴏʀs: {data['Actors']} ([More info](https://www.imdb.com/name/{data['Actors']}))\n"
    # Edit the message with the detailed information
    await query.edit_message_caption(
        caption=caption,
        parse_mode='Markdown'
    )
async def handle_text(update: Update, context: CallbackContext):
    print(update)
    text = update.message.text.lower()
    chat_id = update.message.chat.id
    if text[0] != "/":
        print(text)
        print(chat_id)
        api_key = "288c363f"
    #print(update.message)
        url = f"http://www.omdbapi.com/?s={text}&apikey={api_key}"
        response = requests.get(url)
    # تبدیل پاسخ به فرمت JSON
        data = response.json()
    # Create options for buttons based on search results
        options = []
        if 'Search' in data and len(data['Search']) > 0:
            for result in data['Search']:
                option_text = f"{result['Title']} ({result['Year']})"
                option_callback = f"{result['imdbID']}"
                options.append([InlineKeyboardButton(option_text, callback_data=option_callback)])
        reply_markup = InlineKeyboardMarkup(options)
        await context.bot.send_message(chat_id=chat_id, text="Choose a movie:", reply_markup=reply_markup)


if __name__ == "__main__":
    application = ApplicationBuilder().token(API_TOKEN).build()
    start_handler = CommandHandler("start" , start)
    search_handler = CommandHandler("search" , search)
    button_click_handler = CallbackQueryHandler(button_click)
    inline_search_handler = InlineQueryHandler(inline_search)
    application.add_handler(start_handler)
    application.add_handler(CallbackQueryHandler(more_detail_button_click, pattern=r'^details_'))
    application.add_handler(button_click_handler)
    application.add_handler(search_handler)
    application.add_handler(inline_search_handler)
    application.add_handler(MessageHandler(None, handle_text ))
    application.run_polling()