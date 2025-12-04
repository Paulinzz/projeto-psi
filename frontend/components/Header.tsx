import Link from "next/link";
import Button from "./ui/Button";

export default function Header() {
  return (
    <header className="flex flex-row justify-center gap-1">
      <Link href="/">
        <Button content="Início" />
      </Link>
      <Link href="/login">
        <Button content="Login" />
      </Link>
      <Link href="/cadastro">
        <Button content="Cadastro" />
      </Link>
      <Link href="/logout">
        <Button content="Sair" />
      </Link>
      <Link href="/reclamacoes">
        <Button content="Reclamações" />
      </Link>
    </header>
  );
}
