from PIL import Image
import numpy
import os
import requests
import shutil

IM_WIDTH, IM_HEIGHT = 309, 496
HORIZ_IM_WIDTH, HORIZ_IM_HEIGHT = 473, 290
ALL_CARDS_STRING = '''Black Market	Promo	10
Church	Promo	10
Dismantle	Promo	10
Envoy	Promo	10
Sauna	Promo	5
Avanto	Promo	5
Walled Village	Promo	10
Governor	Promo	10
Captain	Promo	10
Prince	Promo	10
Copper	Base	60
Curse	Base	30
Estate	Base	24
Silver	Base	40
Duchy	Base	12
Gold	Base	30
Province	Base	12
Cellar	Base	10
Chapel	Base	10
Moat	Base	10
Harbinger	Base	10
Merchant	Base	10
Vassal	Base	10
Village	Base	10
Workshop	Base	10
Bureaucrat	Base	10
Gardens	Base	12
Militia	Base	10
Moneylender	Base	10
Poacher	Base	10
Remodel	Base	10
Smithy	Base	10
Throne Room	Base	10
Bandit	Base	10
Council Room	Base	10
Festival	Base	10
Laboratory	Base	10
Library	Base	10
Market	Base	10
Mine	Base	10
Sentry	Base	10
Witch	Base	10
Artisan	Base	10
Courtyard	Intrigue	10
Lurker	Intrigue	10
Pawn	Intrigue	10
Masquerade	Intrigue	10
Shanty Town	Intrigue	10
Steward	Intrigue	10
Swindler	Intrigue	10
Wishing Well	Intrigue	10
Baron	Intrigue	10
Bridge	Intrigue	10
Conspirator	Intrigue	10
Diplomat	Intrigue	10
Ironworks	Intrigue	10
Mill	Intrigue	12
Mining Village	Intrigue	10
Secret Passage	Intrigue	10
Courtier	Intrigue	10
Duke	Intrigue	12
Minion	Intrigue	10
Patrol	Intrigue	10
Replace	Intrigue	10
Torturer	Intrigue	10
Trading Post	Intrigue	10
Upgrade	Intrigue	10
Harem	Intrigue	12
Nobles	Intrigue	12
Embargo	Seaside	10
Haven	Seaside	10
Lighthouse	Seaside	10
Native Village	Seaside	10
Pearl Diver	Seaside	10
Ambassador	Seaside	10
Fishing Village	Seaside	10
Lookout	Seaside	10
Smugglers	Seaside	10
Warehouse	Seaside	10
Caravan	Seaside	10
Cutpurse	Seaside	10
Island	Seaside	12
Navigator	Seaside	10
Pirate Ship	Seaside	10
Salvager	Seaside	10
Sea Hag	Seaside	10
Treasure Map	Seaside	10
Bazaar	Seaside	10
Explorer	Seaside	10
Ghost Ship	Seaside	10
Merchant Ship	Seaside	10
Outpost	Seaside	10
Tactician	Seaside	10
Treasury	Seaside	10
Wharf	Seaside	10
Potion	Alchemy	16
Transmute	Alchemy	10
Vineyard	Alchemy	12
Herbalist	Alchemy	10
Apothecary	Alchemy	10
Scrying Pool	Alchemy	10
University	Alchemy	10
Alchemist	Alchemy	10
Familiar	Alchemy	10
Philosopher's Stone	Alchemy	10
Golem	Alchemy	10
Apprentice	Alchemy	10
Possession	Alchemy	10
Platinum	Prosperity	12
Colony	Prosperity	12
Loan	Prosperity	10
Trade Route	Prosperity	10
Watchtower	Prosperity	10
Bishop	Prosperity	10
Monument	Prosperity	10
Quarry	Prosperity	10
Talisman	Prosperity	10
Worker's Village	Prosperity	10
City	Prosperity	10
Contraband	Prosperity	10
Counting House	Prosperity	10
Mint	Prosperity	10
Mountebank	Prosperity	10
Rabble	Prosperity	10
Royal Seal	Prosperity	10
Vault	Prosperity	10
Venture	Prosperity	10
Goons	Prosperity	10
Grand Market	Prosperity	10
Hoard	Prosperity	10
Bank	Prosperity	10
Expand	Prosperity	10
Forge	Prosperity	10
King's Court	Prosperity	10
Peddler	Prosperity	10
Hamlet	Cornucopia	10
Fortune Teller	Cornucopia	10
Menagerie	Cornucopia	10
Farming Village	Cornucopia	10
Horse Traders	Cornucopia	10
Remake	Cornucopia	10
Tournament	Cornucopia	10
Young Witch	Cornucopia	10
Harvest	Cornucopia	10
Horn of Plenty	Cornucopia	10
Hunting Party	Cornucopia	10
Jester	Cornucopia	10
Fairgrounds	Cornucopia	12
Bag of Gold	Cornucopia	1
Diadem	Cornucopia	1
Followers	Cornucopia	1
Princess	Cornucopia	1
Trusty Steed	Cornucopia	1
Crossroads	Hinterlands	10
Duchess	Hinterlands	10
Fool's Gold	Hinterlands	10
Develop	Hinterlands	10
Oasis	Hinterlands	10
Oracle	Hinterlands	10
Scheme	Hinterlands	10
Tunnel	Hinterlands	12
Jack of All Trades	Hinterlands	10
Noble Brigand	Hinterlands	10
Nomad Camp	Hinterlands	10
Silk Road	Hinterlands	12
Spice Merchant	Hinterlands	10
Trader	Hinterlands	10
Cache	Hinterlands	10
Cartographer	Hinterlands	10
Embassy	Hinterlands	10
Haggler	Hinterlands	10
Highway	Hinterlands	10
Ill-Gotten Gains	Hinterlands	10
Inn	Hinterlands	10
Mandarin	Hinterlands	10
Margrave	Hinterlands	10
Stables	Hinterlands	10
Border Village	Hinterlands	10
Farmland	Hinterlands	12
Poor House	Dark Ages	10
Beggar	Dark Ages	10
Squire	Dark Ages	10
Vagrant	Dark Ages	10
Forager	Dark Ages	10
Hermit	Dark Ages	10
Market Square	Dark Ages	10
Sage	Dark Ages	10
Storeroom	Dark Ages	10
Urchin	Dark Ages	10
Armory	Dark Ages	10
Death Cart	Dark Ages	10
Feodum	Dark Ages	12
Fortress	Dark Ages	10
Ironmonger	Dark Ages	10
Marauder	Dark Ages	10
Procession	Dark Ages	10
Rats	Dark Ages	20
Scavenger	Dark Ages	10
Wandering Minstrel	Dark Ages	10
Band of Misfits	Dark Ages	10
Bandit Camp	Dark Ages	10
Catacombs	Dark Ages	10
Count	Dark Ages	10
Counterfeit	Dark Ages	10
Cultist	Dark Ages	10
Graverobber	Dark Ages	10
Junk Dealer	Dark Ages	10
Mystic	Dark Ages	10
Pillage	Dark Ages	10
Rebuild	Dark Ages	10
Rogue	Dark Ages	10
Altar	Dark Ages	10
Hunting Grounds	Dark Ages	2
Abandoned Mine	Dark Ages	2
Ruined Library	Dark Ages	2
Ruined Market	Dark Ages	2
Ruined Village	Dark Ages	2
Survivors	Dark Ages	2
Hovel	Dark Ages	6
Necropolis	Dark Ages	6
Overgrown Estate	Dark Ages	6
Madman	Dark Ages	10
Mercenary	Dark Ages	10
Spoils	Dark Ages	15
Dame Anna	Dark Ages	1
Dame Josephine	Dark Ages	1
Dame Molly	Dark Ages	1
Dame Natalie	Dark Ages	1
Dame Sylvia	Dark Ages	1
Sir Bailey	Dark Ages	1
Sir Destry	Dark Ages	1
Sir Martin	Dark Ages	1
Sir Michael	Dark Ages	1
Sir Vander	Dark Ages	1
Candlestick Maker	Guilds	10
Stonemason	Guilds	10
Doctor	Guilds	10
Masterpiece	Guilds	10
Advisor	Guilds	10
Plaza	Guilds	10
Taxman	Guilds	10
Herald	Guilds	10
Baker	Guilds	10
Butcher	Guilds	10
Journeyman	Guilds	10
Merchant Guild	Guilds	10
Soothsayer	Guilds	10
Port	Adventures	10
Coin of the Realm	Adventures	10
Ratcatcher	Adventures	10
Raze	Adventures	10
Amulet	Adventures	10
Caravan Guard	Adventures	10
Dungeon	Adventures	10
Gear	Adventures	10
Guide	Adventures	10
Duplicate	Adventures	10
Magpie	Adventures	10
Messenger	Adventures	10
Miser	Adventures	10
Ranger	Adventures	10
Transmogrify	Adventures	10
Artificer	Adventures	10
Bridge Troll	Adventures	10
Distant Lands	Adventures	12
Giant	Adventures	10
Haunted Woods	Adventures	10
Lost City	Adventures	10
Relic	Adventures	10
Royal Carriage	Adventures	10
Storyteller	Adventures	10
Swamp Hag	Adventures	10
Treasure Trove	Adventures	10
Wine Merchant	Adventures	10
Hireling	Adventures	10
Page	Adventures	10
Treasure Hunter	Adventures	5
Warrior	Adventures	5
Hero	Adventures	5
Champion	Adventures	5
Peasant	Adventures	10
Soldier	Adventures	5
Fugitive	Adventures	5
Disciple	Adventures	5
Teacher	Adventures	5
Engineer	Empires	10
City Quarter	Empires	10
Overlord	Empires	10
Royal Blacksmith	Empires	10
Encampment	Empires	5
Plunder	Empires	5
Patrician	Empires	5
Emporium	Empires	5
Settlers	Empires	5
Bustling Village	Empires	5
Catapult	Empires	5
Rocks	Empires	5
Chariot Race	Empires	10
Enchantress	Empires	10
Farmers' Market	Empires	10
Gladiator	Empires	5
Fortune	Empires	5
Sacrifice	Empires	10
Temple	Empires	10
Villa	Empires	10
Archive	Empires	10
Capital	Empires	10
Charm	Empires	10
Crown	Empires	10
Forum	Empires	10
Groundskeeper	Empires	10
Legionary	Empires	10
Wild Hunt	Empires	10
Humble Castle	Empires	1
Crumbling Castle	Empires	1
Small Castle	Empires	1
Haunted Castle	Empires	1
Opulent Castle	Empires	1
Sprawling Castle	Empires	1
Grand Castle	Empires	1
King's Castle	Empires	1
Druid	Nocturne	10
Faithful Hound	Nocturne	10
Guardian	Nocturne	10
Monastery	Nocturne	10
Pixie	Nocturne	10
Tracker	Nocturne	10
Changeling	Nocturne	10
Fool	Nocturne	10
Ghost Town	Nocturne	10
Leprechaun	Nocturne	10
Night Watchman	Nocturne	10
Secret Cave	Nocturne	10
Bard	Nocturne	10
Blessed Village	Nocturne	10
Cemetery	Nocturne	12
Conclave	Nocturne	10
Devil's Workshop	Nocturne	10
Exorcist	Nocturne	10
Necromancer	Nocturne	10
Shepherd	Nocturne	10
Skulk	Nocturne	10
Cobbler	Nocturne	10
Crypt	Nocturne	10
Cursed Village	Nocturne	10
Den of Sin	Nocturne	10
Idol	Nocturne	10
Pooka	Nocturne	10
Sacred Grove	Nocturne	10
Tormentor	Nocturne	10
Tragic Hero	Nocturne	10
Vampire	Nocturne	10
Werewolf	Nocturne	10
Raider	Nocturne	10
Haunted Mirror	Nocturne	6
Magic Lamp	Nocturne	6
Goat	Nocturne	6
Pasture	Nocturne	6
Pouch	Nocturne	6
Cursed Gold	Nocturne	6
Lucky Coin	Nocturne	6
Will-o'-Wisp	Nocturne	12
Wish	Nocturne	12
Bat	Nocturne	10
Imp	Nocturne	13
Zombie Apprentice	Nocturne	1
Zombie Mason	Nocturne	1
Zombie Spy	Nocturne	1
Ghost	Nocturne	6
Border Guard	Renaissance	10
Ducat	Renaissance	10
Lackeys	Renaissance	10
Acting Troupe	Renaissance	10
Cargo Ship	Renaissance	10
Experiment	Renaissance	10
Improve	Renaissance	10
Flag Bearer	Renaissance	10
Hideout	Renaissance	10
Inventor	Renaissance	10
Mountain Village	Renaissance	10
Patron	Renaissance	10
Priest	Renaissance	10
Research	Renaissance	10
Silk Merchant	Renaissance	10
Old Witch	Renaissance	10
Recruiter	Renaissance	10
Scepter	Renaissance	10
Scholar	Renaissance	10
Sculptor	Renaissance	10
Seer	Renaissance	10
Spices	Renaissance	10
Swashbuckler	Renaissance	10
Treasurer	Renaissance	10
Villain	Renaissance	10
Black Cat	Menagerie	10
Sleigh	Menagerie	10
Supplies	Menagerie	10
Camel Train	Menagerie	10
Goatherd	Menagerie	10
Scrap	Menagerie	10
Sheepdog	Menagerie	10
Snowy Village	Menagerie	10
Stockpile	Menagerie	10
Bounty Hunter	Menagerie	10
Cardinal	Menagerie	10
Cavalry	Menagerie	10
Groom	Menagerie	10
Hostelry	Menagerie	10
Village Green	Menagerie	10
Barge	Menagerie	10
Coven	Menagerie	10
Displace	Menagerie	10
Falconer	Menagerie	10
Gatekeeper	Menagerie	10
Hunting Lodge	Menagerie	10
Kiln	Menagerie	10
Livery	Menagerie	10
Mastermind	Menagerie	10
Paddock	Menagerie	10
Sanctuary	Menagerie	10
Fisherman	Menagerie	10
Destrier	Menagerie	10
Wayfarer	Menagerie	10
Animal Fair	Menagerie	10
Horse	Menagerie	30'''

