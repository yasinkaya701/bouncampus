'use client';

import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from 'react';

export type Locale = 'tr' | 'en';

type LocaleContextValue = {
  locale: Locale;
  setLocale: (locale: Locale) => void;
  t: (tr: string, en: string) => string;
};

const LocaleContext = createContext<LocaleContextValue | null>(null);

export function LocaleProvider({ children }: { children: ReactNode }) {
  const [locale, setLocaleState] = useState<Locale>('tr');
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    const saved = window.localStorage.getItem('bouncampus-locale');
    const detected: Locale = window.navigator.language.toLowerCase().startsWith('en') ? 'en' : 'tr';
    setLocaleState(saved === 'tr' || saved === 'en' ? saved : detected);
    setHydrated(true);
  }, []);

  useEffect(() => {
    document.documentElement.lang = locale;
    if (hydrated) window.localStorage.setItem('bouncampus-locale', locale);
  }, [hydrated, locale]);

  const value = useMemo<LocaleContextValue>(() => ({
    locale,
    setLocale: setLocaleState,
    t: (tr, en) => (locale === 'tr' ? tr : en),
  }), [locale]);

  return <LocaleContext.Provider value={value}>{children}</LocaleContext.Provider>;
}

export function useLocale() {
  const value = useContext(LocaleContext);
  if (!value) throw new Error('useLocale must be used inside LocaleProvider');
  return value;
}
