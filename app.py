from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        template = request.form.get('template')

        if template == "vrai.pdf":
            PDF_TEMPLATE = "vrai.pdf"
            OUTPUT_PDF = "resultat.pdf"

            jour_naissance = request.form.get('jour_de_naissance', '')
            mois_naissance = request.form.get('mois_de_naissance', '')
            annee_naissance = request.form.get('annee_de_naissance', '')
            lieu_naissance = request.form.get('lieu_naissance', '')
            jour_conv = request.form.get('jour_conv', '')
            mois_conv = request.form.get('mois_conv', '')
            jour_signature = request.form.get('jour_signature', '')
            mois_signature = request.form.get('mois_signature', '')
            annee_signature = request.form.get('annee_signature', '')
            nom = request.form.get('nom', '')
            prenom = request.form.get('prenom', '')

            original = PdfReader(PDF_TEMPLATE)
            writer = PdfWriter()

            for i, page in enumerate(original.pages):
                if i == 0 or i == 2:
                    packet = io.BytesIO()
                    can = canvas.Canvas(packet, pagesize=A4)

                    if i == 0:
                        can.drawString(190, 427, nom)
                        can.drawString(246, 427, prenom)
                        can.drawString(120, 400, jour_naissance)
                        can.drawString(150, 400, mois_naissance)
                        can.drawString(180, 400, annee_naissance)
                        can.drawString(290, 400, lieu_naissance)

                    if i == 2:
                        can.drawString(433, 708, jour_conv)
                        can.drawString(453, 708, mois_conv)
                        can.drawString(251, 210, jour_signature)
                        can.drawString(273, 210, mois_signature)
                        can.drawString(297, 210, annee_signature)

                    can.save()
                    packet.seek(0)
                    overlay_pdf = PdfReader(packet)
                    page.merge_page(overlay_pdf.pages[0])
                writer.add_page(page)

        elif template == "cerfa.pdf":
            PDF_TEMPLATE = "cerfa.pdf"
            OUTPUT_PDF = "recu_fiscal.pdf"

            num_ordre = request.form.get('num_ordre', '')
            nom_donateur = request.form.get('nom', '')
            prenom_donateur = request.form.get('prenom', '')
            adresse_donateur = request.form.get('adresse_donateur', '')
            code_postal_donateur = request.form.get('code_postal_donateur', '')
            commune_donateur = request.form.get('commune_donateur', '')
            pays_donateur = request.form.get('pays_donateur', '')
            somme_don = request.form.get('montant_chiffre', '')
            somme_don_lettre = request.form.get('montant_lettres', '')
            jour_don = request.form.get('jour_don', '')
            mois_don = request.form.get('mois_don', '')
            annee_don = request.form.get('annee_don', '')
            date_versement = f"{jour_don}/{mois_don}/{annee_don}"

            jour_signature = request.form.get('jour_signature', '')
            mois_signature = request.form.get('mois_signature', '')
            annee_signature = request.form.get('annee_signature', '')
            date_signature = f"{jour_signature}/{mois_signature}/{annee_signature}"
            categories = request.form.getlist('categorie[]')
            categorie_autre = request.form.get('categorie_autre', '')
            nature_don = request.form.getlist('nature_don[]')

            ref_cgi = request.form.getlist('ref_cgi[]')
            forme_don = request.form.getlist('forme_don[]')
            nature_don2 = request.form.getlist('nature_don2[]')
            nature_don2_autre = request.form.get('nature_don2_autre', '')
            versement = request.form.getlist('versement[]')

            original = PdfReader(PDF_TEMPLATE)
            writer = PdfWriter()

            case_coords = {
                "interet_general": (64, 503),
                "utilite_publique": (64, 488),
                "fondation_entreprise": (64, 426),
                "musee": (64, 413),
                "organisme_ss_but": (64, 401),
                "commune_syndicats": (64, 373),
                "fondation_universitaire": (64, 453),
                "autre": (64, 348),
            }

            subcategories = list(case_coords.keys())
            case_principale = (35, 449)

            # Séparation des coordonnées de nature du don
            nature_coords_page1 = {
                "numeraire": (35, 333),
                "nature": (35, 313),
                "prestations": (35, 299),
                "etablissement": (35, 271),
                "etab2": (35, 242),
                "etab3": (35, 223),
                "etab4": (35, 193),
                "etab5": (35, 156),
                "etab6": (35, 115),
            }

            nature_coords_page2 = {
                "etab7": (35, 809),
                "etab8": (35, 791),
                "etab9": (35, 772),
                "etab10": (35, 758),
                "etab11": (35, 740),
                "etab12": (35, 721),
                "etab13": (35, 705),
                "etab14": (35, 685),
                "etab15": (35, 660),
            }

            ref_cgi_coords = {
                "200_cgi": (98, 400),
                "978_cgi": (290, 400)
            }

            forme_don_coords = {
                "authentique": (35, 365),
                "sous_seing_prive": (150, 365),
                "don_manuel": (292, 365),
                "autres_forme": (484, 365)
            }

            nature_don2_coords = {
                "numeraire": (35, 328),
                "titres_cotes": (150, 328),
                "abandon_revenus": (339, 328),
                "frais_benevoles": (35, 308),
                "autres_nature": (339, 308)
            }

            versement_coords = {
                "especes": (35, 260),
                "cheque": (149, 260),
                "virement": (292, 260)
            }

            nature_principale = (3500, 3700)

            for i, page in enumerate(original.pages):
                packet = io.BytesIO()
                can = canvas.Canvas(packet, pagesize=A4)

                if i == 0:
                    can.drawString(480, 718, num_ordre)
                    if any(cat in categories for cat in subcategories):
                        can.drawString(*case_principale, "✓")
                    for cat in categories:
                        if cat in case_coords:
                            can.drawString(*case_coords[cat], "✓")
                        if cat == "autre":
                            can.drawString(90, 355, categorie_autre)
                    if any(n in nature_don for n in nature_coords_page1):
                        can.drawString(*nature_principale, "✓")
                    for n in nature_don:
                        if n in nature_coords_page1:
                            can.drawString(*nature_coords_page1[n], "✓")

                elif i == 1:
                    for n in nature_don:
                        if n in nature_coords_page2:
                            can.drawString(*nature_coords_page2[n], "✓")

                    # ✅ Infos du donateur
                    
                    can.drawString(65, 586, nom_donateur)
                    can.drawString(352, 590, prenom_donateur)
                    can.drawString(82, 558, adresse_donateur)
                    can.drawString(320, 558, code_postal_donateur)
                    can.drawString(445, 558, commune_donateur)
                    can.drawString(65, 543, pays_donateur)
                    can.drawString(70, 481, somme_don)
                    can.drawString(211, 481, somme_don_lettre)
                    can.drawString(180, 445, date_versement)
                    can.drawString(320, 220, f"Fait le {date_signature}")

                    # ✅ Nouveaux blocs
                    for val in ref_cgi:
                        if val in ref_cgi_coords:
                            can.drawString(*ref_cgi_coords[val], "✓")

                    for val in forme_don:
                        if val in forme_don_coords:
                            can.drawString(*forme_don_coords[val], "✓")

                    for val in nature_don2:
                        if val in nature_don2_coords:
                            can.drawString(*nature_don2_coords[val], "✓")
                    if "autres_nature" in nature_don2 and nature_don2_autre:
                        can.drawString(435, 308, nature_don2_autre)

                    for val in versement:
                        if val in versement_coords:
                            can.drawString(*versement_coords[val], "✓")

                can.save()
                packet.seek(0)
                overlay_pdf = PdfReader(packet)
                page.merge_page(overlay_pdf.pages[0])
                writer.add_page(page)

        else:
            return f"Fichier PDF non reconnu : {template}"

        with open(OUTPUT_PDF, "wb") as f:
            writer.write(f)

        return send_file(OUTPUT_PDF, as_attachment=True)

    return render_template("form.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
