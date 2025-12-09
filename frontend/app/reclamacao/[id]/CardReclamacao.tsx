"use client";

import { Reclamacao } from "@/types";
import toLocal from "@/lib/utils/localTime";

export default function CardReclamacao({ reclamacao } : { reclamacao: Reclamacao}) {
  const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

  return (
    <div className="flex flex-col p-3 bg-gray-800 rounded-xl mx-[100px]">
      <h1 className="text-[20px] font-bold">{reclamacao.titulo}</h1>
      <h3 className="text-[15px] font-bold">Descrição: {reclamacao.descricao}</h3>
      <ul>
        <li>Cidade: {reclamacao.cidade}</li>
        <li>Endereço: {reclamacao.endereco}</li>
        <li>Status: {reclamacao.status}</li>
        <li>Autor: {reclamacao.autor}</li>
        <li>Data criada: {toLocal(reclamacao.dataCriacao)}</li>
        <li>Data resolvida: {toLocal(reclamacao.dataResolucao)}</li>
        <li>Data atualizada: {toLocal(reclamacao.dataAtualizacao)}</li>
      </ul>
      <div className="flex flex-row gap-[20px] justify-center items-center">
        {reclamacao.fotos.map((foto) => (
          <img
            className="w-[200px]"
            key={foto.id}
            src={apiUrl + foto.url}
            alt=""
          />
        ))}
      </div>
    </div>  
  );
}
