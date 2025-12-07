"use client"

import Link from "next/link";
import Button from "@/components/ui/Button";
import { useAuth } from "@/context/AuthContext";


export default function Header() {  
  const { autenticado, usuario } = useAuth();
  
  return (
    <header className="flex flex-row justify-center gap-1">
      <Link href="/">
        <Button content="Início" />
      </Link>
      <Link href="/reclamacoes">
        <Button content="Reclamações" />
      </Link>

      { autenticado ? 
        <>
          <Link href="/usuario">
            <Button content="Usuario" />
          </Link>
          <Link href="/logout">
            <Button content="Sair" />
          </Link>
        </>
        :   
        <>
          <Link href="/login">
            <Button content="Login" />
          </Link>
          <Link href="/cadastro">
            <Button content="Cadastro" />
          </Link>     
        </>
      }
    </header>
  );
}
