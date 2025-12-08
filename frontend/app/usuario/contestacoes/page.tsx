"use client";

import { useState, useEffect } from "react";
import toLocal from "@/lib/utils/localTime";
import Link from "next/link";

export default function Page() {
  const [dados, setDados] = useState<any[]>([]);
  const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

  async function getDados() {
    const url = `${apiUrl}/api/usuario/contestacoes`;
    const request = await fetch(url, {
      method: "GET",
      credentials: "include" as RequestCredentials,
    });
    return await request.json();
  }

  useEffect(() => {
    (async () => {
      const dados = await getDados();

      setDados(dados.contestacoes);
    })();
  });
  if (dados) {
    return (
      <div className="flex flex-row gap-[50px] justify-center">
        {dados.map((dados) => (
          <div key={dados.id} className="p-3 bg-gray-800 rounded-xl">
            <h1 className="text-[20px]">Motivo: {dados.motivo}</h1>
            <span>Reclamação: </span><Link className="text-blue-400 underline" href={`/reclamacao?id=${dados.reclamacaoId}`}>{dados.tituloReclamacao}</Link>
            <p>Autor: {dados.autor}</p>
            <p>Data de contestação: {toLocal(dados.dataContestacao)}</p>
            <div className="flex flex-col justify-center items-center">
              {dados.provas.map((foto: any) => (
                <img
                  className="w-[200px]"
                  key={foto.id}
                  src={apiUrl + foto.url}
                  alt=""
                />
              ))}
            </div>
          </div>
        ))}
      </div>
    );
  } else {
    return (
      <>
        <h1>Erro</h1>
      </>
    );
  }
}