HORIZONTAL_ALL_CARDS_STRING = '''Alms	Adventures
Borrow	Adventures
Quest	Adventures
Save	Adventures
Scouting Party	Adventures
Travelling Fair	Adventures
Bonfire	Adventures
Expedition	Adventures
Ferry	Adventures
Plan	Adventures
Mission	Adventures
Pilgrimage	Adventures
Ball	Adventures
Raid	Adventures
Seaway	Adventures
Trade	Adventures
Lost Arts	Adventures
Training	Adventures
Inheritance	Adventures
Pathfinding	Adventures
Triumph	Empires
Annex	Empires
Donate	Empires
Advance	Empires
Delve	Empires
Tax	Empires
Banquet	Empires
Ritual	Empires
Salt the Earth	Empires
Wedding	Empires
Windfall	Empires
Conquest	Empires
Dominate	Empires
Aqueduct	Empires
Arena	Empires
Bandit Fort	Empires
Basilica	Empires
Baths	Empires
Battlefield	Empires
Colonnade	Empires
Defiled Shrine	Empires
Fountain	Empires
Keep	Empires
Labyrinth	Empires
Mountain Pass	Empires
Museum	Empires
Obelisk	Empires
Orchard	Empires
Palace	Empires
Tomb	Empires
Tower	Empires
Triumphal Arch	Empires
Wall	Empires
Wolf Den	Empires
The Earth's Gift	Nocturne
The Field's Gift	Nocturne
The Flame's Gift	Nocturne
The Forest's Gift	Nocturne
The Moon's Gift	Nocturne
The Mountain's Gift	Nocturne
The River's Gift	Nocturne
The Sea's Gift	Nocturne
The Sky's Gift	Nocturne
The Sun's Gift	Nocturne
The Swamp's Gift	Nocturne
The Wind's Gift	Nocturne
Bad Omens	Nocturne
Delusion	Nocturne
Envy	Nocturne
Famine	Nocturne
Fear	Nocturne
Greed	Nocturne
Haunting	Nocturne
Locusts	Nocturne
Misery	Nocturne
Plague	Nocturne
Poverty	Nocturne
War	Nocturne
Cathedral	Renaissance
City Gate	Renaissance
Pageant	Renaissance
Sewers	Renaissance
Star Chart	Renaissance
Exploration	Renaissance
Fair	Renaissance
Silos	Renaissance
Sinister Plot	Renaissance
Academy	Renaissance
Capitalism	Renaissance
Fleet	Renaissance
Guildhall	Renaissance
Piazza	Renaissance
Road Network	Renaissance
Barracks	Renaissance
Crop Rotation	Renaissance
Innovation	Renaissance
Canal	Renaissance
Citadel	Renaissance
Delay	Menagerie
Desperation	Menagerie
Gamble	Menagerie
Pursue	Menagerie
Ride	Menagerie
Toil	Menagerie
Enhance	Menagerie
March	Menagerie
Transport	Menagerie
Banish	Menagerie
Bargain	Menagerie
Invest	Menagerie
Seize the Day	Menagerie
Commerce	Menagerie
Demand	Menagerie
Stampede	Menagerie
Reap	Menagerie
Enclave	Menagerie
Alliance	Menagerie
Populate	Menagerie
Way of the Butterfly	Menagerie
Way of the Camel	Menagerie
Way of the Chameleon	Menagerie
Way of the Frog	Menagerie
Way of the Goat	Menagerie
Way of the Horse	Menagerie
Way of the Mole	Menagerie
Way of the Monkey	Menagerie
Way of the Mouse	Menagerie
Way of the Mule	Menagerie
Way of the Otter	Menagerie
Way of the Owl	Menagerie
Way of the Ox	Menagerie
Way of the Pig	Menagerie
Way of the Rat	Menagerie
Way of the Seal	Menagerie
Way of the Sheep	Menagerie
Way of the Squirrel	Menagerie
Way of the Turtle	Menagerie
Way of the Worm	Menagerie
Summon	Promo'''

