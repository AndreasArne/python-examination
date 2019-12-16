---
author:
    - aar
    - efo
revision:
    "2018-12-10": (B, aar,efo) Skapade examination.
    "2018-09-26": (A, efo) individuella examinationen 2018-lp2.
...
Individuell examination
==================================

Denna individuella examination består av fem uppgifter. De olika uppgifterna förklaras nedanför och varje uppgift ska lösas i filen "exam.py" i en specifik fördefinierad funktion.

För alla uppgifter du löser, uppdatera funktionens docstring (kommentaren längst upp i funktionen) till en relevant kommentar om vad funktionen gör.

Du kan när du vill under hela examinationen köra kommandot `dbwebb exam correct try2` för att rätta dina lösningar och se hur många poäng du har uppnått.

Utöver att lösa uppgifterna behöver du se till att alla filer valideras med `dbwebb validate try2`.

Du har 5 timmar på dig att lösa uppgifterna och publicera dina lösningar med kommandot `dbwebb exam seal try2` inom tidsramen. Den sista `seal` som görs inom tidsramen är den som kommer användas som betygsunderlag.

**För att få godkänt på examinationen måste du klara uppgift 1.**

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

1. **Repetera text**. Denna uppgiften går ut på att du ska repetera text från text filen `repetition.txt`. Filen består strängar och heltal separerade på olika rader. Ditt program ska läsa filen rad för rad alla strängar som efterföljer varandra ska konkateneras till en sträng. När du kommer till en rad med ett heltal ska du skriva ut sträng som har byggts upp lika många gånger som heltalet. Repetitionerna ska separeras med ett komma och ett mellanslag och hela utskriften ska avsluta med en punkt.

    **Exempel**:  
    input:  
    Apa  
    på  
    en  
    gata  
    3  
    output:  
    Apa på en gata, Apa på en gata, Apa på en gata, Apa på en gata.

    Gör inga extra `print()` i din lösning förutom de som efterfrågas i kravspecifikationen.

2. **Konvertera RGB till HEX**. Den här uppgiften går ut på att du ska konvertera ett RGB värde till en HEX kod. Din funktion ska ta en tuple med tre värden som input. Du ska nu konvertera varje värde till ett hexadecimalt tal, 2 karaktärer, och lägga ihop dem till en HEX kod. En HEX börjar alltid med "#", formatera koden enligt `#ffaa00`, "ff" är hex värdet för första talet i tuplen, "aa" det andra värdet och "00" det tredje.

    **Exempel**:  
    input: (255, 99, 71)  
    output: `#ff6347`

3. **Poäng beräkning**.  Du ska räkna ut hur många poäng deltagarna i ett spel har. Din funktion tar emot en sträng som innehåller små och stora bokstäver. En liten bokstav innebär att spelaren med den bokstaven har fått ett poäng. En stor bokstav betyder att spelaren med den bokstaven har förlorat ett poäng. Utskriften ska vara sorterad på antal poäng som respektive spelare har uppnåt. Separera varje spelare med ett komma och ett mellanslag. Separera spelarens bokstav och poäng med ett kolon, se exempel.

    **Exempel**:  
    input: dbbaCEDbdAacCEAadcB  
    output: b:2, d:2, a:1, c:0, e:-2  

4. **Hitta saknade heltal**. Du ska skriva ett program som tar emot en lista med heltal, ditt program ska returnera en lista med de heltal som saknas i talföljden från argument listan. Listan som returneras ska vara sorterad i stigande ordning.
    **Exempel**
    input: [2,4,6,3,8,7]
    output: [5]
    input: [42, 46, 47, 48, 43]
    output: [44, 45]

5. **Analysera datum och tider**. Den här uppgiften går ut på at du ska ska plocka ut giltiga datum och tider från texten i filen "value-of-time.txt". Funktionen `validate_date_time` ska innehålla en while-loop som tar emot input från användaren. Loopen ska avslutas om användaren skriver "q" eller "quit", när programmet avslutas ska funktionen returnera sant, True. Gör inga extra `print()` i din lösning förutom de som efterfrågas i kravspecifikationen.
    - Om användaren skriver "d" eller "date" som input ska alla korrekta datum i filen skrivas ut med `print()`. Separera alla datum med ", ". Där ska inte vara något ", " sist i utskriften.
    - Om användaren skriver "t" eller "time" som input ska alla korrekta tider skrivas ut med `print()`. Separera alla datum med ", ". Där ska inte vara något ", " sist i utskriften.<br><br>

 Funktionen `validate_date_time` ska enbart innehålla while-loopen som tar inputs och if-satsen för valen. Övriga funktioner ska ligga i en ny modul som du även ska skapa. Modulen ska heta `date_time_functions.py`, det ska finns minst en funktion för datum och en för tid. Om användaren skriver ett ej giltigt argument ska "Not an option!" skrivas ut.
    Ett giltigt datum följer [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format, dvs. yyyy-mm-dd, ex. 2018-09-05. Ni kan räkna med att alla månader har 31 dagar.
    En giltig tid följer formatet hh:mm, ex. 08:09.

