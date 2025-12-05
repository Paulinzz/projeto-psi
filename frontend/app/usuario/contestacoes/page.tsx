"use client";

import { useState, useEffect } from "react";
import toLocal from "@/utils/localTime";

export default function Page() {
  const [dados, setDados] = useState<[] | null>(null);
  const API_URL = process.env.NEXT_PUBLIC_BACKEND_URL;

  async function getDados() {
    const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    const url = `${apiUrl}/api/usuario/contestacoes`;
    const request = await fetch(url, {
      method: "GET",
      credentials: "include" as RequestCredentials,
    });
    return await request.json();
  }

  useEffect(() => {
    if (dados === null) {
      (async () => {
        const dados = await getDados();

        setDados(dados.contestacoes);
      })();
    }
  });
  if (dados) {
    return (
      <div className="flex flex-row gap-[50px] justify-center">
        {dados.map((dados) => (
          <div key={dados.id} className="p-3 bg-gray-800 rounded-xl">
            <h1 className="text-[20px]">Motivo: {dados.motivo}</h1>
            <h3 className="text-[15px]">ID Reclamação: {dados.reclamacaoId}</h3>
            <h3 className="text-[15px]">ID Usuário: {dados.usuarioId}</h3>
            <p>Autor: {dados.autor}</p>
            <p>Data de contestação: {toLocal(dados.dataContestacao)}</p>
            <div className="flex flex-col justify-center items-center">
              {dados.provas.map((foto: any) => (
                <img
                  className="w-[200px]"
                  key={foto.id}
                  src={API_URL + foto.url}
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
