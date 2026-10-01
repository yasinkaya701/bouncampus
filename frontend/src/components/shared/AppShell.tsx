'use client';

import { usePathname } from 'next/navigation';
import Footer from '@/components/shared/Footer';
import Header from '@/components/shared/Header';

export default function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isOperatorConsole = pathname === '/food-waste' || pathname.startsWith('/food-waste/');

  if (isOperatorConsole) {
    return (
      <main id="main-content" className="min-h-screen bg-[#f5f6f5]">
        {children}
      </main>
    );
  }

  return (
    <>
      <Header />
      <main id="main-content" className="mx-auto w-full max-w-[1440px] flex-1 px-4 pb-10 pt-6 sm:px-6 sm:pt-8 lg:px-8 lg:pt-10">
        {children}
      </main>
      <Footer />
    </>
  );
}
