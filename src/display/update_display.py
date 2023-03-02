from bs4 import BeautifulSoup

def update_display(gender: str, height: float, age: int, target_url='main.html') -> str:

    soup = BeautifulSoup(open(target_url, mode='r'), 'html.parser')

    gender_value = soup.find(id='gender_value')
    gender_value.string = gender

    height_value = soup.find(id='height_value')
    height_value.string = str(height)

    age_value = soup.find(id='age_value')
    age_value.string = str(age)

    with open(target_url, 'w') as out:
        out.write(str(soup))

    return str(soup)

if __name__ == '__main__':
    update_display('Maaaaan', 1231.1, 23)