from fpdf import FPDF
from datetime import datetime
import re

def capitalize_text(text):
    if not isinstance(text, str):
        return text
    # Capitaliza cada palabra, pero mantiene siglas (3+ mayúsculas) y palabras de 2 letras en mayúsculas
    def smart_cap(word):
        if word.isupper() and len(word) > 2:
            return word  # Siglas
        if len(word) <= 2:
            return word.upper()  # Palabras cortas tipo TI, IA
        return word[:1].upper() + word[1:].lower()
    return ' '.join(smart_cap(w) for w in re.split(r'(\s+)', text))

class PDFReport(FPDF):
    def header(self):
        # Logo (opcional)
        # self.image('logo.png', 10, 8, 33)
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(30, 30, 120)
        self.cell(0, 10, 'Reporte de Evaluación de Riesgo en Proyectos TI', ln=True, align='C')
        self.set_font('Helvetica', '', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, f'Fecha de generación: {datetime.now().strftime("%d/%m/%Y %H:%M")}', ln=True, align='R')
        self.ln(4)
        self.set_draw_color(30, 30, 120)
        self.set_line_width(0.8)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f'Página {self.page_no()}', align='C')

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 13)
        self.set_text_color(30, 30, 120)
        self.cell(0, 10, title, ln=True)
        self.ln(2)

    def section_body(self, text):
        self.set_font('Helvetica', '', 11)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 8, text)
        self.ln(2)

    def add_table(self, data_dict):
        self.set_font('Helvetica', '', 11)
        self.set_fill_color(230, 230, 250)
        for k, v in data_dict.items():
            label = k.replace('_', ' ').capitalize()
            if isinstance(v, str):
                v = capitalize_text(v)
            elif isinstance(v, list):
                v = ', '.join([capitalize_text(x) for x in v])
            self.cell(60, 8, label, 1, 0, 'L', True)
            self.cell(0, 8, str(v), 1, 1, 'L', False)
        self.ln(2)

    def add_probabilities(self, prob_dict):
        self.set_font('Helvetica', '', 11)
        self.set_fill_color(245, 245, 245)
        self.cell(60, 8, 'Clase', 1, 0, 'C', True)
        self.cell(0, 8, 'Probabilidad', 1, 1, 'C', True)
        for clase, prob in prob_dict.items():
            self.cell(60, 8, clase, 1, 0, 'C', False)
            self.cell(0, 8, f'{prob*100:.1f} %', 1, 1, 'C', False)
        self.ln(2)

