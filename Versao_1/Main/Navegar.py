# ===================================== IMPORTS ==============================================
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
import Coleta
import PopUps

# =============================== CONFIGS INICIAIS ===========================================



class navegue :
    def __init__(self, nomeProduto, nMaxPag) :
        Servico = Service(ChromeDriverManager().install())
        Opcoes  = Options()
        Opcoes.add_argument('--window-size=1500,700')
        Opcoes.add_argument('--window-position=15,15')



        # ===================================== CÓDIGO ===============================================
        driver = webdriver.Chrome(service=Servico, options=Opcoes)
        driver.get('https://shopee.com.br/')



        PopUps.RemoverPopUp(driver)

        url = driver.current_url

        inputSearch = WebDriverWait( driver , 11 ).until(EC.presence_of_element_located( ( By.CSS_SELECTOR, '.shopee-searchbar-input__input') ) )
        inputSearch.send_keys(nomeProduto)
        inputSearch.send_keys(Keys.ENTER)




        Coleta.Coletar(nomeProduto, driver , url, nMaxPag)


    

