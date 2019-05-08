from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import User, Category, Item, Base

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Arun Godwin Patel", email="arungodwinpatel@googlemail.com", picture='https://lh5.googleusercontent.com/-YlxROPOjjOQ/AAAAAAAAAAI/AAAAAAAAAAA/ACHi3rfbjGFyUZp8LRwsJewv7h7q08ELzQ/s96-c/photo.jpg')
session.add(User1)
session.commit()

User2 = User(name="Testy McTester", email="test@mctesty.com")
session.add(User2)
session.commit()

# Items for Football
category1 = Category(name="Football", user_id=1)
session.add(category1)
session.commit()

Item1 = Item(title="Shin Pads", description="The best shin pads in the world", category_id=1, user_id=1)
session.add(Item1)
session.commit()

Item2 = Item(title="Goalkeeper Gloves", description="The best gloves in the world", category_id=1, user_id=2)
session.add(Item2)
session.commit()

print("added menu items!")