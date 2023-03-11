from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC


from time import sleep
from bs4 import BeautifulSoup
import Regex


class Coletar :

    def __init__(self, nomeProduto, driver, url, nMaxPag) :
        criarArquivo = open(f'./DadosColetados/{nomeProduto}.txt', 'w', encoding='UTF-8')
        Arquivo      = open(f'./DadosColetados/{nomeProduto}.txt', 'a', encoding='UTF-8')

        Pagina = 0

        for c in range(0, nMaxPag) :

            try : 
                WebDriverWait( driver , 5 ).until(EC.url_changes(url))
                url = driver.current_url
            except :
                print('\033[1;34mSem mais paginas !!!\033[m')
                break    

            Pagina += 1
            print(f'\n\n\n\033[1;36mPagina :{Pagina}\033[m')
            
             
            Grade     = WebDriverWait( driver , 5 ).until(EC.presence_of_element_located(         (By.CSS_SELECTOR, '.shopee-search-item-result'         ) ) )
            Produtos  = WebDriverWait( Grade  , 5 ).until(EC.presence_of_all_elements_located( (By.CSS_SELECTOR, '.shopee-search-item-result__item'              ) ) )
            print(f'\n\n\n\033[1;32mTotal de produtos encontrados: {len(Produtos)}\033[m')


            for p in range(0, 60, 5) :
                driver.execute_script("arguments[0].scrollIntoView();", Produtos[p])
                sleep(0.2)
            sleep(0.5)


            Sopa = BeautifulSoup(driver.page_source, 'html.parser')
            Produtos = Sopa.find_all( attrs={'data-sqe':'item'} )

# PARA CADA PRODUTO ============================================================================================================================================================================================================
            for enum, produto in enumerate(Produtos) : 

                try:     nome = produto.find_all(recursive=False)[0].find_all(recursive=False)[0].find_all(recursive=False)[0].find_all(recursive=False)[1].find_all(recursive=False)[0].get_text()
                except : nome = '\033[1;31m NOME NÂO FOI POSSÍVEL COLETAR\033[m'


                try : 
                    preco = produto.find_all(recursive=False)[0].find_all(recursive=False)[0].find_all(recursive=False)[0].find_all(recursive=False)[1].find_all(recursive=False)[1].find_all(recursive=False)[1].get_text()
                    print(preco)
                    preco = Regex.RePreco(preco)
                    comDesconto = True

                except:
                    try :
                        preco = produto.find_all(recursive=False)[0].find_all(recursive=False)[0].find_all(recursive=False)[0].find_all(recursive=False)[1].find_all(recursive=False)[1].get_text()
                        print(preco)
                        preco = Regex.RePreco(preco)
                        comDesconto = False
                    except :
                        preco = '\033[1;31mPREÇO NÂO FOI POSSÍVEL COLETAR\033[m'
                        comDesconto = False



                
                Arquivo.write(nome+'\n')
                Arquivo.write(preco+'\n\n')

                print(f'\033[1;35m{enum+1} : \033[m')
                print( str(nome) )
                print( str(preco) + '\n' )
            

            
            
            pageController = WebDriverWait(driver, 11).until( EC.presence_of_element_located( (By.CSS_SELECTOR, '.shopee-page-controller') ) ) 
            Next = pageController.find_elements(By.TAG_NAME, 'button')[-1]
            driver.execute_script('arguments[0].click()', Next)



    
