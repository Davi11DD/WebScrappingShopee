from selenium import webdriver
from selenium.webdriver.common.by   import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def EspereUmPorCss(area, selector) : 
    return WebDriverWait(area , 5).until(EC.presence_of_element_located( ( By.CSS_SELECTOR, selector) ) )

def EspereMuitosPorCss(area, selector) : 
    return WebDriverWait(area , 5).until(EC.presence_of_all_elements_located( (By.CSS_SELECTOR, selector) ) )