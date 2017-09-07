# Project Magus

## Que es el project Magus

Es un proyecto de trabajo profesional para la carrera de ingenieria en informatica de la FIUBA. El mismo busca hacer analisis
de sentimientos sobre twitter en tiempo real basado en una metodologia novedosa.

## Clasificacion

De cada tweet se pueden clasificar tantos las emociones como los sentimientos del mismo

### Emociones

Las emociones son las pequeñas unidades que conforman los sentimientos. Cada emocion tiene su contraparte:

|Emocion||Contraparte||
|:-|:-|:-|:-|
|Joy|(Alegria)|Sadness|(Tristeza)|
|Trust|(Confianza)|Disgust|(Desagrado)|
|Fear|(Miedo)|Anger|(Ira)|
|Surprise|(Sorpresa)|Anticipation|(Prevision)|

### Sentimientos

|Sentimiento||Grupo||
|:-|:-|:-|:-|
|Love|(Amor)|Happy|(Feliz)|
|Delight|(Placer)|Happy|(Feliz)|
|Pride|(Orgullo)|Happy|(Feliz)|
|Optimism|(Optimismo)|Happy|(Feliz)|
|Guilt|(Culpa)|Sad|(Triste)|
|Sentimentality|(Sentimentalismo)|Sad|(Triste)|
|Despair|(Desesperacion)|Sad|(Triste)|
|Shame|(Verguenza)|Sad|(Triste)|
|Disappointment|(Decepcion)|Sad|(Triste)|
|Remorse|(Remordimiento)|Sad|(Triste)|
|Pessimism|(Pesimismo)|Sad|(Triste)|
|Fatalism|(Fatalismo)|Sad|(Triste)|
|Alarm|(Alerta)|Angry|(Enojado)|
|Outrage|(Indignacion)|Angry|(Enojado)|
|Envy|(Envidia)|Angry|(Enojado)|
|Contempt|(Desprecio)|Angry|(Enojado)|
|Cynism|(Cinismo)|Angry|(Enojado)|
|Aggression|(Agresion)|Angry|(Enojado)|
|Anxiety|(Ansiedad)|Angry|(Enojado)|
|Submission|(Sumisión)|Indifferent|(Indiferente)|
|Dominance|(Dominacion)|Indifferent|(Indiferente)|
|Curiosity|(Curiosidad)|Indifferent|(Indiferente)|
|Morbidness|(Morbosidad)|Indifferent|(Indiferente)|
|None|(Nada)|Indifferent|(Indiferente)|

## Como colaborar

Para poder hacer hacer funcionar el proyecto, necesitamos lograr armar una base de tweets clasificados segun las emociones y sentimientos
de la persona que lo escribio. Podes colaborar de dos formas:

### Agregar tweets interesantes

Cada vez que veas un tweet que te parezca claramente clasificable, o escribiste un tweet propio que te parezca que aporta a la base,
podes agregarlo desde la seccion "add" en la [pagina web](http://magus-catalog.herokuapp.com/add). 

Los tweets personales son bastante utiles ya que uno mismo tiene bastante en claro como se sentia en el momento de escribirlo.
Los tweets escritos por uno mismo poseen un valor extra ya que en el momento de emitirlo, se conocen el estado emocional y los sentimientos. Así que cuando estés por tweetear, acordate de incluirlo acá ;-). Cuac

|Botones||
|:-|:-|
|Go Back| Sale sin agregar un tweet nuevo |
|Add| Agrega el tweet y vuelve a la pantalla principal |
|Add Another| Agrega el tweet y deja agregar un nuevo tweet |

### Clasificar tweets 

El sistema tiene una base de tweets no clasificados. Podes classificar tweets aleatorios desde la seccion classify en la [pagina web](http://magus-catalog.herokuapp.com/classify).
Si los tweets ya fueron clasificados por alguien antes, podes ver lo que opino el resto al respecto.

|Botones||
|:-|:-|
|Finish|Envia la clasificacion actual y termina|
|Next|Envia la clasificacion actual y propone un nuevo tweet|
|Skip|Descarta la clasificacion actual y propone un nuevo tweet|