from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import User, Category, Item, Base

engine = create_engine('postgresql://catalog:password@localhost/catalog')
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
picture = 'https://lh5.googleusercontent.com/-YlxROPOjjOQ/AAAAAAAAAAI/AAAAA'
picture += 'AAAAAA/ACHi3rfbjGFyUZp8LRwsJewv7h7q08ELzQ/s96-c/photo.jpg'
User1 = User(name="Arun Godwin Patel", email="arungodwinpatel@googlemail.com",
             picture=picture)
session.add(User1)
session.commit()

User2 = User(name="Testy McTester", email="test@mctesty.com")
session.add(User2)
session.commit()

# Items for Football
category = Category(name="Football", image="football.jpg", user_id=1)
session.add(category)
session.commit()
description = "Protective pads to be worn on your shins, essential for "
description += "competitive football matches. Created from a mix of carbon "
description += "fibre and polythene, these shin pads can take the equivalent "
description += "of 5G of force before breaking."
Items = Item(title="Shin Pads", description=description, category_id=1,
             user_id=1)
session.add(Items)
session.commit()
description = "Soft and sturdy gloves that will protect and reinforce saving "
description += "the ball, whilst providing incomparable warmth and touch "
description += "when distributing to your team."
Items = Item(title="Goalkeeper Gloves", description=description,
             category_id=1, user_id=1)
session.add(Items)
session.commit()
description = "The essential piece of equipment for playing football on soft "
description += "grass, a reliable pair of football boots designed to give "
description += "ultimate touch, strength and agility on the field."
Items = Item(title="Football Boots", description=description, category_id=1,
             user_id=1)
session.add(Items)
session.commit()
description = "Without crisp team socks not only will you look out of place "
description += "but your shin pads will be exposed to the elements. These "
description += "socks will keep you warm and you'll look great "
description += "whilst being warm."
Items = Item(title="Team Socks", description=description, category_id=1,
             user_id=1)
session.add(Items)
session.commit()
description = "Some of the most fashionable players use this tape to strap "
description += "around their ankles, but only the best save this for head "
description += "injuries. Use this as you please, for functional or "
description += "fashionable purposes."
Items = Item(title="Multi-purpose Tape", description=description,
             category_id=1, user_id=1)
session.add(Items)
session.commit()
description = "Another essential piece of equipment, without these it won't "
description += "take long before the police are called. Make sure when buying "
description += "shorts that they have an elastic and firm grip, as you don't"
description += "want these to fall."
Items = Item(title="Football Shorts", description=description, category_id=1,
             user_id=1)
session.add(Items)
session.commit()
description = "Available in all colours, sizes and strips. The best style is "
description += "to choose the Newcastle United strip, this will guarantee "
description += "heart, passion and no investment in the team."
Items = Item(title="Team Jersey", description=description, category_id=1,
             user_id=1)
session.add(Items)
session.commit()
print("Added football items!")

# Items for Rugby
category = Category(name="Rugby", image="rugby.jpg", user_id=1)
session.add(category)
session.commit()
description = "The essential piece of equipment for playing rugby, a reliable "
description += "pair of football boots designed to give ultimate touch, "
description += "strength and agility on the field."
Items = Item(title="Rugby Boots", description=description, category_id=2,
             user_id=1)
session.add(Items)
session.commit()
description = "Without crisp team socks not only will you look out of place "
description += "but your shins will be exposed to the elements. These socks "
description += "will keep you warm and you'll look great whilst being warm."
Items = Item(title="Team Socks", description=description, category_id=2,
             user_id=1)
session.add(Items)
session.commit()
description = "Some of the most fashionable players use this tape to strap "
description += "around their ankles, but only the best save this for head "
description += "injuries. Use this as you please, for functional or "
description += "fashionable purposes."
Items = Item(title="Multi-purpose Tape", description=description,
             category_id=2, user_id=1)
session.add(Items)
session.commit()
description = "Another essential piece of equipment, without these it won't "
description += "take long before the police are called. Veruy similar to "
description += "football shorts, but more rugged and more suited to "
description += "sliding on the grass."
Items = Item(title="Rugby Shorts", description=description, category_id=2,
             user_id=1)
session.add(Items)
session.commit()
description = "Available in all colours, sizes and strips. A classic, "
description += "rugged, dirty looking jersey ideal for die-hard rugby fans "
description += "and players looking for that post-match battered look."
Items = Item(title="Team Jersey", description=description, category_id=2,
             user_id=1)
session.add(Items)
session.commit()
description = "Made with the highest quality rubber to ensure a guppy "
description += "looking set of gnashers and absolutely no ability communicate "
description += "with your team mates. Leave in boiling water to make as "
description += "mushy as soggy spaghetti."
Items = Item(title="Gum Shield", description=description, category_id=2,
             user_id=1)
session.add(Items)
session.commit()
description = "No rugby player is complete without the cherry on the cake, "
description += "being the scrum cap. This will ensure sprouts of hairs poking "
description += "through and the genuine madman look whilst on the field. "
description += "Nobody will dare to take you on whilst wearing this."
Items = Item(title="Scrum Cap", description=description, category_id=2,
             user_id=1)
session.add(Items)
session.commit()
print("Added rugby items!")

# Items for Tennis
category = Category(name="Tennis", image="tennis.jpg", user_id=2)
session.add(category)
session.commit()
description = "Bright green, fluffy and very bouncy... these tennis balls are "
description += "exactly as expected and you can guarantee that at least half "
description += "of these will be lost within a day of buying them."
Items = Item(title="Tennis Balls", description=description, category_id=3,
             user_id=2)
