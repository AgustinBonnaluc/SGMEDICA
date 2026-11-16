import { formatearHora } from "../formato";

export default function Alertas({ alertas }) {
  return (
    <>
      <h2>Alertas en tiempo real</h2>
      <p className="suave">Se muestran los pulsos que superan el umbral desde que ingresaste.</p>

      {alertas.length === 0 ? (
        <p className="tarjeta suave">Sin alertas por ahora.</p>
      ) : (
        <ul className="tarjeta">
          {alertas.map((alerta, indice) => (
            <li key={alertas.length - indice} className="alerta">
              <span className="suave">{formatearHora(alerta.hora)}</span>
              {alerta.mensaje}
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
