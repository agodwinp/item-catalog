from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import User, Category, Item, Base

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
category= Category(name="Football", image="football.jpg", user_id=1)
session.add(category)
session.commit()
Items = Item(title="Shin Pads", description="Protective pads to be worn on your shins, essential for competitive football matches. Created from a mix of carbon fibre and polythene, these shin pads can take the equivalent of 5G of force before breaking.", category_id=1, user_id=1)
session.add(Items)
session.commit()
Items = Item(title="Goalkeeper Gloves", description="Soft and sturdy gloves that will protect and reinforce saving the ball, whilst providing incomparable warmth and touch when distributing to your team.", category_id=1, user_id=1)
session.add(Items)
session.commit()
Items = Item(title="Football Boots", description="The essential piece of equipment for playing football on soft grass, a reliable pair of football boots designed to give ultimate touch, strength and agility on the field.", category_id=1, user_id=1)
session.add(Items)
session.commit()
Items = Item(title="Team Socks", description="Without crisp team socks not only will you look out of place but your shin pads will be exposed to the elements. These socks will keep you warm and you'll look great whilst being warm.", category_id=1, user_id=1)
session.add(Items)
session.commit()
Items = Item(title="Multi-purpose Tape", description="Some of the most fashionable players use this tape to strap around their ankles, but only the best save this for head injuries. Use this as you please, for functional or fashionable purposes.", category_id=1, user_id=1)
session.add(Items)
session.commit()
Items = Item(title="Football Shorts", description="Another essential piece of equipment, without these it won't take long before the police are called. Make sure when buying shorts that they have an elastic and firm grip, as you don't want these to fall.", category_id=1, user_id=1)
session.add(Items)
session.commit()
Items = Item(title="Team Jersey", description="Available in all colours, sizes and strips. The best style is to choose the Newcastle United strip, this will guarantee heart, passion and no investment in the team.", category_id=1, user_id=1)
session.add(Items)
session.commit()
print("Added football items!")

# Items for Rugby
category = Category(name="Rugby", image="rugby.jpg", user_id=1)
session.add(category)
session.commit()
Items = Item(title="Rugby Boots", description="The essential piece of equipment for playing rugby, a reliable pair of football boots designed to give ultimate touch, strength and agility on the field.", category_id=2, user_id=1)
session.add(Items)
session.commit()
Items = Item(title="Team Socks", description="Without crisp team socks not only will you look out of place but your shins will be exposed to the elements. These socks will keep you warm and you'll look great whilst being warm.", category_id=2, user_id=1)
session.add(Items)
session.commit()
Items = Item(title="Multi-purpose Tape", description="Some of the most fashionable players use this tape to strap around their ankles, but only the best save this for head injuries. Use this as you please, for functional or fashionable purposes.", category_id=2, user_id=1)
session.add(Items)
session.commit()
Items = Item(title="Rugby Shorts", description="Another essential piece of equipment, without these it won't take long before the police are called. Veruy similar to football shorts, but more rugged and more suited to sliding on the grass.", category_id=2, user_id=1)
session.add(Items)
session.commit()
Items = Item(title="Team Jersey", description="Available in all colours, sizes and strips. A classic, rugged, dirty looking jersey ideal for die-hard rugby fans and players looking for that post-match battered look.", category_id=2, user_id=1)
session.add(Items)
session.commit()
Items = Item(title="Gum Shield", description="Made with the highest quality rubber to ensure a guppy looking set of gnashers and absolutely no ability communicate with your team mates. Leave in boiling water to make as mushy as soggy spaghetti.", category_id=2, user_id=1)
session.add(Items)
session.commit()
Items = Item(title="Scrum Cap", description="No rugby player is complete without the cherry on the cake, being the scrum cap. This will ensure sprouts of hairs poking through and the genuine madman look whilst on the field. Nobody will dare to take you on whilst wearing this.", category_id=2, user_id=1)
session.add(Items)
session.commit()
print("Added rugby items!")

