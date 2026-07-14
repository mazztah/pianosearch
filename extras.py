# -*- coding: utf-8 -*-
"""
extras.py — ergaenzende Daten, getrennt von data.py gehalten, damit Fakten (data.py)
und redaktionelle Zusaetze (hier) klar auseinandergehalten werden.

INSTAGRAM:
  Nur Handles, die ueber eine Websuche gegen den offiziellen Auftritt (Bio-Text,
  Verifizierungs-Hinweise, Verlinkung von der offiziellen Kuenstlerinnen-Website o.ae.)
  bestaetigt werden konnten. Fehlt ein Eintrag, wird im Frontend kein Instagram-Button
  angezeigt statt eines geratenen/falschen Links.

LISTENING_NOTES:
  Kurzer redaktioneller "Hoertipp"-Absatz (2-3 Saetze) pro Kuenstlerin - explizit als
  subjektive Höreinordnung gekennzeichnet, keine zusaetzlichen Fakten ueber Wettbewerbe
  o.ae., die nicht auch in data.py stehen.
"""

INSTAGRAM = {
    "khatia-buniatishvili": "khatiabuniatishvili",
    "yuja-wang": "yujawang.official",
    "isata-kanneh-mason": "isatakannehmason",
    "claire-huangci": "clairehuangci",
    "nathalia-milstein": "nathaliamilstein_pianist",
    "anna-fedorova": "annapianist",
    "beatrice-rana": "beatricerana",
    "tiffany-poon": "tiffanypianist",
    "alice-sara-ott": "alicesaraott_official",
    "zhang-zuo": "zeezeepiano",
}

# Nur EXAKT verifizierte Spotify-Artist-Profile (per Websuche bestaetigt). Fuer alle
# anderen Kuenstlerinnen baut das Backend automatisch einen Spotify-Suchlink
# (https://open.spotify.com/search/<Name>) - niemals eine geratene Artist-ID.
SPOTIFY = {
    "yuja-wang": "https://open.spotify.com/artist/7HUNjWo242UAVHZvj9zk4w",
    "khatia-buniatishvili": "https://open.spotify.com/artist/0bouHpX4JiuPnIfP2jFxRi",
    "isata-kanneh-mason": "https://open.spotify.com/artist/7FEzSfCBSOo0wAmdk9pQ6M",
    "eva-gevorgyan": "https://open.spotify.com/artist/5s4B157iLV2E6o5Iz6uyTy",
}

# Offizielle Presse-/Medienseiten, auf die verlinkt wird (Bilder werden NICHT
# heruntergeladen/eingebettet, da Presskit-Fotos i. d. R. urheberrechtlich geschuetzt
# und nur fuer redaktionelle Nutzung mit Namensnennung freigegeben sind - siehe README).
PRESS_URL = {
    "zhang-zuo": "https://www.zeezee-piano.com/",
    "isata-kanneh-mason": "https://www.isatakannehmason.com/",
    "anna-fedorova": "https://www.annafedorova.com/",
    "claire-huangci": "https://clairehuangci.com/",
    "nathalia-milstein": "https://www.nathaliamilstein.com/",
    "rachel-cheung": "https://www.rachelcheung.com/",
    "sophia-liu": "https://sophialiu.com/",
    "yeol-eum-son": "http://www.yeoleumson.com/",
    "mitsuko-uchida": "https://mitsukouchida.com/",
}

