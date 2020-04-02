## Natural Language Processing

Odločili smo se, da bomo uporabljali podatke iz 2 socialnih omrežij, Twitterja in Reddita.
Najprej smo zbrali podatke iz omrežja Reddit. Odločili smo se da bomo preučili vsebino posameznih objav. Izbrali smo si analizo ključnih besed ter ocenjevanje razpoloženja. Ker nismo imeli dostopa do dobrih učnih podatkov, dovolj znanja in časa, da bi sami implementirali zgoraj omenjeni metodi, smo poiskali rešitve, ki že obstajajo. 
Najprej smo si izbrali Googlovo storitev [Natural Language Procesing](https://cloud.google.com/natural-language/docs/), narejeno za razpoznavanje razpoloženja generičnih dokumentov ter iskanja njihovih ključnih besed. To je ustrezalo našim kriterijem, vendar smo ugotovili, da bo cena uporabe API-ja višja kot smo si predstavljali in smo zato morali po 10000 klicih poiskati alternativo. 
[stara skripta](/old_nlp/NLP_script.py), [ključne besede](/old_nlp/old_entities.json), [sentiment](/old_nlp/old_nlp.csv)
Hoteli smo poiskati rešitev, ki nam bi vračala podobne rezultate, saj smo bili z trenutnimi precej zadovoljni. Tako smo našli [Text Analysis Endpoint na RapidAPI](https://rapidapi.com/aylien/api/text-analysis?endpoint=53aa5a0ee4b0f2c975470d76).
Izkazalo se je, da je to še bolj primerno za naše podatke, saj je bil model natreniran na podlagi tweetov, ki so vsebinsko precej podobni objavam na Redditu, druga polovica naših podatkov pa bodo tweeti. 
[skripta](/nlp.py), [ključne besede](/entities.json), [sentiment](/nlp.csv), 
Z uporabo novega API-ja smo seveda naleteli na težavo kako podatke združiti. Prvotni je vračal vrednosti razpoloženja (sentiment) kot zvezne spremenljivko na interval [-1, 1] trenutni pa kot nominalno z vrednostmi {positive, neutral in negative}. Tako smo se odložili, da bomo prvotne podatke preslikali v nove vrednosti torej [-1, -0.33] negative, (-0.33, 0.33) neutral ter [0.33, 1] positive. Na srečo so bile ključne besede v enakem formatu ter smo jih lahko brez težav združili. [skripta za zrduževanje](/old_nlp/format.py)


