// Único lugar del frontend que conoce las URLs y el formato de la API

const API_URL = "http://localhost:8000";
export const ALERTAS_WS_URL = "ws://localhost:8001/ws/alertas";

export const hayToken = () => localStorage.getItem("token") !== null;
export const cerrarSesion = () => localStorage.removeItem("token");

const ERRORES_DE_CAMPO = {
  nombre: "Ingresá tu nombre y apellido",
  email: "El email no tiene un formato válido",
  password: "La contraseña debe tener entre 6 y 50 caracteres",
  fecha_nacimiento: "La fecha de nacimiento debe ser anterior a hoy",
  matricula: "La matrícula debe ser MN o MP seguido de 4 a 6 dígitos, por ejemplo MN 12345",
  especialidad: "Elegí una especialidad de la lista",
};

// En un error de validación (422) el detalle es una lista con el campo que falló
function mensajeDeError(detalle) {
  if (typeof detalle === "string") return detalle;
  const campo = detalle[0].loc.at(-1);
  return ERRORES_DE_CAMPO[campo] ?? "Revisá los datos ingresados";
}

async function pedir(metodo, ruta, cuerpo) {
  const token = localStorage.getItem("token");
  const respuesta = await fetch(API_URL + ruta, {
    method: metodo,
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
    },
    body: cuerpo && JSON.stringify(cuerpo),
  });
  const datos = await respuesta.json();
  if (!respuesta.ok) throw new Error(mensajeDeError(datos.detail));
  return datos;
}

export async function iniciarSesion(email, password) {
  const { access_token } = await pedir("POST", "/login", { email, password });
  localStorage.setItem("token", access_token);
  return obtenerUsuarioActual();
}

export const obtenerUsuarioActual = () => pedir("GET", "/yo");

export const registrarPaciente = ({ nombre, email, password, fecha_nacimiento }) =>
  pedir("POST", "/pacientes", { nombre, email, password, fecha_nacimiento });

export const registrarMedico = ({ nombre, email, password, matricula, especialidad }) =>
  pedir("POST", "/medicos", { nombre, email, password, matricula, especialidad });

export const listarMedicos = () => pedir("GET", "/medicos");
export const listarCitas = () => pedir("GET", "/citas");
export const agendarCita = (medico_id, fecha) => pedir("POST", "/citas", { medico_id, fecha });
export const confirmarCita = (id) => pedir("POST", `/citas/${id}/confirmar`);
export const cancelarCita = (id) => pedir("POST", `/citas/${id}/cancelar`);

export const agregarDiagnostico = (pacienteId, descripcion) =>
  pedir("POST", `/expedientes/${pacienteId}/diagnosticos`, { descripcion });

// GraphQL: se piden diagnósticos y métricas en una sola consulta
const CONSULTA_EXPEDIENTE = `
  query ($pacienteId: Int!) {
    expediente(pacienteId: $pacienteId) {
      diagnosticos { id descripcion fecha }
      metricas(limite: 10) { tipo valor timestamp }
    }
  }`;

export async function obtenerExpediente(pacienteId) {
  const { data, errors } = await pedir("POST", "/graphql", {
    query: CONSULTA_EXPEDIENTE,
    variables: { pacienteId },
  });
  if (errors) throw new Error(errors[0].message);
  return data.expediente;
}