# Obtain card images via
# wget -r -np http://wiki.dominionstrategy.com/images/
# (You can probably do something smart with filtering ('-R'), but I'm dumb and didn't)

is_card_used = {}
for l in HORIZONTAL_ALL_CARDS_STRING.split('\n'):
    name, expansion = l.split('\t')
    is_card_used[name] = False

card_data = []
for l in ALL_CARDS_STRING.split('\n'):
    name, expansion, num = l.split('\t')
    card_data.append((name, expansion, int(num)))

horizontal_card_data = []
for l in HORIZONTAL_ALL_CARDS_STRING.split('\n'):
    horizontal_card_data.append(tuple(l.split('\t')))
    
def crawl(root_dir, dest_dir):
    for root, dirs, files in os.walk(root_dir):
        for name in files:
            try:
                no_suffix, suffix = name.split('.')
                if suffix not in ('jpg', 'png'):
                    continue
                for card_name in is_card_used:
                    formatted_name = card_name.replace(' ', '_')
                    if formatted_name+'Digital' == no_suffix:
                        shutil.copy(os.path.join(root, name), os.path.join(dest_dir, name))
                        is_card_used[card_name] = True
            except Exception as e:
                print(name, 'failed because', e)
    for card_name, used in is_card_used.items():
        if not used:
            print(card_name, 'was not used')

