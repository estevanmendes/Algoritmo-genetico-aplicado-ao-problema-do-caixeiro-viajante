# Algoritmos Genéritos Aplicados ao problema do Caixeiro Viajante
 
 ## O Problema do Caixeiro Viajante 

 O problema do caixeiro viajante, ou traveling salesman problem(TSP), consiste  em determinar o caminho mais eficiente entre dois pontos passando em todas N cidades no meio do caminho sem repetir. Se trata de uma problema de análise combinatória, uma vez que o caixeiro pode realizar N! caminhos. Computacionalmente seria muito custoso realizar o cálculo de todos caminhos possíveis, por exemplos, se ele tivesse que passar por 10 cidades haveriam 10!=3628800 caminhos.

<br/><br/>
 <br/><br/>
![image](/img/tsp.png=100x100)
 <br/><br/>

 



## Algoritmos Genéticos
 Os algoritmos genéticos foram inicialmente desenvolvidos na década de 60 [2] para tentar imitar a evolução, especeficamente o processo de seleção natural. O algoritmo é projetado de tal forma que faz uma pressão evolutiva para selecionar as melhores soluções a cada geração. A fim de representar esse processo da seleção natural o algoritmo é iniciado com uma população aleatória, onde os melhores indivídos (com os melhores fitness) são selecionados para reprodução que pode se dar de inúmeras formas, por último após os genes dos novos indivíduos serem selecionados um fator probabilistico pode gerar uma mutação nos genes incluindo variabilidade na população. 


### Fitness da População

Para determinar o quão bom os genes de um indivíduo são utiliza-se uma função f(x) para determinar o fitness. Os algoritmos genéticos foram idealizados para resolver problemas de maximização, no caso do problema do caixeiro viajante e de problemas de minimização definimos uma função F(x)= 1/f(x) por exemplo.

No nosso problema o fitness do indivíduo é inversamente proporcioanl a  distância total percorrida ao longo do caminho passando por todas as cidades. 

### A Roleta da Escolha dos pais

Para escolher os indivíduos que farão a reprodução é utilizado o método da roleta. Ele consiste em somar todos os fitness, gerar um número aleatoriamente dentro do intervalo [0,soma dos fitness) e escolher o indivíduo que estiver contiver o número sorteado.

Por exemplo, sejam os fitness 100,200,400. A soma dos fitness é de 700.

[0,100) -> indivíduo A é escolhido
[100,300) -> indivíduo B é escolhido
[300,700) -> indivíduo C é escolhido

Se o número sorteado for 359, o indivíduo C será escolhido para a reprodução e passará seus genes a diante

Utilizando esse método damos prioridade aos indivíduos com maior fitness, pois ele é chamado de um método de seleção proporcional. Um problema que pode surgir na utilização deste método é um indivíduo com alto fitness tomar conta da população de forma a inibir a variabilidade.


### Operadores de Crossover

Há diversos tipos de algoritmos de crossover cujo objetivo é fazer a mistura dos genes dos pais de forma aleatória preservando o conceito do problema do caixeiro viajante. Conforme demostrado no artigo referenciado abaixo [1], o operador de construção sequencial (Sequential constructive crossover operator) apresenta melhores resultados que outros dois operadores que serão implementados futuramente na classe Crossover.

#### SCRX

O Operador SCRX consiste em pegar olhar o caminhos que os dois pais fazer e ir construindo o gene dos filhos a partir das melhores carcterísticas nos dois. Por exemplo, sejam os pais [1,2,3,5,4,6,7] e [1,2,5,4,3,6,7], isto significa que o caminhos que o primeiro pai começa na cidade numero 1, depois vai para a cidade numero 2 e  assim sucessivamente. Conforme exemplificado inicia-se no primeiro nodo, em seguindo verifica-se em cada pai o primeiro nodo legítimo, isto é, aquele que ainda não foi inserido no filho. Após termos dois nodos válidos, observamos o custo, ou o fit de cada opção, aquela que tiver o melhor fit permanecerá enquanto gene do filho. Isto é feito sucessivamente até que os genes do filho estejam definidos.

Se nenhum dos pais tiver um gene válido, procuramos o primeiro gene válido na lista de todos os genes possíveis. Ou seja, vemos de forma ordenada qual a primeira cidade que não faz parte do caminho do filho.

[1,2,3,5,4,6,7] e [1,2,5,4,3,6,7] ---- filho [None,None,None,None,None,None,None]

Pai 1, Mae 1 - filho [1,None,None,None,None,None,None]
Pai 2, Mae 2 - filho [1,2,None,None,None,None,None]
Pai 3(fit=50), Mae 5(fit=70) - filho [1,2,5,None,None,None,None]
Pai 4, Mae 4 - filho [1,2,5,4,None,None,None]
Pai 6(fit=40), Mae 3(fit=70) - filho [1,2,5,4,3,None,None]
Pai 6, Mae 6 - filho [1,2,5,4,3,6,None]
Pai 7, Mae 7 - filho [1,2,5,4,3,6,7]
filho [1,2,5,4,3,6,7]


### Mutação



## Guia Rápido do Código 

Há duas classes no programa a primeira detem a estrutura fundamental para um tipo de tratamento dos algoritmos genéticos, a segunda contém os operadores que realizam o crossovers nos arrays fazendo o cruzamento entre os pais. 

### Genetic algorithm

#### Atributos

#### Métodos 


### Crossover

#### Atributos

#### Métodos 


## Referências

[1] [Ahmed, Zakir. (2010). Genetic Algorithm for the Traveling Salesman Problem using Sequential Constructive Crossover Operator. International Journal of Biometric and Bioinformatics. 3. 10.14569/IJACSA.2020.0110275.](https://www.researchgate.net/publication/41847011_Genetic_Algorithm_for_the_Traveling_Salesman_Problem_using_Sequential_Constructive_Crossover_Operator) 

## Comentários

O presente código foi inicialmente desenvolvido para ser o trabalho final da matéria [Métodos Computacionais em Física II](). Além do código um [relatório](/pdf/relatorio.pdf) foi produzido, e pode ser encontrado na pasta pdf.