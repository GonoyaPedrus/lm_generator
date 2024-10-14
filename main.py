from openai import OpenAI
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from dotenv import load_dotenv
import textwrap
import os

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
def generate_cover_letter(poste, entreprise, description):
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content" : f"Je suis Pierre Bourdel, voici mes coordonnées : Je suis jeune diplômé ingénieur en IA de l'ESME Sudria, je maîtrise kafka hadoop scala spark python genAI, LLM, Machine et deep learning models, j'ai une expérience de data engineer chez Orange via le Groupe SII où j'ai pu Implemented monitoring for batch processing (file mode) and streaming processes using Apache tools (Spark, Kafka, Flink) and analytics tools such as Grafana. Metrics such as Probes, IMSIs, Cells for Mediation NetXLR8 HubData. Une autre expérience en tant qu'ingénieur logiciel Java chez MBDA Missile systems. Je voudrais que tu m'écrives une lettre de motivation pour le poste de {poste} chez {entreprise} dont la description est {description} en mentionnant mes coordonnées au début et avec une bonne mise en page ainsi que des formules de politesses. JE NE VEUX PAS DE TEXTE A PERSONNALISER ENTRE CROCHETS NI LA DATE JE NE VEUX PAS QUE TU ECRIVES LES COORDONNEES DU CORRESPONDANT à REMPLIR, JE VEUX SEULEMENT LA LETTRE DE MOTIVATION",
                }
            ],
            model="gpt-4o",
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erreur : {e}")
        return None

def create_pdf(content, filename):
    # Créer le PDF
    pdf = SimpleDocTemplate(filename, pagesize=letter)

    # Styles
    styles = getSampleStyleSheet()

    # Style personnalisé avec espacement
    custom_style = ParagraphStyle(
        'CustomStyle',
        parent=styles['Normal'],
        spaceAfter=4,  # Ajouter de l'espace après chaque paragraphe
        leading=14,  # Ajuste la hauteur de ligne pour plus d'aération
    )

    # Ajouter des marges
    pdf.leftMargin = 50
    pdf.rightMargin = 50
    pdf.topMargin = 50
    pdf.bottomMargin = 50

    # Préparer le contenu
    story = []

    # Remplacer les sauts de ligne par des paragraphes
    paragraphs = content.split('\n')  # Sépare le texte par lignes
    for paragraph in paragraphs:
        wrapped_text = textwrap.fill(paragraph, width=75)  # Ajuster la largeur pour éviter les débordements
        p = Paragraph(wrapped_text, custom_style)
        story.append(p)
        story.append(Spacer(1, 4))  # Ajouter un espacement vertical entre les paragraphes

    # Construire le PDF
    pdf.build(story)

def main():
    entreprise = input("Entrez le nom de l'entreprise : ")
    poste = input("Entrez le titre du poste : ")
    description = input("Entrez la description du poste : ")

    lettre_motivation = generate_cover_letter(poste, entreprise, description)
    if lettre_motivation:
        print("Lettre de motivation générée avec succès", lettre_motivation)
        create_pdf(lettre_motivation, f"lettre motivation Pierre Bourdel {entreprise}.pdf")
    else:
        print("Erreur lors de la génération de la lettre de motivation")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
