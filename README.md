
# twitter-bot-eleicoes

twitter-bot-eleicoes é uma aplicação que realiza postagens periódicas contendo a apuração em andamento do TSE.


## Demonstração

![imagem](https://i.imgur.com/JUlFiUF.png)
## Instalação

Para rodar a aplicação é necessário instalar as seguintes bibliotecas:

```bash
    pip install tweepy
    pip install python-dotenv
```
## Variáveis de Ambiente

As seguintes variáveis de ambiente devem ser preenchidas no .env

`API_KEY`

`API_KEY_SECRET`

`ACESS_TOKEN`

`ACESS_TOKEN_SECRET`

Para obter estas chaves é necessário criar uma
[conta de desenvolvedor](https://developer.twitter.com/en/portal/dashboard) no twitter

**Observação:** É necessário 
[solicitar acesso elevado](https://developer.twitter.com/en/portal/products/elevated) a API.
## FAQ

#### 1- Onde posso obter a API contendo a apuração de votos do TSE?

Até o presente momento da criação da aplicação, podemos obter a **URL da API**
abrindo a página de resultados do TSE abrindo o console do navegador:

![imagem2](https://i.imgur.com/gLne5ln.png)

#### 2- A aplicação realiza postagens iguais?

Não, a aplicação realiza uma verificação e caso o conteúdo da API seja igual o do 
último post uma nova postagem não é realizada.

#### 3- A cada quanto tempo a aplicação tenta realizar uma nova postagem?

Inicialmente uma tentativa de postagem é realizada a cada 5 minutos. 
Quando a quantidade de urnas apuradas chega a 96% o cooldown é alterado para 10 minutos.
Ao atingir 99% o cooldown é elevado para 20 minutos, podendo atingir até 1 hora conforme a apuração chega ao fim.

## Licença

[MIT](https://choosealicense.com/licenses/mit/)

