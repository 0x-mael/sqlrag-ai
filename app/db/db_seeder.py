import os
import random
from datetime import datetime, timedelta
from faker import Faker
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv




faker = Faker ("fr_FR")
random.seed(42)
load_dotenv()


class Seeder:
    def __init__(self):
        self.dbname = os.getenv("DB_NAME")
        self.dbhost = os.getenv("DB_HOST")
        self.dbuser = os.getenv("DB_USER")
        self.dbpass = os.getenv("DB_PASSWORD")
        self.dbport = os.getenv("DB_PORT")

        self.DB_CONFIG = {
            "dbname": self.dbname,
            "user": self.dbuser,
            "password": self.dbpass,
            "host": self.dbhost,
            "port": self.dbport,
        }

    def init_schema(self, cursor):
        """Create structured tables"""
        cursor.execute("""
            DROP TABLE IF EXISTS incidents CASCADE;
            DROP TABLE IF EXISTS fatures CASCADE;
            DROP TABLE IF EXISTS clients CASCADE;

            CREATE TABLE clients (
            client_id VARCHAR(10) PRIMARY KEY,
            nom VARCHAR(100) NOT NULL,
            secteur VARCHAR(50) NOT NULL,
            date_signature DATE NOT NULL,
            email VARCHAR(100)
            );

            CREATE TABLE factures (
            facture_id VARCHAR(15) PRIMARY KEY,
            client_id VARCHAR(10) REFERENCES clients(client_id),
            montant_ht NUMERIC (10,2) NOT NULL,
            statut VARCHAR(20) CHECK (statut IN ('PAYEE','EN_RETARD','EN_ATTENTE')),
            date_emission DATE NOT NULL,
            retard_jours INT DEFAULT 0
            );

            CREATE TABLE incidents (
            incident_id VARCHAR(15) PRIMARY KEY,
            client_id VARCHAR(10) REFERENCES clients(client_id),
            severite VARCHAR(20) CHECK (severite IN ('CRITIQUE','MAJEURE','MINEURE')) ,
            description TEXT NOT NULL,
            date_signalement DATE NOT NULL,
            resolu BOOLEAN DEFAULT TRUE
            );



        """)

    def seed_data(self,conn):
        with conn.cursor() as cur :
            self.init_schema(cur)

            secteurs = ["Finance","Santé","Logistique","Rétail","Energie"]
            clients  = []
            for i in range(1, 21):
                c_id = f"CLT-{i:03d}"
                nom = faker.company()
                secteur = random.choice(secteurs)
                date_sig = faker.date_between(start_date='-2y',end_date="-6m")
                email = f"contact@{nom.lower().replace(' ','').replace(',','')}.fr"
                clients.append((c_id, nom,secteur, date_sig,email))

            cur.executemany(
                """
                INSERT INTO clients(client_id,nom,secteur,date_signature,email) VALUES (%s,%s,%s,%s,%s);
                """, clients,
            )


            factures = []
            f_idx = 1
            for client in clients:
                c_id = client[0]
                for _ in range(random.randint(3,6)):
                    f_id = f"FAC-{f_idx:04d}"
                    montant = round(random.uniform(2500, 45000),2)
                    statut = random.choices(['PAYEE','EN_RETARD','EN_ATTENTE'], weights= [0.7, 0.2, 0.1])[0]
                    retard = random.randint(5,45) if statut == 'EN_RETARD' else 0
                    date_em = faker.date_between(start_date =  "-1y", end_date= "today")
                    factures.append((f_id,c_id,montant, statut,date_em,retard ))
                    f_idx += 1
            cur.executemany("""INSERT INTO factures(facture_id, client_id, montant_ht, statut, date_emission, retard_jours) 
                VALUES (%s, %s, %s, %s, %s, %s);"""
                        ,factures,)


            incidents = []
            inc_idx = 1
            descriptions = [
                "Panne API supérieure à 4 heures",
                "Latence anormale sur le service de streaming",
                "Perte partielle de paquets sur le cluster B2B",
                "Erreur d'authentification SSO récurrente",
                "Échec de la sauvegarde hebdomadaire",
            ]

            for client in clients :
                c_id = client[0]
                for _ in range(random.randint(0,3)):
                    i_id = f"INC-{inc_idx:04d}"
                    sev= random.choice(["CRITIQUE", "MAJEURE", "MINEURE"])
                    desc = random.choice(descriptions)
                    date_inc = faker.date_between(start_date="-6m", end_date="today")
                    resolu = random.choices([True,False],weights=[0.85,0.15])[0]
                    incidents.append((i_id, c_id,sev, desc,date_inc,resolu))
                    inc_idx += 1
            
            cur.executemany(
                """ INSERT INTO incidents(incident_id, client_id, severite, description, date_signalement, resolu) 
                            VALUES (%s, %s, %s, %s, %s, %s);"""
                , incidents,

            )

        conn.commit()
        print(f"Database ready : {len(clients)} clients, {len(factures)} factures")





if __name__=="__main__":
    seeder = Seeder()
    config = seeder.DB_CONFIG
    connection = psycopg2.connect(**config)
    seeder.seed_data(connection)
    connection.close()