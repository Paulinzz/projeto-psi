"use client";

import { useState, useEffect } from "react";
import toLocal from "@/lib/utils/localTime";
import { useSearchParams, useRouter } from "next/navigation";
import clsx from "clsx";
import { useAuth } from "@/context/AuthContext";

export default function Page() {
  const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
  const [dados, setDados] = useState<any[]>([]);
  const pPesquisa = useSearchParams();
  const reclamacaoId = pPesquisa.get("idReclamacao");
  const router = useRouter();
  const { autenticado, usuario } = useAuth();
  
  async function getDados() {
    const url = `${apiUrl}/api/reclamacao/${reclamacaoId}/contestacoes`;
    const response = await fetch(url, {
      method: "GET"
    });
    return response;
  }

  useEffect(() => {
    (async () => {
      const response = await getDados();
      const result = await response.json();
      setDados(result.contestacoes);
    })();
    }, []);

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
                  src={apiUrl + foto.url}
                  alt=""
                />
              ))}
            </div>
            <button
              className={clsx("bg-gray-700 rounded p-3 cursor-pointer", {
                invisible: Number(dados.usuarioId) !== Number(usuario?.id),
                visible: Number(dados.usuarioId) === Number(usuario?.id),
              })}
              type="button"
              onClick={() => {
                router.push(`/contestacao/atualizar?id=${dados.id}`);
              }}
            >
              Atualizar contestação
            </button>
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
