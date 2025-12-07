"use client";

import { getIconByStatus } from "@/lib/utils/alerts";
import "@/public/css/form.css";
import { useRouter, useSearchParams } from "next/navigation";
import { useState } from "react";
import Swal from "sweetalert2";

export default function Page() {
  const router = useRouter();

  const [files, setFiles] = useState<File[]>([]);
  const pPesquisa = useSearchParams();
  const id = Number(pPesquisa.get("id"));

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    const formData = new FormData(form);
    const url = `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/contestacao/${id}/atualizar`;
    const response = await fetch(url, {
      method: "POST",
      credentials: "include" as RequestCredentials,
      body: formData,
    });

    const json = await response.json();
  
    if (json.message) {
      Swal.fire({
        title:"Atualizar Contestação",
        text: json.message,
        icon: getIconByStatus(response.status)
      }).then(() => {
        if (response.status === 200) {
          router.push(`/reclamacao?id=${id}`)
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
    <main className="flex justify-center">
      <form
        onSubmit={handleSubmit}
        className="flex flex-col gap-2 bg-gray-800 rounded-xl p-2 px-10"
      >
        <label htmlFor="motivo">
          Motivo
        </label>
        <input
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
