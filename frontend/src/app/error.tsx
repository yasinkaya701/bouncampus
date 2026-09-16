'use client';

import { useEffect } from 'react';
import Link from 'next/link';
import { AlertTriangle, Home, RefreshCw } from 'lucide-react';

export default function Error({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="grid min-h-[62vh] place-items-center">
      <div className="w-full max-w-2xl rounded-[30px] border border-amber-200 bg-[#fff8eb] p-7 shadow-sm sm:p-9">
        <div className="grid h-11 w-11 place-items-center rounded-[16px] bg-amber-100 text-amber-800"><AlertTriangle size={20} /></div>
        <div className="bc-eyebrow mt-6 !text-amber-800">Workspace error</div>
        <h1 className="mt-2 text-2xl font-black tracking-[-0.045em] text-[#0a1020]">This workspace could not be rendered safely.</h1>
        <p className="mt-3 max-w-xl text-sm leading-relaxed text-slate-600">BOUNCAMPUS will not replace a failed source with fabricated live values. Retry the workspace, inspect Data Trust, or return to Overview.</p>
        <div className="mt-6 flex flex-wrap gap-2">
          <button onClick={reset} className="bc-focus-ring inline-flex items-center gap-2 rounded-full bg-[#0b1226] px-4 py-2.5 text-xs font-black text-white"><RefreshCw size={13} /> Retry workspace</button>
          <Link href="/data" className="bc-focus-ring inline-flex items-center gap-2 rounded-full border border-slate-950/10 bg-white px-4 py-2.5 text-xs font-black text-slate-700">Inspect Data Trust</Link>
          <Link href="/" className="bc-focus-ring inline-flex items-center gap-2 rounded-full border border-slate-950/10 bg-white px-4 py-2.5 text-xs font-black text-slate-700"><Home size={13} /> Overview</Link>
        </div>
      </div>
    </div>
  );
}
