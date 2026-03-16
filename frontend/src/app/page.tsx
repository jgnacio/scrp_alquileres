"use client";

import { useEffect, useState } from "react";
import Image from "next/image";

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

export default function Home() {
  const [inmuebles, setInmuebles] = useState<Inmueble[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch from the public directory (served at root in Vercel)
    fetch("/alquileres.json")
      .then((res) => {
        if (!res.ok) throw new Error("No data found");
        return res.json();
      })
      .then((data) => {
        setInmuebles(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        setLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen bg-white text-black font-sans selection:bg-gray-200">
      <header className="border-b border-black py-8 px-6 md:px-12 flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tighter uppercase">
            Alquileres
          </h1>
          <p className="text-gray-500 text-sm mt-2 tracking-widest uppercase">
            Actualizados diariamente
          </p>
        </div>
        <div className="text-sm font-semibold tracking-wider">
          {inmuebles.length} RESULTADOS
        </div>
      </header>

      <main className="max-w-[1600px] mx-auto py-12 px-6 md:px-12">
        {loading ? (
          <div className="flex h-64 items-center justify-center">
            <p className="text-gray-400 tracking-widest text-sm uppercase animate-pulse">
              Cargando datos...
            </p>
          </div>
        ) : inmuebles.length === 0 ? (
          <div className="flex h-64 items-center justify-center">
            <p className="text-gray-400 tracking-widest text-sm uppercase">
              No se encontraron listados.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
            {inmuebles.map((inm, idx) => (
              <a
                key={inm.id || idx}
                href={inm.url}
                target="_blank"
                rel="noopener noreferrer"
                className="group flex flex-col border border-gray-200 hover:border-black transition-all duration-300 relative bg-white"
              >
                {inm.es_dueno && (
                  <div className="absolute top-4 left-4 z-10 bg-black text-white text-[10px] font-bold uppercase py-1 px-3 tracking-widest">
                    Dueño Directo
                  </div>
                )}
                
                <div className="aspect-[4/3] w-full overflow-hidden bg-gray-50 border-b border-gray-100 relative">
                  {inm.imagen_url ? (
                    <img
                      src={inm.imagen_url}
                      alt={inm.titulo || "Inmueble"}
                      className="object-cover w-full h-full group-hover:scale-105 transition-transform duration-700 ease-in-out grayscale-[20%] group-hover:grayscale-0"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-gray-300 text-xs tracking-widest uppercase">
                      Sin imagen
                    </div>
                  )}
                </div>

                <div className="p-6 flex flex-col flex-grow">
                  <div className="mb-4">
                    <h2 className="font-bold text-lg leading-snug mb-2 line-clamp-2">
                      {inm.titulo || "Inmueble sin título"}
                    </h2>
                    <p className="text-gray-500 text-xs leading-relaxed line-clamp-3">
                      {inm.detalles}
                    </p>
                  </div>

                  <div className="mt-auto pt-6 border-t border-gray-100 flex items-end justify-between">
                    <div>
                      <span className="text-[10px] text-gray-400 uppercase tracking-widest block mb-1">
                        Precio
                      </span>
                      <span className="font-black text-2xl tracking-tight">
                        {inm.moneda} {inm.precio}
                      </span>
                    </div>
                    <span className="text-xs font-bold uppercase tracking-wider border-b border-transparent group-hover:border-black transition-colors pb-0.5">
                      Ver Detalles →
                    </span>
                  </div>
                </div>
              </a>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
