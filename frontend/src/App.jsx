import { useEffect, useState } from "react";

import { cerrarSesion, hayToken, obtenerUsuarioActual } from "./api/cliente";
import { useAlertas } from "./api/useAlertas";
import Navegacion from "./componentes/Navegacion";
import Alertas from "./paginas/Alertas";
import Citas from "./paginas/Citas";
import Expediente from "./paginas/Expediente";
import Login from "./paginas/Login";

export default function App() {
  const [usuario, setUsuario] = useState(null);
  const [cargando, setCargando] = useState(hayToken());
  const [pagina, setPagina] = useState("citas");
  // Paciente cuyo expediente está viendo un médico
  const [pacienteElegido, setPacienteElegido] = useState(null);

  const esMedico = usuario?.rol === "medico";
  const alertas = useAlertas(esMedico);

  // Si quedó un token guardado, se recupera la sesión al abrir la página
  useEffect(() => {
    if (!hayToken()) return;
    obtenerUsuarioActual()
      .then(setUsuario)
      .catch(cerrarSesion)
      .finally(() => setCargando(false));
  }, []);

  function salir() {
    cerrarSesion();
    setUsuario(null);
    setPagina("citas");
  }

  function verExpediente(paciente) {
    setPacienteElegido(paciente);
    setPagina("expediente");
  }

  if (cargando) return null;
  if (!usuario) return <Login alIngresar={setUsuario} />;

  return (
    <>
      <Navegacion
        usuario={usuario}
        pagina={pagina}
        cantidadAlertas={alertas.length}
        alCambiar={setPagina}
        alSalir={salir}
      />
      <main>
        {pagina === "citas" && <Citas esMedico={esMedico} alVerExpediente={verExpediente} />}
        {pagina === "expediente" && (
          <Expediente
            paciente={esMedico ? pacienteElegido : usuario}
            esMedico={esMedico}
            alVolver={() => setPagina("citas")}
          />
        )}
        {pagina === "alertas" && <Alertas alertas={alertas} />}
      </main>
    </>
  );
}
