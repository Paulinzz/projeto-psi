"use client"

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Swal from "sweetalert2";
import { getIconByStatus } from "@/lib/utils/alerts";
import { useAuth } from "@/context/AuthContext";

export default function Page() {
  const router = useRouter();
  const { clearAuthState } = useAuth();

  async function logout() {
    const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

    const options = {
        method: "POST",
        credentials: "include" as RequestCredentials
    };
    const response = await fetch(`${apiUrl}/api/logout`, options);
    const json = await response.json();

    return {
      ok: response.ok,
      status: response.status,
      data: json
    }
  }

  useEffect(() => {
    (async () => {
      const response = await logout();

      Swal.fire({
          title: "Encerrar Sessão",
          text: response.data.message,
          icon: getIconByStatus(response.status),
        }
      ).then(()=> {
        if (response.status === 200) {
          clearAuthState();
          router.push("/");
        }
      })
    })();
  }, []);
}