def calculate_sizes(directory):
    min_width, max_width = float('inf'), 0
    min_height, max_height = float('inf'), 0
    for filename in os.listdir(directory):
        try:
            im = Image.open(os.path.join(directory, filename))
            width, height = im.size
            min_width, max_width = min(min_width, width), max(max_width, width)
            min_height, max_height = min(min_height, height), max(max_height, height)
        except: # not an image file
            pass
    print(min_width, max_width, min_height, max_height)
    # prints 

def canonicalize_images(inputs, outputs):
    for root, dirs, files in os.walk(inputs):
        for name in files:
            try:
                im = Image.open(os.path.join(inputs, name))
                new_file_name = os.path.join(outputs, name.replace('Digital', ''))
                im.resize((IM_WIDTH, IM_HEIGHT)).save(new_file_name)
            except Exception as e:
                print(name, 'failed because', e)

def calculate_average(canon_images, expansion, weighted, output):
    total = 0
    res = numpy.zeros((IM_HEIGHT, IM_WIDTH, 3), dtype='float')
    for name, exp, count in card_data:
        if expansion == 'All' or exp == expansion:
            im = Image.open(os.path.join(canon_images, name.replace(' ', '_')+'.jpg'))
            numpy_im = numpy.array(im, dtype='float')
            if weighted:
                res += numpy_im*count
                total += count
            else:
                res += numpy_im
                total += 1
    if total != 0:
        res /= total
        Image.fromarray(numpy.round(res).astype('uint8'), 'RGB').save(os.path.join(
            output, expansion+('weighted' if weighted else 'unweighted')+'.jpg'))

            

