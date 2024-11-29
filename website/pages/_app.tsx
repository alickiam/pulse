import "@/styles/globals.css";
import type { AppProps } from "next/app";
import { UserProvider } from '@/lib/hooks/useUser'
import { Toaster } from 'sonner'

export default function App({ Component, pageProps }: AppProps) {
  return (
    <UserProvider>
      <Component {...pageProps} />
      <Toaster position="top-right" />
    </UserProvider>
  );
}
