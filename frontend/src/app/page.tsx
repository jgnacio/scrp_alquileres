"use client";

import { useEffect, useState } from "react";

type Inmueble = {
  imagen_url: string;
  es_dueno: boolean;
  moneda: string;
  precio: string;
  titulo: string;
  detalles: string;
  area_m2: string;
  id: string;
  tiene_telefono: boolean;
  whatsapp_link: string;
  url: string;
};

type ScraperData = {
  last_updated: string;
  data: Inmueble[];
};

export default function Home() {
  const [inmuebles, setInmuebles] = useState<Inmueble[]>([]);
  const [lastUpdated, setLastUpdated] = useState<string>("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/alquileres.json")
      .then((res) => {
        if (!res.ok) throw new Error("No hay datos disponibles.");
        return res.json();
      })
      .then((payload: ScraperData) => {
        setInmuebles(payload.data || []);
        setLastUpdated(payload.last_updated || "");
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error cargando el JSON:", error);
        setLoading(false);
      });
  }, []);

  const getSourceBadge = (url: string) => {
    const u = url.toLowerCase();
    if (u.includes("gallito")) return "Gallito Luis";
    if (u.includes("infocasas")) return "InfoCasas";
    if (u.includes("mercadolibre")) return "MercadoLibre";
    return "Propiedad";
  };

  return (
    <div className="min-h-screen bg-white text-black font-sans selection:bg-gray-100">
      <header className="border-b border-black py-10 px-6 md:px-12 bg-white flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
          <h1 className="text-5xl md:text-6xl font-black tracking-tighter uppercase leading-none">
            Alquileres
          </h1>
          <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 mt-4">
            <p className="text-gray-400 text-[10px] tracking-[0.2em] uppercase font-bold">
              Monitor de Propiedades
            </p>
            {lastUpdated && (
              <span className="hidden sm:inline-block w-1 h-1 rounded-full bg-gray-300"></span>
            )}
            {lastUpdated && (
              <p className="text-black text-[10px] tracking-[0.1em] uppercase font-bold">
                Actualizado: {lastUpdated}
              </p>
            )}
          </div>
        </div>
        <div className="text-xs font-black tracking-widest border border-black px-4 py-2 uppercase">
          {inmuebles.length} Resultados
        </div>
      </header>

      <main className="max-w-[1500px] mx-auto py-16 px-6 md:px-12">
        {loading ? (
          <div className="flex flex-col items-center justify-center py-40">
            <div className="w-12 h-1 bg-black animate-pulse mb-4"></div>
            <p className="text-[10px] tracking-[0.3em] font-bold uppercase text-gray-400">
              Sincronizando...
            </p>
          </div>
        ) : inmuebles.length === 0 ? (
          <div className="text-center py-40">
            <p className="text-gray-400 tracking-widest text-sm uppercase">
              No se encontraron listados en este momento.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-x-8 gap-y-16">
            {inmuebles.map((inm, idx) => (
              <div
                key={inm.id || idx}
                className="group flex flex-col relative bg-white"
              >
                {/* Image Container */}
                <a
                  href={inm.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="aspect-[4/5] w-full overflow-hidden bg-gray-50 border border-gray-100 relative block"
                >
                  {inm.es_dueno && (
                    <div className="absolute top-0 left-0 z-10 bg-black text-white text-[9px] font-black uppercase py-1.5 px-3 tracking-[0.15em]">
                      Dueño Directo
                    </div>
                  )}
                  
                  <div className="absolute top-0 right-0 z-10 bg-white border-l border-b border-gray-100 text-black text-[9px] font-black uppercase py-1.5 px-3 tracking-[0.15em]">
                    {getSourceBadge(inm.url)}
                  </div>

                  {inm.imagen_url ? (
                    <img
                      src={inm.imagen_url}
                      alt={inm.titulo}
                      className="object-cover w-full h-full grayscale-[100%] group-hover:grayscale-0 transition-all duration-700 ease-in-out group-hover:scale-105"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-gray-200 text-[10px] tracking-widest uppercase">
                      Imagen no disponible
                    </div>
                  )}
                </a>

                {/* Content */}
                <div className="pt-6 flex flex-col flex-grow">
                  <header className="mb-4">
                    <div className="flex items-baseline justify-between gap-2 mb-2">
                       <span className="font-black text-2xl tracking-tighter">
                        {inm.moneda} {inm.precio}
                      </span>
                      {inm.area_m2 && (
                        <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">
                          {inm.area_m2}
                        </span>
                      )}
                    </div>
                    <h2 className="font-bold text-sm tracking-tight leading-snug line-clamp-2 uppercase group-hover:underline underline-offset-4 decoration-1">
                      {inm.titulo || "PROPIEDAD SIN TÍTULO"}
                    </h2>
                  </header>

                  <p className="text-gray-500 text-[11px] leading-relaxed line-clamp-3 mb-6 font-medium">
                    {inm.detalles}
                  </p>

                  <div className="mt-auto grid grid-cols-1 gap-2">
                    {inm.whatsapp_link ? (
                      <a
                        href={inm.whatsapp_link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="bg-black text-white text-[10px] font-black uppercase py-4 px-4 tracking-[0.2em] flex items-center justify-center hover:bg-gray-800 transition-colors"
                      >
                         WhatsApp Chat
                      </a>
                    ) : (
                      <a
                      href={inm.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="bg-black text-white text-[10px] font-black uppercase py-4 px-4 tracking-[0.2em] flex items-center justify-center hover:bg-gray-800 transition-colors"
                    >
                       Ver Publicación
                    </a>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      <footer className="border-t border-gray-100 mt-20 py-12 px-6 text-center">
        <p className="text-[10px] tracking-[0.4em] font-black uppercase text-gray-300">
          {new Date().getFullYear()}
        </p>
      </footer>
    </div>
  );
}
