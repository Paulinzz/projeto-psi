import Link from "next/link";
import Button from "./ui/Button";

export default function Header() {
  const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

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
    </header>
  );
}
