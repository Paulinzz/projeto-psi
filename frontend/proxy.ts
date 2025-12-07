import { NextResponse } from 'next/server';
import { NextRequest } from 'next/server';

export async function proxy(request: NextRequest) {
  const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
  
  const response = await fetch(`${apiUrl}/api/me`, {
    method: "GET",
    headers: {
      cookie: request.headers.get("cookie") ?? ""
    }
  }); 

  const usuario = await response.json();

  if (!usuario.autenticado) {
    return NextResponse.redirect(new URL(`/login?redirect=${request.nextUrl.pathname}`, request.url));
  }

  return NextResponse.next();
}

// SÓ EXECUTA O PROXY EM ROTAS QUE REQUEREM AUTENTICAÇÃO
export const config = {
  matcher: [
    "/usuario/:path*",
    "/logout",
  ]
};