session.add(Items)
session.commit()
description = "Legend has it that this racket holds the world record for the "
description += "farthest distance a tennis ball has ever been hit by a human. "
description += "Guaranteed power, scary power."
Items = Item(title="Tennis Racket", description=description, category_id=3,
             user_id=2)
session.add(Items)
session.commit()
description = "Only a psycopath would dare to play tennis without one of "
description += "these. Don't let the sweat ruin your game, this headband will "
description += "take care of that for you and you'll look amazing."
Items = Item(title="Headband", description=description, category_id=3,
             user_id=2)
session.add(Items)
session.commit()
description = "For the players that find a headband just simply not enough. "
description += "Add this fluffy accessory to your arsenal and you'll always "
description += "have something to wipe up any spillage."
Items = Item(title="Wristband", description=description, category_id=3,
             user_id=2)
session.add(Items)
session.commit()
print("Added tennis items!")

# Items for Swimming
category = Category(name="Swimming", image="swimming.jpg", user_id=1)
session.add(category)
session.commit()
description = "It's proven impossible to swim in mainland Europe without one "
description += "of these caps, if you're planning a holiday, make sure you "
description += "have plenty of these packed."
Items = Item(title="Swimming Cap", description=description, category_id=4,
             user_id=1)
session.add(Items)
session.commit()
description = "Not only great for people of all ages to explore the "
description += "interesting findings of public swimming pools, but also a "
description += "great accessory if you feel like protecting your eyes against "
description += "pollution."
Items = Item(title="Goggles", description=description, category_id=4,
             user_id=1)
session.add(Items)
session.commit()
description = "Not only for ladies, in the modern world that we live in, "
description += "these are for all ages, sizes, genders and creeds. Only "
description += "suitable for swimming pools, definitely not recommended for "
description += "parties, dinner or dates."
Items = Item(title="Swimsuit", description=description, category_id=4,
             user_id=1)
session.add(Items)
session.commit()
description = "If you can't swim, it's quite simply essential that you use "
description += "these. If not, you will simple sink the the bottom "
description += "and nobody wants that."
Items = Item(title="Armbands", description=description, category_id=4,
             user_id=1)
session.add(Items)
session.commit()
description = "Imperative that you buy one of these just to lay down on "
description += "anything that you'd like to lay claim to whilst on holiday. "
description += "Works very well with sun loungers next to the pool."
Items = Item(title="Towel", description=description, category_id=4, user_id=1)
session.add(Items)
session.commit()
print("Added swimming items!")

# Items for Weightlifting
category = Category(name="Weightlifting", image="weightlifting.jpg", user_id=1)
session.add(category)
session.commit()
description = "Provides you an unexpected amount of grip and strength when "
description += "lifting weights. Also great as a substitute for flour or to "
description += "make a nice mess in the kitchen"
Items = Item(title="Chalk", description=description, category_id=5, user_id=1)
session.add(Items)
session.commit()
description = "Ideal for getting and extra 10 percent out of your lifts, and "
description += "looking like a hungry viking whilst doing so. If you're not "
description += "using a belt, theres a real danger everything will fall out "
description += "whilst lifting."
Items = Item(title="Lifting Belt", description=description, category_id=5,
             user_id=1)
session.add(Items)
session.commit()
description = "These make you look like the real part and will help you to get"
description = "that extra power when going for PB's. Also a good substitute "
description = "for astro turfs if you get a last minute call up to play."
Items = Item(title="Powerlifting Shoes", description=description,
             category_id=5, user_id=1)
session.add(Items)
session.commit()
print("Added weightlifting items!")

# Items for Basketball
category = Category(name="Basketball", image="basketball.jpg", user_id=1)
session.add(category)
session.commit()
description = "Without a basketball, you can't play ball... So this is by far "
description += "the most essential component to this sport. Make sure it has "
description += "lots of nice dimples to help you grip it."
Items = Item(title="Basketball", description=description, category_id=6,
             user_id=1)
session.add(Items)
session.commit()
description = "Whatever you do, make sure you oly purchase sneakers to play "
description += "basketball in. Under no circumstances should you wear trainers"
description += "for basketball. These sneakers will make very loud squeaks on "
description += "the court to improve performance."
Items = Item(title="Sneakers", description=description, category_id=6,
             user_id=1)
session.add(Items)
session.commit()
description = "The baggiest, loosest and most breezy shorts on the market "
description += "today. The provide excellent breathability and will make you "
description += "look much cooler than when you weren't wearing them."
Items = Item(title="Shorts", description=description, category_id=6, user_id=1)
session.add(Items)
session.commit()
description = "Available in all sizes, colours and strips. The best seller "
description += "is the Raptors jersey due to the awesome Velociraptor "
description += "starring on the front but also due to the famous players "
description += "that used to play for them."
Items = Item(title="Team Vest", description=description, category_id=6,
             user_id=1)
session.add(Items)
session.commit()
print("Added basketball items!")

# Items for Volleyball
category = Category(name="Volleyball", image="volleyball.jpg", user_id=1)
session.add(category)
session.commit()
description = "Easy to set up and easy to take down, "
description += "exactly what it says on the tin really."
Items = Item(title="Volleyball Net",
             description=description, category_id=7, user_id=1)
session.add(Items)
session.commit()
print("Added volleyball items!")
