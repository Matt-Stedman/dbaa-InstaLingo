from instagrapi import Client
import time
import toml
import deepl
import spacy
import random
nlp = spacy.load("en_core_web_lg")

# lang
FR = "FR"
EN = "EN"


def await_reply(user_id, timeout = 30):
    start_time = time.time()
    while 1:
        threads = cl.direct_threads()
        try:
            for t in threads:
                if u["id"] in (t_u.pk for t_u in t.users):
                    last_message = get_last_message(user_id, t)
                    if not last_message:
                        return False
                    if last_message.timestamp.timestamp() > start_time:
                        return last_message
        except:
            print("Error handling messages")
            return False
        if (time.time() > start_time + timeout):
            print("Response timed out")
            return False

def propose_translation(user_id, phrase, lang):
    print("Sending translation challenge:")
    print(phrase)
    if lang == FR:
        cl.direct_send(f'Veuillez traduire le texte suivant en français :\n {phrase}', user_ids=[user_id])
    else:
        cl.direct_send(f'Please translate this into English: {translator.translate_text(phrase, target_lang="FR").text}.', user_ids=[user_id])
    
    response = await_reply(user_id)
    if response:
        if lang == FR:
            response_txt = translator.translate_text(response.text, target_lang="EN-GB").text
        else:
            response_txt = response.text
        
        if response_txt.strip() == "STOP":
            u["last_msg_tstamp"] = last_message.timestamp.timestamp() + 3
            time.sleep(3)
            return

        phrase_sent = nlp(response_txt)
        phrase_reci = nlp(phrase)
        similarity = phrase_sent.similarity(phrase_reci)
        print(phrase_sent, "<->", phrase_reci, similarity)       
        if similarity > .85:
            cl.direct_send("'Well done!", user_ids=[user_id])
        else:
            cl.direct_send("Oohhh, that's not quite right.", user_ids=[user_id])

    else:
        print("Not continuing")

def handle_message(msg):
    if (msg.text[2:4] == " >"):
        lang = msg.text[0:2]
        if lang == "EN":
            lang = "EN-GB"
        cl.direct_send(f'> {msg.text[0:2]}:\n{translator.translate_text(msg.text[4:-1].strip(), target_lang=lang).text}', user_ids=[msg.user_id])
    elif (msg.text[0:4] == "INFO"):
        cl.direct_send(INSTRUCTIONS["INFO"], user_ids=[msg.user_id])
    else:
        propose_translation(msg.user_id, random.choices(phrases)[0], random.choices([EN, FR])[0])



def get_last_message(user_id, thread):
    results = list(filter(lambda msg: str(user_id) == str(msg.user_id), cl.direct_messages(thread.id)))
    if len(results):
        return results[0]
    else:
        return False
    
def get_active_conversations():
    users = []
    for u_name in ["i.think.its.a.stedman.thing"]:
        users.append({"id": cl.user_id_from_username(u_name), "last_msg_tstamp": time.time()})

    return users


if __name__ == "__main__":
    SECRETS = toml.load("dbaa-InstaLingo\secrets.toml")
    INSTRUCTIONS = toml.load("dbaa-InstaLingo\instructions.toml")
    translator = deepl.Translator(SECRETS["DEEPL"]["AUTH_KEY"])
    
    cl = Client()
    cl.login(SECRETS["INSTAGRAM"]["USER"], SECRETS["INSTAGRAM"]["PASS"])

    users = get_active_conversations()

    phrases = []
    with open("dbaa-InstaLingo\\french_phrases.txt") as f:
        phrases = f.readlines()
    
    # Get a response to an input statement
    while 1:
        threads = cl.direct_threads()
        print(f"Size of threads: {len(threads)}")
        try:
            for u in users:
                for t in threads:
                    if u["id"] in (t_u.pk for t_u in t.users):
                        last_message = get_last_message(u["id"], t)
                        if not last_message:
                            continue
                        if last_message.timestamp.timestamp() > u["last_msg_tstamp"]:
                            handle_message(last_message)
                            u["last_msg_tstamp"] = last_message.timestamp.timestamp()
        except:
            cl.login(SECRETS["INSTAGRAM"]["USER"], SECRETS["INSTAGRAM"]["PASS"])
