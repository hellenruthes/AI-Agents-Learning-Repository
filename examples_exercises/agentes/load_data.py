import os
from io import StringIO
import pandas as pd
from sqlalchemy import create_engine

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_URL = f"postgresql+psycopg2://admin:admin123@{DB_HOST}:5433/suporte_ai"


CONVERSATIONS_CSV = """ticket_id,conversation_id,user_id,speaker,message,timestamp,ticket_status
1001,1,101,client,I cant log in,2026-04-01 09:00,open
1001,1,101,agent,Can you try resetting your password,2026-04-01 09:02,pending
1001,1,101,client,I already tried and it didnt work,2026-04-01 09:05,open

1002,2,102,client,My payment didnt go through,2026-04-01 10:00,open
1002,2,102,agent,Can you check your card,2026-04-01 10:02,pending
1002,2,102,client,I managed to solve it here thanks,2026-04-01 14:10,solved

1003,3,103,client,My delivery is delayed,2026-04-01 11:00,open
1003,3,103,agent,We are checking with the carrier,2026-04-01 11:03,pending
1003,3,103,client,Ok thanks,2026-04-01 11:10,solved

1004,4,104,client,I want to cancel my order,2026-04-01 12:00,open
1004,4,104,agent,I can help you with that,2026-04-01 12:02,pending
1004,4,104,client,I already solved it thanks,2026-04-01 12:10,solved

1005,5,105,client,I cant access my account,2026-04-01 13:00,open
1005,5,105,agent,Please try resetting your password,2026-04-01 13:02,pending

1006,6,106,client,The app keeps freezing a lot,2026-04-02 09:00,open
1006,6,106,agent,Can you restart the app,2026-04-02 09:05,pending

1007,7,107,client,Payment declined for no reason,2026-04-02 10:00,open
1007,7,107,agent,Please check your card limit,2026-04-02 10:03,pending

1008,8,108,client,It takes too long to load,2026-04-02 11:00,open
1008,8,108,agent,We are analyzing the slowness,2026-04-02 11:02,pending

1009,9,109,client,The delivery arrived wrong,2026-04-02 12:00,open
1009,9,109,agent,We can replace it for you,2026-04-02 12:05,pending

1010,10,110,client,I want to cancel my subscription,2026-04-02 13:00,open
1010,10,110,agent,Cancellation requested,2026-04-02 13:05,solved
"""


FEEDBACKS_CSV = """feedback_id,feedback_text,created_at,channel
1,The app crashes when I try to open the payment screen,2026-04-01 10:30,app
2,I really liked the new interface it became easier to use,2026-04-01 11:00,site
3,The system is very slow to load my information,2026-04-01 14:20,app
4,I couldn't complete my purchase on the website,2026-04-02 09:15,site
5,Excellent service they solved my problem quickly,2026-04-02 10:40,app
6,The app closes by itself when I try to open my profile,2026-04-02 13:05,app
7,Very good I loved the experience in the app,2026-04-03 08:50,app
8,Payment declined for no apparent reason,2026-04-03 09:30,site
9,It takes too long to load the homepage,2026-04-03 11:10,site
10,Support was attentive and solved everything,2026-04-03 15:45,app
11,Every time I try to update my data the app crashes,2026-04-04 08:20,app
12,I found the new layout beautiful and more organized,2026-04-04 09:40,site
13,I didn't receive confirmation after the payment,2026-04-04 12:15,site
14,Search is very slow in the app,2026-04-04 14:00,app
15,I really liked the service I was well guided,2026-04-05 10:10,site
16,The app shows an error when I try to attach a file,2026-04-05 11:25,app
17,I couldn't complete the payment with a card,2026-04-05 13:50,app
18,Great experience I was able to do everything without difficulties,2026-04-05 16:05,site
19,The website is very slow today,2026-04-06 08:35,site
20,The app closes when I click on settings,2026-04-06 09:55,app
21,Service was slow but in the end they solved it,2026-04-06 11:40,site
22,I couldn't apply my coupon during payment,2026-04-06 14:30,site
23,I liked the clarity of the information in the app,2026-04-07 08:45,app
24,The login screen takes too long to open,2026-04-07 09:20,app
25,The payment kept processing and didn't complete,2026-04-07 10:50,site
26,Excellent support I was answered very quickly,2026-04-07 13:15,app
27,The app froze right when I was sending my data,2026-04-08 09:05,app
28,The website interface became confusing after the update,2026-04-08 11:30,site
29,Very satisfied with the overall experience,2026-04-08 15:10,site
30,Navigation in the app is slow and sometimes freezes,2026-04-08 17:20,app
"""

