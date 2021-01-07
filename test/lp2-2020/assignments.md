Authors:
    - aar, Andreas Arnesson
Revisions:
    - "2020-01-04": (A, aar) Skapad inför lp2 HT20.


Individuell examination (try2)
==================================

Denna individuella examination består av fem uppgifter. De olika uppgifterna förklaras nedanför och varje uppgift ska lösas i filen "exam.py" i en specifik fördefinierad funktion.

Om det inte står i en uppgift att en modul ska importeras får man **inte** använda sig av importerade moduler/biblioteket.

Du kan när du vill under hela examinationen köra kommandot `dbwebb exam correct try2` för att rätta dina lösningar och se hur många poäng du har uppnått.

Utöver att lösa uppgifterna behöver du se till att alla filer validera med `dbwebb validate try2`.

Du har 5 timmar på dig att lösa uppgifterna och publicera dina lösningar med kommandot `dbwebb exam seal try2` inom tidsramen. Den sista `seal` som görs inom tidsramen är den som kommer användas som betygsunderlag.

**För att få godkänt på examinationen måste du få minst 20 poäng**

Följande tabell används vid bedömning av den individuella examinationen.

| Bedömningspunkt | Poäng | Din poäng |
|-----------------|-------|-----------|
| Uppgift 1 är implementerad och fungerar enligt specifikationen. | 20 | |
| Uppgift 2 är implementerad och fungerar enligt specifikationen. | 10 | |
| Uppgift 3 är implementerad och fungerar enligt specifikationen. | 10 | |
| Uppgift 4 är implementerad och fungerar enligt specifikationen. | 10 | |
| Uppgift 5 är implementerad och fungerar enligt specifikationen. | 10 | |
| TOTALT | 60 | |

Tillsammans med kursmoment 01-06 ger dessa poäng ditt slutbetyg, [Bedömning och betygsättning](http://dbwebb.se/kurser/faq/bedomning-och-betygsattning-individuell).


Uppgifter
---------------------------------

1. **Repetera text**. Fyll i funktionen `text_repetition`. Denna uppgiften går ut på att du ska läsa upp och repetera text från filen `repetition.txt`. Filen består av strängar och heltal separerade på olika rader. Ett tips är att öppna filen och bekanta sig med strukturen. Ditt program ska läsa filen rad för rad, alla strängar som efterföljer varandra ska konkateneras till en sträng med ett mellanrum mellan strängarna. **När** du kommer till en rad med ett heltal ska du skriva ut strängen som har byggts upp, lika många gånger som heltalet. Repetitionerna ska separeras med ett komma och ett mellanslag och hela utskriften ska avsluta med en punkt. Gör inga extra `print()` i din lösning förutom de som efterfrågas i kravspecifikationen.

    **Exempel**:

    input:
        Apa
        på
        en
        gata
        3

    output:
        Apa på en gata, Apa på en gata, Apa på en gata.



2. **Konvertera RGB till HEX**. Fyll i funktionen `convert_to_hex`, den ska ta emot en tuple med tre element som argument. Du ska nu konvertera varje element till ett hexadecimalt tal, 2 karaktärer, och lägga ihop dem till en HEX kod. En HEX kod börjar alltid med "#", formatera koden enligt `#ffaa00`, "ff" är hex värdet för första talet i tuplen, "aa" det andra värdet och "00" det tredje. Använd funktionen `hex()` för att göra om ett heltal till ett HEX tal.

    **Exempel**:  
    input:
        (255, 99, 71)  
    output:
        `#ff6347`



3. **Hitta ord**. Fyll i funktionen `find_words`. Funktionen tar emot två stycken argument. En sträng med karaktärer och en lista med ord. Funktionen ska returnera det längsta ordet från listan där alla bokstäver som finns i ordet också finns i strängen. Om en bokstav finns två gånger i ett ord måste bokstaven även finnas två gånger i strängen för att ordet ska räknas som en matchning.

    **Exempel**:
        input:
            "abplee", ["able", "ale", "apple", "kangaroo"]

        output:
            "able"

        input:
            "abppplee", ["able", "ale", "apple", "kangaroo"]

        output:
            "apple"


4. **Hitta saknade bokstäver**. Funktionen `missing_letters` tar emot en lista med bokstäver som argument, a-z, funktionen ska returnera en lista med de bokstäver som saknas i bokstavsföljden från argumentlistan. Listan som returneras ska vara sorterad i bokstavs ordning.

    **Exempel**

    input:
        ["a", "b", "d"]
    output:
        ["c"]

    input:
        ["p", "r", "s", "t", "v"]
    output:
        ["q", "u"]



5. **Räkna skottdagar**. Funktionen `leap_days` tar emot två år och ska räkna ut antalet skottdagar (29:e februari) som inträffar mellan den 1:e januari från det första året och den 1:e januari det andra året. Uträkningen ska utgå från "The Revised Julian Calendar", där ett år har en skottdag om följande är sant:
    - År som är jämt delbara med 4.
    - Undantag: År som är jämt delbara med 100 är inte skottår.
    - Undantag till undantaget: År där resten av division med 900 är antingen 200 eller 600 är skottår.
Till exempel är 2000 ett undantag till undantaget, 2000 dividerat med 900 är 200. Så 2000 är ett skott år.

    **Exempel**
    input:
        2000, 2001
    output:
        1

    input:
        2000, 2005
    output:
        2
