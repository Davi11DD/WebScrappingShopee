from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC


class RemoverPopUp :
    def __init__(self, driver) :
        try : 
            body =  WebDriverWait( driver , 3 ).until(EC.presence_of_element_located( (By.TAG_NAME, 'body') ) )
            popUp = WebDriverWait( driver , 3 ).until(EC.presence_of_element_located( (By.TAG_NAME, 'shopee-banner-popup-stateful') ) )
            driver.execute_script('arguments[0].remove()', popUp)
            driver.execute_script('arguments[0].removeAttribute("class")', body)
            print('\033[1;32mPopUp Removido\033[m')

        except : 
            print('\033[1;33mSem popUp na tela inicial :)\033[m ')
