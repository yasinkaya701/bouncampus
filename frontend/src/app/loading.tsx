export default function Loading() {
  return (
    <div className="grid min-h-[62vh] place-items-center">
      <div className="w-full max-w-xl rounded-[28px] border border-slate-950/10 bg-white/80 p-6 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="h-9 w-9 animate-spin rounded-full border-2 border-slate-200 border-t-[#0b1226]" />
          <div>
            <div className="text-sm font-black tracking-[-0.02em] text-[#0a1020]">BOUNCAMPUS is preparing the workspace</div>
            <p className="mt-1 text-[11px] text-slate-500">Loading source metadata, campus state and decision models.</p>
          </div>
        </div>
        <div className="mt-6 grid gap-2 sm:grid-cols-3">
          {[0, 1, 2].map(item => <div key={item} className="h-20 animate-pulse rounded-[18px] bg-[#f0f1ee]" />)}
        </div>
      </div>
    </div>
  );
}
