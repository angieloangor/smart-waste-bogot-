# FORMULARIO DE CARACTERIZACIÓN Y FORMULACIÓN DEL PROBLEMA
## Bogotá Datajam: Uso y Aprovechamiento de Datos (Edición 2) - 2026

## Sección 1 – Información general del equipo

### 1. Nombre del equipo:

SmartWaste Bogotá / Data Dolls

### 2. Entidad u organización a la que pertenece cada integrante

- Danna Vanessa Caballero Urrego: Universidad Externado de Colombia
- Allison Michelle Loango Rayo: Universidad Externado de Colombia
- Angie Katherine Loango Rayo: Universidad Externado de Colombia

### 3. Nombre completo, rol y perfil principal de cada integrante

- Danna Vanessa Caballero Urrego. Analista de datos. Estudiante
- Allison Michelle Loango Rayo. Analista de políticas públicas. Estudiante
- Angie Katherine Loango Rayo. Experto temático. Estudiante

### 4. Correo electrónico de contacto del equipo (líder):

danna.caballero@est.uexternado.edu.co

## Sección 2 – Formulación del problema

### 6. Problema público a abordar:
Describa de manera clara y concreta el problema que desea analizar.

El problema público que aborda este proyecto es la presencia y persistencia de puntos críticos de arrojo clandestino de residuos en la ciudad de Bogotá, así como la ineficiencia de la cobertura y priorización operativa de la red de recolección y barrido. Esta situación genera impactos ambientales, de salud pública, percepción ciudadana y presión sobre la gestión del servicio.

### 7. Justificación del problema:
¿Por qué es relevante analizar este problema? ¿A quién afecta?

Es relevante porque la acumulación de residuos en zonas críticas afecta la calidad ambiental, la percepción de seguridad y orden en la ciudad, y puede aumentar la necesidad de intervención de las autoridades y operadores de servicios públicos. Afecta principalmente a comunidades vecinas, actores de la gestión pública, administradores de servicios, y a la ciudad en general, porque compromete la sostenibilidad operativa de la recolección y la limpieza.

### 8. Delimitación del análisis:
Indique el ámbito territorial, sectorial, poblacional o institucional sobre el cual se desarrollará el ejercicio.

El análisis se desarrolla a nivel territorial en la ciudad de Bogotá, con énfasis en la identificación de zonas prioritarias por riesgo de arrojo clandestino y necesidad de intervención operativa. El ejercicio se enfoca en la gestión de residuos, infraestructura de servicio y territorio urbano.

### 9. Pregunta de análisis
Formule la pregunta principal que guiará su ejercicio.

¿Cómo pueden integrarse distintas fuentes de datos geoespaciales y de gestión pública para identificar las zonas de Bogotá con mayor riesgo de residuos clandestinos y priorizar intervenciones de limpieza, vigilancia y operación del servicio?

### 10. Hipótesis o expectativa analítica preliminar
¿Cuál es la relación o explicación que esperan encontrar en los datos?

Se espera encontrar una relación entre la concentración de reportes, la presencia de puntos críticos, la disponibilidad de infraestructura para recolección y la estructura territorial, de modo que las zonas con mayor riesgo se puedan predecir y priorizar para intervención.

## Sección 3 – Datos y fuentes

### 11. Fuentes de datos identificadas (mínimo 2, preferiblemente provenientes del Portal de Datos Abiertos Bogotá)

- Cestas de recolección. Secretaría Distrital / entidad responsable de gestión de residuos. Enlace no público o disponible en el repositorio del proyecto.
- Macrorutas de barrido. Secretaría Distrital / entidad responsable de servicios de limpieza. Enlace no público o disponible en el repositorio del proyecto.
- Puntos críticos de arrojo clandestino de residuos. Datos geográficos públicos asociados al problema urbano. Enlace no público o incluido en la carpeta de datos del proyecto.
- Reportes/gestión de residuos y base geográfica. Información institucional o base integrada para análisis territorial. Enlace no público o incluido en el repositorio del proyecto.

### 12. Variables clave identificadas
Mencione las principales variables que utilizarán en el análisis.

- Ubicación geográfica de los puntos críticos
- Número de reportes por zona
- Distancia a cestas de recolección
- Cobertura de rutas de barrido
- Densidad de residuos en zonas críticas
- Indicadores territoriales de riesgo
- Variables de infraestructura y accesibilidad

### 13. Posible estrategia de integración de datos
¿Cómo planean relacionar las diferentes fuentes? (llaves, territorio, tiempo, etc.)

La estrategia de integración se basa en la relación geoespacial entre capas, mediante la proyección y unificación de los datasets a un mismo sistema de referencia. Se relacionan por territorio (geometría), además de variables de infraestructura y densidad de reportes, permitiendo construir una grilla analítica de Bogotá para modelar el riesgo.

### 14. ¿Los datos seleccionados contienen información geográfica, territorial o de segmentación institucional relevante para el análisis?
Sí ☐ No ☐ Parcialmente ☒

Sí, los datos tienen un fuerte componente geográfico y territorial, con capas espacializadas que permiten analizar la distribución del riesgo en la ciudad.

### 15. ¿Cuál es la principal entidad, sector o temática sobre la cual se enfoca el análisis?

Gestión pública / ambiente / residuos sólidos / servicios públicos urbanos.

## Sección 4 – Enfoque técnico y analítico

### 16. ¿El análisis incorpora variables o enfoques relacionados con género, inclusión o poblaciones diferenciales?
Seleccione una opción: Sí ☐ No ☐ En evaluación ☒

