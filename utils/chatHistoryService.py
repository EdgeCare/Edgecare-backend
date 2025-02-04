from sqlalchemy.orm import Session
from db.models.user import Chat


def create_or_update_chat(db: Session, chat_id: int, user_id: int, chat: str):
    existing_chat = db.query(Chat).filter(Chat.chat_id == chat_id, Chat.user_id == user_id).first()
    
    if existing_chat:
        # Update existing record
        existing_chat.chat = chat
    else:
        # Insert new record
        existing_chat = Chat(chat_id=chat_id, user_id=user_id, chat=chat)
        db.add(existing_chat)

    db.commit()
    db.refresh(existing_chat)
    return existing_chat


def create_chat(db: Session, chat_id: int, user_id: int, chat: str):
    new_chat = Chat(chat_id=chat_id, user_id=user_id, chat=chat)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat

def get_all_chats(db: Session):
    return db.query(Chat).all()


def get_chats_by_user(db: Session, user_id: int):
    return db.query(Chat).filter(Chat.user_id == user_id).all()

def get_chat_by_user_and_id(db: Session, user_id: int, chat_id: int):
    return db.query(Chat).filter(Chat.user_id == user_id, Chat.chat_id == chat_id).first() 





def delete_chat(db: Session, chat_id: int):
    chat = db.query(Chat).filter(Chat.chat_id == chat_id).first()
    if chat:
        db.delete(chat)
        db.commit()


