import { useEffect, useState } from "react";

import { agregarDiagnostico, obtenerExpediente } from "../api/cliente";
import { formatearFecha, formatearFechaHora, nombreDeMetrica } from "../formato";

export default function Expediente({ paciente, esMedico, alVolver }) {
  const [expediente, setExpediente] = useState(null);
  const [descripcion, setDescripcion] = useState("");
  const [error, setError] = useState("");

  const cargar = () =>
    obtenerExpediente(paciente.id)
      .then(setExpediente)
      .catch((fallo) => setError(fallo.message));

  useEffect(() => {
    cargar();
  }, [paciente.id]);

  async function guardarDiagnostico(evento) {
    evento.preventDefault();
    setError("");
    try {
      await agregarDiagnostico(paciente.id, descripcion);
      setDescripcion("");
      await cargar();
    } catch (fallo) {
      setError(fallo.message);
    }
  }

  return (
    <>
      <div className="titulo">
        <h2>{esMedico ? `Expediente de ${paciente.nombre}` : "Mi expediente"}</h2>
        <button className="secundario" onClick={cargar}>
          Actualizar
        </button>
        {esMedico && (
          <button className="secundario" onClick={alVolver}>
            Volver a citas
          </button>
        )}
      </div>

      {error && <p className="error">{error}</p>}

      {expediente && (
        <>
          <section className="tarjeta">
            <h3>Diagnósticos</h3>
            {expediente.diagnosticos.length === 0 && (
              <p className="suave">Sin diagnósticos cargados.</p>
            )}
            <ul>
              {expediente.diagnosticos.map((diagnostico) => (
                <li key={diagnostico.id}>
                  <span className="suave">{formatearFecha(diagnostico.fecha + "T00:00")}</span>
                  {diagnostico.descripcion}
                </li>
              ))}
            </ul>
            {esMedico && (
              <form className="fila" onSubmit={guardarDiagnostico}>
                <input
                  placeholder="Nuevo diagnóstico"
                  value={descripcion}
                  onChange={(e) => setDescripcion(e.target.value)}
                  required
                />
                <button type="submit">Agregar</button>
              </form>
            )}
          </section>

          <section className="tarjeta">
            <h3>Últimas métricas del dispositivo</h3>
            {expediente.metricas.length === 0 ? (
              <p className="suave">El dispositivo todavía no envió métricas.</p>
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>Fecha</th>
                    <th>Métrica</th>
                    <th>Valor</th>
                  </tr>
                </thead>
                <tbody>
                  {expediente.metricas.map((metrica) => (
                    <tr key={metrica.timestamp + metrica.tipo}>
                      <td>{formatearFechaHora(metrica.timestamp)}</td>
                      <td>{nombreDeMetrica(metrica.tipo)}</td>
                      <td>{metrica.valor}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </section>
        </>
      )}
    </>
  );
}
