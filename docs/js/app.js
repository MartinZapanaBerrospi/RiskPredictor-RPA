// Init Technologies
const techs = ["cloud", "big data", "IA", "IoT", "blockchain", "mobile", "web"];
const container = document.getElementById('techContainer');

techs.forEach(tech => {
    const label = document.createElement('label');
    label.className = 'tech-label';
    if(tech === 'web' || tech === 'cloud') label.classList.add('selected'); // Def seleccionados
    
    const input = document.createElement('input');
    input.type = 'checkbox';
    input.value = tech;
    if(tech === 'web' || tech === 'cloud') input.checked = true;
    
    input.addEventListener('change', (e) => {
        if(e.target.checked) label.classList.add('selected');
        else label.classList.remove('selected');
    });
    
    label.appendChild(input);
    label.appendChild(document.createTextNode(tech.toUpperCase()));
    container.appendChild(label);
});

// Form Submission
document.getElementById('predictionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Get data
    const selectedTechs = Array.from(document.querySelectorAll('.tech-label input:checked')).map(cb => cb.value).join(',');
    
    if(!selectedTechs) {
        alert('Debes seleccionar al menos una tecnología.');
        return;
    }

    const data = {
        tipo_proyecto: document.getElementById('tipo_proyecto').value,
        metodologia: document.getElementById('metodologia').value,
        duracion_estimacion: Number(document.getElementById('duracion_estimacion').value),
        presupuesto_estimado: Number(document.getElementById('presupuesto_estimado').value),
        numero_recursos: Number(document.getElementById('numero_recursos').value),
        tecnologias: selectedTechs,
        complejidad: document.getElementById('complejidad').value,
        experiencia_equipo: Number(document.getElementById('experiencia_equipo').value),
        hitos_clave: Number(document.getElementById('hitos_clave').value)
    };

    // Loading state
    const btn = document.getElementById('submitBtn');
    const btnText = document.getElementById('btnText');
    const loader = document.getElementById('loader');
    
    btn.disabled = true;
    btnText.style.display = 'none';
    loader.style.display = 'block';

    // Determinar si corre local para fetch al backend o si está en github pages
    const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';

    try {
        if (isLocalhost) {
            const response = await fetch('http://localhost:8000/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            if(!response.ok) throw new Error('API Error');
            
            const result = await response.json();
            showResults(result, false);
        } else {
            // Entorno de GitHub Pages: saltar directamente a la simulación sin intentar fetch localhost
            throw new Error('Entorno estático');
        }

    } catch (error) {
        // Fallback / Simulated calculation logic for static GitHub Pages hosting
        if (isLocalhost) {
            console.log('Backend no disponible. Generando resultado simulado...');
        }
        
        // Extremely simple simulated risk calculation based on inputs just for demo purposes
        let baseRisk = 0.5;
        if(data.complejidad === 'alta') baseRisk += 0.2;
        if(data.complejidad === 'baja') baseRisk -= 0.15;
        if(data.experiencia_equipo < 3) baseRisk += 0.15;
        if(data.experiencia_equipo > 6) baseRisk -= 0.1;
        if(data.tecnologias.split(',').length > 3) baseRisk += 0.1;
        
        // Normalizing
        baseRisk = Math.max(0.1, Math.min(0.9, baseRisk));
        
        const valAlto = baseRisk;
        const valMedio = 1 - baseRisk > 0.4 ? 0.4 : 1 - baseRisk;
        const valBajo = 1 - (valAlto + valMedio);

        const simulatedResult = {
            riesgo_general: valAlto > 0.45 ? 'Alto' : (valAlto < 0.2 ? 'Bajo' : 'Medio'),
            probabilidades_riesgo: {
                "Alto": valAlto,
                "Medio": valMedio,
                "Bajo": valBajo
            },
            probabilidad_sobrecosto: Math.min(0.95, baseRisk + (data.presupuesto_estimado / data.numero_recursos < 5000 ? 0.2 : -0.1)),
            probabilidad_retraso: Math.min(0.95, baseRisk + (data.duracion_estimacion > 12 ? 0.15 : 0))
        };
        
        // artificial delay
        await new Promise(r => setTimeout(r, 800));
        showResults(simulatedResult, true);
    } finally {
        btn.disabled = false;
        btnText.style.display = 'block';
        loader.style.display = 'none';
    }
});

function showResults(data, isSimulated) {
    const modal = document.getElementById('resultModal');
    const badge = document.getElementById('riskBadge');
    
    // Set risk text & color
    const riskStr = data.riesgo_general.toLowerCase();
    badge.textContent = data.riesgo_general.toUpperCase();
    badge.className = `risk-badge ${riskStr}`;

    // Reset bars
    document.querySelectorAll('.prob-bar').forEach(bar => bar.style.width = '0%');
    
    modal.classList.add('active');
    
    // Warning visibilty
    document.getElementById('apiWarning').style.display = isSimulated ? 'block' : 'none';

    // Animate bars
    setTimeout(() => {
        const parsePct = (val) => `${(val * 100).toFixed(1)}%`;
        
        document.getElementById('valAlto').textContent = parsePct(data.probabilidades_riesgo.Alto);
        document.getElementById('barAlto').style.width = parsePct(data.probabilidades_riesgo.Alto);
        
        document.getElementById('valMedio').textContent = parsePct(data.probabilidades_riesgo.Medio);
        document.getElementById('barMedio').style.width = parsePct(data.probabilidades_riesgo.Medio);
        
        document.getElementById('valBajo').textContent = parsePct(data.probabilidades_riesgo.Bajo);
        document.getElementById('barBajo').style.width = parsePct(data.probabilidades_riesgo.Bajo);

        document.getElementById('valSobre').textContent = parsePct(data.probabilidad_sobrecosto);
        document.getElementById('barSobre').style.width = parsePct(data.probabilidad_sobrecosto);

        document.getElementById('valRetraso').textContent = parsePct(data.probabilidad_retraso);
        document.getElementById('barRetraso').style.width = parsePct(data.probabilidad_retraso);
    }, 100);
}

function closeModal() {
    document.getElementById('resultModal').classList.remove('active');
}