LISTENING_NOTES = {
    "alexandra-dovgan": "Wer sie hört, bemerkt zuerst die Ruhe: Dovgan drängt nie, auch in virtuosen Passagen bleibt der Klang durchsichtig. Ein guter Einstieg ist ihre Aufnahme des Mozart-Konzerts KV 466 – kindliche Klarheit trifft auf erwachsene Struktur.",
    "eva-gevorgyan": "Ihre Chopin-Mazurken zeigen die für ihr Alter erstaunliche rhythmische Freiheit, die den Chopin-Wettbewerb-Juroren auffiel. Empfehlenswert: ihre Skrjabin-Einspielungen, die zwischen Zartheit und Ekstase pendeln.",
    "sophia-liu": "Trotz ihres jungen Alters spielt sie mit einer fast altmodischen Klangkultur – hörbar in ihren Chopin-Nocturnes, die nie ins Sentimentale kippen. Ein Name, den man sich für die kommenden zehn Jahre merken sollte.",
    "anna-geniushene": "Ihre Rachmaninow-Interpretationen leben von orchestralem Klangvolumen, ohne die leisen Zwischentöne zu verlieren. Die Cliburn-Wettbewerbsaufnahmen von 2022 zeigen das eindrücklich.",
    "kate-liu": "Ihr Chopin ist bewusst uneitel: mehr Rubato, mehr Risiko, weniger Politur als bei vielen Wettbewerbskolleginnen. Genau das macht ihre Warschau-Aufnahmen von 2015 bis heute hörenswert.",
    "tiffany-poon": "Wer klassische Musik jemandem näherbringen will, der bisher wenig damit anfangen konnte, kann mit Poons YouTube-Kanal beginnen – ihre Schumann-Einspielungen verbinden Zugänglichkeit mit echter Substanz.",
    "beatrice-rana": "Ihre Bach-Goldberg-Variationen, aufgenommen mit erst 23 Jahren, gelten als eine der reifsten Einspielungen ihrer Generation. Auch ihr Prokofjew hat einen seltenen Sinn für Struktur bei gleichzeitiger Wärme.",
    "khatia-buniatishvili": "Ihre Liszt- und Rachmaninow-Interpretationen sind bewusst extrem – manche Kritiker nennen es Manierismus, andere puren Mut zur eigenen Stimme. Am besten selbst hören und urteilen.",
    "alice-sara-ott": "Ihre barfuß gespielten Live-Konzerte sind auch visuell ein Erlebnis; klanglich beeindruckt vor allem ihr Debussy, der zwischen Präzision und Traumhaftigkeit changiert.",
    "yuja-wang": "Kaum eine Pianistin verbindet technische Extreme so selbstverständlich mit Bühnenpräsenz. Ihre Prokofjew-Konzerte mit Gustavo Dudamel zählen zu den meistdiskutierten Livemitschnitten der letzten Jahre.",
    "marie-ange-nguci": "Ihr Ravel – insbesondere „Gaspard de la Nuit“ – zeigt eine seltene Kombination aus analytischer Klarheit und klanglicher Fantasie, geprägt durch ihre parallele musikwissenschaftliche Ausbildung.",
    "ying-li": "Ihre Doppel-Qualifikation bei Chopin- und Queen-Elisabeth-Wettbewerb macht neugierig auf ihren Mozart, der Eleganz ohne Kühle zeigt.",
    "yulianna-avdeeva": "Ihre Schostakowitsch-Präludien und -Fugen sind ein mutiges, selten aufgeführtes Programm, das die intellektuelle Seite ihrer Kunst zeigt – jenseits des Chopin-Images, das ihr der Wettbewerbssieg 2010 einbrachte.",
    "zlata-chochieva": "Insider-Tipp unter Pianophilen: Ihre Rachmaninow-Études-Tableaux verbinden russische Klangkultur mit einer Zurückhaltung, die dem Werk ungewohnt viel Raum zum Atmen gibt.",
    "hj-lim": "Ihr kompletter Beethoven-Sonatenzyklus polarisiert bis heute – ungewöhnliche Tempi, mutige Akzente. Wer Beethoven neu hören will, sollte hier ansetzen, auch um anschließend zu widersprechen.",
    "aimi-kobayashi": "Ihr Chopin-Konzert Nr. 1 vom Warschauer Wettbewerbsfinale 2021 zeigt, warum sie zu den gefragtesten Chopin-Interpretinnen ihrer Generation zählt: klar, aber nie kühl.",
    "elisabeth-brauss": "Ihre Programme kombinieren bewusst Bekanntes mit Seltenem – ein guter Einstieg sind ihre Brahms-Klavierstücke op. 118, die Reife und Zurückhaltung zugleich zeigen.",
    "avery-gagliano": "Ihre Beethoven-Interpretationen fallen durch kammermusikalische Sensibilität auf, statt auf reine Orchestergröße zu setzen – ungewöhnlich für eine so junge Solistin.",
    "isata-kanneh-mason": "Ihr Debütalbum mit Werken von Clara Schumann bleibt der beste Einstieg: persönlich, unaufgeregt, und mitverantwortlich dafür, dass Clara Schumanns Musik heute wieder öfter im Konzertsaal zu hören ist.",
    "anna-fedorova": "Ihre Live-Aufnahme von Rachmaninows 2. Klavierkonzert erklärt sich selbst: 46 Millionen Aufrufe kommen nicht durch Marketing, sondern durch eine Interpretation, die Emotion nie überzeichnet.",
    "claire-huangci": "Ihre stilistische Bandbreite – von Scarlatti bis Florence Price – macht sie zu einer der interessantesten Programmgestalterinnen ihrer Generation; ein guter Einstieg ist ihr Scarlatti-Zyklus.",
    "zhang-zuo": "Ihre Liszt- und Wagner-Transkriptionen zeigen orchestrales Denken am Klavier; als künstlerische Leiterin des Z+ Festivals prägt sie inzwischen auch abseits der eigenen Konzerte das Musikleben Shanghais mit.",
    "yeol-eum-son": "Ihre live mitgeschnittene Interpretation von Mozarts Klavierkonzert Nr. 21 beim Tschaikowsky-Wettbewerb gehört zu den meistgesehenen klassischen Aufnahmen auf YouTube überhaupt – zu Recht, wie ein Hören schnell zeigt.",
    "nathalia-milstein": "Ihre Duo-Aufnahmen mit ihrer Schwester Maria Milstein zeigen eine seltene musikalische Vertrautheit; solistisch überzeugt vor allem ihr Schumann durch undogmatische Klarheit.",
    "rachel-cheung": "Der Publikumspreis beim Van-Cliburn-Wettbewerb 2017 war kein Zufall – live hat sie eine unmittelbare Ausstrahlung, die auf ihrem Debütalbum „Reflections“ gut eingefangen ist.",
    "martha-argerich": "Jede ihrer Aufnahmen ist ein Pflichttermin, aber ihre Prokofjew-3.-Klavierkonzert-Einspielungen aus den 1960er-Jahren bleiben unerreicht an Spontaneität und Risikofreude.",
    "mitsuko-uchida": "Ihre Schubert-Sonaten gelten als Referenz, weil sie Fragilität nicht als Schwäche, sondern als eigene Klangqualität behandelt – am eindrücklichsten in den späten Sonaten D. 959 und D. 960.",
    "helene-grimaud": "Ihre Rachmaninow-Konzerte sind bewusst dunkel timbriert – wer den Wolf-Conservationist-Hintergrund kennt, hört darin fast eine klangliche Verwandtschaft zu ihrem zweiten großen Lebensthema.",
    "maria-joao-pires": "Ihr Mozart verzichtet konsequent auf jede Effekthascherei; die berühmte Aufnahme, bei der sie live ins falsche Konzert einsteigt und sich in Sekunden umorientiert, zeigt ihre außergewöhnliche musikalische Sicherheit.",
    "angela-hewitt": "Ihre Bach-Gesamteinspielung ist für viele Pianistinnen und Pianisten die erste Referenz, wenn es um historisch informierte, aber warme Bach-Interpretation auf dem modernen Konzertflügel geht.",
    "elisabeth-leonskaja": "Ihre Schubert-Interpretationen sind unaufgeregt bis an die Grenze der Kargheit – und gerade dadurch enorm konzentriert; ein Erbe ihrer jahrelangen Zusammenarbeit mit Richter.",
    "gabriela-montero": "Ihre Live-Improvisationen über Publikumsvorschläge sind im klassischen Konzertbetrieb einzigartig – kein Konzert gleicht dem anderen, weil buchstäblich nichts vorbereitet ist.",
    "lise-de-la-salle": "Ihr Prokofjew und Bartók zeigen eine kraftvolle, fast perkussive Seite des Klaviers, die selten so kontrolliert eingesetzt wird wie bei ihr.",
    "simone-dinnerstein": "Ihre in Eigenregie finanzierten Goldberg-Variationen von 2007 sind eine der ungewöhnlichsten Erfolgsgeschichten der jüngeren Klassikwelt – unabhängig produziert und trotzdem ein Bestseller.",
    "olga-kern": "Ihr Rachmaninow trägt hörbar die Handschrift der russischen Klaviertradition, die sie über ihre Familie direkt von Konstantin Igumnow geerbt hat.",
    "clara-schumann": "Ihre eigenen Kompositionen – lange im Schatten ihres Mannes – werden heute zunehmend eigenständig aufgeführt, etwa ihr Klavierkonzert a-Moll, das sie bereits als Jugendliche komponierte.",
    "alicia-de-larrocha": "Ihre Albéniz- und Granados-Einspielungen gelten bis heute als unübertroffen, weil sie das spanische Repertoire nie folkloristisch verkürzte, sondern seine pianistische Komplexität ernst nahm.",
    "clara-haskil": "Ihre Mozart-Aufnahmen aus den 1950er-Jahren zeigen eine Zerbrechlichkeit, die nie schwach wirkt – ein Widerspruch, der ihre gesamte Karriere prägte.",
    "myra-hess": "Ihre Bach-Transkription „Jesu, Joy of Man's Desiring“ ist Millionen Menschen vertraut, ohne dass viele wissen, dass sie von einer Konzertpianistin stammt, die damit auch durch den Krieg trug.",
    "annie-fischer": "Ihre postum veröffentlichte Beethoven-Gesamtaufnahme, die sie selbst zu Lebzeiten zurückhielt, gilt heute als eine der ehrlichsten und am wenigsten routinierten Beethoven-Einspielungen überhaupt.",
}

