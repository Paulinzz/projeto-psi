"use client";

import "../../login/form.css";
import { useSearchParams } from "next/navigation";
import { useState } from "react";

export default function Page() {
  const [files, setFiles] = useState<File[]>([]);
  const pPesquisa = useSearchParams();
  const id = Number(pPesquisa.get("id"));

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    const formData = new FormData(form);
    const url = `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/reclamacao/${id}/contestacao/atualizar`;
    const requisicao = await fetch(url, {
      method: "POST",
      credentials: "include" as RequestCredentials,
      body: formData,
    });

    return await requisicao.json();
  }

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    if (!e.target.files) return;

    const files = Array.from(e.target.files);
    setFiles(files);
  }
  return (
    <main className="flex justify-center">
      <form
        onSubmit={handleSubmit}
        className="flex flex-col gap-2 bg-gray-800 rounded-xl p-2 px-10"
      >
        <label htmlFor="motivo">
          Motivo<span className="text-red-500">*</span>
        </label>
        <input
          required
          id="motivo"
          name="motivo"
          type="text"
          placeholder="Insira o motivo"
        />
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
          Atualizar
        </button>
      </form>
    </main>
  );
}
