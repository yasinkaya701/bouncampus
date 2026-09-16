import Link from 'next/link';
import { ArrowLeft, MapPinned } from 'lucide-react';

export default function NotFound() {
  return (
    <div className="grid min-h-[62vh] place-items-center">
      <div className="w-full max-w-2xl rounded-[30px] border border-slate-950/10 bg-white/85 p-8 text-center shadow-sm sm:p-10">
        <div className="mx-auto grid h-12 w-12 place-items-center rounded-[18px] bg-[#0b1226] text-white"><MapPinned size={20} /></div>
        <div className="bc-eyebrow mt-6">404 / Workspace not found</div>
        <h1 className="mt-2 text-3xl font-black tracking-[-0.05em] text-[#0a1020]">This campus workspace does not exist.</h1>
        <p className="mx-auto mt-3 max-w-md text-sm leading-relaxed text-slate-500">Return to the operating overview or continue with a known product workspace.</p>
        <Link href="/" className="bc-focus-ring mt-6 inline-flex items-center gap-2 rounded-full bg-[#0b1226] px-4 py-2.5 text-xs font-black text-white"><ArrowLeft size={13} /> Back to Overview</Link>
      </div>
    </div>
  );
}
