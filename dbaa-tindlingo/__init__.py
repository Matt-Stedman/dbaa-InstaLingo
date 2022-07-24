from instagrapi import Client
import time

def respond_to_message(msg):
    print("Sending message")
    cl.direct_send(f'Returning {msg.text}.', user_ids=[msg.user_id])
    time.sleep(1)


def get_last_message(user_id, thread):
    return list(filter(lambda msg: str(user_id) == u["id"], cl.direct_messages(thread.id)))[0]
    
def get_active_conversations():
    users = []
    for u_name in ["i.think.its.a.stedman.thing"]:
        users.append({"id": cl.user_id_from_username(u_name), "last_msg_tstamp": time.time()})

    return users

if __name__ == "__main__":
    cl = Client()
    cl.login("matts.experiments.playground", "fFWvTWH&i84*h?f")

    users = get_active_conversations()
    while 1:
        threads = cl.direct_threads()
        for u in users:
            for t in threads:
                if u["id"] in (t_u.pk for t_u in t.users):
                    last_message = get_last_message(u["id"], t)
                    if last_message.timestamp.timestamp() > u["last_msg_tstamp"]:
                        respond_to_message(last_message)
                        u["last_msg_tstamp"] = last_message.timestamp.timestamp()

        time.sleep(1)
