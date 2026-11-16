export const formatearFecha = (fecha) => new Date(fecha).toLocaleDateString("es-AR");

export const formatearFechaHora = (fecha) =>
  new Date(fecha).toLocaleString("es-AR", { dateStyle: "short", timeStyle: "short" });

export const formatearHora = (fecha) => new Date(fecha).toLocaleTimeString("es-AR");

const NOMBRES_DE_METRICAS = {
  pulso: "Pulso",
  presion_sistolica: "Presión sistólica",
  presion_diastolica: "Presión diastólica",
};

export const nombreDeMetrica = (tipo) => NOMBRES_DE_METRICAS[tipo] ?? tipo;
