import requests
import tweepy
import dotenv
import os
from time import sleep

# Carregando as variáveis de ambiente
dotenv.load_dotenv(dotenv.find_dotenv())
access_token_dot = os.getenv("ACESS_TOKEN")
access_token_secret_dot = os.getenv("ACESS_TOKEN_SECRET")
consumer_key_dot = os.getenv("CONSUMER_KEY")
consumer_secret_dot = os.getenv("CONSUMER_SECRET")
webhook_url_dot = os.getenv("WEBHOOK_URL")

access_token_dot = str(access_token_dot)
access_token_secret_dot = str(access_token_secret_dot)
consumer_key_dot = str(consumer_key_dot)
consumer_secret_dot = str(consumer_secret_dot)

# Autenticação
auth = tweepy.OAuthHandler(consumer_key_dot, consumer_secret_dot)
auth.set_access_token(access_token_dot, access_token_secret_dot)
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Autenticação bem sucedida")

except Exception as e:
    print("Erro durante a autenticação\n")
    print(e)



# Função main
def main():

    while True:

        try:
            timeline = api.user_timeline()
            if len(timeline) > 0:
                ultimo_post = timeline[0].text
            else:
                ultimo_post = ''

            # Requisição do JSON nos servidores da justiça eleitoral
            url = 'https://resultados.tse.jus.br/oficial/ele2022/544/dados-simplificados/br/br-c0001-e000544-r.json'
            r = requests.get(url)

            # Transformando o JSON em um dicionário
            data = r.json()

            # Novo post a ser enviado
            post_enviar = f'📊 Resultados das eleições 2022\nDados atualizados em {data["dg"]} às {data["hg"]}h\n\n'
            for i in range(0, 4):
                num_votos = data["cand"][i]["vap"]
                num_votos = int(num_votos)
                post_enviar = post_enviar + f'{data["cand"][i]["nm"]} - {num_votos:,} - {data["cand"][i]["pvap"]}%\n'

            post_enviar = post_enviar + f'\nUrnas apuradas: {data["psi"]}%'
            if (post_enviar == ultimo_post):
                print("O ultimo post é igual ao post a ser enviado")
            else:
                api.update_status(post_enviar)
                print('Post enviado com sucesso.')
                print('Conteúdo:\n\n' + post_enviar)
                if(data['psi'] == '100,00'):
                    print('\n\nEleições finalizadas, todas as urnas apuradas. Aplicação encerrada.')
                    break
                print('\nAguardando 5 minutos para o próximo post.')

        except Exception as e:
            print("Erro durante a execução do programa, tentando novamente em 30 segundos. \nErro: " + str(e))
            sleep(30) # Delay de 30 segundos para tentar novamente em caso de erro
        
        sleep(300) # Delay de 5 minutos (300 segundos) para tentar novamente em caso de erro

if __name__ == "__main__":
    main()