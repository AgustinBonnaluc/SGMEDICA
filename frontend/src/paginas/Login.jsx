import { useState } from "react";

import { iniciarSesion, registrarMedico, registrarPaciente } from "../api/cliente";

const MODOS = [
  { id: "ingresar", texto: "Ingresar" },
  { id: "paciente", texto: "Soy paciente nuevo" },
  { id: "medico", texto: "Soy médico nuevo" },
];

// Misma lista que valida el backend en schemas.py
const ESPECIALIDADES = [
  "Clínica médica",
  "Cardiología",
  "Pediatría",
  "Traumatología",
  "Dermatología",
  "Ginecología",
];

export default function Login({ alIngresar }) {
  const [modo, setModo] = useState("ingresar");
  const [datos, setDatos] = useState({});
  const [error, setError] = useState("");

  const cambiar = (evento) => setDatos({ ...datos, [evento.target.name]: evento.target.value });

  async function enviar(evento) {
    evento.preventDefault();
    setError("");
    try {
      if (modo === "paciente") await registrarPaciente(datos);
      if (modo === "medico") await registrarMedico(datos);
      alIngresar(await iniciarSesion(datos.email, datos.password));
    } catch (fallo) {
      setError(fallo.message);
    }
  }

  const campo = (nombre, etiqueta, tipo = "text", extras = {}) => (
    <label>
      {etiqueta}
      <input
        name={nombre}
        type={tipo}
        value={datos[nombre] ?? ""}
        onChange={cambiar}
        required
        {...extras}
      />
    </label>
  );

  return (
    <main className="login">
      <h1>SGMEDICA</h1>
      <p className="suave">Gestión médica y telemedicina</p>

      <div className="modos">
        {MODOS.map((opcion) => (
          <button
            key={opcion.id}
            type="button"
            className={modo === opcion.id ? "solapa activa" : "solapa"}
            onClick={() => setModo(opcion.id)}
          >
            {opcion.texto}
          </button>
        ))}
      </div>

      <form className="tarjeta" onSubmit={enviar}>
        {modo !== "ingresar" && campo("nombre", "Nombre y apellido")}
        {campo("email", "Email", "email")}
        {campo("password", "Contraseña (mínimo 6 caracteres)", "password", { minLength: 6 })}
        {modo === "paciente" && campo("fecha_nacimiento", "Fecha de nacimiento", "date")}
        {modo === "medico" && campo("matricula", "Matrícula", "text", { placeholder: "MN 12345" })}
        {modo === "medico" && (
          <label>
            Especialidad
            <select name="especialidad" value={datos.especialidad ?? ""} onChange={cambiar} required>
              <option value="">Elegir…</option>
              {ESPECIALIDADES.map((especialidad) => (
                <option key={especialidad}>{especialidad}</option>
              ))}
            </select>
          </label>
        )}
        {error && <p className="error">{error}</p>}
        <button type="submit">{modo === "ingresar" ? "Ingresar" : "Crear cuenta"}</button>
      </form>
    </main>
  );
}
