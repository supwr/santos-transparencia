## Santos Transparência

Projeto open source que visa permitir um melhor entendimento e leitura de informações disponibilizadas pela prefeitura de Santos-SP, no seu [portal de transparência](http://www.santos.sp.gov.br/?q=portal/transparencia).

### Detalhes do projeto

- Desenvolvido em Março/2019 por Marcelo Rodrigues (marcelo@capybara.com.br);
- Este projeto utiliza Python 3, scrapy, flask e sqlite;
- Inicialmente desenvolvido para extrair, do portal de transparência da prefeitura de Santos, dados de contratos, locações e convênios;
- Sinta-se livre para forkar este projeto, criando melhorias e correções. A idéia é dar sentido aos dados disponibilizados pela prefeitura, permitindo ao cidadão ter uma melhor idéia de como está sendo feita a administração da cidade.  

### Como usar


#### Excutando o scraper

- Inicie instalando um virtual environment(virtualenv), assim as dependencias do projeto ficarão contidas somente á ele;
- Clone o projeto;
- Dentro do diretório do projeto ative o virtualenv:
```sh
source venv\bin\activate 
```
- Instale os pacotes do projeto:
```sh 
pip install -r requirements.txt 
```
- Entre na pasta santos-transparência e execute o arquivo *santos-transparencia.py*;
- Os arquivos baixados, em formato csv ficarão disponíveis nas pastas *contratos, locacoes e convenios*.

#### Visualizando os dados

- Após a execução do scraper, acesse a pasta *site/app* e execute o arquivo *main.py*
```sh
python main.py
```
