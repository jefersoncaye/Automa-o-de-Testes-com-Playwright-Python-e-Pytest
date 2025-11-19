

def test_get_by_role(page):
    '''page.goto('https://automationexercise.com/')
    page.pause()
    page.get_by_role('link', name=' Signup / Login').click()
    page.get_by_role('button', name='Login').click()'''
    page.goto('https://bootswatch.com/default/')
    page.pause()
    page.locator('#navbarColor01').get_by_role('button', name='Dropdown').click()


def test_get_by_text(page):
    page.goto('https://automationexercise.com/')
    page.pause()
    page.get_by_text('Full-Fledged practice website for').first.click()

def test_get_by_label(page):
    page.goto('https://bootswatch.com/default/')
    page.pause()
    page.get_by_label('Valid input', exact=True).fill('Teste')
    page.get_by_label("Recipient's username", exact=True).fill('Teste')


def test_get_by_placeholder(page):
    page.goto('https://automationexercise.com/login')
    page.pause()
    page.get_by_placeholder('Name').fill('Teste')

def test_get_by_title(page):
    page.goto('https://bootswatch.com/default/')
    page.pause()
    page.get_by_title('Source Title').nth(1).click()


def test_locator_css(page):
    page.goto('https://automationexercise.com/')
    page.pause()
    page.locator('#accordian .panel-title').first.click()

def test_locator_xpath(page):
    page.goto('https://automationexercise.com/login')
    page.pause()
    page.locator('//*[@id="form"]/div/div/div[1]/div/form/button').click()
