from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by   import By

from Esperas import *
from bs4 import BeautifulSoup
from time import sleep
from RegexCode import *
import time

class Coletar :

    def __init__(self, produto, driver, url, preco_min, preco_max, nPaginas):
        self.driver = driver
        self.preco_min = preco_min
        self.preco_max = preco_max
        self.nPaginas  = nPaginas
        self.tempoPorPagina = []
        self.ProdutosTotais = 0
        self.produtosAramzenados  = 0
        self.produtosNaoColetados = 0
        self.produtosComDesconto  = 0

        self.nomesList  = []
        self.precosList = []
        self.linksList  = []


        WebDriverWait( driver , 5 ).until(EC.url_changes(url))

        open(f'./Versao_2/DadosColetados/Geral_{produto}.txt', 'w', encoding='UTF-8')
        open(f'./Versao_2/DadosColetados/{produto}.txt', 'w', encoding='UTF-8')
        self.Arquivo = open(f'./Versao_2/DadosColetados/{produto}.txt', 'a', encoding='UTF-8')
        
        for pagina in range( 1, nPaginas+1 ) : # PAGINAÇÃO ======================================= <>

            inicio = time.time() # INICIO ----------------------------------------------------------------------------------------------------------- >

            WebDriverWait( driver , 5 ).until(EC.url_changes(url))
            url = driver.current_url
            print(f'\033[1;33mPagina : {pagina}\033[m')
        
    

            Grade     = EspereUmPorCss    ( driver , '.shopee-search-item-result'       )
            Elementos = EspereMuitosPorCss( Grade  , '.shopee-search-item-result__item' )
            print(f'\033[1;36mNúmero total de elemetos encontrados : \033[1;32m{len(Elementos)}\033[m' ) # NUMERO DE ELEMENTOS -------------------------------- >

            self.verProdutos(Elementos)
            self.guardarProdutos()



            pageController = WebDriverWait(driver, 11).until( EC.presence_of_element_located( (By.CSS_SELECTOR, '.shopee-page-controller') ) ) 
            Next = pageController.find_elements(By.TAG_NAME, 'button')[-1]
            driver.execute_script('arguments[0].click()', Next)

            fim = time.time() # FIM ----------------------------------------------------------------------------------------------------------------- <
            print(f'\033[1;33mTempo total para armazenar essas informações dessa pagina: \033[1;32m{fim - inicio:.2f}s\033[m\n\n\n')
            self.tempoPorPagina.append(fim-inicio)

            # =================================================================================== </>
        
        with open(f'./Versao_2/DadosColetados/Geral_{produto}.txt', 'a', encoding='UTF-8') as Geral :
            Geral.write(f"""
Preço mínimo :            {preco_min}  
Preço máximo :            {preco_max}
Produtos Encontrados :    {self.ProdutosTotais}
Produtos Armazenados :    {self.produtosAramzenados}
Produtos não coletados  : {self.produtosNaoColetados}
Produtos com Desconto   : {self.produtosComDesconto}\n
Numero total de páginas : {pagina}\n                     """)

            for a, p in enumerate( self.tempoPorPagina ) :
                Geral.write(f'\nTempo de coleta da página {a+1} : {p:.2f}s')


# VER PRODUTOS =================================================================================================================================
    def verProdutos(self, produtos) :
        print('\033[1;34mCarregando informações...\033[m')
 
        for p in range(0, 60, 1) :  
            self.driver.execute_script("arguments[0].scrollIntoView();", produtos[p])
            sleep(0.05)

  

# ARMAZENAR =================================================================================================================================

    def guardarProdutos(self) :

        Sopa = BeautifulSoup(self.driver.page_source, 'html.parser')
        Produtos = Sopa.find_all( attrs={'data-sqe':'item'}        ) 

        for produto in Produtos :
            naoColetado = False
            ComDesconto = False

            self.ProdutosTotais += 1

            try : 
                link = produto.find_all(recursive=False)[0].get('href')
            except :
                link = '\033[1;31mNÂO FOI POSSÍVEL COLETAR O lINK\033[m'

            try:    
                nome = produto.find_all(recursive=False)[0].find_all(recursive=False)[0].find_all(recursive=False)[0].find_all(recursive=False)[1].find_all(recursive=False)[0].get_text()
            except : 
                nome = '\033[1;31mNÂO FOI POSSÍVEL COLETAR O NOME\033[m'
                

            try : 
                    preco = produto.find_all(recursive=False)[0].find_all(recursive=False)[0].find_all(recursive=False)[0].find_all(recursive=False)[1].find_all(recursive=False)[1].find_all(recursive=False)[1].get_text()
                    preco = RePreco(preco)
                    ComDesconto = True

            except  :
                try :
                    preco = produto.find_all(recursive=False)[0].find_all(recursive=False)[0].find_all(recursive=False)[0].find_all(recursive=False)[1].find_all(recursive=False)[1].get_text()                   
                    preco = RePreco(preco)
                   
                except :
                    preco = -1
                    self.produtosNaoColetados += 1
                    naoColetado = True


            #print( str(nome) )
            #print( str(preco) + '\n' )


            if (self.preco_min <= int(preco) <= self.preco_max) and (naoColetado == False) : 
                self.Arquivo.write(f'{nome}\n')                           # NOME
                self.Arquivo.write(f'{preco}\n')                          # PREÇO
                self.Arquivo.write('https://shopee.com.br'+link+'\n\n') # LINK

                self.nomesList.append(nome)
                self.precosList.append(preco)
                self.linksList.append(link)




                if ComDesconto == True : self.produtosComDesconto += 1
                self.produtosAramzenados += 1


        
        print(f'\033[1;31mPRODUTOS NÃO COLETADOS : {self.produtosNaoColetados}\033[m')

       


        def NomesList(self)  :
            return self.nomesList
        

        def PrecosList(self) :
            return self.precosList
        
        
        def LinksList(self)  :
            return self.linksList