def generar_reporte_pdf(proyecto, prediccion=None, filename="reporte_riesgo.pdf"):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=False, margin=15)

    # Sección: Datos del Proyecto
    pdf.section_title('Datos del Proyecto')
    pdf.add_table(proyecto)

    # Sección: Resultado de la Predicción (solo si hay predicción)
    if prediccion and isinstance(prediccion, dict) and prediccion.get('riesgo_general'):
        pdf.section_title('Resultado de la Predicción')
        pdf.section_body(f"Riesgo General: {prediccion['riesgo_general']}")
        if 'probabilidades' in prediccion:
            pdf.add_probabilities(prediccion['probabilidades'])
    else:
        pdf.section_title('Resultado de la Predicción')
        pdf.section_body("No se ha realizado una predicción para este proyecto.")

    # Sección: Interpretación
    pdf.section_title('Interpretación de Resultados')
    interpretacion = ""
    riesgo = prediccion.get('riesgo_general', '').lower() if prediccion else ''
    if riesgo == 'alto':
        interpretacion += (
            "El modelo ha determinado que el riesgo general del proyecto es ALTO. Esto significa que, según los datos ingresados, existe una alta probabilidad de que el proyecto enfrente dificultades significativas en su ejecución, como retrasos, sobrecostos o problemas de calidad. Se recomienda tomar medidas preventivas inmediatas, reforzar la gestión y monitorear de cerca los hitos críticos.\n\n"
        )
    elif riesgo == 'medio':
        interpretacion += (
            "El modelo ha determinado que el riesgo general del proyecto es MEDIO. Esto indica que el proyecto tiene una probabilidad moderada de enfrentar algunos desafíos, pero con una gestión adecuada es posible mitigar los riesgos y lograr los objetivos. Se recomienda mantener un monitoreo constante y ajustar los planes según sea necesario.\n\n"
        )
    elif riesgo == 'bajo':
        interpretacion += (
            "El modelo ha determinado que el riesgo general del proyecto es BAJO. Esto sugiere que, de acuerdo a los datos proporcionados, el proyecto tiene buenas condiciones para su éxito. Sin embargo, es importante no descuidar la gestión y continuar con buenas prácticas de seguimiento.\n\n"
        )
    else:
        interpretacion += (
            "El modelo ha generado un resultado de riesgo general no esperado o no se realizó predicción.\n\n"
        )

    # Interpretación de probabilidades
    probabilidades = prediccion.get('probabilidades', {}) if prediccion else {}
    if probabilidades:
        clase_max = max(probabilidades, key=probabilidades.get)
        prob_max = probabilidades[clase_max]
        interpretacion += (
            f"La clase con mayor probabilidad es '{clase_max}' con un {prob_max*100:.1f}% de confianza. "
            "Esto significa que, de todas las categorías posibles, el modelo considera que esta es la más probable para el proyecto evaluado.\n"
        )
        otras = [(k, v) for k, v in probabilidades.items() if k != clase_max]
        if otras:
            interpretacion += "Las otras probabilidades son: "
            interpretacion += ", ".join([f"{k}: {v*100:.1f}%" for k, v in otras]) + ".\n"
    elif prediccion:
        interpretacion += "No se encontraron probabilidades detalladas para interpretar.\n"
    else:
        interpretacion += "No se realizó predicción para este proyecto.\n"

    # Interpretación de sobrecosto y retraso si existen
    prob_sobrecosto = prediccion.get('probabilidad_sobrecosto') if prediccion else None
    prob_retraso = prediccion.get('probabilidad_retraso') if prediccion else None
    if prob_sobrecosto is not None:
        interpretacion += (f"\nProbabilidad de sobrecosto: {prob_sobrecosto*100:.1f}%. "
            + ("Un valor alto indica que el proyecto tiene una alta probabilidad de exceder el presupuesto estimado. Se recomienda revisar los costos, identificar posibles desviaciones y establecer controles financieros más estrictos."
               if prob_sobrecosto >= 0.5 else
               "Un valor bajo indica que el proyecto tiene buenas perspectivas de mantenerse dentro del presupuesto, aunque siempre es recomendable monitorear los gastos."))
    if prob_retraso is not None:
        interpretacion += (f"\nProbabilidad de retraso: {prob_retraso*100:.1f}%. "
            + ("Un valor alto sugiere que el proyecto podría no cumplir con los plazos establecidos. Se recomienda reforzar la planificación, monitorear los hitos y gestionar los recursos de manera eficiente."
               if prob_retraso >= 0.5 else
               "Un valor bajo indica que el proyecto tiene buenas perspectivas de cumplir los plazos, pero es importante mantener un seguimiento constante del cronograma."))

    # Explicación final
    interpretacion += ("\nEsta interpretación se basa únicamente en los resultados obtenidos y busca orientar la toma de decisiones. Recuerde que el reporte es una herramienta de apoyo y no reemplaza el juicio profesional del equipo gestor.")
    pdf.section_body(interpretacion)

    pdf.output(filename)
    print(f"Reporte generado: {filename}")

# Ejemplo de uso
if __name__ == "__main__":
    proyecto = {
        "Tipo de proyecto": "Implementación ERP",
        "Duración estimada (meses)": 18,
        "Presupuesto estimado (USD)": 800000,
        "Número de recursos": 12,
        "Tecnologías": "ERP, Cloud",
        "Complejidad": "Alta",
        "Experiencia del equipo": "Media",
        "Hitos clave": 6
    }
    prediccion = {
        "riesgo_general": "Alto",
        "probabilidades": {
            "Bajo": 0.10,
            "Medio": 0.25,
            "Alto": 0.65
        },
        "probabilidad_sobrecosto": 0.7,
        "probabilidad_retraso": 0.8
    }
    generar_reporte_pdf(proyecto, prediccion)
