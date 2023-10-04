import requests
from bs4 import BeautifulSoup
import csv
import os

def fetch_html(url, session):
    response = session.get(url)
    response.raise_for_status()
    return response.text

def extract_numbers(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    cells = soup.find_all('td', {'width': '20', 'height': '20'})
    return [int(cell.text) for cell in cells if cell.text.isdigit()]

def save_to_csv(folder, filename, data):
    with open(os.path.join(folder, filename), 'w', newline='') as file:
        writer = csv.writer(file)
        for item in data:
            writer.writerow([item])

if __name__ == "__main__":
    base_url = "https://casci.binghamton.edu/academics/ssie501/blackbox/BlackBox_N.php"
    
    num_cycles = int(input("Enter the number of cycles: "))
    
    with requests.Session() as session:
        for cycle in range(num_cycles):
            html_content = fetch_html(base_url, session)
            
            # Create a folder for each cycle
            folder_name = f"cycle_{cycle + 1}"
            os.makedirs(folder_name, exist_ok=True)
            
            # Save the HTML content to a file for each cycle
            with open(os.path.join(folder_name, "output.html"), "w", encoding="utf-8") as file:
                file.write(html_content)

            numbers = extract_numbers(html_content)

            Q1 = [numbers[i*20 : i*20+10] for i in range(10)]
            Q1 = [item for sublist in Q1 for item in sublist]

            Q2 = [numbers[i*20+10 : i*20+20] for i in range(10)]
            Q2 = [item for sublist in Q2 for item in sublist]

            Q3 = [numbers[i*20 : i*20+10] for i in range(10, 20)]
            Q3 = [item for sublist in Q3 for item in sublist]

            Q4 = [numbers[i*20+10 : i*20+20] for i in range(10, 20)]
            Q4 = [item for sublist in Q4 for item in sublist]

            save_to_csv(folder_name, "master_list.csv", numbers)
            save_to_csv(folder_name, "Q1.csv", Q1)
            save_to_csv(folder_name, "Q2.csv", Q2)
            save_to_csv(folder_name, "Q3.csv", Q3)
            save_to_csv(folder_name, "Q4.csv", Q4)

            # Advance the simulation by 100 steps (or any other number you desire) for the next cycle
            session.get(base_url, params={"cycles": 100})
