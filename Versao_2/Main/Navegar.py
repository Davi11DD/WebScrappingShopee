from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by   import By

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
import time

import PopUp
import Esperas
import Coleta



# INICIAL CONFIGS ============================================================================================
chromeService = Service(ChromeDriverManager().install())
chormeOptions = Options()
chormeOptions.add_argument('--window-size=800,600')



# DRIVER =====================================================================================================

def Navegue(produto, preco_min=0, preco_max=99999, nPaginas=5) :

    inicio = time.time()
    url = 'https://shopee.com.br/'
    driver = webdriver.Chrome(service=chromeService, options=chormeOptions)
    driver.get(url)

# PAGINA INICIAL =============================================================================================

    PopUp.RemoverPopUp(driver) 

    inputSearch = Esperas.EspereUmPorCss(driver, '.shopee-searchbar-input__input')
    inputSearch.send_keys(produto)
    inputSearch.send_keys(Keys.ENTER)
    print('\033[1;35mPESQUISANDO...\033[m\n')


# PAGINAS DE CONTEUDO =============================================================================================


    thisColeta = Coleta.Coletar(produto, driver, url, preco_min, preco_max, nPaginas)
    fim = time.time()

    print(f'\033[1;32mTEMPO TOTAL DE EXECUÇÃO: {fim - inicio:.2f}s\033[m')
    open(f'./Versao_2/DadosColetados/Geral_{produto}.txt', 'a', encoding='UTF-8').write(f'\n\nTempo total de execução de todo o código: {fim-inicio:.2f}s')

    print(thisColeta.nomesList)


    print('\033[1;32m< =========================== FIM =============================== >\033[m')