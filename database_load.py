from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Book, User

engine = create_engine('sqlite:///bookstore.db')
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
User1 = User(name="Sasha Romello", email="sasha_rm@yahoo.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Create Books
book1 = Book(user_id=1, title="Humans of New York: Stories", author="Brandon Stanton", category="Arts & Photography",
       price=float(18.88), inventoryCount=4, rating="3", dateUpdated=datetime.today(),
       description="In the summer of 2010, photographer Brandon Stanton began an ambitious project to single-handedly create a photographic census of New York City. The photos he took and the accompanying interviews became the blog Humans of New York. In the first three years, his audience steadily grew from a few hundred to over one million. In 2013, his book Humans of New York, based on that blog, was published and immediately catapulted to the top of the NY Times Bestseller List. It has appeared on that list for over twenty-five weeks to date. The appeal of HONY has been so great that in the course of the next year Brandon's following increased tenfold to, now, over 12 million followers on Facebook.")

session.add(book1)
session.commit()

book1 = Book(user_id=1, title="Ephemeral Works", author="Andy Goldsworthy", category="Arts & Photography",
       price=float(70.70), inventoryCount=25, rating="5", dateUpdated=datetime.today(),
       description="On an almost daily basis, Andy Goldsworthy makes art using the materials and conditions he encounters wherever he is, be it the land around his Scottish home, the mountain regions of France or Spain, or the sidewalks of New York City, Glasgow, or Rio de Janeiro. Out of earth, rocks, leaves, ice, snow, rain, sunlight, and shadow he creates works that exist briefly before they are altered and erased by natural processes. They are documented in his photographs, and their larger meanings are bound up with the forces that they embody: materiality, temporality, growth, vitality, permanence, decay, chance, labor, and memory")

session.add(book1)
session.commit()

book1 = Book(user_id=1, title="Dust & Grooves: Adventures in Record Collecting", author="Eilon Paz", category="Arts & Photography",
       price=float(19.99), inventoryCount=189, rating="2", dateUpdated=datetime.today(),
       description="Dust & Grooves: Adventures in Record Collecting is an inside look into the world of vinyl record collectors in the most intimate of environments their record rooms. Compelling photographic essays from photographer Eilon Paz are paired with in-depth and insightful interviews to illustrate what motivates these collectors to keep digging for more records. The reader gets an up close and personal look at a variety of well-known vinyl champions, including Gilles Peterson and King Britt, as well as a glimpse into the collections of known and unknown DJs, producers, record dealers, and everyday enthusiasts. Driven by his love for vinyl records, Paz takes us on a five-year journey unearthing the very soul of the vinyl community.")

session.add(book1)
session.commit()

book1 = Book(user_id=1, title="One Hundred & One Beautiful Small Towns in Italy", author="Paolo Lazzarin", category="Arts & Photography",
       price=float(19.18), inventoryCount=4, rating="3", dateUpdated=datetime.today(),
       description="The perfect guide for those who can't resist succumbing to Italy's charms again and again, now in a popular pocket-sized format. Who hasn't dreamt of being whisked away to a sweet little Italian town buried deep in the countryside? The small towns sprinkled throughout this expansive book are not only rich with beauty but also saturated with as much historical and cultural importance as their sister cities. The fact that they are off the beaten path though sometimes extraordinarily famous for their art, food, and wine, or simply their setting-makes them rare gems even more desirable to see. The 101 towns featured represent the twenty diverse regions of Italy and their varied landscapes, architecture, and local specialties.")

session.add(book1)
session.commit()

book1 = Book(user_id=1, title="Caps for Sale: A Tale of a Peddler, Some Monkeys and Their Monkey Business", author="Esphyr Slobodkina", category="Children's Books",
       price=float(4.99), inventoryCount=350, rating="2.5", dateUpdated=datetime.today(),
       description="This story about a peddler and a band of mischievous monkeys is filled with warmth, humor, and simplicity and teaches children about problem and resolution. Children will delight in following the peddler's efforts to outwit the monkeys and will ask to read it again and again. Caps for Sale is an excellent easy-to-read book that includes repetition, patterns, and colors, perfect for early readers")

session.add(book1)
session.commit()

book1 = Book(user_id=1, title="My Friend Bear", author="", category="Children's Books",
       price=float(18.88), inventoryCount=4, rating="3", dateUpdated=datetime.today(),
       description="")

session.add(book1)
session.commit()

book1 = Book(user_id=1, title="Humans of New York: Stories", author="Jez Alborough", category="Children's Books",
       price=float(14.99), inventoryCount=189, rating="5", dateUpdated=datetime.today(),
       description="Eddie's feeling sad, and so is the bear. They both wish they had a friend to talk to. All they have are their teddies, and teddies can't talk. Or can they? Teddy fans, prepare! From the author/illustrator of the best-selling WHERE'S MY TEDDY? and IT'S THE BEAR! comes a third warm and funny story about this odd-sized, lovable pair, a small boy and a rather large bear!")

session.add(book1)
session.commit()

book1 = Book(user_id=1, title="The Curious Kid's Science Book: 100+ Creative Hands-On Activities for Ages", author="Asia Citro", category="Children's Books",
       price=float(6.99), inventoryCount=38, rating="3", dateUpdated=datetime.today(),
       description="How would your child find the answers to these questions? In The Curious Kid's Science Book, your child will learn to design his or her own science investigations to determine the answers! Children will learn to ask their own scientific questions, discover value in failed experiments, and -- most importantly -- have a blast with science. The 100+ hands-on activities in the book use household items to playfully teach important science, technology, engineering, and math skills. Each creative activity includes age-appropriate explanations and (when possible) real life applications of the concepts covered")

session.add(book1)
session.commit()

book1 = Book(user_id=1, title="The Wonderful Things You Will Be", author="Emily Winfield Martin", category="Children's Books",
       price=float(10.99), inventoryCount=4, rating="3", dateUpdated=datetime.today(),
       description="From brave and bold to creative and clever, Emily Winfield Martin's rhythmic rhyme expresses all the loving things that parents think of when they look at their children. With beautiful, and sometimes humorous, illustrations, and a clever gatefold with kids in costumes, this is a book grown-ups will love reading over and over to kids both young and old. A great gift for any occasion, but a special stand-out for baby showers, birthdays, and graduation.")

session.add(book1)
session.commit()

book1 = Book(user_id=1, title="One with You", author="Sylvia Day", category="Romance",
       price=float(9.99), inventoryCount=1089, rating="5", dateUpdated=datetime.today(),
       description="The final chapter in the global blockbuster Crossfire quintet Gideon Cross. Falling in love with him was the easiest thing I've ever done. It happened instantly. Completely. Irrevocably. Marrying him was a dream come true. Staying married to him is the fight of my life. Love transforms. Ours is both a refuge from the storm and the most violent of tempests. Two damaged souls entwined as one.")

session.add(book1)
session.commit()

book1 = Book(user_id=1, title="The Beast (Black Dagger Brotherhood)", author="J. R. Ward", category="Romance",
       price=float(13.99), inventoryCount=18, rating="2.5", dateUpdated=datetime.today(),
       description="Nothing is as it used to be for the Black Dagger Brotherhood. After avoiding war with the Shadows, alliances have shifted and lines have been drawn. The slayers of the Lessening Society are stronger than ever, preying on human weakness to acquire more money, more weapons, more power. But as the Brotherhood readies for an all-out attack on them, one of their own fights a battle within himsel")

session.add(book1)
session.commit()

book1 = Book(user_id=1, title="Key of Valor", author="Nora Roberts", category="Romance",
       price=float(13.42), inventoryCount=79, rating="4", dateUpdated=datetime.today(),
       description="Growing up, Zoe McCourt did not have an easy life some might call it disadvantaged. A hairstylist from a West Virginia trailer park, she ended up in beautiful Pleasant Valley, Pennsylvania, by sheer determination. How she ended up on a quest for a key to unlock the soul of a warrior demigoddess is another story")

session.add(book1)
session.commit()

book1 = Book(user_id=1, title="Precious Gifts", author="Danielle Steel", category="Romance",
       price=float(13.99), inventoryCount=1998, rating="5", dateUpdated=datetime.today(),
       description="Handsome, widowed, sophisticated, utterly charming, Paul Parker won the heart of a wealthy young Frenchwoman the daughter of an American financier, the granddaughter of a major French art dealer as his second wife. In two marriages, he fathered a challenging son and three very different daughters. But as irresponsible as he was irresistible, he ultimately shrugged off the demands of marriage and parenting to pursue life as an international bon vivant")

session.add(book1)
session.commit()

book1 = Book(user_id=1, title="The Prada Plan 4: Love & War", author="Ashley Antoinette", category="African American",
       price=float(9.90), inventoryCount=4, rating="3", dateUpdated=datetime.today(),
       description="The feud between YaYa and Leah has ruined the lives of everyone around them. In The Prada Plan 4, the animosity is alive, and resentments run deeper than ever. Indie has watched YaYa's past destroy the woman he once knew, and his patience has run thin. After being left at the altar, he is heartbroken and confused. His quests to save YaYa from herself have failed, and he finally decides that it's time to let the love of his life go. ")

session.add(book1)
session.commit()

book1 = Book(user_id=1, title="Murderville 3: The Black Dahlia", author="Ashley & JaQuavis", category="African American",
       price=float(11.84), inventoryCount=489, rating="2", dateUpdated=datetime.today(),
       description="THIS THRILLING PAGE-TURNER INTRODUCES THE STORY OF THE BLACK DAHLIA AND HER BLOODSTAINED ASCENT TO POWER. AFTER ESTABLISHING A CONNECTION WITH THE FIVE FAMILIES, DAHLIA BECOMES LITERALLY UNTOUCHABLE. HER BRAZEN TACTICS AND MAFIA-STYLE ANTICS BECOME INFAMOUS AS SHE IS SET TO TAKE OVER THE COUNTRY'S BLACK MARKET. BUT THERE IS ONLY ONE THING STILL STANDING IN HER WAY SHE IS A WOMAN. THE COMPETITION DOESN'T RESPECT HER SO DAHLIA SETS OUT ON A BLOODY MISSION TO ENSURE THE PROTECTION OF HER NEW KINGDOM")

session.add(book1)
session.commit()

book1 = Book(user_id=1, title="Possessed by Passion (Forged of Steele)", author="Brenda Jackson", category="African American",
       price=float(6.50), inventoryCount=4, rating="5", dateUpdated=datetime.today(),
       description="Burned-by-love architect Hunter McKay came home to Phoenix to open her own firm, not rekindle her fleeting high school romance with playboy Tyson Steele. But when she runs into the sexy surgeon at a nightclub and he unleashes that legendary Steele charm Hunter fears she's headed straight for heartbreak once again.")

session.add(book1)
session.commit()

book1 = Book(user_id=1, title="A Wanted Woman", author="Eric Jerome Dickey", category="African American",
       price=float(10.00), inventoryCount=893, rating="2.5", dateUpdated=datetime.today(),
       description="The assassin called Reaper is a woman of a thousand faces, and just as many accents.  In the blink of an eye, she can become anyone.  Some desirable.  All dangerous. For Reaper, the Trinidad contract should be simple: infiltrate the infamous Laventille Killers' organization, earn access to her political target, eliminate him, and then escape from the island.")

session.add(book1)
session.commit()



print "Books loaded to database!"

