import { useEffect, useState } from "react";

import { ALERTAS_WS_URL } from "./cliente";

// Mantiene abierta la conexión WebSocket y acumula las alertas recibidas
export function useAlertas(activo) {
  const [alertas, setAlertas] = useState([]);

  useEffect(() => {
    if (!activo) return;
    const socket = new WebSocket(ALERTAS_WS_URL);
    socket.onmessage = (evento) => {
      const alerta = { ...JSON.parse(evento.data), hora: new Date() };
      setAlertas((anteriores) => [alerta, ...anteriores]);
    };
    return () => socket.close();
  }, [activo]);

  return alertas;
}
