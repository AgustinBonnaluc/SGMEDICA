export default function Navegacion({ usuario, pagina, cantidadAlertas, alCambiar, alSalir }) {
  const esMedico = usuario.rol === "medico";
  const solapas = esMedico
    ? [
        { id: "citas", texto: "Citas" },
        { id: "alertas", texto: `Alertas (${cantidadAlertas})` },
      ]
    : [
        { id: "citas", texto: "Mis citas" },
        { id: "expediente", texto: "Mi expediente" },
      ];

  return (
    <header className="navegacion">
      <strong className="marca">SGMEDICA</strong>
      <nav>
        {solapas.map((solapa) => (
          <button
            key={solapa.id}
            className={pagina === solapa.id ? "solapa activa" : "solapa"}
            onClick={() => alCambiar(solapa.id)}
          >
            {solapa.texto}
          </button>
        ))}
      </nav>
      <span className="usuario">
        {usuario.nombre} · {esMedico ? "Médico" : "Paciente"}
      </span>
      <button className="secundario" onClick={alSalir}>
        Salir
      </button>
    </header>
  );
}
