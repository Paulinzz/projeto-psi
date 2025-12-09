"use client";

import "@/public/css/form.css";
import cadastroAction from "./actions";
import Required from "@/components/ui/Required";
import React, { useState } from "react";
import Swal from "sweetalert2";
import { getIconByStatus } from "@/lib/utils/alerts";
import { useRouter } from "next/navigation";

export default function CadastroForm() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const router = useRouter();

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setIsSubmitting(true);

    const form = e.currentTarget;
    const formData = new FormData(form);
    const data = {
      username: String(formData.get("nome")),
      email: String(formData.get("email")),
      password: String(formData.get("senha")),
    };

    const response = await cadastroAction(data);
    
    if (response.data.message) {
      Swal.fire({
        title: "Cadastro",
        text: response.data.message,
        icon: getIconByStatus(response.status)
      }).then(() => {
        if (response.status === 201) {
          router.push("/login");
        }
      });
    }

    setIsSubmitting(false);
  }

  return (
    <form
      onSubmit={onSubmit}
      className="flex flex-col gap-2 bg-gray-800 rounded-xl p-2 px-5"
      method="post"
    >
      <label htmlFor="nome">Nome<Required/></label>
      <input type="text" id="nome" name="nome" required />

      <label htmlFor="email">Email<Required/></label>
      <input type="email" id="email" name="email" required />

      <label htmlFor="senha">Senha<Required/></label>
      <input type="password" id="senha" name="senha" required />

      <button
        className="rounded"
        type="submit"
        disabled={isSubmitting}
      >
        {
          isSubmitting ? "Entrando..." : "Iniciar sessão"
        }
      </button>
    </form>
  );
}