# EXTRA_PARAGRAPHS: ein zusaetzlicher, redaktioneller Kontext-Absatz pro Kuenstlerin
# (Werdegang/Einordnung), der dem Bio-Text serverseitig als dritter Absatz angehaengt
# wird - fuer mehr Tiefe, ohne die Kernfakten in data.py anzufassen.
EXTRA_PARAGRAPHS = {
    "alexandra-dovgan": "Nach dem Umzug nach Málaga 2022 hat sie ihre Konzerttätigkeit trotz des Ortswechsels kaum unterbrochen – ein Beleg für die Stabilität, mit der ihr Umfeld sie durch den Übergang vom Wunderkind zur jungen Erwachsenen begleitet.",
    "eva-gevorgyan": "Ihre parallele Ausbildung in Moskau und Madrid gibt ihr Zugang zu zwei sehr unterschiedlichen Klaviertraditionen – ein Umstand, der sich zunehmend auch in der stilistischen Breite ihrer Konzertprogramme zeigt.",
    "sophia-liu": "Dass sie mit gerade einmal 17 Jahren bereits von Le Monde besprochen wird, zeigt, wie schnell sich ihr internationales Renommee seit dem Wechsel zu Dang Thai Son aufgebaut hat.",
    "anna-geniushene": "Ihr Mann, der Pianist Lukas Geniušas, ist ebenfalls ein international erfolgreicher Wettbewerbspreisträger – eine der wenigen Konzertpianisten-Ehen, in denen beide Partner auf höchstem Niveau aktiv sind.",
    "kate-liu": "Nach dem Chopin-Wettbewerb 2015 hat sie bewusst ein ruhigeres Karrieretempo gewählt als viele Wettbewerbskolleginnen – ein Umstand, den sie selbst als notwendig für ihre künstlerische Entwicklung beschrieben hat.",
    "tiffany-poon": "Ihr Doppelstudium an Juilliard und Columbia ist unter Konzertpianistinnen ihrer Generation ungewöhnlich und prägt bis heute ihren analytischen, erklärenden Zugang zur Musikvermittlung auf YouTube.",
    "beatrice-rana": "Ihre Schwester Ludovica Rana ist Cellistin; gemeinsam bilden sie gelegentlich ein Duo, das die kammermusikalische Seite von Beatrice Ranas Kunst zeigt, die im Konzertsaal oft hinter der Solokarriere zurücktritt.",
    "khatia-buniatishvili": "Auch ihre Schwester Gvantsa Buniatishvili ist Pianistin; beide sind gelegentlich gemeinsam auf der Bühne zu erleben, unter anderem in vierhändigen Programmen.",
    "alice-sara-ott": "Ihr offener Umgang mit der MS-Diagnose hat in der klassischen Musikbranche, in der Krankheit lange ein Tabuthema war, eine bemerkenswert offene Debatte über Gesundheit und Verletzlichkeit im Berufsalltag von Konzertkünstlerinnen angestoßen.",
    "yuja-wang": "Ihr Bühnenstil – enge, oft kurze Kleider und hohe Absätze – wird in der Klassikpresse regelmäßig diskutiert; sie selbst hat wiederholt betont, dass die Aufmerksamkeit auf die Musik und nicht auf die Garderobe gerichtet sein sollte.",
    "marie-ange-nguci": "Ihre parallele musikwissenschaftliche Promotion ist unter aktiven Konzertpianistinnen selten und zeigt sich in oft ungewöhnlich durchdachten, thematisch verknüpften Konzertprogrammen.",
    "ying-li": "Ihre Doppelqualifikation bei zwei der renommiertesten Wettbewerbe überhaupt – Chopin und Queen Elisabeth – ist unter Pianistinnen ihrer Generation eine Seltenheit und öffnete ihr Türen zu Orchestern auf mehreren Kontinenten gleichzeitig.",
    "yulianna-avdeeva": "Nach ihrem Chopin-Sieg 2010 hat sie sich bewusst gegen eine reine Chopin-Karriere entschieden und stattdessen ein breites, auch selten gespieltes Repertoire aufgebaut – eine für Wettbewerbsgewinnerinnen ungewöhnliche Strategie.",
    "zlata-chochieva": "Trotz ihres Kultstatus unter Kennerinnen und Kennern tritt sie medial eher zurückhaltend auf – ihr Ruf beruht fast ausschließlich auf den Aufnahmen selbst, kaum auf Öffentlichkeitsarbeit.",
    "hj-lim": "Ihr Wechsel vom reinen Konzertbetrieb hin zu eigenen Buchveröffentlichungen über Musik zeigt eine für Solokünstlerinnen ungewöhnliche zusätzliche publizistische Ambition.",
    "aimi-kobayashi": "Sie erhält weiterhin Unterricht bei renommierten Pädagog:innen, obwohl sie längst eine etablierte internationale Konzertkarriere hat – ein Zeichen für die in Japan stark verwurzelte Tradition lebenslangen Lernens im klassischen Musikbetrieb.",
    "elisabeth-brauss": "Ihre bewusste Programmgestaltung – Bekanntes neben selten Gespieltem – wird von Kritikern regelmäßig als Zeichen einer für ihr Alter ungewöhnlich eigenständigen künstlerischen Handschrift hervorgehoben.",
    "avery-gagliano": "Als Preisträgerin mehrerer US-amerikanischer Nachwuchswettbewerbe gehört sie zu einer kleinen Gruppe junger amerikanischer Pianistinnen, die zunehmend auch international reüssieren, statt sich auf den US-Markt zu beschränken.",
    "isata-kanneh-mason": "Als älteste von sieben musikalischen Geschwistern hat sie eine besondere Rolle in einer Familie, die das britische Musikleben der letzten Jahre wie kaum eine andere geprägt hat – regelmäßig gemeinsame Auftritte mit ihren Geschwistern inklusive.",
    "anna-fedorova": "Ihr Engagement für die Ukraine seit 2022 hat sie zu einer der öffentlich sichtbarsten klassischen Musikerinnen im Kontext des Kriegs gemacht, ohne dass dies ihre rein musikalische Karriere in den Hintergrund gedrängt hätte.",
    "claire-huangci": "Ihr bewusstes Interesse an bislang selten gespielten Komponistinnen wie Amy Beach und Florence Price positioniert sie zunehmend auch als Fürsprecherin für ein diverseres klassisches Repertoire.",
    "zhang-zuo": "Mit der Gründung des Z+ Festivals hat sie sich neben der Solokarriere ein zweites Standbein als Kulturmanagerin aufgebaut – ein Schritt, den nur wenige aktive Konzertpianistinnen ihrer Generation in diesem Umfang gehen.",
    "yeol-eum-son": "Ihre doppelte Silbermedaille bei Cliburn und Tschaikowsky-Wettbewerb macht sie zu einer von sehr wenigen Pianistinnen, die bei beiden Wettbewerben auf dem Podium standen.",
    "nathalia-milstein": "Das Geschwister-Duo mit ihrer Schwester Maria ist in der Kammermusikwelt inzwischen fest etabliert und ergänzt Nathalia Milsteins Solokarriere um eine kontinuierliche kammermusikalische Partnerschaft.",
    "rachel-cheung": "Mit der Gründung ihrer eigenen Musikakademie 2025 hat sie begonnen, ihre internationale Erfahrung gezielt an die nächste Generation Hongkonger Musikerinnen und Musiker weiterzugeben.",
    "martha-argerich": "Ihr eigenes Festival in Hamburg sowie das Argerich-Projekt in Genf gehören zu den wichtigsten Förderplattformen für junge Kammermusikerinnen und -musiker weltweit und sind Teil ihres bis heute aktiven Engagements für den Nachwuchs.",
    "mitsuko-uchida": "Als künstlerische Co-Leiterin des Marlboro Music Festivals in Vermont investiert sie seit Jahrzehnten einen erheblichen Teil ihrer Zeit in die Förderung junger Kammermusikerinnen und -musiker, abseits der eigenen Solokarriere.",
    "helene-grimaud": "Ihr Wolf Conservation Center ist kein symbolisches Nebenprojekt, sondern eine aktiv von ihr mitfinanzierte und mitgeleitete Organisation – ein für Konzertpianistinnen außergewöhnliches zweites Lebenswerk.",
    "maria-joao-pires": "Ihr zeitweiliger bewusster Rückzug aus dem großen Konzertbetrieb zugunsten musikpädagogischer Arbeit gilt in der Klassikwelt als seltenes Beispiel dafür, Erfolg nicht linear fortzusetzen, sondern eigene Prioritäten zu setzen.",
    "angela-hewitt": "Mit der Gründung des Trasimeno Music Festivals in Italien hat sie sich, ähnlich wie einige ihrer Kolleginnen, zusätzlich zur Solokarriere als Festivalgründerin und Förderin junger Talente etabliert.",
    "elisabeth-leonskaja": "Ihre jahrzehntelange künstlerische Partnerschaft mit Swjatoslaw Richter gilt als eine der prägendsten Pianisten-Mentorschaften des 20. Jahrhunderts und beeinflusst ihre Interpretationsästhetik bis heute.",
    "gabriela-montero": "Ihr politisches Engagement für Venezuela hat sie wiederholt in Konflikt mit den dortigen Behörden gebracht – ein seltenes Beispiel einer Konzertpianistin, die ihre öffentliche Plattform aktiv für politische Anliegen nutzt.",
    "lise-de-la-salle": "Ihr ungewöhnlich früher Start – Plattenvertrag mit 13 – hat sie zu einer der am längsten aktiven Konzertpianistinnen ihrer Generation gemacht, trotz eines noch vergleichsweise jungen Alters.",
    "simone-dinnerstein": "Dass sie ihr Debütalbum komplett in Eigenregie finanzierte, war zum Zeitpunkt der Veröffentlichung höchst ungewöhnlich für die klassische Musikbranche und wird bis heute als Fallbeispiel für unabhängige Karrierewege zitiert.",
    "olga-kern": "Als Professorin an mehreren US-Musikhochschulen und künstlerische Leiterin gleich mehrerer Klavierwettbewerbe prägt sie inzwischen aktiv die nächste Generation amerikanischer Pianistinnen und Pianisten mit.",
    "clara-schumann": "Sie unterrichtete bis kurz vor ihrem Tod und bildete damit über Jahrzehnte hinweg Generationen von Pianistinnen und Pianisten aus – ihr pädagogisches Erbe ist kaum weniger bedeutend als ihre eigene Konzertkarriere.",
    "alicia-de-larrocha": "Ihre Fähigkeit, trotz kleiner Hände auch die technisch anspruchsvollsten Werke des Repertoires zu meistern, wird bis heute in der Klavierpädagogik als Beispiel dafür angeführt, dass Körperbau kein Karrierehindernis sein muss.",
    "clara-haskil": "Dass ihr internationaler Durchbruch erst nach dem 50. Lebensjahr gelang, macht ihre Karriere zu einem der bemerkenswertesten Beispiele für späten Erfolg in der Geschichte der klassischen Musik.",
    "myra-hess": "Ihre Kriegskonzerte in der National Gallery gelten bis heute als eines der eindrücklichsten Beispiele dafür, welche Rolle klassische Musik in gesellschaftlichen Krisenzeiten spielen kann.",
    "annie-fischer": "Dass sie ihre eigene Beethoven-Gesamtaufnahme jahrzehntelang zurückhielt, weil sie den eigenen Ansprüchen nicht genügte, macht sie zu einem seltenen Beispiel künstlerischer Kompromisslosigkeit gegenüber dem eigenen Werk.",
}
