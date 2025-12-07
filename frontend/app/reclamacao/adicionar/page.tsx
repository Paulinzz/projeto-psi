"use client";

import Required from "@/components/ui/Required";
import "@/public/css/form.css";
import { getIconByStatus } from "@/lib/utils/alerts";
import { useRouter } from "next/navigation";
import { useState } from "react";
import Swal from "sweetalert2";

export default function Page() {
  const [files, setFiles] = useState<File[]>([]);
  const router = useRouter();

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;

    const formData = new FormData(form);

    const url = `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/reclamacao/adicionar`;
    const response = await fetch(url, {
      method: "POST",
      credentials: "include" as RequestCredentials,
      body: formData,
    });

    const json = await response.json();

    if (json.message) {
      Swal.fire({
        title:"Reclamação",
        text: json.message,
        icon: getIconByStatus(response.status)
      }).then(() => {
        if (response.status === 201) {
          router.push(`/reclamacao?id=${json.reclamacao.id}`)
        }
      });
    }
    return {
      ok: response.ok,
      status: response.status,
      data: json
    };
  }

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    if (!e.target.files) return;

    const files = Array.from(e.target.files);
    setFiles(files);
  }

  return (
    <main className="flex align-center justify-center h-full">
      <form
        onSubmit={handleSubmit}
        className="flex flex-col gap-2 bg-gray-800 rounded-xl p-2 px-10"
      >
        <label htmlFor="titulo">
          Titulo<Required/>
        </label>
        <input
          required
          id="titulo"
          name="titulo"
          type="text"
          placeholder="Insira o título"
        />
        <label htmlFor="descricao">
          Descrição<Required/>
        </label>
        <input
          required
          id="descricao"
          name="descricao"
          type="text"
          placeholder="Insira a descrição"
        />
        <label htmlFor="cidade">
          Cidade<Required/>
        </label>
        <input
          required
          id="cidade"
          name="cidade"
          type="text"
          placeholder="Insira a cidade"
        />
        <label htmlFor="endereco">Endereço</label>
        <input
          id="endereco"
          name="endereco"
          type="text"
          placeholder="Insira a cidade"
        />
        <label htmlFor="endereco">Fotos</label>
        <input
          type="file"
          name="fotos"
          multiple
          onChange={handleFileChange}
          accept="image/*"
        />
        <ul>
          {files.map((file, index) => (
            <li key={index}>{file.name}</li>
          ))}
        </ul>
        <button type="submit" className="rounded">
          Adicionar
        </button>
      </form>
    </main>
  );
}