En caso afirmativo, describa brevemente cómo se incorporan estos enfoques en el análisis.

El análisis no incorpora de manera explícita variables de género o población diferencial como eje principal, pero puede considerarse en evaluación para interpretar la distribución territorial del riesgo y su relación con condiciones de acceso, infraestructura y densidad residencial en diferentes zonas de la ciudad.

### 17. Herramientas a utilizar (Selección múltiple)

· Python ☒

· R ☐

· Power BI ☐

· Excel ☐

· QGIS ☒

· Tableau ☐

· Looker Studio ☐

· Otro: Introduzca el nombre de cada una de las herramientas que emplearán.

Otros: GeoPandas, Folium, Streamlit, Jupyter Notebook, Scikit-learn

### 18. Tipo de análisis que esperan realizar (Selección múltiple)

· Análisis exploratorio ☒

· Construcción de indicadores ☒

· Modelos estadísticos ☒

· Visualización de datos ☒

· Modelos de IA ☐

· Análisis geoespacial ☒

· Otro: Introduzca el tipo de análisis que espera realizar.

Otro: Modelado predictivo de riesgo territorial y priorización operativa.

## Sección 5 – Visualización desarrollada y principales resultados

### 19. Descripción de la herramienta desarrollada
Describa la herramienta o visualización desarrollada por el equipo, indicando sus principales funcionalidades, la forma en que opera y los indicadores, análisis o visualizaciones más relevantes que presenta. Adjunte capturas de pantalla que permitan ilustrar la solución desarrollada y los principales hallazgos obtenidos.

Se desarrolló una herramienta interactiva en Streamlit para visualizar el riesgo territorial asociado a la gestión de residuos en Bogotá. La aplicación permite explorar un mapa general de riesgo, clasificar celdas por nivel de riesgo (alto, medio, bajo), simular rutas de servicio y visualizar el ranking de zonas prioritarias. La herramienta integra indicadores como probabilidad de riesgo, nivel de prioridad, número de reportes y cercanía a infraestructura de recolección.

### 20. Hallazgos y conclusiones
Describa los principales hallazgos obtenidos a partir del análisis realizado y las conclusiones o recomendaciones derivadas del ejercicio.

Se evidenció que existen zonas con mayor concentración de riesgo y puntos críticos, lo cual sugiere una brecha territorial significativa entre la cobertura de infraestructura y la demanda de servicio. Esto permite priorizar intervenciones en sitios con mayores niveles de riesgo y mayor necesidad operativa. La recomendación principal es orientar campañas de vigilancia, limpieza y reforzamiento de rutas hacia las zonas más críticas.

### 21. Impacto y utilidad de la solución desarrollada para la toma de decisiones
1. Explique de qué manera la solución desarrollada y los resultados del análisis podrían aportar a la comprensión o solución del problema público abordado.
2. Describa cómo la herramienta desarrollada y los resultados obtenidos pueden apoyar la toma de decisiones, la formulación de acciones, el diseño de políticas públicas o la comprensión de la problemática analizada.

La solución permite apoyar la toma de decisiones de forma territorial y operativa, identificando zonas prioritarias para intervención y orientación de recursos. Esto puede contribuir a mejorar la planeación, la asignación de rutas, la vigilancia de puntos críticos y la toma de decisiones sobre políticas públicas relacionadas con limpieza, gestión de residuos y servicios urbanos.

## Sección 6 – Experiencia de uso del Portal de Datos Abiertos de Bogotá

### 22. Describa brevemente su experiencia durante el desarrollo del DataJam, indicando, en caso de aplicar:
- Si había utilizado previamente el Portal de Datos Abiertos de Bogotá.
- Cómo califica la facilidad de uso del Portal.
- Las principales dificultades encontradas durante la búsqueda o uso de la información.
- Los aspectos que considera podrían mejorarse.
- Los elementos o funcionalidades que facilitaron su interacción con el Portal.

Durante el ejercicio se utilizó información geoespacial y datos de gestión territorial de la ciudad, con un proceso de revisión y limpieza necesario para integrar las distintas capas. El Portal resultó útil para la búsqueda inicial de información, aunque la disponibilidad, estructura y nomenclatura de algunos datasets requieren mayor estandarización. La experiencia puede calificarse como parcialmente favorable, con desafíos en la interoperabilidad y estandarización de atributos.

## Sección 7 – Observaciones del ejercicio

### 23. ¿Cuál ha sido el principal reto técnico o metodológico hasta el momento?
Detalle el principal reto encontrado.

El principal reto ha sido integrar distintas capas de información con diferencias en estructura, sistema de referencia espacial y calidad de datos, para construir una base analítica coherente que permita modelar el riesgo territorial.

### 24. ¿Qué consideran que les hace falta para desarrollar mejor su análisis?
Enliste los elementos que considera le podrían haber servido para desarrollar mejor el ejercicio.

- Mejor disponibilidad de metadatos y diccionarios de datos
- Mayor estandarización de nombres y atributos entre datasets
- Información con más frecuencia de actualización
- Mayor acceso a datos de contexto socioeconómico y de infraestructura
- Validación institucional del modelo y variables utilizadas

### 25. Comentarios adicionales sobre el DataJam o el uso de datos abiertos

El ejercicio permite fortalecer el uso de datos abiertos para la generación de diagnósticos territoriales con enfoque operativo y de política pública. La combinación entre datos geográficos, infraestructura y gestión de residuos resulta especialmente útil para orientar decisiones institucionales más informadas.
