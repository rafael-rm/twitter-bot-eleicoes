import requests
import tweepy
import dotenv
import os
from time import sleep


# Carregando as variáveis de ambiente
dotenv.load_dotenv(dotenv.find_dotenv())
access_token_dot = str(os.getenv("ACESS_TOKEN"))
access_token_secret_dot = str(os.getenv("ACESS_TOKEN_SECRET"))
consumer_key_dot = str(os.getenv("CONSUMER_KEY"))
consumer_secret_dot = str(os.getenv("CONSUMER_SECRET"))

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

            NUMERO_CANDIDATOS_EXIBIR = 2

            # Verificar tamanho da lista
            quantidade_candidatos = len(data['cand'])
            if quantidade_candidatos < NUMERO_CANDIDATOS_EXIBIR:
                print('A quantidade de candidatos não coincide com o tamanho do looping para criação do post.')
                print('Verifique o tamanho da lista de candidatos e o looping.')
                break

            # Novo post a ser enviado
            post_enviar = f'📊 Resultados das eleições 2022\nDados atualizados em {data["dg"]} às {data["hg"]}h\n\n'
            for i in range(0, NUMERO_CANDIDATOS_EXIBIR):
                num_votos = data["cand"][i]["vap"]
                num_votos = int(num_votos)
                post_enviar = post_enviar + f'{data["cand"][i]["nm"]} - {num_votos:,} - {data["cand"][i]["pvap"]}%\n'
            post_enviar = post_enviar + f'\nUrnas apuradas: {data["psi"]}%'

            num_urnas_ap = data["psi"]
            num_urnas_ap = float(num_urnas_ap.replace(',', '.'))

            if (post_enviar == ultimo_post):
                print("O ultimo post é igual ao post a ser enviado")
            else:
                api.update_status(post_enviar)
                print('Post enviado com sucesso.')
                print('Conteúdo:\n\n' + post_enviar)
                if(data['psi'] == '100,00'):
                    print('\n\nEleições finalizadas, todas as urnas apuradas. Aplicação encerrada.')
                    break

            if (num_urnas_ap >= 99):
                print(f'\nAgurdando 20 minutos para o próximo post, pois o número de urnas apuradas é maior que 99% ({num_urnas_ap}%).')
                sleep(1200) # 20 minutos caso as urnas estejam com 99% ou mais apuradas
            elif (num_urnas_ap <= 96):
                print(f'\nAgurdando 5 minuto para o próximo post, pois o número de urnas apuradas é menor que 96% ({num_urnas_ap}%).')
                sleep(300) # 5 minutos caso o número de urnas apuradas seja menor que 96
            else:
                print(f'\nAgurdando 10 minutos para o próximo post, pois o número de urnas apuradas é entre 96% e 99% ({num_urnas_ap}%).')
                sleep(600) # 10 minutos caso o número de urnas apuradas seja maior que 96 e menor que 99

        except Exception as e:
            print("Erro durante a execução do programa, tentando novamente em 30 segundos. \nErro: " + str(e))
            sleep(30) # Delay de 30 segundos para tentar novamente em caso de erro
        

if __name__ == "__main__":
    main()