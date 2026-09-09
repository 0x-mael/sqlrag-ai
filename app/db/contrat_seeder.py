import os 
from faker import Faker
import random
from dotenv import load_dotenv
from app.db.db_functions import Dbconn


faker = Faker("fr-FR")
random.seed(42)
CONTRAT_TEMPLATE = ""
path = "assets/templates/contrat_template.txt"
with open(path,'rt',encoding='utf-8') as f :
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
    save_path = "assets/contrats"
    for client in clients:
        nom_fichier = client['client_id']
        path = os.path.join(save_path,nom_fichier)
        path = path + ".md"
        text = seed_contrat(client_id=client['client_id'], nom_client=client['nom_client'], date_signature=client['date_signature'])
        with open(path,'wt',encoding='utf-8') as contrat:
            contrat.write(text)
        print(f"Contract generated for customer {nom_fichier}\n")


if __name__=="__main__":
    clients = get_clients()
    make_contrat(clients)
