# Problema de negocio

## La empresa

StreamView Analytics es una plataforma de streaming fundada en 2018, especializada
en la distribución de contenido audiovisual (películas, series, documentales y
producciones originales) en distintos mercados de Latinoamérica, bajo un modelo
de suscripción digital.

## Situación actual

StreamView administra miles de títulos, pero cada área de la organización utiliza
reportes independientes construidos con criterios distintos. Como consecuencia:

- existen múltiples versiones de un mismo indicador;
- los ejecutivos dedican gran parte de su tiempo a interpretar reportes;
- las decisiones de adquisición de contenidos se toman con información parcial;
- no es posible comparar rápidamente géneros, países o el desempeño financiero
  de las películas.

## Pregunta que responde este proyecto

> ¿Qué caracteriza al catálogo audiovisual de StreamView Analytics, qué contenido
> genera más interés y valoración, y qué evidencia financiera respalda las
> decisiones de adquisición de nuevas películas?

Es un problema descriptivo y de comunicación visual (Visual Analytics), no un
problema de modelamiento predictivo: el objetivo es transformar los datos
disponibles en conocimiento accionable para el Directorio y las gerencias de
Contenidos, Marketing y Producto.

## Fuente de datos

- `data/raw/netflix_movies_detailed_up_to_2025.csv` (16.000 películas, 18 variables)
- `data/raw/netflix_tv_shows_detailed_up_to_2025.csv` (16.000 series, 16 variables)

Ambos datasets son la fuente oficial entregada para el caso semestral y no se
reemplazan ni se modifica su estructura original.

## Stakeholders y sus necesidades

| Stakeholder | Necesidad |
|---|---|
| Directorio | Indicadores consolidados, tendencias, recomendaciones ejecutivas |
| Gerencia General | Visión global del catálogo para planificación estratégica |
| Gerencia de Contenidos y Adquisición | Géneros, países y contenidos con mayor potencial estratégico |
| Gerencia de Marketing | Contenidos más populares, categorías con mayor potencial comercial |
| Gerencia de Producto | Características del catálogo para mejorar la experiencia de navegación |
| Equipo de Data & Analytics | Mantenimiento y calidad de los dashboards corporativos |

## KPIs y reglas de negocio oficiales

- Total de contenidos, películas, series, países, idiomas y géneros.
- Popularidad y calificación promedio (general y por género/país/idioma).
- Presupuesto promedio, ingresos totales y ROI aproximado (`revenue / budget`),
  **solo para películas** con presupuesto e ingresos conocidos.
- `popularity` es un índice relativo (no representa reproducciones).
- `vote_average` está en escala 0 a 10.
- Los contenidos sin datos financieros se excluyen de los indicadores financieros
  en vez de tratarse como presupuesto/ingreso igual a cero.

## Alcance

El proyecto no considera modelos predictivos, algoritmos de inteligencia
artificial ni procesos ETL sobre sistemas operacionales reales: se trabaja
exclusivamente sobre los dos datasets entregados, con foco en preparación de
datos, reglas de negocio, visualización y storytelling ejecutivo.
