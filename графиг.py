
from flask import Flask, request
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import requests
import os

app = Flask(__name__)

# Telegram Bot API token and chat ID
TG_BOT_TOKEN = '7012344017:AAGq63MZUzSbAHyC5dB26X_sKWjRvrMF6uI'
TG_CHAT_ID = '5664066382'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    contract_number = generate_contract_number()
    pdf_filename = create_pdf(data, contract_number)
    send_pdf_to_telegram(pdf_filename)
    os.remove(pdf_filename)  # Удаляем файл после отправки
    return 'PDF created and sent', 200

def create_pdf(data, contract_number):
    filename = f"contract_{contract_number}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    textobject = c.beginText(40, height - 40)
    textobject.setFont("Helvetica-Bold", 16)
    textobject.textLine("Договор аренды квартиры")
    
    textobject.setFont("Helvetica", 12)
    textobject.textLine(f"Номер договора: {contract_number}")
    textobject.textLine("")
    
    textobject.setFont("Helvetica-Bold", 14)
    textobject.textLine("Данные арендатора:")
    textobject.setFont("Helvetica", 12)
    textobject.textLine(f"Фамилия: {data['surname']}")
    textobject.textLine(f"Имя: {data['name']}")
    textobject.textLine(f"Отчество: {data['patronymic']}")
    textobject.textLine(f"Дата рождения: {data['birth_date']}")
    textobject.textLine(f"Паспорт: {data['passport']}")
    textobject.textLine("")
    
    textobject.setFont("Helvetica-Bold", 14)
    textobject.textLine("Даты и время заезда/выезда:")
    textobject.setFont("Helvetica", 12)
    textobject.textLine(f"Дата заезда: {data['check_in_date']}")
    textobject.textLine(f"Время заезда: {data['check_in_time']}")
    textobject.textLine(f"Дата выезда: {data['check_out_date']}")
    textobject.textLine(f"Время выезда: {data['check_out_time']}")
    textobject.textLine("")
    
    textobject.setFont("Helvetica-Bold", 14)
    textobject.textLine("Контактные данные:")
    textobject.setFont("Helvetica", 12)
    textobject.textLine(f"Электронная почта: {data['email']}")
    textobject.textLine(f"Телефон: {data['phone']}")
    
    c.drawText(textobject)
    c.save()
    return filename

def generate_contract_number():
    # Логика для генерации уникального номера договора
    if not os.path.exists('contract_number.txt'):
        with open('contract_number.txt', 'w') as f:
            f.write('0001')
    
    with open('contract_number.txt', 'r') as f:
        number = int(f.read().strip())
    
    new_number = f'{number:04d}'
    
    with open('contract_number.txt', 'w') as f:
        f.write(f'{number + 1:04d}')
    
    return new_number

def send_pdf_to_telegram(filename):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendDocument"
    files = {'document': open(filename, 'rb')}
    data = {'chat_id': TG_CHAT_ID}
    response = requests.post(url, files=files, data=data)
    print(response.text)  # Логирование ответа от Telegram API
    return response

if __name__ == '__main__':
    app.run(port=5000)
