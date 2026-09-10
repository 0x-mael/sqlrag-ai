import os 
from faker import Faker
import random
from pathlib import Path
from dotenv import load_dotenv
from app.db.db_functions import Dbconn


BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATE_PATH = BASE_DIR / "assets" / "templates" / "contrat_template.txt"
OUTPUT_DIR = BASE_DIR / "assets" / "contrats"

faker = Faker("fr-FR")
random.seed(42)
CONTRAT_TEMPLATE = ""

with open(TEMPLATE_PATH, 'rt', encoding='utf-8') as f:
    CONTRAT_TEMPLATE = f.read()



db_conn = Dbconn()

def get_clients():
    query = "SELECT client_id, nom, date_signature FROM clients;"
    clients = db_conn.exec_query(query)
    clients_tab = []
    for i in range(len(clients)):
        client = {
            "client_id":clients[i][0],
            "nom_client":clients[i][1],
            "date_signature":clients[i][2]
        }
        clients_tab.append(client)
    return clients_tab


def seed_contrat(client_id:str="", nom_client:str="", date_signature:str="") -> str :
    """Function to generate fake contrat for knowns clients in the database using a template and faker seeder """



    sla = random.choice(["99,5", "99,9", "99,95"])
    gtr = random.choice([2, 4, 8])
    penalite = random.choice([3, 5, 10])
    delai = random.choice([30, 45, 60])
    seuil_suspension = random.choice([15, 30])
    preavis = random.choice([5, 8, 15])

    return CONTRAT_TEMPLATE.format(
        client_id=client_id,
        nom_client=nom_client,
        capital=f"{random.randint(10, 500) * 1000:,}".replace(",", " "),
        adresse_client=faker.address().replace("\n", ", "),
        siren=faker.siren(),
        representant=faker.name(),
        poste=random.choice(["Président-Directeur Général", "Directeur Technique", "Directrice des Achats"]),
        date_effet=date_signature,
        sla_disponibilite=sla,
        gtr_heures=gtr,
        penalite_sla=penalite,
        delai_paiement=delai,
        seuil_retard_suspension=seuil_suspension,
        preavis_jours=preavis,
    )

def make_contrat(clients):
    """Function to create and save every retrieved client contrat according to their personal data and random seed"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for client in clients:
        nom_fichier = f"{client['client_id']}.md"
        file_path = OUTPUT_DIR / nom_fichier
        text = seed_contrat(client_id=client['client_id'], nom_client=client['nom_client'], date_signature=client['date_signature'])
        with open(file_path, 'wt', encoding='utf-8') as contrat:
            contrat.write(text)
        print(f"Contract generated for customer {client['client_id']}\n")


if __name__=="__main__":
    clients = get_clients()
    make_contrat(clients)
