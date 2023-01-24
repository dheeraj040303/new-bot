
def sample_response(input_text):
    text = input_text.lower()
    if text in ("hi", "hello"):
        return "Hi there this is linkerIn bot"
    elif text in ("who are you", "who are you?"):
        return "I'am a bot that all about movie"
    elif text.split(" ")[0] == '/convert':
        try:
            return
        except Exception as error:
            return error
    return