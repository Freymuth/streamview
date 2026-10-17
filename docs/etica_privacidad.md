# Ética y uso responsable de los datos

## Naturaleza de los datos

Los datasets utilizados corresponden a un extracto anonimizado y consolidado
del catálogo corporativo de StreamView Analytics, entregado con fines
académicos. No contienen datos personales de usuarios ni de suscriptores: la
información es a nivel de título (película o serie), no de persona.

## Riesgos de interpretación

- **`popularity` no es calidad ni éxito comercial real**: es un índice relativo
  de una fuente externa (estilo TMDB). Usarlo como único criterio para decidir
  qué contenido promocionar o retirar puede sobrerrepresentar títulos con
  buena exposición mediática por sobre contenido de nicho igualmente valioso.
- **Representación geográfica desigual**: la mayoría del catálogo proviene de
  un número reducido de países (liderado por Estados Unidos). Cualquier
  recomendación de "priorizar mercados" debe considerar que la ausencia de un
  país en el top no necesariamente indica falta de demanda, sino falta de
  representación en el catálogo actual.
- **Cobertura financiera parcial**: solo el 11% de los títulos tiene
  presupuesto e ingresos conocidos. Cualquier conclusión financiera (ROI,
  rentabilidad por género) aplica solo a ese subconjunto y no debe
  generalizarse al catálogo completo sin esa advertencia explícita.

## Uso previsto

Este análisis está pensado como apoyo a la toma de decisiones humana
(Directorio, Gerencia de Contenidos, Marketing), no como un sistema que decida
automáticamente qué contenido adquirir, promocionar o retirar. El proyecto no
incluye modelos predictivos ni algoritmos de decisión automatizada.
