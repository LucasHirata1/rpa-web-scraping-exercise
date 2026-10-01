Desafio Técnico de Automação 20h

Os textos a partir daqui vão registrar o que eu estava pensando no momento. Em uma tentativa de explicar o que estou pensando, vou realizar comentários, junto dos códigos que utilizei. Como estudo Engenharia de Produção, peço desculpas caso utilize algum termo de maneira errônea ou equivocada.

Neste primeiro momento, estarei utilizando de uma IA para me auxiliar com a plataforma GITHUB e com as instalações. Após avaliar o desafio com meus conhecimentos e desenvolver a solução, irei utilizar da IA para sofisticar minha solução, se eu identificar melhorias.


1. Enquanto leio o enunciado, pauso por um momento para verificar como funcionam as categorias e páginas. Percebi alguns pontos na URL:
	- Não notei a diferença entre "https://books.toscrape.com/index.html" e "https://books.toscrape.com/catalogue/category/books_1/index.html", além do título "Books" e endereço "Home / Books".
	- Para a primeira página, a URL primeiro aparece com o final "...index.html", porém ao avançar para a segunda e retroceder para a primeira, o final é alterado para "...page-1.html".
	- As categorias estão indexadas conforme sua posição na lista da esquerda, sendo a primeira posição "books" e a última "crime".
	- Os livros estão indexados conforme sua disposição em "Books" ou "All Products", sendo esta contagem decrescente, começando pelo 1000 "A Light in the Attic", até o 1 "1,000 Places to See Before You Die".
	- O endereço para a visualização do livro segue o padrão "Home / Books / Category / Title", o que me faz pensar que cada livro aparece apenas em uma categoria.
	
2. Sobre os test cases, fiquei com algumas dúvidas:
    - Não definir `max_books` no comando `uv run scrape-books`, significa `max_books` deve ser o maior possível ou igual a 0?
    (Ps: Fiz esse teste e descobri que `max_books` fica igual a 30 como default e confirmei isso lendo o código do main.py)
    - Definir o número da página também será uma das opções da função?(Ex. pegar todos os livros da pagina X)

3. Primeira lógica:
    a. primeiro tratar os casos em que não precisa fazer scrape, apenas retornar uma lista vazia
        - PRIMEIRA CONDIÇÃO: `max_books` <= 0
        - SEGUNDA CONDIÇÃO: `category` não existe na lista
    b. definir o URL para scrape (se vão ser todas as categorias alguma em específico)
    c. definir o número máximo de páginas
    d. para cada página, recolher as informações necessárias de cada livro da página e adicionar na lista que será entregue
    e. Retornar lista.

4. Depois de aprender a usar as funções, muitos testes e usar "CTRL+SHIFT+C", consegui criar a lista das categorias

5. Preciso validar se é possível extrair as informações dos livros pela pagina das categorias, ou se vou ter que entrar dentro da página de cada livro para obter as informações.

6. Nao entendi muito bem o porque do erro ao tentar atualizar a variável URL. De qualquer forma, criar outra variável chamada newURL funcionou. (Aparentemente jogar a linha que define URL la no começo, dentro da função, corrige o erro de atualizar)

7. Vou precisar montar uma lógica para avançar as páginas e acrescentar todos os livros em uma só lista.

8. Descobri este método `locator.clicl()`. Pelo código, me parece que é melhor (pelo menos mais simples) do que o método do `page.goto(url)` que eu estava usando. Na minha visão, como o método `page.goto(url)` requer que eu armazene e trate os dados da página, enquanto o `locator.clicl()` não. Contudo, não irei alterar a lógica da escolha das categorias, pois não consigo pensar em um método para salvar uma coordenada precisa de um elemento (um valor que eu consiga usar o locator uma vez e chegar exatamente no elemento que eu quero).

8. Eu tinha reparado que ao final da página de cada livro tem uma sessão chamada `Products you recently viewed`. Agora que estou entendendo mais sobre como localizar os elementos, imagino que esta funcionalidade sirva para gerar erros nos códigos em que o elemento está mal localizado. 
Estou certo? Lembrar de perguntar

9. Cheguei na parte de registrar o restante das informações dos livros e enquanto estudava o como registrar os livros como `BookData`, percebi que meu código não está seguindo a especificação **5- Type hints**. Acredito que posso tentar copiar o formato para todas as variáveis que criei, mas talvez eu tenha que pedir para a IA analisar estas falhas e adaptar qualquer pedaço do código que esteja fora de especificação.

10. Para fazer a lista de livros, pensei na possibilidade de requerir um número maior do que o número de livros para aquela categoria. Por isso, criei a variavel `newmax_books`.

11. Não consegui achar um livro que não estivesse em estoque, para criar uma regra. Então vou considerar qualquer valor diferente do formato `In stock (x available)` como fora de estoque.

12.
    




