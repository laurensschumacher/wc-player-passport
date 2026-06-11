"""
350 candidate players believed to have appeared in at least 2 World Cups (2002–2026).
Each entry contains the player's name, nationality, position, and Transfermarkt profile URL.
The scraper will validate eligibility and correct any wrong IDs by flagging needs_manual_review.
"""

# fmt: off
CANDIDATES = [

    # ===== ARGENTINA =====
    {"name": "Lionel Messi",          "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "attacker",   "tm_slug": "lionel-messi",            "tm_id": 28003},
    {"name": "Sergio Aguero",         "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "attacker",   "tm_slug": "sergio-aguero",           "tm_id": 40778},
    {"name": "Gonzalo Higuain",       "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "attacker",   "tm_slug": "gonzalo-higuain",         "tm_id": 39153},
    {"name": "Carlos Tevez",          "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "attacker",   "tm_slug": "carlos-tevez",            "tm_id": 33066},
    {"name": "Juan Roman Riquelme",   "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "midfielder", "tm_slug": "juan-roman-riquelme",     "tm_id": 13004},
    {"name": "Hernan Crespo",         "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "attacker",   "tm_slug": "hernan-crespo",           "tm_id": 3303},
    {"name": "Javier Zanetti",        "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "defender",   "tm_slug": "javier-zanetti",          "tm_id": 3330},
    {"name": "Javier Mascherano",     "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "midfielder", "tm_slug": "javier-mascherano",       "tm_id": 32298},
    {"name": "Walter Samuel",         "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "defender",   "tm_slug": "walter-samuel",           "tm_id": 11453},
    {"name": "Roberto Ayala",         "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "defender",   "tm_slug": "roberto-ayala",           "tm_id": 11298},
    {"name": "Juan Sebastian Veron",  "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "midfielder", "tm_slug": "juan-sebastian-veron",    "tm_id": 3665},
    {"name": "Angel Di Maria",        "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "midfielder", "tm_slug": "angel-di-maria",          "tm_id": 84619},
    {"name": "Ezequiel Lavezzi",      "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "attacker",   "tm_slug": "ezequiel-lavezzi",        "tm_id": 54949},
    {"name": "Pablo Zabaleta",        "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "defender",   "tm_slug": "pablo-zabaleta",          "tm_id": 59940},
    {"name": "Nicolas Otamendi",      "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "defender",   "tm_slug": "nicolas-otamendi",        "tm_id": 121781},
    {"name": "Marcos Rojo",           "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "defender",   "tm_slug": "marcos-rojo",             "tm_id": 170765},
    {"name": "Ever Banega",           "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "midfielder", "tm_slug": "ever-banega",             "tm_id": 56680},
    {"name": "Lucas Biglia",          "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "midfielder", "tm_slug": "lucas-biglia",            "tm_id": 49296},
    {"name": "Emiliano Martinez",     "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "gk",         "tm_slug": "emiliano-martinez",       "tm_id": 161953},
    {"name": "Rodrigo De Paul",       "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "midfielder", "tm_slug": "rodrigo-de-paul",         "tm_id": 186942},
    {"name": "Julian Alvarez",        "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "attacker",   "tm_slug": "julian-alvarez",          "tm_id": 478553},
    {"name": "Lautaro Martinez",      "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "attacker",   "tm_slug": "lautaro-martinez",        "tm_id": 406625},
    {"name": "Enzo Fernandez",        "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "midfielder", "tm_slug": "enzo-fernandez",          "tm_id": 781892},
    {"name": "Maxi Rodriguez",        "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "midfielder", "tm_slug": "maxi-rodriguez",          "tm_id": 13085},
    {"name": "German Pezzella",       "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "defender",   "tm_slug": "german-pezzella",         "tm_id": 174847},

    # ===== BRAZIL =====
    {"name": "Ronaldo Nazario",       "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "attacker",   "tm_slug": "ronaldo",                 "tm_id": 3140},
    {"name": "Ronaldinho",            "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "attacker",   "tm_slug": "ronaldinho",              "tm_id": 3659},
    {"name": "Cafu",                  "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "defender",   "tm_slug": "cafu",                    "tm_id": 3266},
    {"name": "Roberto Carlos",        "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "defender",   "tm_slug": "roberto-carlos",          "tm_id": 3127},
    {"name": "Kaka",                  "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "midfielder", "tm_slug": "kaka",                    "tm_id": 4940},
    {"name": "Adriano",               "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "attacker",   "tm_slug": "adriano",                 "tm_id": 6482},
    {"name": "Robinho",               "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "attacker",   "tm_slug": "robinho",                 "tm_id": 8205},
    {"name": "Hulk",                  "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "attacker",   "tm_slug": "hulk",                    "tm_id": 39369},
    {"name": "Oscar",                 "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "midfielder", "tm_slug": "oscar",                   "tm_id": 170803},
    {"name": "Neymar",                "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "attacker",   "tm_slug": "neymar",                  "tm_id": 68290},
    {"name": "Thiago Silva",          "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "defender",   "tm_slug": "thiago-silva",            "tm_id": 34408},
    {"name": "David Luiz",            "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "defender",   "tm_slug": "david-luiz",              "tm_id": 106959},
    {"name": "Marcelo",               "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "defender",   "tm_slug": "marcelo",                 "tm_id": 57100},
    {"name": "Dani Alves",            "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "defender",   "tm_slug": "dani-alves",              "tm_id": 31071},
    {"name": "Alisson",               "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "gk",         "tm_slug": "alisson",                 "tm_id": 105470},
    {"name": "Casemiro",              "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "midfielder", "tm_slug": "casemiro",                "tm_id": 199530},
    {"name": "Philippe Coutinho",     "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "midfielder", "tm_slug": "philippe-coutinho",       "tm_id": 120616},
    {"name": "Vinicius Junior",       "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "attacker",   "tm_slug": "vinicius-junior",         "tm_id": 371998},
    {"name": "Richarlison",           "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "attacker",   "tm_slug": "richarlison",             "tm_id": 387168},
    {"name": "Rodrygo",               "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "attacker",   "tm_slug": "rodrygo",                 "tm_id": 412363},
    {"name": "Lucas Paqueta",         "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "midfielder", "tm_slug": "lucas-paqueta",           "tm_id": 432957},
    {"name": "Fernandinho",           "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "midfielder", "tm_slug": "fernandinho",             "tm_id": 65743},
    {"name": "Julio Cesar",           "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "gk",         "tm_slug": "julio-cesar",             "tm_id": 13636},
    {"name": "Ramires",               "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "midfielder", "tm_slug": "ramires",                 "tm_id": 88748},
    {"name": "Elano",                 "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "midfielder", "tm_slug": "elano",                   "tm_id": 21066},

    # ===== GERMANY =====
    {"name": "Miroslav Klose",        "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "attacker",   "tm_slug": "miroslav-klose",          "tm_id": 8528},
    {"name": "Michael Ballack",       "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "midfielder", "tm_slug": "michael-ballack",         "tm_id": 2897},
    {"name": "Philipp Lahm",          "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "defender",   "tm_slug": "philipp-lahm",            "tm_id": 26253},
    {"name": "Bastian Schweinsteiger","nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "midfielder", "tm_slug": "bastian-schweinsteiger",  "tm_id": 26589},
    {"name": "Lukas Podolski",        "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "attacker",   "tm_slug": "lukas-podolski",          "tm_id": 20951},
    {"name": "Thomas Muller",         "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "attacker",   "tm_slug": "thomas-muller",           "tm_id": 58358},
    {"name": "Manuel Neuer",          "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "gk",         "tm_slug": "manuel-neuer",            "tm_id": 17259},
    {"name": "Toni Kroos",            "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "midfielder", "tm_slug": "toni-kroos",              "tm_id": 100436},
    {"name": "Mesut Ozil",            "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "midfielder", "tm_slug": "mesut-oezil",             "tm_id": 73627},
    {"name": "Mats Hummels",          "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "defender",   "tm_slug": "mats-hummels",            "tm_id": 59996},
    {"name": "Jerome Boateng",        "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "defender",   "tm_slug": "jerome-boateng",          "tm_id": 105432},
    {"name": "Sami Khedira",          "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "midfielder", "tm_slug": "sami-khedira",            "tm_id": 79499},
    {"name": "Per Mertesacker",       "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "defender",   "tm_slug": "per-mertesacker",         "tm_id": 42793},
    {"name": "Mario Gomez",           "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "attacker",   "tm_slug": "mario-gomez",             "tm_id": 68780},
    {"name": "Oliver Kahn",           "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "gk",         "tm_slug": "oliver-kahn",             "tm_id": 1891},
    {"name": "Jens Lehmann",          "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "gk",         "tm_slug": "jens-lehmann",            "tm_id": 4706},
    {"name": "Joshua Kimmich",        "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "midfielder", "tm_slug": "joshua-kimmich",          "tm_id": 161056},
    {"name": "Ilkay Gundogan",        "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "midfielder", "tm_slug": "ilkay-guendogan",         "tm_id": 93463},
    {"name": "Leroy Sane",            "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "attacker",   "tm_slug": "leroy-sane",              "tm_id": 232461},
    {"name": "Serge Gnabry",          "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "attacker",   "tm_slug": "serge-gnabry",            "tm_id": 160644},
    {"name": "Kai Havertz",           "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "attacker",   "tm_slug": "kai-havertz",             "tm_id": 402006},
    {"name": "Florian Wirtz",         "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "midfielder", "tm_slug": "florian-wirtz",           "tm_id": 521361},
    {"name": "Jamal Musiala",         "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "midfielder", "tm_slug": "jamal-musiala",           "tm_id": 580195},
    {"name": "Antonio Rudiger",       "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "defender",   "tm_slug": "antonio-rudiger",         "tm_id": 241694},
    {"name": "Marc-Andre ter Stegen", "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "gk",         "tm_slug": "marc-andre-ter-stegen",   "tm_id": 74070},

    # ===== SPAIN =====
    {"name": "Iker Casillas",         "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "gk",         "tm_slug": "iker-casillas",           "tm_id": 3371},
    {"name": "David Villa",           "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "attacker",   "tm_slug": "david-villa",             "tm_id": 17780},
    {"name": "Fernando Torres",       "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "attacker",   "tm_slug": "fernando-torres",         "tm_id": 36956},
    {"name": "Xavi Hernandez",        "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "midfielder", "tm_slug": "xavi",                    "tm_id": 3661},
    {"name": "Andres Iniesta",        "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "midfielder", "tm_slug": "andres-iniesta",          "tm_id": 6399},
    {"name": "Carles Puyol",          "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "defender",   "tm_slug": "carles-puyol",            "tm_id": 3365},
    {"name": "Gerard Pique",          "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "defender",   "tm_slug": "gerard-pique",            "tm_id": 103823},
    {"name": "Sergio Ramos",          "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "defender",   "tm_slug": "sergio-ramos",            "tm_id": 25557},
    {"name": "Cesc Fabregas",         "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "midfielder", "tm_slug": "cesc-fabregas",           "tm_id": 44297},
    {"name": "Xabi Alonso",           "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "midfielder", "tm_slug": "xabi-alonso",             "tm_id": 8203},
    {"name": "David Silva",           "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "midfielder", "tm_slug": "david-silva",             "tm_id": 36275},
    {"name": "Juan Mata",             "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "midfielder", "tm_slug": "juan-mata",               "tm_id": 100543},
    {"name": "Alvaro Morata",         "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "attacker",   "tm_slug": "alvaro-morata",           "tm_id": 161947},
    {"name": "Pedri",                 "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "midfielder", "tm_slug": "pedri",                   "tm_id": 547179},
    {"name": "Gavi",                  "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "midfielder", "tm_slug": "gavi",                    "tm_id": 557782},
    {"name": "Ferran Torres",         "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "attacker",   "tm_slug": "ferran-torres",           "tm_id": 401181},
    {"name": "Rodri",                 "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "midfielder", "tm_slug": "rodri",                   "tm_id": 357565},
    {"name": "Dani Carvajal",         "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "defender",   "tm_slug": "dani-carvajal",           "tm_id": 138927},
    {"name": "Jordi Alba",            "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "defender",   "tm_slug": "jordi-alba",              "tm_id": 69844},
    {"name": "Raul",                  "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "attacker",   "tm_slug": "raul",                    "tm_id": 3519},
    {"name": "Fernando Hierro",       "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "defender",   "tm_slug": "fernando-hierro",         "tm_id": 3439},
    {"name": "Joseba Etxeberria",     "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "attacker",   "tm_slug": "joseba-etxeberria",       "tm_id": 6671},
    {"name": "Victor Valdes",         "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "gk",         "tm_slug": "victor-valdes",           "tm_id": 19499},
    {"name": "Joan Capdevila",        "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "defender",   "tm_slug": "joan-capdevila",          "tm_id": 7267},
    {"name": "Marcos Senna",          "nationality": "Spain", "code": "ESP", "flag": "🇪🇸", "position": "midfielder", "tm_slug": "marcos-senna",            "tm_id": 6453},

    # ===== FRANCE =====
    {"name": "Thierry Henry",         "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "attacker",   "tm_slug": "thierry-henry",           "tm_id": 18096},
    {"name": "Zinedine Zidane",       "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "midfielder", "tm_slug": "zinedine-zidane",         "tm_id": 3469},
    {"name": "Patrick Vieira",        "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "midfielder", "tm_slug": "patrick-vieira",          "tm_id": 3340},
    {"name": "Robert Pires",          "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "midfielder", "tm_slug": "robert-pires",            "tm_id": 4742},
    {"name": "David Trezeguet",       "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "attacker",   "tm_slug": "david-trezeguet",         "tm_id": 3380},
    {"name": "Franck Ribery",         "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "attacker",   "tm_slug": "franck-ribery",           "tm_id": 15963},
    {"name": "Nicolas Anelka",        "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "attacker",   "tm_slug": "nicolas-anelka",          "tm_id": 1444},
    {"name": "Karim Benzema",         "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "attacker",   "tm_slug": "karim-benzema",           "tm_id": 18921},
    {"name": "Hugo Lloris",           "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "gk",         "tm_slug": "hugo-lloris",             "tm_id": 42501},
    {"name": "Raphael Varane",        "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "defender",   "tm_slug": "raphael-varane",          "tm_id": 139813},
    {"name": "Paul Pogba",            "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "midfielder", "tm_slug": "paul-pogba",              "tm_id": 193017},
    {"name": "Kylian Mbappe",         "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "attacker",   "tm_slug": "kylian-mbappe",           "tm_id": 342229},
    {"name": "Antoine Griezmann",     "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "attacker",   "tm_slug": "antoine-griezmann",       "tm_id": 125022},
    {"name": "Ousmane Dembele",       "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "attacker",   "tm_slug": "ousmane-dembele",         "tm_id": 300904},
    {"name": "Olivier Giroud",        "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "attacker",   "tm_slug": "olivier-giroud",          "tm_id": 82716},
    {"name": "N'Golo Kante",          "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "midfielder", "tm_slug": "ngolo-kante",             "tm_id": 201022},
    {"name": "Lucas Hernandez",       "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "defender",   "tm_slug": "lucas-hernandez",         "tm_id": 376192},
    {"name": "Aurelien Tchouameni",   "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "midfielder", "tm_slug": "aurelien-tchouameni",     "tm_id": 483310},
    {"name": "Eduardo Camavinga",     "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "midfielder", "tm_slug": "eduardo-camavinga",       "tm_id": 502751},
    {"name": "William Gallas",        "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "defender",   "tm_slug": "william-gallas",          "tm_id": 16818},

    # ===== PORTUGAL =====
    {"name": "Cristiano Ronaldo",     "nationality": "Portugal", "code": "POR", "flag": "🇵🇹", "position": "attacker",   "tm_slug": "cristiano-ronaldo",       "tm_id": 8198},
    {"name": "Luis Figo",             "nationality": "Portugal", "code": "POR", "flag": "🇵🇹", "position": "attacker",   "tm_slug": "luis-figo",               "tm_id": 3501},
    {"name": "Deco",                  "nationality": "Portugal", "code": "POR", "flag": "🇵🇹", "position": "midfielder", "tm_slug": "deco",                    "tm_id": 5399},
    {"name": "Maniche",               "nationality": "Portugal", "code": "POR", "flag": "🇵🇹", "position": "midfielder", "tm_slug": "maniche",                 "tm_id": 9228},
    {"name": "Simao Sabrosa",         "nationality": "Portugal", "code": "POR", "flag": "🇵🇹", "position": "attacker",   "tm_slug": "simao-sabrosa",           "tm_id": 6652},
    {"name": "Joao Moutinho",         "nationality": "Portugal", "code": "POR", "flag": "🇵🇹", "position": "midfielder", "tm_slug": "joao-moutinho",           "tm_id": 42652},
    {"name": "Pepe",                  "nationality": "Portugal", "code": "POR", "flag": "🇵🇹", "position": "defender",   "tm_slug": "pepe",                    "tm_id": 29218},
    {"name": "Nani",                  "nationality": "Portugal", "code": "POR", "flag": "🇵🇹", "position": "attacker",   "tm_slug": "nani",                    "tm_id": 74801},
    {"name": "Bruno Alves",           "nationality": "Portugal", "code": "POR", "flag": "🇵🇹", "position": "defender",   "tm_slug": "bruno-alves",             "tm_id": 77499},
    {"name": "Helder Postiga",        "nationality": "Portugal", "code": "POR", "flag": "🇵🇹", "position": "attacker",   "tm_slug": "helder-postiga",          "tm_id": 6680},
    {"name": "Joao Felix",            "nationality": "Portugal", "code": "POR", "flag": "🇵🇹", "position": "attacker",   "tm_slug": "joao-felix",              "tm_id": 345705},
    {"name": "Bernardo Silva",        "nationality": "Portugal", "code": "POR", "flag": "🇵🇹", "position": "midfielder", "tm_slug": "bernardo-silva",          "tm_id": 200471},
    {"name": "Diogo Jota",            "nationality": "Portugal", "code": "POR", "flag": "🇵🇹", "position": "attacker",   "tm_slug": "diogo-jota",              "tm_id": 283912},
    {"name": "Ruben Dias",            "nationality": "Portugal", "code": "POR", "flag": "🇵🇹", "position": "defender",   "tm_slug": "ruben-dias",              "tm_id": 321699},
    {"name": "Bruno Fernandes",       "nationality": "Portugal", "code": "POR", "flag": "🇵🇹", "position": "midfielder", "tm_slug": "bruno-fernandes",         "tm_id": 240306},

    # ===== NETHERLANDS =====
    {"name": "Ruud van Nistelrooy",   "nationality": "Netherlands", "code": "NED", "flag": "🇳🇱", "position": "attacker",   "tm_slug": "ruud-van-nistelrooy",     "tm_id": 7296},
    {"name": "Arjen Robben",          "nationality": "Netherlands", "code": "NED", "flag": "🇳🇱", "position": "attacker",   "tm_slug": "arjen-robben",            "tm_id": 18982},
    {"name": "Dirk Kuyt",             "nationality": "Netherlands", "code": "NED", "flag": "🇳🇱", "position": "attacker",   "tm_slug": "dirk-kuyt",               "tm_id": 26265},
    {"name": "Robin van Persie",      "nationality": "Netherlands", "code": "NED", "flag": "🇳🇱", "position": "attacker",   "tm_slug": "robin-van-persie",        "tm_id": 6448},
    {"name": "Wesley Sneijder",       "nationality": "Netherlands", "code": "NED", "flag": "🇳🇱", "position": "midfielder", "tm_slug": "wesley-sneijder",         "tm_id": 15937},
    {"name": "Mark van Bommel",       "nationality": "Netherlands", "code": "NED", "flag": "🇳🇱", "position": "midfielder", "tm_slug": "mark-van-bommel",         "tm_id": 21029},
    {"name": "Edwin van der Sar",     "nationality": "Netherlands", "code": "NED", "flag": "🇳🇱", "position": "gk",         "tm_slug": "edwin-van-der-sar",       "tm_id": 2526},
    {"name": "Virgil van Dijk",       "nationality": "Netherlands", "code": "NED", "flag": "🇳🇱", "position": "defender",   "tm_slug": "virgil-van-dijk",         "tm_id": 139208},
    {"name": "Memphis Depay",         "nationality": "Netherlands", "code": "NED", "flag": "🇳🇱", "position": "attacker",   "tm_slug": "memphis-depay",           "tm_id": 295241},
    {"name": "Frenkie de Jong",       "nationality": "Netherlands", "code": "NED", "flag": "🇳🇱", "position": "midfielder", "tm_slug": "frenkie-de-jong",         "tm_id": 384072},
    {"name": "Georginio Wijnaldum",   "nationality": "Netherlands", "code": "NED", "flag": "🇳🇱", "position": "midfielder", "tm_slug": "georginio-wijnaldum",     "tm_id": 147055},
    {"name": "Denzel Dumfries",       "nationality": "Netherlands", "code": "NED", "flag": "🇳🇱", "position": "defender",   "tm_slug": "denzel-dumfries",         "tm_id": 363040},

    # ===== ENGLAND =====
    {"name": "David Beckham",         "nationality": "England", "code": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "position": "midfielder", "tm_slug": "david-beckham",           "tm_id": 6722},
    {"name": "Wayne Rooney",          "nationality": "England", "code": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "position": "attacker",   "tm_slug": "wayne-rooney",            "tm_id": 9971},
    {"name": "Frank Lampard",         "nationality": "England", "code": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "position": "midfielder", "tm_slug": "frank-lampard",           "tm_id": 5952},
    {"name": "Steven Gerrard",        "nationality": "England", "code": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "position": "midfielder", "tm_slug": "steven-gerrard",          "tm_id": 5902},
    {"name": "Michael Owen",          "nationality": "England", "code": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "position": "attacker",   "tm_slug": "michael-owen",            "tm_id": 1452},
    {"name": "Ashley Cole",           "nationality": "England", "code": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "position": "defender",   "tm_slug": "ashley-cole",             "tm_id": 12310},
    {"name": "Rio Ferdinand",         "nationality": "England", "code": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "position": "defender",   "tm_slug": "rio-ferdinand",           "tm_id": 5965},
    {"name": "Peter Crouch",          "nationality": "England", "code": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "position": "attacker",   "tm_slug": "peter-crouch",            "tm_id": 6696},
    {"name": "Joe Cole",              "nationality": "England", "code": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "position": "midfielder", "tm_slug": "joe-cole",                "tm_id": 3895},
    {"name": "Harry Kane",            "nationality": "England", "code": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "position": "attacker",   "tm_slug": "harry-kane",              "tm_id": 132098},
    {"name": "Raheem Sterling",       "nationality": "England", "code": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "position": "attacker",   "tm_slug": "raheem-sterling",         "tm_id": 151114},
    {"name": "Marcus Rashford",       "nationality": "England", "code": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "position": "attacker",   "tm_slug": "marcus-rashford",         "tm_id": 258923},
    {"name": "Phil Foden",            "nationality": "England", "code": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "position": "midfielder", "tm_slug": "phil-foden",              "tm_id": 363770},
    {"name": "Jude Bellingham",       "nationality": "England", "code": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "position": "midfielder", "tm_slug": "jude-bellingham",         "tm_id": 505770},
    {"name": "Bukayo Saka",           "nationality": "England", "code": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "position": "attacker",   "tm_slug": "bukayo-saka",             "tm_id": 433177},

    # ===== ITALY =====
    {"name": "Gianluigi Buffon",      "nationality": "Italy", "code": "ITA", "flag": "🇮🇹", "position": "gk",         "tm_slug": "gianluigi-buffon",        "tm_id": 3836},
    {"name": "Fabio Cannavaro",       "nationality": "Italy", "code": "ITA", "flag": "🇮🇹", "position": "defender",   "tm_slug": "fabio-cannavaro",         "tm_id": 3655},
    {"name": "Andrea Pirlo",          "nationality": "Italy", "code": "ITA", "flag": "🇮🇹", "position": "midfielder", "tm_slug": "andrea-pirlo",            "tm_id": 3354},
    {"name": "Francesco Totti",       "nationality": "Italy", "code": "ITA", "flag": "🇮🇹", "position": "attacker",   "tm_slug": "francesco-totti",         "tm_id": 3470},
    {"name": "Alessandro Del Piero",  "nationality": "Italy", "code": "ITA", "flag": "🇮🇹", "position": "attacker",   "tm_slug": "alessandro-del-piero",    "tm_id": 3524},
    {"name": "Gianluca Zambrotta",    "nationality": "Italy", "code": "ITA", "flag": "🇮🇹", "position": "defender",   "tm_slug": "gianluca-zambrotta",      "tm_id": 6017},
    {"name": "Gennaro Gattuso",       "nationality": "Italy", "code": "ITA", "flag": "🇮🇹", "position": "midfielder", "tm_slug": "gennaro-gattuso",         "tm_id": 3360},
    {"name": "Luca Toni",             "nationality": "Italy", "code": "ITA", "flag": "🇮🇹", "position": "attacker",   "tm_slug": "luca-toni",               "tm_id": 30793},
    {"name": "Daniele De Rossi",      "nationality": "Italy", "code": "ITA", "flag": "🇮🇹", "position": "midfielder", "tm_slug": "daniele-de-rossi",        "tm_id": 89059},
    {"name": "Giorgio Chiellini",     "nationality": "Italy", "code": "ITA", "flag": "🇮🇹", "position": "defender",   "tm_slug": "giorgio-chiellini",       "tm_id": 83199},
    {"name": "Leonardo Bonucci",      "nationality": "Italy", "code": "ITA", "flag": "🇮🇹", "position": "defender",   "tm_slug": "leonardo-bonucci",        "tm_id": 87005},
    {"name": "Claudio Marchisio",     "nationality": "Italy", "code": "ITA", "flag": "🇮🇹", "position": "midfielder", "tm_slug": "claudio-marchisio",       "tm_id": 95730},
    {"name": "Mario Balotelli",       "nationality": "Italy", "code": "ITA", "flag": "🇮🇹", "position": "attacker",   "tm_slug": "mario-balotelli",         "tm_id": 97665},
    {"name": "Marco Verratti",        "nationality": "Italy", "code": "ITA", "flag": "🇮🇹", "position": "midfielder", "tm_slug": "marco-verratti",          "tm_id": 106941},
    {"name": "Federico Chiesa",       "nationality": "Italy", "code": "ITA", "flag": "🇮🇹", "position": "attacker",   "tm_slug": "federico-chiesa",         "tm_id": 341810},

    # ===== BELGIUM =====
    {"name": "Eden Hazard",           "nationality": "Belgium", "code": "BEL", "flag": "🇧🇪", "position": "attacker",   "tm_slug": "eden-hazard",             "tm_id": 50202},
    {"name": "Kevin De Bruyne",       "nationality": "Belgium", "code": "BEL", "flag": "🇧🇪", "position": "midfielder", "tm_slug": "kevin-de-bruyne",         "tm_id": 88755},
    {"name": "Romelu Lukaku",         "nationality": "Belgium", "code": "BEL", "flag": "🇧🇪", "position": "attacker",   "tm_slug": "romelu-lukaku",           "tm_id": 166596},
    {"name": "Jan Vertonghen",        "nationality": "Belgium", "code": "BEL", "flag": "🇧🇪", "position": "defender",   "tm_slug": "jan-vertonghen",          "tm_id": 104592},
    {"name": "Toby Alderweireld",     "nationality": "Belgium", "code": "BEL", "flag": "🇧🇪", "position": "defender",   "tm_slug": "toby-alderweireld",       "tm_id": 104600},
    {"name": "Vincent Kompany",       "nationality": "Belgium", "code": "BEL", "flag": "🇧🇪", "position": "defender",   "tm_slug": "vincent-kompany",         "tm_id": 67667},
    {"name": "Axel Witsel",           "nationality": "Belgium", "code": "BEL", "flag": "🇧🇪", "position": "midfielder", "tm_slug": "axel-witsel",             "tm_id": 95160},
    {"name": "Dries Mertens",         "nationality": "Belgium", "code": "BEL", "flag": "🇧🇪", "position": "attacker",   "tm_slug": "dries-mertens",           "tm_id": 103621},
    {"name": "Nacer Chadli",          "nationality": "Belgium", "code": "BEL", "flag": "🇧🇪", "position": "midfielder", "tm_slug": "nacer-chadli",            "tm_id": 133099},
    {"name": "Yannick Carrasco",      "nationality": "Belgium", "code": "BEL", "flag": "🇧🇪", "position": "attacker",   "tm_slug": "yannick-carrasco",        "tm_id": 261465},
    {"name": "Thibaut Courtois",      "nationality": "Belgium", "code": "BEL", "flag": "🇧🇪", "position": "gk",         "tm_slug": "thibaut-courtois",        "tm_id": 153487},
    {"name": "Moussa Dembele",        "nationality": "Belgium", "code": "BEL", "flag": "🇧🇪", "position": "midfielder", "tm_slug": "moussa-dembele",          "tm_id": 115882},

    # ===== URUGUAY =====
    {"name": "Diego Forlan",          "nationality": "Uruguay", "code": "URU", "flag": "🇺🇾", "position": "attacker",   "tm_slug": "diego-forlan",            "tm_id": 13059},
    {"name": "Luis Suarez",           "nationality": "Uruguay", "code": "URU", "flag": "🇺🇾", "position": "attacker",   "tm_slug": "luis-suarez",             "tm_id": 44352},
    {"name": "Edison Cavani",         "nationality": "Uruguay", "code": "URU", "flag": "🇺🇾", "position": "attacker",   "tm_slug": "edinson-cavani",          "tm_id": 84378},
    {"name": "Diego Godin",           "nationality": "Uruguay", "code": "URU", "flag": "🇺🇾", "position": "defender",   "tm_slug": "diego-godin",             "tm_id": 46059},
    {"name": "Maximiliano Pereira",   "nationality": "Uruguay", "code": "URU", "flag": "🇺🇾", "position": "defender",   "tm_slug": "maximiliano-pereira",     "tm_id": 82396},
    {"name": "Nicolas Lodeiro",       "nationality": "Uruguay", "code": "URU", "flag": "🇺🇾", "position": "midfielder", "tm_slug": "nicolas-lodeiro",         "tm_id": 74424},
    {"name": "Rodrigo Bentancur",     "nationality": "Uruguay", "code": "URU", "flag": "🇺🇾", "position": "midfielder", "tm_slug": "rodrigo-bentancur",       "tm_id": 405512},
    {"name": "Federico Valverde",     "nationality": "Uruguay", "code": "URU", "flag": "🇺🇾", "position": "midfielder", "tm_slug": "federico-valverde",       "tm_id": 374504},
    {"name": "Darwin Nunez",          "nationality": "Uruguay", "code": "URU", "flag": "🇺🇾", "position": "attacker",   "tm_slug": "darwin-nunez",            "tm_id": 528855},
    {"name": "Diego Lugano",          "nationality": "Uruguay", "code": "URU", "flag": "🇺🇾", "position": "defender",   "tm_slug": "diego-lugano",            "tm_id": 21462},

    # ===== CROATIA =====
    {"name": "Luka Modric",           "nationality": "Croatia", "code": "CRO", "flag": "🇭🇷", "position": "midfielder", "tm_slug": "luka-modric",             "tm_id": 27992},
    {"name": "Darijo Srna",           "nationality": "Croatia", "code": "CRO", "flag": "🇭🇷", "position": "defender",   "tm_slug": "darijo-srna",             "tm_id": 29677},
    {"name": "Ivan Rakitic",          "nationality": "Croatia", "code": "CRO", "flag": "🇭🇷", "position": "midfielder", "tm_slug": "ivan-rakitic",            "tm_id": 39680},
    {"name": "Mario Mandzukic",       "nationality": "Croatia", "code": "CRO", "flag": "🇭🇷", "position": "attacker",   "tm_slug": "mario-mandzukic",         "tm_id": 44395},
    {"name": "Ivan Perisic",          "nationality": "Croatia", "code": "CRO", "flag": "🇭🇷", "position": "attacker",   "tm_slug": "ivan-perisic",            "tm_id": 84753},
    {"name": "Mateo Kovacic",         "nationality": "Croatia", "code": "CRO", "flag": "🇭🇷", "position": "midfielder", "tm_slug": "mateo-kovacic",           "tm_id": 193218},
    {"name": "Marcelo Brozovic",      "nationality": "Croatia", "code": "CRO", "flag": "🇭🇷", "position": "midfielder", "tm_slug": "marcelo-brozovic",        "tm_id": 180442},
    {"name": "Dejan Lovren",          "nationality": "Croatia", "code": "CRO", "flag": "🇭🇷", "position": "defender",   "tm_slug": "dejan-lovren",            "tm_id": 100674},
    {"name": "Andrej Kramaric",       "nationality": "Croatia", "code": "CRO", "flag": "🇭🇷", "position": "attacker",   "tm_slug": "andrej-kramaric",         "tm_id": 211368},
    {"name": "Stipe Pletikosa",       "nationality": "Croatia", "code": "CRO", "flag": "🇭🇷", "position": "gk",         "tm_slug": "stipe-pletikosa",         "tm_id": 7427},
    {"name": "Ivica Olic",            "nationality": "Croatia", "code": "CRO", "flag": "🇭🇷", "position": "attacker",   "tm_slug": "ivica-olic",              "tm_id": 13063},
    {"name": "Josko Gvardiol",        "nationality": "Croatia", "code": "CRO", "flag": "🇭🇷", "position": "defender",   "tm_slug": "josko-gvardiol",          "tm_id": 527025},

    # ===== MEXICO =====
    {"name": "Rafael Marquez",        "nationality": "Mexico", "code": "MEX", "flag": "🇲🇽", "position": "defender",   "tm_slug": "rafael-marquez",          "tm_id": 11369},
    {"name": "Guillermo Ochoa",       "nationality": "Mexico", "code": "MEX", "flag": "🇲🇽", "position": "gk",         "tm_slug": "guillermo-ochoa",         "tm_id": 103612},
    {"name": "Andres Guardado",       "nationality": "Mexico", "code": "MEX", "flag": "🇲🇽", "position": "midfielder", "tm_slug": "andres-guardado",         "tm_id": 95023},
    {"name": "Javier Hernandez",      "nationality": "Mexico", "code": "MEX", "flag": "🇲🇽", "position": "attacker",   "tm_slug": "javier-hernandez",        "tm_id": 64297},
    {"name": "Giovani Dos Santos",    "nationality": "Mexico", "code": "MEX", "flag": "🇲🇽", "position": "attacker",   "tm_slug": "giovani-dos-santos",      "tm_id": 97887},
    {"name": "Carlos Salcido",        "nationality": "Mexico", "code": "MEX", "flag": "🇲🇽", "position": "defender",   "tm_slug": "carlos-salcido",          "tm_id": 33748},
    {"name": "Miguel Layun",          "nationality": "Mexico", "code": "MEX", "flag": "🇲🇽", "position": "defender",   "tm_slug": "miguel-layun",            "tm_id": 222009},
    {"name": "Hirving Lozano",        "nationality": "Mexico", "code": "MEX", "flag": "🇲🇽", "position": "attacker",   "tm_slug": "hirving-lozano",          "tm_id": 317678},
    {"name": "Carlos Vela",           "nationality": "Mexico", "code": "MEX", "flag": "🇲🇽", "position": "attacker",   "tm_slug": "carlos-vela",             "tm_id": 34547},
    {"name": "Edson Alvarez",         "nationality": "Mexico", "code": "MEX", "flag": "🇲🇽", "position": "midfielder", "tm_slug": "edson-alvarez",           "tm_id": 368826},

    # ===== USA =====
    {"name": "Landon Donovan",        "nationality": "United States", "code": "USA", "flag": "🇺🇸", "position": "midfielder", "tm_slug": "landon-donovan",          "tm_id": 9009},
    {"name": "Clint Dempsey",         "nationality": "United States", "code": "USA", "flag": "🇺🇸", "position": "attacker",   "tm_slug": "clint-dempsey",           "tm_id": 63659},
    {"name": "Tim Howard",            "nationality": "United States", "code": "USA", "flag": "🇺🇸", "position": "gk",         "tm_slug": "tim-howard",              "tm_id": 12988},
    {"name": "DaMarcus Beasley",      "nationality": "United States", "code": "USA", "flag": "🇺🇸", "position": "midfielder", "tm_slug": "damarcus-beasley",        "tm_id": 28007},
    {"name": "Jozy Altidore",         "nationality": "United States", "code": "USA", "flag": "🇺🇸", "position": "attacker",   "tm_slug": "jozy-altidore",           "tm_id": 93553},
    {"name": "Michael Bradley",       "nationality": "United States", "code": "USA", "flag": "🇺🇸", "position": "midfielder", "tm_slug": "michael-bradley",         "tm_id": 80503},
    {"name": "Christian Pulisic",     "nationality": "United States", "code": "USA", "flag": "🇺🇸", "position": "attacker",   "tm_slug": "christian-pulisic",       "tm_id": 318574},
    {"name": "Weston McKennie",       "nationality": "United States", "code": "USA", "flag": "🇺🇸", "position": "midfielder", "tm_slug": "weston-mckennie",         "tm_id": 443070},
    {"name": "Tyler Adams",           "nationality": "United States", "code": "USA", "flag": "🇺🇸", "position": "midfielder", "tm_slug": "tyler-adams",             "tm_id": 415427},
    {"name": "Carlos Bocanegra",      "nationality": "United States", "code": "USA", "flag": "🇺🇸", "position": "defender",   "tm_slug": "carlos-bocanegra",        "tm_id": 11372},

    # ===== JAPAN =====
    {"name": "Shunsuke Nakamura",     "nationality": "Japan", "code": "JPN", "flag": "🇯🇵", "position": "midfielder", "tm_slug": "shunsuke-nakamura",       "tm_id": 17978},
    {"name": "Hidetoshi Nakata",      "nationality": "Japan", "code": "JPN", "flag": "🇯🇵", "position": "midfielder", "tm_slug": "hidetoshi-nakata",        "tm_id": 6630},
    {"name": "Keisuke Honda",         "nationality": "Japan", "code": "JPN", "flag": "🇯🇵", "position": "midfielder", "tm_slug": "keisuke-honda",           "tm_id": 67285},
    {"name": "Yuto Nagatomo",         "nationality": "Japan", "code": "JPN", "flag": "🇯🇵", "position": "defender",   "tm_slug": "yuto-nagatomo",           "tm_id": 61523},
    {"name": "Makoto Hasebe",         "nationality": "Japan", "code": "JPN", "flag": "🇯🇵", "position": "midfielder", "tm_slug": "makoto-hasebe",           "tm_id": 32283},
    {"name": "Shinji Kagawa",         "nationality": "Japan", "code": "JPN", "flag": "🇯🇵", "position": "midfielder", "tm_slug": "shinji-kagawa",           "tm_id": 63621},
    {"name": "Maya Yoshida",          "nationality": "Japan", "code": "JPN", "flag": "🇯🇵", "position": "defender",   "tm_slug": "maya-yoshida",            "tm_id": 93834},
    {"name": "Ritsu Doan",            "nationality": "Japan", "code": "JPN", "flag": "🇯🇵", "position": "attacker",   "tm_slug": "ritsu-doan",              "tm_id": 417358},
    {"name": "Takumi Minamino",       "nationality": "Japan", "code": "JPN", "flag": "🇯🇵", "position": "attacker",   "tm_slug": "takumi-minamino",         "tm_id": 329988},
    {"name": "Wataru Endo",           "nationality": "Japan", "code": "JPN", "flag": "🇯🇵", "position": "midfielder", "tm_slug": "wataru-endo",             "tm_id": 280085},

    # ===== SOUTH KOREA =====
    {"name": "Park Ji-sung",          "nationality": "South Korea", "code": "KOR", "flag": "🇰🇷", "position": "midfielder", "tm_slug": "park-ji-sung",            "tm_id": 18053},
    {"name": "Lee Young-pyo",         "nationality": "South Korea", "code": "KOR", "flag": "🇰🇷", "position": "defender",   "tm_slug": "lee-young-pyo",           "tm_id": 14738},
    {"name": "Ki Sung-yueng",         "nationality": "South Korea", "code": "KOR", "flag": "🇰🇷", "position": "midfielder", "tm_slug": "ki-sung-yueng",           "tm_id": 109948},
    {"name": "Park Chu-young",        "nationality": "South Korea", "code": "KOR", "flag": "🇰🇷", "position": "attacker",   "tm_slug": "park-chu-young",          "tm_id": 37891},
    {"name": "Son Heung-min",         "nationality": "South Korea", "code": "KOR", "flag": "🇰🇷", "position": "attacker",   "tm_slug": "son-heung-min",           "tm_id": 160318},
    {"name": "Lee Kang-in",           "nationality": "South Korea", "code": "KOR", "flag": "🇰🇷", "position": "midfielder", "tm_slug": "lee-kang-in",             "tm_id": 415432},
    {"name": "Hwang Hee-chan",         "nationality": "South Korea", "code": "KOR", "flag": "🇰🇷", "position": "attacker",   "tm_slug": "hwang-hee-chan",           "tm_id": 354892},
    {"name": "Cha Du-ri",             "nationality": "South Korea", "code": "KOR", "flag": "🇰🇷", "position": "defender",   "tm_slug": "cha-du-ri",               "tm_id": 10975},
    {"name": "Seol Ki-hyeon",         "nationality": "South Korea", "code": "KOR", "flag": "🇰🇷", "position": "attacker",   "tm_slug": "seol-ki-hyeon",           "tm_id": 8924},
    {"name": "Cho Gue-sung",          "nationality": "South Korea", "code": "KOR", "flag": "🇰🇷", "position": "attacker",   "tm_slug": "cho-gue-sung",            "tm_id": 603218},

    # ===== SENEGAL =====
    {"name": "El Hadji Diouf",        "nationality": "Senegal", "code": "SEN", "flag": "🇸🇳", "position": "attacker",   "tm_slug": "el-hadji-diouf",          "tm_id": 11392},
    {"name": "Aliou Cisse",           "nationality": "Senegal", "code": "SEN", "flag": "🇸🇳", "position": "midfielder", "tm_slug": "aliou-cisse",             "tm_id": 7014},
    {"name": "Sadio Mane",            "nationality": "Senegal", "code": "SEN", "flag": "🇸🇳", "position": "attacker",   "tm_slug": "sadio-mane",              "tm_id": 200512},
    {"name": "Kalidou Koulibaly",     "nationality": "Senegal", "code": "SEN", "flag": "🇸🇳", "position": "defender",   "tm_slug": "kalidou-koulibaly",       "tm_id": 173272},
    {"name": "Edouard Mendy",         "nationality": "Senegal", "code": "SEN", "flag": "🇸🇳", "position": "gk",         "tm_slug": "edouard-mendy",           "tm_id": 342245},
    {"name": "Idrissa Gueye",         "nationality": "Senegal", "code": "SEN", "flag": "🇸🇳", "position": "midfielder", "tm_slug": "idrissa-gueye",           "tm_id": 178572},
    {"name": "Ismaila Sarr",          "nationality": "Senegal", "code": "SEN", "flag": "🇸🇳", "position": "attacker",   "tm_slug": "ismaila-sarr",            "tm_id": 432353},
    {"name": "Khalilou Fadiga",       "nationality": "Senegal", "code": "SEN", "flag": "🇸🇳", "position": "midfielder", "tm_slug": "khalilou-fadiga",         "tm_id": 9061},

    # ===== GHANA =====
    {"name": "Asamoah Gyan",          "nationality": "Ghana", "code": "GHA", "flag": "🇬🇭", "position": "attacker",   "tm_slug": "asamoah-gyan",            "tm_id": 33541},
    {"name": "Michael Essien",        "nationality": "Ghana", "code": "GHA", "flag": "🇬🇭", "position": "midfielder", "tm_slug": "michael-essien",          "tm_id": 15278},
    {"name": "Stephen Appiah",        "nationality": "Ghana", "code": "GHA", "flag": "🇬🇭", "position": "midfielder", "tm_slug": "stephen-appiah",          "tm_id": 11391},
    {"name": "Sulley Muntari",        "nationality": "Ghana", "code": "GHA", "flag": "🇬🇭", "position": "midfielder", "tm_slug": "sulley-muntari",          "tm_id": 29462},
    {"name": "Andre Ayew",            "nationality": "Ghana", "code": "GHA", "flag": "🇬🇭", "position": "attacker",   "tm_slug": "andre-ayew",              "tm_id": 119662},
    {"name": "Jordan Ayew",           "nationality": "Ghana", "code": "GHA", "flag": "🇬🇭", "position": "attacker",   "tm_slug": "jordan-ayew",             "tm_id": 224802},
    {"name": "Richard Kingston",      "nationality": "Ghana", "code": "GHA", "flag": "🇬🇭", "position": "gk",         "tm_slug": "richard-kingston",        "tm_id": 24597},
    {"name": "John Mensah",           "nationality": "Ghana", "code": "GHA", "flag": "🇬🇭", "position": "defender",   "tm_slug": "john-mensah",             "tm_id": 13987},

    # ===== IVORY COAST =====
    {"name": "Didier Drogba",         "nationality": "Ivory Coast", "code": "CIV", "flag": "🇨🇮", "position": "attacker",   "tm_slug": "didier-drogba",           "tm_id": 25049},
    {"name": "Yaya Toure",            "nationality": "Ivory Coast", "code": "CIV", "flag": "🇨🇮", "position": "midfielder", "tm_slug": "yaya-toure",              "tm_id": 48801},
    {"name": "Kolo Toure",            "nationality": "Ivory Coast", "code": "CIV", "flag": "🇨🇮", "position": "defender",   "tm_slug": "kolo-toure",              "tm_id": 15693},
    {"name": "Didier Zokora",         "nationality": "Ivory Coast", "code": "CIV", "flag": "🇨🇮", "position": "midfielder", "tm_slug": "didier-zokora",           "tm_id": 37398},
    {"name": "Emmanuel Eboue",        "nationality": "Ivory Coast", "code": "CIV", "flag": "🇨🇮", "position": "defender",   "tm_slug": "emmanuel-eboue",          "tm_id": 39009},
    {"name": "Salomon Kalou",         "nationality": "Ivory Coast", "code": "CIV", "flag": "🇨🇮", "position": "attacker",   "tm_slug": "salomon-kalou",           "tm_id": 62785},
    {"name": "Franck Kessie",         "nationality": "Ivory Coast", "code": "CIV", "flag": "🇨🇮", "position": "midfielder", "tm_slug": "franck-kessie",           "tm_id": 397529},
    {"name": "Wilfried Bony",         "nationality": "Ivory Coast", "code": "CIV", "flag": "🇨🇮", "position": "attacker",   "tm_slug": "wilfried-bony",           "tm_id": 193669},

    # ===== NIGERIA =====
    {"name": "John Obi Mikel",        "nationality": "Nigeria", "code": "NGA", "flag": "🇳🇬", "position": "midfielder", "tm_slug": "john-obi-mikel",          "tm_id": 74298},
    {"name": "Nwankwo Kanu",          "nationality": "Nigeria", "code": "NGA", "flag": "🇳🇬", "position": "attacker",   "tm_slug": "nwankwo-kanu",            "tm_id": 9057},
    {"name": "Peter Odemwingie",      "nationality": "Nigeria", "code": "NGA", "flag": "🇳🇬", "position": "attacker",   "tm_slug": "peter-odemwingie",        "tm_id": 37438},
    {"name": "Ahmed Musa",            "nationality": "Nigeria", "code": "NGA", "flag": "🇳🇬", "position": "attacker",   "tm_slug": "ahmed-musa",              "tm_id": 107752},
    {"name": "Victor Moses",          "nationality": "Nigeria", "code": "NGA", "flag": "🇳🇬", "position": "attacker",   "tm_slug": "victor-moses",            "tm_id": 166153},
    {"name": "Joseph Yobo",           "nationality": "Nigeria", "code": "NGA", "flag": "🇳🇬", "position": "defender",   "tm_slug": "joseph-yobo",             "tm_id": 28483},
    {"name": "Alex Iwobi",            "nationality": "Nigeria", "code": "NGA", "flag": "🇳🇬", "position": "midfielder", "tm_slug": "alex-iwobi",              "tm_id": 340716},
    {"name": "Odion Ighalo",          "nationality": "Nigeria", "code": "NGA", "flag": "🇳🇬", "position": "attacker",   "tm_slug": "odion-ighalo",            "tm_id": 129659},

    # ===== SWITZERLAND =====
    {"name": "Xherdan Shaqiri",       "nationality": "Switzerland", "code": "SUI", "flag": "🇨🇭", "position": "attacker",   "tm_slug": "xherdan-shaqiri",         "tm_id": 152774},
    {"name": "Granit Xhaka",          "nationality": "Switzerland", "code": "SUI", "flag": "🇨🇭", "position": "midfielder", "tm_slug": "granit-xhaka",            "tm_id": 177681},
    {"name": "Yann Sommer",           "nationality": "Switzerland", "code": "SUI", "flag": "🇨🇭", "position": "gk",         "tm_slug": "yann-sommer",             "tm_id": 143081},
    {"name": "Stephan Lichtsteiner",  "nationality": "Switzerland", "code": "SUI", "flag": "🇨🇭", "position": "defender",   "tm_slug": "stephan-lichtsteiner",    "tm_id": 54751},
    {"name": "Valon Behrami",         "nationality": "Switzerland", "code": "SUI", "flag": "🇨🇭", "position": "midfielder", "tm_slug": "valon-behrami",           "tm_id": 38534},
    {"name": "Philippe Senderos",     "nationality": "Switzerland", "code": "SUI", "flag": "🇨🇭", "position": "defender",   "tm_slug": "philippe-senderos",       "tm_id": 55526},
    {"name": "Hakan Yakin",           "nationality": "Switzerland", "code": "SUI", "flag": "🇨🇭", "position": "midfielder", "tm_slug": "hakan-yakin",             "tm_id": 6651},
    {"name": "Manuel Akanji",         "nationality": "Switzerland", "code": "SUI", "flag": "🇨🇭", "position": "defender",   "tm_slug": "manuel-akanji",           "tm_id": 357825},

    # ===== POLAND =====
    {"name": "Robert Lewandowski",    "nationality": "Poland", "code": "POL", "flag": "🇵🇱", "position": "attacker",   "tm_slug": "robert-lewandowski",      "tm_id": 38253},
    {"name": "Jakub Blaszczykowski", "nationality": "Poland", "code": "POL", "flag": "🇵🇱", "position": "attacker",   "tm_slug": "jakub-blaszczykowski",    "tm_id": 64028},
    {"name": "Artur Boruc",           "nationality": "Poland", "code": "POL", "flag": "🇵🇱", "position": "gk",         "tm_slug": "artur-boruc",             "tm_id": 21434},
    {"name": "Wojciech Szczesny",     "nationality": "Poland", "code": "POL", "flag": "🇵🇱", "position": "gk",         "tm_slug": "wojciech-szczesny",       "tm_id": 125651},
    {"name": "Grzegorz Krychowiak",   "nationality": "Poland", "code": "POL", "flag": "🇵🇱", "position": "midfielder", "tm_slug": "grzegorz-krychowiak",     "tm_id": 174026},
    {"name": "Arkadiusz Milik",       "nationality": "Poland", "code": "POL", "flag": "🇵🇱", "position": "attacker",   "tm_slug": "arkadiusz-milik",         "tm_id": 250467},
    {"name": "Piotr Zielinski",       "nationality": "Poland", "code": "POL", "flag": "🇵🇱", "position": "midfielder", "tm_slug": "piotr-zielinski",         "tm_id": 245360},
    {"name": "Kamil Glik",            "nationality": "Poland", "code": "POL", "flag": "🇵🇱", "position": "defender",   "tm_slug": "kamil-glik",              "tm_id": 113208},

    # ===== COLOMBIA =====
    {"name": "Radamel Falcao",        "nationality": "Colombia", "code": "COL", "flag": "🇨🇴", "position": "attacker",   "tm_slug": "radamel-falcao",          "tm_id": 62685},
    {"name": "James Rodriguez",       "nationality": "Colombia", "code": "COL", "flag": "🇨🇴", "position": "midfielder", "tm_slug": "james-rodriguez",         "tm_id": 88103},
    {"name": "Juan Cuadrado",         "nationality": "Colombia", "code": "COL", "flag": "🇨🇴", "position": "midfielder", "tm_slug": "juan-cuadrado",           "tm_id": 104206},
    {"name": "Davinson Sanchez",      "nationality": "Colombia", "code": "COL", "flag": "🇨🇴", "position": "defender",   "tm_slug": "davinson-sanchez",        "tm_id": 371178},
    {"name": "Yerry Mina",            "nationality": "Colombia", "code": "COL", "flag": "🇨🇴", "position": "defender",   "tm_slug": "yerry-mina",              "tm_id": 265799},

    # ===== CZECH REPUBLIC =====
    {"name": "Pavel Nedved",          "nationality": "Czech Republic", "code": "CZE", "flag": "🇨🇿", "position": "midfielder", "tm_slug": "pavel-nedved",            "tm_id": 3455},
    {"name": "Tomas Rosicky",         "nationality": "Czech Republic", "code": "CZE", "flag": "🇨🇿", "position": "midfielder", "tm_slug": "tomas-rosicky",           "tm_id": 16547},
    {"name": "Jan Koller",            "nationality": "Czech Republic", "code": "CZE", "flag": "🇨🇿", "position": "attacker",   "tm_slug": "jan-koller",              "tm_id": 10490},
    {"name": "Petr Cech",             "nationality": "Czech Republic", "code": "CZE", "flag": "🇨🇿", "position": "gk",         "tm_slug": "petr-cech",               "tm_id": 55759},

    # ===== DENMARK =====
    {"name": "Jon Dahl Tomasson",     "nationality": "Denmark", "code": "DEN", "flag": "🇩🇰", "position": "attacker",   "tm_slug": "jon-dahl-tomasson",       "tm_id": 7293},
    {"name": "Nicklas Bendtner",      "nationality": "Denmark", "code": "DEN", "flag": "🇩🇰", "position": "attacker",   "tm_slug": "nicklas-bendtner",        "tm_id": 50858},
    {"name": "Christian Eriksen",     "nationality": "Denmark", "code": "DEN", "flag": "🇩🇰", "position": "midfielder", "tm_slug": "christian-eriksen",       "tm_id": 152674},
    {"name": "Pierre-Emile Hojbjerg", "nationality": "Denmark", "code": "DEN", "flag": "🇩🇰", "position": "midfielder", "tm_slug": "pierre-emile-hojbjerg",   "tm_id": 205425},
    {"name": "Simon Kjaer",           "nationality": "Denmark", "code": "DEN", "flag": "🇩🇰", "position": "defender",   "tm_slug": "simon-kjaer",             "tm_id": 120429},

    # ===== SWEDEN =====
    {"name": "Freddie Ljungberg",     "nationality": "Sweden", "code": "SWE", "flag": "🇸🇪", "position": "midfielder", "tm_slug": "freddie-ljungberg",       "tm_id": 4048},
    {"name": "Olof Mellberg",         "nationality": "Sweden", "code": "SWE", "flag": "🇸🇪", "position": "defender",   "tm_slug": "olof-mellberg",           "tm_id": 15053},
    {"name": "Zlatan Ibrahimovic",    "nationality": "Sweden", "code": "SWE", "flag": "🇸🇪", "position": "attacker",   "tm_slug": "zlatan-ibrahimovic",      "tm_id": 14927},
    {"name": "Victor Lindelof",       "nationality": "Sweden", "code": "SWE", "flag": "🇸🇪", "position": "defender",   "tm_slug": "victor-lindelof",         "tm_id": 253078},
    {"name": "Emil Forsberg",         "nationality": "Sweden", "code": "SWE", "flag": "🇸🇪", "position": "midfielder", "tm_slug": "emil-forsberg",           "tm_id": 218096},

    # ===== AUSTRALIA =====
    {"name": "Tim Cahill",            "nationality": "Australia", "code": "AUS", "flag": "🇦🇺", "position": "attacker",   "tm_slug": "tim-cahill",              "tm_id": 25459},
    {"name": "Harry Kewell",          "nationality": "Australia", "code": "AUS", "flag": "🇦🇺", "position": "attacker",   "tm_slug": "harry-kewell",            "tm_id": 5380},
    {"name": "Mile Jedinak",          "nationality": "Australia", "code": "AUS", "flag": "🇦🇺", "position": "midfielder", "tm_slug": "mile-jedinak",            "tm_id": 70012},
    {"name": "Matthew Ryan",          "nationality": "Australia", "code": "AUS", "flag": "🇦🇺", "position": "gk",         "tm_slug": "matthew-ryan",            "tm_id": 181742},

    # ===== CAMEROON =====
    {"name": "Samuel Eto'o",          "nationality": "Cameroon", "code": "CMR", "flag": "🇨🇲", "position": "attacker",   "tm_slug": "samuel-etoo",             "tm_id": 14948},
    {"name": "Geremi",                "nationality": "Cameroon", "code": "CMR", "flag": "🇨🇲", "position": "midfielder", "tm_slug": "geremi",                  "tm_id": 14671},
    {"name": "Rigobert Song",         "nationality": "Cameroon", "code": "CMR", "flag": "🇨🇲", "position": "defender",   "tm_slug": "rigobert-song",           "tm_id": 6777},
    {"name": "Lauren",                "nationality": "Cameroon", "code": "CMR", "flag": "🇨🇲", "position": "defender",   "tm_slug": "lauren",                  "tm_id": 15052},

    # ===== ECUADOR =====
    {"name": "Antonio Valencia",      "nationality": "Ecuador", "code": "ECU", "flag": "🇪🇨", "position": "midfielder", "tm_slug": "antonio-valencia",        "tm_id": 47187},
    {"name": "Agustin Delgado",       "nationality": "Ecuador", "code": "ECU", "flag": "🇪🇨", "position": "attacker",   "tm_slug": "agustin-delgado",         "tm_id": 11527},
    {"name": "Enner Valencia",        "nationality": "Ecuador", "code": "ECU", "flag": "🇪🇨", "position": "attacker",   "tm_slug": "enner-valencia",          "tm_id": 248512},
    {"name": "Moises Caicedo",        "nationality": "Ecuador", "code": "ECU", "flag": "🇪🇨", "position": "midfielder", "tm_slug": "moises-caicedo",          "tm_id": 563186},

    # ===== IRAN =====
    {"name": "Javad Nekounam",        "nationality": "Iran", "code": "IRN", "flag": "🇮🇷", "position": "midfielder", "tm_slug": "javad-nekounam",          "tm_id": 26461},
    {"name": "Sardar Azmoun",         "nationality": "Iran", "code": "IRN", "flag": "🇮🇷", "position": "attacker",   "tm_slug": "sardar-azmoun",           "tm_id": 316081},
    {"name": "Mehdi Mahdavikia",      "nationality": "Iran", "code": "IRN", "flag": "🇮🇷", "position": "midfielder", "tm_slug": "mehdi-mahdavikia",        "tm_id": 9221},

    # ===== RUSSIA =====
    {"name": "Andrey Arshavin",       "nationality": "Russia", "code": "RUS", "flag": "🇷🇺", "position": "attacker",   "tm_slug": "andrey-arshavin",         "tm_id": 32798},
    {"name": "Denis Cheryshev",       "nationality": "Russia", "code": "RUS", "flag": "🇷🇺", "position": "attacker",   "tm_slug": "denis-cheryshev",         "tm_id": 118753},
    {"name": "Igor Akinfeev",         "nationality": "Russia", "code": "RUS", "flag": "🇷🇺", "position": "gk",         "tm_slug": "igor-akinfeev",           "tm_id": 17197},

    # ===== ICELAND =====
    {"name": "Gylfi Sigurdsson",      "nationality": "Iceland", "code": "ISL", "flag": "🇮🇸", "position": "midfielder", "tm_slug": "gylfi-sigurdsson",        "tm_id": 131232},
    {"name": "Aron Gunnarsson",       "nationality": "Iceland", "code": "ISL", "flag": "🇮🇸", "position": "midfielder", "tm_slug": "aron-gunnarsson",         "tm_id": 101929},

    # ===== WALES =====
    {"name": "Gareth Bale",           "nationality": "Wales", "code": "WAL", "flag": "🏴󠁧󠁢󠁷󠁬󠁳󠁿", "position": "attacker",   "tm_slug": "gareth-bale",             "tm_id": 39381},
    {"name": "Aaron Ramsey",          "nationality": "Wales", "code": "WAL", "flag": "🏴󠁧󠁢󠁷󠁬󠁳󠁿", "position": "midfielder", "tm_slug": "aaron-ramsey",            "tm_id": 50855},

    # ===== TURKEY =====
    {"name": "Hakan Sukur",           "nationality": "Turkey", "code": "TUR", "flag": "🇹🇷", "position": "attacker",   "tm_slug": "hakan-sukur",             "tm_id": 5534},
    {"name": "Emre Belozoglu",        "nationality": "Turkey", "code": "TUR", "flag": "🇹🇷", "position": "midfielder", "tm_slug": "emre-belozoglu",          "tm_id": 5862},

    # ===== SERBIA =====
    {"name": "Nemanja Vidic",         "nationality": "Serbia", "code": "SRB", "flag": "🇷🇸", "position": "defender",   "tm_slug": "nemanja-vidic",           "tm_id": 25519},
    {"name": "Dejan Stankovic",       "nationality": "Serbia", "code": "SRB", "flag": "🇷🇸", "position": "midfielder", "tm_slug": "dejan-stankovic",         "tm_id": 4651},

    # ===== PARAGUAY =====
    {"name": "Nelson Valdez",         "nationality": "Paraguay", "code": "PAR", "flag": "🇵🇾", "position": "attacker",   "tm_slug": "nelson-valdez",           "tm_id": 44614},
    {"name": "Oscar Cardozo",         "nationality": "Paraguay", "code": "PAR", "flag": "🇵🇾", "position": "attacker",   "tm_slug": "oscar-cardozo",           "tm_id": 21463},

    # ===== MOROCCO =====
    {"name": "Hakim Ziyech",          "nationality": "Morocco", "code": "MAR", "flag": "🇲🇦", "position": "midfielder", "tm_slug": "hakim-ziyech",            "tm_id": 189917},
    {"name": "Achraf Hakimi",         "nationality": "Morocco", "code": "MAR", "flag": "🇲🇦", "position": "defender",   "tm_slug": "achraf-hakimi",           "tm_id": 400162},
    {"name": "Youssef En-Nesyri",     "nationality": "Morocco", "code": "MAR", "flag": "🇲🇦", "position": "attacker",   "tm_slug": "youssef-en-nesyri",       "tm_id": 313551},

    # ===== DENMARK (extra) =====
    {"name": "Kasper Schmeichel",     "nationality": "Denmark", "code": "DEN", "flag": "🇩🇰", "position": "gk",         "tm_slug": "kasper-schmeichel",       "tm_id": 49020},

    # ====================================================================
    # ROUND 2 EXTENSIONS - additional candidates (tm_id=0 -> scraper search fallback)
    # ====================================================================

    # ----- ARGENTINA (extra) -----
    {"name": "Diego Maradona", "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "midfielder", "tm_slug": "diego-maradona", "tm_id": 0},
    {"name": "Gabriel Batistuta", "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "attacker", "tm_slug": "gabriel-batistuta", "tm_id": 0},
    {"name": "Pablo Aimar", "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "midfielder", "tm_slug": "pablo-aimar", "tm_id": 0},
    {"name": "Ariel Ortega", "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "attacker", "tm_slug": "ariel-ortega", "tm_id": 0},
    {"name": "Martin Demichelis", "nationality": "Argentina", "code": "ARG", "flag": "🇦🇷", "position": "defender", "tm_slug": "martin-demichelis", "tm_id": 0},

    # ----- BRAZIL (extra) -----
    {"name": "Rivaldo", "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "attacker", "tm_slug": "rivaldo", "tm_id": 0},
    {"name": "Lucio", "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "defender", "tm_slug": "lucio", "tm_id": 0},
    {"name": "Maicon", "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "defender", "tm_slug": "maicon", "tm_id": 0},
    {"name": "Gilberto Silva", "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "midfielder", "tm_slug": "gilberto-silva", "tm_id": 0},
    {"name": "Edmilson", "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "defender", "tm_slug": "edmilson", "tm_id": 0},
    {"name": "Juan", "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "defender", "tm_slug": "juan", "tm_id": 0},
    {"name": "Gabriel Jesus", "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "attacker", "tm_slug": "gabriel-jesus", "tm_id": 0},
    {"name": "Marquinhos", "nationality": "Brazil", "code": "BRA", "flag": "🇧🇷", "position": "defender", "tm_slug": "marquinhos", "tm_id": 0},

    # ----- MEXICO (extra) -----
    {"name": "Cuauhtemoc Blanco", "nationality": "Mexico", "code": "MEX", "flag": "🇲🇽", "position": "attacker", "tm_slug": "cuauhtemoc-blanco", "tm_id": 0},
    {"name": "Jared Borgetti", "nationality": "Mexico", "code": "MEX", "flag": "🇲🇽", "position": "attacker", "tm_slug": "jared-borgetti", "tm_id": 0},
    {"name": "Pavel Pardo", "nationality": "Mexico", "code": "MEX", "flag": "🇲🇽", "position": "midfielder", "tm_slug": "pavel-pardo", "tm_id": 0},
    {"name": "Hector Moreno", "nationality": "Mexico", "code": "MEX", "flag": "🇲🇽", "position": "defender", "tm_slug": "hector-moreno", "tm_id": 0},
    {"name": "Raul Jimenez", "nationality": "Mexico", "code": "MEX", "flag": "🇲🇽", "position": "attacker", "tm_slug": "raul-jimenez", "tm_id": 0},
    {"name": "Gerardo Torrado", "nationality": "Mexico", "code": "MEX", "flag": "🇲🇽", "position": "midfielder", "tm_slug": "gerardo-torrado", "tm_id": 0},
    {"name": "Hector Herrera", "nationality": "Mexico", "code": "MEX", "flag": "🇲🇽", "position": "midfielder", "tm_slug": "hector-herrera", "tm_id": 0},
    {"name": "Jesus Corona", "nationality": "Mexico", "code": "MEX", "flag": "🇲🇽", "position": "attacker", "tm_slug": "jesus-corona", "tm_id": 0},
    {"name": "Santiago Gimenez", "nationality": "Mexico", "code": "MEX", "flag": "🇲🇽", "position": "attacker", "tm_slug": "santiago-gimenez", "tm_id": 0},

    # ----- ENGLAND (extra) -----
    {"name": "Joe Hart", "nationality": "England", "code": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "position": "gk", "tm_slug": "joe-hart", "tm_id": 0},
    {"name": "John Terry", "nationality": "England", "code": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "position": "defender", "tm_slug": "john-terry", "tm_id": 0},
    {"name": "Sol Campbell", "nationality": "England", "code": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "position": "defender", "tm_slug": "sol-campbell", "tm_id": 0},
    {"name": "Gary Neville", "nationality": "England", "code": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "position": "defender", "tm_slug": "gary-neville", "tm_id": 0},
    {"name": "Paul Scholes", "nationality": "England", "code": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "position": "midfielder", "tm_slug": "paul-scholes", "tm_id": 0},
    {"name": "Jamie Carragher", "nationality": "England", "code": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "position": "defender", "tm_slug": "jamie-carragher", "tm_id": 0},
    {"name": "James Milner", "nationality": "England", "code": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "position": "midfielder", "tm_slug": "james-milner", "tm_id": 0},
    {"name": "Jordan Henderson", "nationality": "England", "code": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "position": "midfielder", "tm_slug": "jordan-henderson", "tm_id": 0},

    # ----- FRANCE (extra) -----
    {"name": "Lilian Thuram", "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "defender", "tm_slug": "lilian-thuram", "tm_id": 0},
    {"name": "Bixente Lizarazu", "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "defender", "tm_slug": "bixente-lizarazu", "tm_id": 0},
    {"name": "Marcel Desailly", "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "defender", "tm_slug": "marcel-desailly", "tm_id": 0},
    {"name": "Claude Makelele", "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "midfielder", "tm_slug": "claude-makelele", "tm_id": 0},
    {"name": "Patrice Evra", "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "defender", "tm_slug": "patrice-evra", "tm_id": 0},
    {"name": "Sylvain Wiltord", "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "attacker", "tm_slug": "sylvain-wiltord", "tm_id": 0},
    {"name": "Fabien Barthez", "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "gk", "tm_slug": "fabien-barthez", "tm_id": 0},
    {"name": "Theo Hernandez", "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "defender", "tm_slug": "theo-hernandez", "tm_id": 0},
    {"name": "Mike Maignan", "nationality": "France", "code": "FRA", "flag": "🇫🇷", "position": "gk", "tm_slug": "mike-maignan", "tm_id": 0},

    # ----- ITALY (extra) -----
    {"name": "Marco Materazzi", "nationality": "Italy", "code": "ITA", "flag": "🇮🇹", "position": "defender", "tm_slug": "marco-materazzi", "tm_id": 0},
    {"name": "Mauro Camoranesi", "nationality": "Italy", "code": "ITA", "flag": "🇮🇹", "position": "midfielder", "tm_slug": "mauro-camoranesi", "tm_id": 0},

    # ----- PORTUGAL (extra) -----
    {"name": "Ricardo Carvalho", "nationality": "Portugal", "code": "POR", "flag": "🇵🇹", "position": "defender", "tm_slug": "ricardo-carvalho", "tm_id": 0},
    {"name": "Raul Meireles", "nationality": "Portugal", "code": "POR", "flag": "🇵🇹", "position": "midfielder", "tm_slug": "raul-meireles", "tm_id": 0},
    {"name": "Fabio Coentrao", "nationality": "Portugal", "code": "POR", "flag": "🇵🇹", "position": "defender", "tm_slug": "fabio-coentrao", "tm_id": 0},
    {"name": "Rui Patricio", "nationality": "Portugal", "code": "POR", "flag": "🇵🇹", "position": "gk", "tm_slug": "rui-patricio", "tm_id": 0},
    {"name": "Quaresma", "nationality": "Portugal", "code": "POR", "flag": "🇵🇹", "position": "attacker", "tm_slug": "ricardo-quaresma", "tm_id": 0},
    {"name": "Tiago Mendes", "nationality": "Portugal", "code": "POR", "flag": "🇵🇹", "position": "midfielder", "tm_slug": "tiago", "tm_id": 0},
    {"name": "Diogo Dalot", "nationality": "Portugal", "code": "POR", "flag": "🇵🇹", "position": "defender", "tm_slug": "diogo-dalot", "tm_id": 0},

    # ----- NETHERLANDS (extra) -----
    {"name": "Klaas-Jan Huntelaar", "nationality": "Netherlands", "code": "NED", "flag": "🇳🇱", "position": "attacker", "tm_slug": "klaas-jan-huntelaar", "tm_id": 0},
    {"name": "Patrick Kluivert", "nationality": "Netherlands", "code": "NED", "flag": "🇳🇱", "position": "attacker", "tm_slug": "patrick-kluivert", "tm_id": 0},
    {"name": "Edgar Davids", "nationality": "Netherlands", "code": "NED", "flag": "🇳🇱", "position": "midfielder", "tm_slug": "edgar-davids", "tm_id": 0},
    {"name": "Clarence Seedorf", "nationality": "Netherlands", "code": "NED", "flag": "🇳🇱", "position": "midfielder", "tm_slug": "clarence-seedorf", "tm_id": 0},
    {"name": "Rafael van der Vaart", "nationality": "Netherlands", "code": "NED", "flag": "🇳🇱", "position": "midfielder", "tm_slug": "rafael-van-der-vaart", "tm_id": 0},
    {"name": "John Heitinga", "nationality": "Netherlands", "code": "NED", "flag": "🇳🇱", "position": "defender", "tm_slug": "john-heitinga", "tm_id": 0},

    # ----- CROATIA (extra) -----
    {"name": "Robert Prosinecki", "nationality": "Croatia", "code": "CRO", "flag": "🇭🇷", "position": "midfielder", "tm_slug": "robert-prosinecki", "tm_id": 0},
    {"name": "Davor Suker", "nationality": "Croatia", "code": "CRO", "flag": "🇭🇷", "position": "attacker", "tm_slug": "davor-suker", "tm_id": 0},
    {"name": "Igor Tudor", "nationality": "Croatia", "code": "CRO", "flag": "🇭🇷", "position": "defender", "tm_slug": "igor-tudor", "tm_id": 0},
    {"name": "Slaven Bilic", "nationality": "Croatia", "code": "CRO", "flag": "🇭🇷", "position": "defender", "tm_slug": "slaven-bilic", "tm_id": 0},
    {"name": "Niko Kranjcar", "nationality": "Croatia", "code": "CRO", "flag": "🇭🇷", "position": "midfielder", "tm_slug": "niko-kranjcar", "tm_id": 0},
    {"name": "Eduardo da Silva", "nationality": "Croatia", "code": "CRO", "flag": "🇭🇷", "position": "attacker", "tm_slug": "eduardo-da-silva", "tm_id": 0},
    {"name": "Mladen Petric", "nationality": "Croatia", "code": "CRO", "flag": "🇭🇷", "position": "attacker", "tm_slug": "mladen-petric", "tm_id": 0},

    # ----- BELGIUM (extra) -----
    {"name": "Marouane Fellaini", "nationality": "Belgium", "code": "BEL", "flag": "🇧🇪", "position": "midfielder", "tm_slug": "marouane-fellaini", "tm_id": 0},
    {"name": "Thomas Meunier", "nationality": "Belgium", "code": "BEL", "flag": "🇧🇪", "position": "defender", "tm_slug": "thomas-meunier", "tm_id": 0},

    # ----- URUGUAY (extra) -----
    {"name": "Egidio Arevalo", "nationality": "Uruguay", "code": "URU", "flag": "🇺🇾", "position": "midfielder", "tm_slug": "egidio-arevalo", "tm_id": 0},

    # ----- USA (extra) -----
    {"name": "Brian McBride", "nationality": "USA", "code": "USA", "flag": "🇺🇸", "position": "attacker", "tm_slug": "brian-mcbride", "tm_id": 0},

    # ----- SOUTH KOREA (extra) -----
    {"name": "Lee Chung-yong", "nationality": "South Korea", "code": "KOR", "flag": "🇰🇷", "position": "midfielder", "tm_slug": "chung-yong-lee", "tm_id": 0},
    {"name": "Hwang Ui-jo", "nationality": "South Korea", "code": "KOR", "flag": "🇰🇷", "position": "attacker", "tm_slug": "ui-jo-hwang", "tm_id": 0},
    {"name": "Cho Hyun-woo", "nationality": "South Korea", "code": "KOR", "flag": "🇰🇷", "position": "gk", "tm_slug": "hyun-woo-cho", "tm_id": 0},

    # ----- JAPAN (extra) -----
    {"name": "Naohiro Takahara", "nationality": "Japan", "code": "JPN", "flag": "🇯🇵", "position": "attacker", "tm_slug": "naohiro-takahara", "tm_id": 0},
    {"name": "Yuya Osako", "nationality": "Japan", "code": "JPN", "flag": "🇯🇵", "position": "attacker", "tm_slug": "yuya-osako", "tm_id": 0},

    # ----- EGYPT (extra) -----
    {"name": "Mohamed Salah", "nationality": "Egypt", "code": "EGY", "flag": "🇪🇬", "position": "attacker", "tm_slug": "mohamed-salah", "tm_id": 0},

    # ----- ALGERIA (extra) -----
    {"name": "Riyad Mahrez", "nationality": "Algeria", "code": "ALG", "flag": "🇩🇿", "position": "attacker", "tm_slug": "riyad-mahrez", "tm_id": 0},

    # ----- CHILE (extra) -----
    {"name": "Arturo Vidal", "nationality": "Chile", "code": "CHI", "flag": "🇨🇱", "position": "midfielder", "tm_slug": "arturo-vidal", "tm_id": 0},
    {"name": "Alexis Sanchez", "nationality": "Chile", "code": "CHI", "flag": "🇨🇱", "position": "attacker", "tm_slug": "alexis-sanchez", "tm_id": 0},
    {"name": "Claudio Bravo", "nationality": "Chile", "code": "CHI", "flag": "🇨🇱", "position": "gk", "tm_slug": "claudio-bravo", "tm_id": 0},

    # ----- SENEGAL (extra) -----
    {"name": "El-Hadji Diouf", "nationality": "Senegal", "code": "SEN", "flag": "🇸🇳", "position": "attacker", "tm_slug": "el-hadji-diouf", "tm_id": 0},

    # ----- NIGERIA (extra) -----
    {"name": "Vincent Enyeama", "nationality": "Nigeria", "code": "NGA", "flag": "🇳🇬", "position": "gk", "tm_slug": "vincent-enyeama", "tm_id": 0},
    {"name": "Mikel John Obi", "nationality": "Nigeria", "code": "NGA", "flag": "🇳🇬", "position": "midfielder", "tm_slug": "mikel-john-obi", "tm_id": 0},
    {"name": "Victor Osimhen", "nationality": "Nigeria", "code": "NGA", "flag": "🇳🇬", "position": "attacker", "tm_slug": "victor-osimhen", "tm_id": 0},

    # ----- GHANA (extra) -----
    {"name": "Kevin-Prince Boateng", "nationality": "Ghana", "code": "GHA", "flag": "🇬🇭", "position": "midfielder", "tm_slug": "kevin-prince-boateng", "tm_id": 0},
    {"name": "Mohammed Kudus", "nationality": "Ghana", "code": "GHA", "flag": "🇬🇭", "position": "midfielder", "tm_slug": "mohammed-kudus", "tm_id": 0},

    # ----- AUSTRALIA (extra) -----
    {"name": "Mark Schwarzer", "nationality": "Australia", "code": "AUS", "flag": "🇦🇺", "position": "gk", "tm_slug": "mark-schwarzer", "tm_id": 0},
    {"name": "Mark Bresciano", "nationality": "Australia", "code": "AUS", "flag": "🇦🇺", "position": "midfielder", "tm_slug": "mark-bresciano", "tm_id": 0},
    {"name": "Mathew Ryan", "nationality": "Australia", "code": "AUS", "flag": "🇦🇺", "position": "gk", "tm_slug": "mathew-ryan", "tm_id": 0},

    # ----- IRAN (extra) -----
    {"name": "Ali Daei", "nationality": "Iran", "code": "IRN", "flag": "🇮🇷", "position": "attacker", "tm_slug": "ali-daei", "tm_id": 0},
    {"name": "Ali Karimi", "nationality": "Iran", "code": "IRN", "flag": "🇮🇷", "position": "midfielder", "tm_slug": "ali-karimi", "tm_id": 0},
    {"name": "Alireza Beiranvand", "nationality": "Iran", "code": "IRN", "flag": "🇮🇷", "position": "gk", "tm_slug": "alireza-beiranvand", "tm_id": 0},

    # ----- COLOMBIA (extra) -----
    {"name": "Carlos Valderrama", "nationality": "Colombia", "code": "COL", "flag": "🇨🇴", "position": "midfielder", "tm_slug": "carlos-valderrama", "tm_id": 0},

    # ----- CANADA (extra) -----
    {"name": "Alphonso Davies", "nationality": "Canada", "code": "CAN", "flag": "🇨🇦", "position": "defender", "tm_slug": "alphonso-davies", "tm_id": 0},
    {"name": "Jonathan David", "nationality": "Canada", "code": "CAN", "flag": "🇨🇦", "position": "attacker", "tm_slug": "jonathan-david", "tm_id": 0},
    {"name": "Stephen Eustaquio", "nationality": "Canada", "code": "CAN", "flag": "🇨🇦", "position": "midfielder", "tm_slug": "stephen-eustaquio", "tm_id": 0},

    # ----- SAUDI ARABIA (extra) -----
    {"name": "Salem Al-Dawsari", "nationality": "Saudi Arabia", "code": "SAU", "flag": "🇸🇦", "position": "midfielder", "tm_slug": "salem-al-dawsari", "tm_id": 0},

    # ----- COSTA RICA (extra) -----
    {"name": "Bryan Ruiz", "nationality": "Costa Rica", "code": "CRC", "flag": "🇨🇷", "position": "attacker", "tm_slug": "bryan-ruiz", "tm_id": 0},
    {"name": "Joel Campbell", "nationality": "Costa Rica", "code": "CRC", "flag": "🇨🇷", "position": "attacker", "tm_slug": "joel-campbell", "tm_id": 0},
    {"name": "Keylor Navas", "nationality": "Costa Rica", "code": "CRC", "flag": "🇨🇷", "position": "gk", "tm_slug": "keylor-navas", "tm_id": 0},

    # ----- GERMANY (extra) -----
    {"name": "Mario Gotze", "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "attacker", "tm_slug": "mario-gotze", "tm_id": 0},
    {"name": "Niklas Sule", "nationality": "Germany", "code": "GER", "flag": "🇩🇪", "position": "defender", "tm_slug": "niklas-suele", "tm_id": 0},

    # ----- SWITZERLAND (extra) -----
    {"name": "Breel Embolo", "nationality": "Switzerland", "code": "SUI", "flag": "🇨🇭", "position": "attacker", "tm_slug": "breel-embolo", "tm_id": 0},

]
# fmt: on

assert len(CANDIDATES) == 448, f"Expected 448 candidates, got {len(CANDIDATES)}"
