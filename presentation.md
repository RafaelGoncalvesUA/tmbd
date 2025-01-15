Movie recommendations are vital in enhancing user experience and satisfaction by helping individuals discover content aligned with their preferences, saving time, and avoiding decision fatigue. For streaming platforms, effective recommendation systems drive user engagement, retention, and revenue by promoting personalized content. They also encourage the discovery of lesser-known titles, boosting viewership diversity. Beyond individual benefits, these systems optimize platform resources by showcasing content with higher relevance, thus increasing efficiency. In an era of overwhelming content choices, movie recommendations play a critical role in connecting users with entertainment that resonates with their tastes, fostering enjoyment and loyalty to the platform.

Volume:
A potentially large amount of data is produced and published through a Kafka topic (movielens), representing new added movies.
The proposed solution is meant to be scalable. For instance, the data to be processed is accumulated in a buffer with limited size.

Velocity:
There is a consumer that processes streaming data in real time and triggers model retraining whenever the data buffer is full.

Variety:
Movie descriptions are unstructured data and require vectorisation to be fed into the model.

Low Veracity:
Movie descriptions may have ambiguous or misleading information, which can affect the categorisation process.




Bom dia a todos.
O nosso projeto consiste numa pipeline end-to-end para um sistema de recomendação de filmes. O intuito aqui era aplicar alguns dos métodos de Big Data / IA aprendidos nas aulas ou aprendidos de forma autónoma.

Dentro dos sistemas de recomendação, obviamente há várias abordagens possíveis. Neste caso, optámos por uma abordagem baseada no conteúdo, recorrendo a técnicas de processamento de linguagem natural (NLP) para analisar as descrições dos filmes e os categorizar. A partir da lista de categorias de um filme, aplicamos Machine Learning clássico para prever a classificação que um utilizador daria, com base nas suas preferências. Por exemplo, se o filme é de comédia e o utilizador gosta de comédia, o rating será perto de 5.

Para colocar esta solução de software em produção, há ainda 3 variáveis a considerar: o processamento de novos filmes em tempo real, o retreino do modelo de NLP e o deployment contínuo do mesmo, através de uma REST API.

Como infraestrutura subjacente, temos um Raspberry Pi 5 que conta com várias tecnologias: o próprio Docker, o Scikit, o Tensorflow e o Apache Kafka, que nos permite publicar e subscrever streams de dados em tempo real.

Finalmente, utilizámos o MovieLens, já que é um dataset de referência na literatura.

Tudo isto é pertinente para Big Data.
1º a nossa solução está preparada para um elevado volume de dados. As descrições dos filmes são acumuladas num buffer com tamanho limitado. Quando este enche, o modelo é fine-tuned.
2º velocity: estamos a processar streams de dados.
3º variety: as descrições dos filmes são dados não estruturados, que precisam de ser vertorizados para poderem ser usados no modelo.
4º veracity: muitas vezes estes textos podem conter termos ambíguos ou enganosos, o que pode afetar o processo de categorização.

Olhando agora de uma forma geral para a arquitetura da solução,
todos os componentes desenvolvidos foram dockerizados e orquestrados com o Docker Compose, bem como o próprio Apache Kafka e a dependência Zookeeper (que ajuda na sincronização dos brokers, se não me engano).
Isto contribui para a portabilidade e escalabilidade da solução, visto que todas as dependências estão encapsuladas em containers.

Como ponto de partida da pipeline, temos um modelo pré-treinado para um conjunto limitado de filmes, e um produtor que publica novos filmes no tópico 'movilens' do Kafka.
O consumidor, por sua vez, subscreve este tópico e acumula os novos filmes num buffer. Chegado a um certo limite, como referi, o modelo é fine-tuned e é guardado num volume partilhado por todos os containers.

Em paralelo, há uma REST API em Flask com um endpoint que recebe a descrição de um filme e opcionalmente um perfil de utilizador, e retorna as categorias e o rating estimado.

Todos estes serviços correm em paralelo e de forma separada. Além do kafka, a única "comunicação" entre eles é feita através do volume partilhado onde é guardado o modelo.