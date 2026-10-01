'use client';

import { RotateCcw, ShieldAlert } from 'lucide-react';

export default function FoodWasteError({ reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <div className="grid min-h-screen place-items-center bg-[#f5f6f5] px-5 text-[#111713]">
      <div className="w-full max-w-lg rounded-2xl border border-[#dfe3df] bg-white p-6 shadow-[0_10px_35px_rgba(11,29,23,0.08)] sm:p-8">
        <div className="grid h-10 w-10 place-items-center rounded-xl bg-[#fff1ef] text-[#b74740]">
          <ShieldAlert size={19} />
        </div>
        <div className="mt-5 text-[10px] font-semibold uppercase tracking-[0.14em] text-[#737c75]">OPERATOR CONSOLE</div>
        <h1 className="mt-2 text-[24px] font-semibold tracking-[-0.035em]">Decision surface could not load</h1>
        <p className="mt-3 text-[11px] leading-5 text-[#667068]">
          No production recommendation has been dispatched. The safe operational state remains HOLD until the decision context is available again.
        </p>
        <button
          type="button"
          onClick={reset}
          className="mt-6 inline-flex h-10 items-center gap-2 rounded-lg bg-[#0d4634] px-4 text-[10px] font-semibold text-white transition hover:bg-[#093a2b] focus:outline-none focus:ring-2 focus:ring-[#7ac59f] focus:ring-offset-2"
        >
          <RotateCcw size={14} /> Retry decision context
        </button>
      </div>
    </div>
  );
}
