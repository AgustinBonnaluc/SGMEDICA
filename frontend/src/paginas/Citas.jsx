import { useEffect, useState } from "react";

import { agendarCita, cancelarCita, confirmarCita, listarCitas, listarMedicos } from "../api/cliente";
import { formatearFechaHora } from "../formato";

export default function Citas({ esMedico, alVerExpediente }) {
  const [citas, setCitas] = useState([]);
  const [medicos, setMedicos] = useState([]);
  const [medicoId, setMedicoId] = useState("");
  const [fecha, setFecha] = useState("");
  const [error, setError] = useState("");

  const cargarCitas = () => listarCitas().then(setCitas);

  useEffect(() => {
    cargarCitas().catch((fallo) => setError(fallo.message));
    if (!esMedico) listarMedicos().then(setMedicos);
  }, []);

  // Ejecuta una acción sobre las citas y refresca el listado
  async function ejecutar(accion) {
    setError("");
    try {
      await accion();
      await cargarCitas();
    } catch (fallo) {
      setError(fallo.message);
    }
  }

  function agendar(evento) {
    evento.preventDefault();
    ejecutar(() => agendarCita(Number(medicoId), fecha));
  }

  return (
    <>
      <h2>{esMedico ? "Citas de mis pacientes" : "Mis citas"}</h2>

      {!esMedico && (
        <form className="tarjeta fila" onSubmit={agendar}>
          <label>
            Médico
            <select value={medicoId} onChange={(e) => setMedicoId(e.target.value)} required>
              <option value="">Elegir…</option>
              {medicos.map((medico) => (
                <option key={medico.id} value={medico.id}>
                  {medico.nombre} · {medico.especialidad}
                </option>
              ))}
            </select>
          </label>
          <label>
            Fecha y hora
            <input
              type="datetime-local"
              value={fecha}
              onChange={(e) => setFecha(e.target.value)}
              required
            />
          </label>
          <button type="submit">Agendar cita</button>
        </form>
      )}

      {error && <p className="error">{error}</p>}

      {citas.length === 0 ? (
        <p className="suave">Todavía no hay citas.</p>
      ) : (
        <table className="tarjeta">
          <thead>
            <tr>
              <th>Fecha</th>
              <th>{esMedico ? "Paciente" : "Médico"}</th>
              <th>Estado</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {citas.map((cita) => (
              <tr key={cita.id}>
                <td>{formatearFechaHora(cita.fecha)}</td>
                <td>{esMedico ? cita.paciente.nombre : cita.medico.nombre}</td>
                <td>
                  <span className={`estado ${cita.estado}`}>{cita.estado}</span>
                </td>
                <td className="acciones">
                  {esMedico && cita.estado === "pendiente" && (
                    <button onClick={() => ejecutar(() => confirmarCita(cita.id))}>Confirmar</button>
                  )}
                  {cita.estado !== "cancelada" && (
                    <button
                      className="secundario"
                      onClick={() => ejecutar(() => cancelarCita(cita.id))}
                    >
                      Cancelar
                    </button>
                  )}
                  {esMedico && (
                    <button className="secundario" onClick={() => alVerExpediente(cita.paciente)}>
                      Ver expediente
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </>
  );
}
