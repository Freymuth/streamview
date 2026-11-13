// ============================================================================
// StreamView Analytics - Power Query (M) para Power BI Desktop
//
// 1) Inicio > Transformar datos > Administrar parametros > Nuevo parametro:
//      Nombre: RutaDatos   Tipo: Texto   Valor actual: la carpeta powerbi\data\ de TU computador,
//      con la barra final. Ej.: C:\Users\chris\streamview-analytics\powerbi\data\
// 2) Inicio > Nueva fuente > Consulta en blanco > Editor avanzado, y pegar UNA consulta por tabla
//    (renombrar cada consulta con el nombre indicado en el comentario).
//
// IMPORTANTE: cada consulta fuerza la cultura "en-US" al convertir tipos. Tu Windows usa coma
// decimal (es-CL): sin esto, 6.63 se leeria como 663 y los promedios saldrian mal.
// Para cambiar de computador solo se edita el parametro RutaDatos.
// ============================================================================

// ---- Consulta: fact_catalogo ----
let
    Origen = Csv.Document(File.Contents(RutaDatos & "fact_catalogo.csv"), [Delimiter=",", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    Tipos = Table.TransformColumnTypes(Encabezados, {{"uid", type text}, {"show_id", Int64.Type}, {"tipo", type text}, {"titulo", type text}, {"anio_estreno", Int64.Type}, {"anio_incorporacion", Int64.Type}, {"idioma", type text}, {"popularidad", type number}, {"popularidad_percentil", type number}, {"votos", Int64.Type}, {"vote_average_original", type number}, {"calificacion", type number}}, "en-US")
in
    Tipos

// ---- Consulta: fact_financiero ----
let
    Origen = Csv.Document(File.Contents(RutaDatos & "fact_financiero.csv"), [Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    Tipos = Table.TransformColumnTypes(Encabezados, {{"uid", type text}, {"titulo", type text}, {"presupuesto", type number}, {"ingresos", type number}, {"roi", type number}, {"ganancia", type number}, {"presupuesto_realista", type logical}}, "en-US")
in
    Tipos

// ---- Consulta: bridge_genero ----
let
    Origen = Csv.Document(File.Contents(RutaDatos & "bridge_genero.csv"), [Delimiter=",", Columns=2, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    Tipos = Table.TransformColumnTypes(Encabezados, {{"uid", type text}, {"genero", type text}}, "en-US")
in
    Tipos

// ---- Consulta: bridge_pais ----
let
    Origen = Csv.Document(File.Contents(RutaDatos & "bridge_pais.csv"), [Delimiter=",", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    Tipos = Table.TransformColumnTypes(Encabezados, {{"uid", type text}, {"pais", type text}, {"iso3", type text}}, "en-US")
in
    Tipos

// ---- Consulta: bridge_director ----
let
    Origen = Csv.Document(File.Contents(RutaDatos & "bridge_director.csv"), [Delimiter=",", Columns=2, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    Tipos = Table.TransformColumnTypes(Encabezados, {{"uid", type text}, {"director", type text}}, "en-US")
in
    Tipos

// ---- Consulta: bridge_actor ----
let
    Origen = Csv.Document(File.Contents(RutaDatos & "bridge_actor.csv"), [Delimiter=",", Columns=2, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    Tipos = Table.TransformColumnTypes(Encabezados, {{"uid", type text}, {"actor", type text}}, "en-US")
in
    Tipos

// ---- Consulta: dim_calendario ----
let
    Origen = Csv.Document(File.Contents(RutaDatos & "dim_calendario.csv"), [Delimiter=",", Columns=1, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    Tipos = Table.TransformColumnTypes(Encabezados, {{"anio", Int64.Type}}, "en-US")
in
    Tipos
