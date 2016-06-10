# twitter-mining-sentiment
Experimento na área de análise de sentimento, usando Twitter como corpus.

# Para executar aplicação em modo de avaliação:
1. Alterar arquivo APP.cfg do direitório config, mudando valor para TRUE.
2. python index.py Frequency
[Sentimento será avaliado de acordo com sua frequência]
3. python index.py Average
[Sentimento será avaliado de acordo com média do score]
4. python index.py Weight
[Sentimento será avaliado de acordo com média do score, mas será dado peso dobrado aos sentimentos negativos]

# Para executar aplicação em modo de mineração, usando os trends topics do twitter:
1. Alterar arquivo APP.cfg do direitório config, mudando valor para FALSE.
2. python index.py Frequency Positive
[Sentimento será avaliado de acordo com sua frequência, permanecendo apenas tópicos positivos nos resultados]
3. python index.py Average Positive
[Sentimento será avaliado de acordo com média do score, permanecendo apenas tópicos positivos nos resultados]
4. python index.py Weight Positive
[Sentimento será avaliado de acordo com média do score, mas será dado peso dobrado aos sentimentos negativos, permanecendo apenas tópicos positivos nos resultados]