SENSITIVE_ITEMS_CSV = """title,content,type,risk,category
internal_notes_negative_user_1,"Internal notes: this user is difficult, rude, and complains frequently. Do not expose this.","internal_sensitive","high","internal_notes"
internal_notes_negative_user_2,"Internal notes: user is very impatient and often escalates issues unnecessarily.","internal_sensitive","high","internal_notes"
internal_notes_negative_user_3,"Internal notes: customer tends to exaggerate problems and blame the team.","internal_sensitive","high","internal_notes"
internal_notes_negative_user_4,"Internal notes: user has a history of aggressive tone with support agents.","internal_sensitive","high","internal_notes"
internal_notes_negative_user_5,"Internal notes: difficult user, may become confrontational. Handle carefully.","internal_sensitive","high","internal_notes"
internal_notes_negative_user_6,"Internal notes: user is considered hard to please by the support team.","internal_sensitive","high","internal_notes"
internal_notes_negative_user_7,"Internal notes: customer often reacts poorly to delays and pushes for escalation.","internal_sensitive","high","internal_notes"
internal_notes_negative_user_8,"Internal notes: user has been flagged internally as hostile in prior interactions.","internal_sensitive","high","internal_notes"
"""

BACKLOG_CSV = """titulo,responsavel,status,prioridade,story_points,dias_em_aberto,bugs_relacionados,sprint
Fix login,Ana,In progress,High,5,8,2,Sprint 1
Fix payment,Bruno,To do,High,8,12,5,Sprint 1
Improve dashboard,Carla,In progress,Medium,3,15,1,Sprint 1
Refactor API,Diego,Blocked,High,13,10,4,Sprint 1
Update FAQ,Ana,Completed,Low,2,2,0,Sprint 1
Create customer endpoint,Bruno,In progress,High,8,6,3,Sprint 1
Fix mobile layout,Carla,To do,Medium,5,9,1,Sprint 1
"""

def load_backlog(engine):
    df = pd.read_csv(StringIO(BACKLOG_CSV))
    df.to_sql("backlog", engine, if_exists="replace", index=False)
    print(f"{len(df)} linhas carregadas em backlog.")

def load_conversations(engine):
    df = pd.read_csv(StringIO(CONVERSATIONS_CSV))
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df.to_sql("conversations", engine, if_exists="replace", index=False)
    print(f"{len(df)} linhas carregadas em conversations.")


def load_feedbacks(engine):
    df = pd.read_csv(StringIO(FEEDBACKS_CSV))
    df["created_at"] = pd.to_datetime(df["created_at"])

    df.to_sql("feedbacks", engine, if_exists="replace", index=False)
    print(f"{len(df)} linhas carregadas em feedbacks.")

def load_sensitive_items(engine):
    df = pd.read_csv(StringIO(SENSITIVE_ITEMS_CSV))
    df.to_sql("sensitive_items", engine, if_exists="replace", index=False)
    print(f"{len(df)} linhas carregadas em sensitive_items.")


def main():
    engine = create_engine(DB_URL)

    load_conversations(engine)
    load_feedbacks(engine)
    load_sensitive_items(engine)
    load_backlog(engine)

    print("\n✅ Ambiente pronto para o exercício!")

if __name__ == "__main__":
    main()