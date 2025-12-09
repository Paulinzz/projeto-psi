"use client";

import React, { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Swal from "sweetalert2";
import { getIconByStatus } from "@/lib/utils/alerts"
import "@/public/css/form.css";
import Required from "@/components/ui/Required";
import { useAuth } from "@/context/AuthContext";


export default function LoginForm() {
  const params = useSearchParams();
  const redirect = params.get("redirect");
  const [showModal, setShowModal] = useState(true);
  
  if (redirect && showModal) {
    Swal.fire(
      {
        title: "Autenticação Necessária",
        text: "Faça login para acessar essa página",
        icon: "error"
      }
    );
    
    setShowModal(false);
  }
  
  const [isSubmitting, setIsSubmitting] = useState(false);
  const router = useRouter();
  const { setAuthState } = useAuth();
  
  async function requisitarLogin(data: {
    email: string;
    password: string;
  }) {
    const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    
    const url = `${apiUrl}/api/login`;
    const options = {
      method: "POST",
      credentials: "include" as RequestCredentials,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    };
    const response = await fetch(url, options);
    const json = await response.json();
    
    return {
      ok: response.ok,
      status: response.status,
      data: json
    };
  }
  
  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setIsSubmitting(true);
    
    const form = e.currentTarget;
    const formData = new FormData(form);
    const data = {
      email: String(formData.get("email")),
      password: String(formData.get("senha")),
    };

    const response = await requisitarLogin(data);
    if (response.data.message) {
      Swal.fire({
        title:"Login",
        text: response.data.message,
        icon: getIconByStatus(response.status)
      }).then(() => {
        if (response.status === 200) {
          setAuthState(true, response.data.usuario);
          if (redirect) {
            router.push(redirect);
          }
          else {
            router.push("/")
          }
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
      <label htmlFor="email">Email <Required/></label>
      <input type="text" id="email" name="email" required />

      <label htmlFor="senha">Senha <Required/></label>
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