# Items for Tennis
category = Category(name="Tennis", image="tennis.jpg", user_id=2)
session.add(category)
session.commit()
Items = Item(title="Tennis Balls", description="Bright green, fluffy and very bouncy... these tennis balls are exactly as expected and you can guarantee that at least half of these will be lost within a day of byuing them.", category_id=3, user_id=2)
session.add(Items)
session.commit()
Items = Item(title="Tennis Racket", description="Legend has it that this racket holds the world record for the farthest distance a tennis ball has ever been hit by a human. Guaranteed power, scary power.", category_id=3, user_id=2)
session.add(Items)
session.commit()
Items = Item(title="Headband", description="Only a psycopath would dare to play tennis without one of these. Don't let the sweat ruin your game, this headband will take care of that for you and you'll look amazing.", category_id=3, user_id=2)
session.add(Items)
session.commit()
Items = Item(title="Wristband", description="For the players that find a headband just simply not enough. Add this fluffy accessory to your arsenal and you'll always have something to wipe up any spillage.", category_id=3, user_id=2)
session.add(Items)
session.commit()
print("Added tennis items!")

# Items for Swimming
category = Category(name="Swimming", image="swimming.jpg", user_id=1)
session.add(category)
session.commit()
Items = Item(title="Swimming Cap", description="It's proven impossible to swim in mainland Europe without one of these caps, if you're planning a holiday, make sure you have plenty of these packed.", category_id=4, user_id=1)
session.add(Items)
session.commit()
Items = Item(title="Goggles", description="Not only great for people of all ages to explore the interesting findings of public swimming pools, but also a great accessory if you feel like protecting your eyes against pollution.", category_id=4, user_id=1)
session.add(Items)
session.commit()
Items = Item(title="Swimsuit", description="Not only for ladies, in the modern world that we live in, these are for all ages, sizes, genders and creeds. Only suitable for swimming pools, definitely not recommended for parties, dinner or dates.", category_id=4, user_id=1)
session.add(Items)
session.commit()
Items = Item(title="Armbands", description="If you can't swim, it's quite simply essential that you use these. If not, you will simple sink the the bottom and nobody wants that.", category_id=4, user_id=1)
session.add(Items)
session.commit()
Items = Item(title="Towel", description="Imperative that you buy one of these just to lay down on anything that you'd like to lay claim to whilst on holiday. Works very well with sun loungers next to the pool.", category_id=4, user_id=1)
session.add(Items)
session.commit()
print("Added swimming items!")

# Items for Weightlifting
category = Category(name="Weightlifting", image="weightlifting.jpg", user_id=1)
session.add(category)
session.commit()
Items = Item(title="Chalk", description="Provides you an unexpected amount of grip and strength when lifting weights. Also great as a substitute for flour or to make a nice mess in the kitchen", category_id=5, user_id=1)
session.add(Items)
session.commit()
Items = Item(title="Lifting Belt", description="Ideal for getting and extra 10 percent out of your lifts, and looking like a hungry viking whilst doing so. If you're not using a belt, theres a real danger everything will fall out whilst lifting.", category_id=5, user_id=1)
session.add(Items)
session.commit()
Items = Item(title="Powerlifting Shoes", description="These make you look like the real part and will help you to get that extra power when going for PB's. Also a good substitute for astro turfs if you get a last minute call up to play.", category_id=5, user_id=1)
session.add(Items)
session.commit()
print("Added weightlifting items!")

# Items for Basketball
category = Category(name="Basketball", image="basketball.jpg", user_id=1)
session.add(category)
session.commit()
Items = Item(title="Basketball", description="Without a basketball, you can't play ball... So this is by far the most essential component to this sport. Make sure it has lots of nice dimples to help you grip it.", category_id=6, user_id=1)
session.add(Items)
session.commit()
Items = Item(title="Sneakers", description="Whatever you do, make sure you oly purchase sneakers to play basketball in. Under no circumstances should you wear trainers for basketball. These sneakers will make very loud squeaks on the court to improve performance.", category_id=6, user_id=1)
session.add(Items)
session.commit()
Items = Item(title="Shorts", description="The baggiest, loosest and most breezy shorts on the market today. The provide excellent breathability and will make you look much cooler than when you weren't wearing them.", category_id=6, user_id=1)
session.add(Items)
session.commit()
Items = Item(title="Team Vest", description="Available in all sizes, colours and strips. The best seller is the Raptors jersey due to the awesome Velociraptor starring on the front but also due to the famous players that used to play for them.", category_id=6, user_id=1)
session.add(Items)
session.commit()
print("Added basketball items!")

# Items for Volleyball
category = Category(name="Volleyball", image="volleyball.jpg", user_id=1)
session.add(category)
session.commit()
Items = Item(title="Volleyball Net", description="Easy to set up and easy to take down, exactly what it says on the tin really.", category_id=7, user_id=1)
session.add(Items)
session.commit()
print("Added volleyball items!")