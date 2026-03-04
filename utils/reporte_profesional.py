from fpdf import FPDF
from datetime import datetime
import re

def capitalize_text(text):
    if not isinstance(text, str):
        return text
    # Si hay comas sin espacio, añadirles espacio para correcta separación
    text = str(text).replace(',', ', ')
    text = re.sub(r'\s+', ' ', text).strip()
    
    def smart_cap(word):
        clean_word = word.strip(',.')
        if clean_word.isupper() and len(clean_word) > 2:
            return word  # Mantener siglas (ej. ERP, API)
        if len(clean_word) <= 2:
            return word.upper()  # AI, BD, TI
        return word.capitalize()
    return ' '.join(smart_cap(w) for w in text.split(' '))

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
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Sección: Datos del Proyecto
    pdf.section_title('Datos del Proyecto')
    pdf.add_table(proyecto)

    # Sección: Resultado de la Predicción (debajo de la tabla, en la misma hoja si hay espacio)
    pdf.section_title('Resultado de la Predicción')
    if prediccion and isinstance(prediccion, dict) and prediccion.get('riesgo_general'):
        pdf.section_body(f"Riesgo General: {prediccion['riesgo_general']}")
        if 'probabilidades' in prediccion:
            pdf.add_probabilities(prediccion['probabilidades'])
        if 'probabilidad_sobrecosto' in prediccion:
            pdf.section_body(f"Probabilidad de sobrecosto: {prediccion['probabilidad_sobrecosto']*100:.1f}%")
        if 'probabilidad_retraso' in prediccion:
            pdf.section_body(f"Probabilidad de retraso: {prediccion['probabilidad_retraso']*100:.1f}%")
    else:
        pdf.section_body("No se ha realizado una predicción para este proyecto.")

    # Sección: Interpretación (debajo de lo anterior, en la misma hoja si hay espacio)
    pdf.section_title('Análisis Ejecutivo y Recomendaciones')
    interpretacion = ""
    riesgo = prediccion.get('riesgo_general', '').lower() if prediccion else ''
    
    if riesgo == 'alto':
        interpretacion += (
            "Nivel de Riesgo General: ALTO (Estado Crítico)\n"
            "El algoritmo predictivo ha identificado una probabilidad significativa de que este proyecto experimente desviaciones severas. "
            "Se detectan patrones históricos que apuntan a posibles obstáculos estructurales. "
            "Recomendación Estratégica: Se sugiere la intervención inmediata de la PMO (Project Management Office) para reestructurar la planificación, auditar el alcance inicial y establecer métricas de monitoreo iterativo (KPIs diarios).\n\n"
        )
    elif riesgo == 'medio':
        interpretacion += (
            "Nivel de Riesgo General: MEDIO (Alerta Preventiva)\n"
            "Las características ingresadas perfilan un proyecto con desafíos operativos moderados. "
            "El modelo señala áreas de fricción típicas que podrían materializarse afectando el ROI si no reciben antención proactiva. "
            "Recomendación Estratégica: Establecer puntos de control semanales, afinar las estimaciones presupuestales y mantener una comunicación directa con los stakeholders para la aprobación de cambios.\n\n"
        )
    elif riesgo == 'bajo':
        interpretacion += (
            "Nivel de Riesgo General: BAJO (Estable)\n"
            "Los indicadores predictivos sugieren condiciones altamente favorables para la ejecución técnica y financiera del proyecto. "
            "Los parámetros estructurales ingresados se alinean firmemente con los perfiles históricos de éxito y entrega a tiempo. "
            "Recomendación Estratégica: Continuar con la hoja de ruta establecida, asegurando prácticas estándar de calidad e integración continua.\n\n"
        )
    else:
        interpretacion += (
            "El modelo no logró determinar un perfil de riesgo claro basándose en los datos provistos.\n\n"
        )

    # Interpretación de probabilidades
    probabilidades = prediccion.get('probabilidades', {}) if prediccion else {}
    if probabilidades:
        clase_max = max(probabilidades, key=probabilidades.get)
        prob_max = probabilidades[clase_max]
        interpretacion += (
            f"Evaluación de Confiabilidad: El motor clasifica el proyecto primariamente como '{clase_max}' con un nivel de certidumbre analítica del {prob_max*100:.1f}%. "
            "El margen estadístico apoya fehacientemente este análisis direccional.\n"
        )
    elif prediccion:
        interpretacion += "No se dispone del desglose de varianzas para interpretación.\n"
    else:
        interpretacion += "No se realizó evaluación predictiva para el documento en curso.\n"

    # Interpretación de sobrecosto y retraso si existen
    prob_sobrecosto = prediccion.get('probabilidad_sobrecosto') if prediccion else None
    prob_retraso = prediccion.get('probabilidad_retraso') if prediccion else None
    
    if prob_sobrecosto is not None:
        interpretacion += (f"\nAnálisis Financiero (Exposición a Sobrecosto: {prob_sobrecosto*100:.1f}%):\n"
            + ("Alta exposición a desviaciones presupuestarias perjudiciales. Es perentorio revisar el Capex y blindar las reservas de contingencia.\n"
               if prob_sobrecosto >= 0.5 else
               "La viabilidad financiera es robusta; el dimensionamiento del presupuesto proyecta ser suficiente y previsiblemente holgado.\n"))
               
    if prob_retraso is not None:
        interpretacion += (f"\nAnálisis Operativo (Exposición a Retraso: {prob_retraso*100:.1f}%):\n"
            + ("Riesgo patente de violar la línea base del cronograma maestro. Resulta imperante aplicar técnicas de compresión y examinar el camino crítico logístico.\n"
               if prob_retraso >= 0.5 else
               "Plena factibilidad temporal para alcanzar el delivery en los plazos contractuales previamente pactados, recomendando sostener el control de hitos.\n"))

    # Explicación final
    interpretacion += ("\nAviso de Exención de Responsabilidad: Este compendio inferencial se sustenta en el aprendizaje empírico de modelos algorítmicos. Está diseñado para elevar la calidad de decisión directiva, complementando y jamás sustituyendo la pericia subjetiva humana y el juicio del Project Manager.")
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
