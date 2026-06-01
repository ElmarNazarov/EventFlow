import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const publicPaths = ["/login"];
const protectedPrefixes = ["/dashboard", "/settings", "/orders", "/workflows", "/events", "/inventory", "/notifications"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const token = request.cookies.get("eventflow_token")?.value;

  const isPublic = publicPaths.some((p) => pathname === p || pathname.startsWith(`${p}/`));
  const isProtected = protectedPrefixes.some(
    (p) => pathname === p || pathname.startsWith(`${p}/`),
  );

  if (pathname === "/") {
    return NextResponse.redirect(new URL(token ? "/dashboard" : "/login", request.url));
  }

  if (isPublic && token) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  if (isProtected && !token) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("from", pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