crawl('/Users/jennahimawan/Downloads/big-ims', '/Users/jennahimawan/Downloads/vertical')
calculate_sizes('/Users/jennahimawan/Downloads/vertical')
canonicalize_images('/Users/jennahimawan/Downloads/vertical', '/Users/jennahimawan/Downloads/vertical-canon')

for exp in ('Adventures', 'Alchemy', 'All', 'Base', 'Cornucopia', 'Dark Ages', 'Empires',
        'Guilds', 'Hinterlands', 'Intrigue', 'Menagerie', 'Nocturne', 'Promo', 'Prosperity',
        'Renaissance', 'Seaside'):
    for weighted in (True, False):
        calculate_average('/Users/jennahimawan/Downloads/vertical-canon',
                exp, weighted, '/Users/jennahimawan/Downloads/outputs')


crawl('/Users/jennahimawan/Downloads/big-ims', '/Users/jennahimawan/Downloads/horizontal')
calculate_sizes('/Users/jennahimawan/Downloads/horizontal')
canonicalize_images('/Users/jennahimawan/Downloads/horizontal', '/Users/jennahimawan/Downloads/horizontal-canon')

for exp in ('Adventures', 'Alchemy', 'All', 'Base', 'Cornucopia', 'Dark Ages', 'Empires',
        'Guilds', 'Hinterlands', 'Intrigue', 'Menagerie', 'Nocturne', 'Promo', 'Prosperity',
        'Renaissance', 'Seaside'):
    calculate_average('/Users/jennahimawan/Downloads/horizontal-canon',
            exp, False, '/Users/jennahimawan/Downloads/horizontal-outputs')
